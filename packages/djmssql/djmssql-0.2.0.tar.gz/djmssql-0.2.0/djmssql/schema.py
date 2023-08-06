import binascii
import datetime

from django.db.backends.base.schema import (
    BaseDatabaseSchemaEditor, logger, _is_relevant_relation, _related_non_m2m_objects,
)
from django.db.backends.ddl_references import (
    Statement,
)
from django.db.models import Index
from django.db.models.fields import SmallAutoField, AutoField, BigAutoField
from django.db.models.fields.related import ManyToManyField
from django.db.transaction import TransactionManagementError
from .cursor import _quote_value


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):

    _sql_check_constraint = " CONSTRAINT %(name)s CHECK (%(check)s)"
    _sql_select_default_constraint_name = "SELECT" \
                                          " d.name " \
                                          "FROM sys.default_constraints d " \
                                          "INNER JOIN sys.tables t ON" \
                                          " d.parent_object_id = t.object_id " \
                                          "INNER JOIN sys.columns c ON" \
                                          " d.parent_object_id = c.object_id AND" \
                                          " d.parent_column_id = c.column_id " \
                                          "INNER JOIN sys.schemas s ON" \
                                          " t.schema_id = s.schema_id " \
                                          "WHERE" \
                                          " t.name = %(table)s AND" \
                                          " c.name = %(column)s"
    _sql_select_foreign_key_constraints = "SELECT" \
                                          " po.name AS table_name," \
                                          " co.name AS constraint_name " \
                                          "FROM sys.foreign_key_columns fkc " \
                                          "INNER JOIN sys.objects co ON" \
                                          " fkc.constraint_object_id = co.object_id " \
                                          "INNER JOIN sys.tables po ON" \
                                          " fkc.parent_object_id = po.object_id " \
                                          "INNER JOIN sys.tables ro ON" \
                                          " fkc.referenced_object_id = ro.object_id " \
                                          "WHERE ro.name = %(table)s"
    sql_alter_column_default = "ADD DEFAULT %(default)s FOR %(column)s"
    sql_alter_column_no_default = "DROP CONSTRAINT %(column)s"
    sql_alter_column_not_null = "ALTER COLUMN %(column)s %(type)s NOT NULL"
    sql_alter_column_null = "ALTER COLUMN %(column)s %(type)s NULL"
    sql_alter_column_type = "ALTER COLUMN %(column)s %(type)s"
    sql_create_column = "ALTER TABLE %(table)s ADD %(column)s %(definition)s"
    sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s"
    sql_delete_index = "DROP INDEX %(name)s ON %(table)s"
    sql_delete_table = "DROP TABLE %(table)s"
    sql_rename_column = "EXEC sp_rename '%(table)s.%(old_column)s', %(new_column)s, 'COLUMN'"
    sql_rename_table = "EXEC sp_rename %(old_table)s, %(new_table)s"

    def _alter_column_default_sql(self, model, old_field, new_field, drop=False):
        """
        Hook to specialize column default alteration.

        Return a (sql, params) fragment to add or drop (depending on the drop
        argument) a default to new_field's column.
        """
        new_default = self.effective_default(new_field)
        default = '%s'
        params = [new_default]
        column = self.quote_name(new_field.column)

        if drop:
            params = []
            # SQL Server requires the name of the default constraint
            result = self.execute(
                self._sql_select_default_constraint_name % {
                    "table": _quote_value(model._meta.db_table),
                    "column": _quote_value(new_field.column),
                },
            )
            for row in self.connection.connection._last_rows:
                column = self.quote_name(next(iter(row)))
        elif self.connection.features.requires_literal_defaults:
            # Some databases (Oracle) can't take defaults as a parameter
            # If this is the case, the SchemaEditor for that database should
            # implement prepare_default().
            default = self.prepare_default(new_default)
            params = []

        new_db_params = new_field.db_parameters(connection=self.connection)
        sql = self.sql_alter_column_no_default if drop else self.sql_alter_column_default
        return (
            sql % {
                'column': column,
                'type': new_db_params['type'],
                'default': default,
            },
            params,
        )

    def _alter_column_null_sql(self, model, old_field, new_field):
        """
        Hook to specialize column null alteration.

        Return a (sql, params) fragment to set a column to null or non-null
        as required by new_field, or None if no changes are required.
        """
        if (self.connection.features.interprets_empty_strings_as_nulls and
                new_field.get_internal_type() in ("CharField", "TextField")):
            # The field is nullable in the database anyway, leave it alone.
            return
        else:
            new_db_params = new_field.db_parameters(connection=self.connection)
            sql = self.sql_alter_column_null if new_field.null else self.sql_alter_column_not_null
            return (
                sql % {
                    'column': self.quote_name(new_field.column),
                    'type': new_db_params['type'],
                },
                [],
            )

    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        new_type = self._set_field_new_type_null_status(old_field, new_type)
        return super()._alter_column_type_sql(model, old_field, new_field, new_type)

    def _delete_unique_constraints(self, model, old_field, new_field, strict=False):
        unique_columns = []
        if old_field.unique and new_field.unique:
            unique_columns.append([old_field.column])
        else:
            for fields in model._meta.unique_together:
                columns = [model._meta.get_field(field).column for field in fields]
                if old_field.column in columns:
                    unique_columns.append(columns)
        if unique_columns:
            for columns in unique_columns:
                constraint_names = self._constraint_names(model, columns, unique=True)
                if strict and len(constraint_names) != 1:
                    raise ValueError("Found wrong number (%s) of unique constraints for %s.%s" % (
                        len(constraint_names),
                        model._meta.db_table,
                        old_field.column,
                    ))
                for constraint_name in constraint_names:
                    self.execute(self._delete_constraint_sql(self.sql_delete_unique, model, constraint_name))

    def _rename_field_sql(self, table, old_field, new_field, new_type):
        new_type = self._set_field_new_type_null_status(old_field, new_type)
        return super()._rename_field_sql(table, old_field, new_field, new_type)

    def _set_field_new_type_null_status(self, field, new_type):
        """
        Keep the null property of the old field. If it has changed, it will be
        handled separately.
        """
        if field.null:
            new_type += " NULL"
        else:
            new_type += " NOT NULL"
        return new_type

    def add_field(self, model, field):
        """
        Create a field on a model. Usually involves adding a column, but may
        involve adding a table instead (for M2M fields).
        """
        # Special-case implicit M2M tables
        if field.many_to_many and field.remote_field.through._meta.auto_created:
            return self.create_model(field.remote_field.through)
        # Get the column's definition
        definition, params = self.column_sql(model, field, include_default=True)
        # It might not actually have a column behind it
        if definition is None:
            return
        # Check constraints can go on the column SQL here
        db_params = field.db_parameters(connection=self.connection)
        if db_params['check']:
            definition += " CHECK (%s)" % db_params['check']
        # Build the SQL and run it
        sql = self.sql_create_column % {
            "table": self.quote_name(model._meta.db_table),
            "column": self.quote_name(field.column),
            "definition": definition,
        }
        self.execute(sql, params)
        # Drop the default if we need to
        # (Django usually does not use in-database defaults)
        if not self.skip_default(field) and self.effective_default(field) is not None:
            changes_sql, params = self._alter_column_default_sql(model, None, field, drop=True)
            sql = self.sql_alter_column % {
                "table": self.quote_name(model._meta.db_table),
                "changes": changes_sql,
            }
            self.execute(sql, params)
        # Add an index, if required
        self.deferred_sql.extend(self._field_indexes_sql(model, field))
        # Add any FK constraints later
        if field.remote_field and self.connection.features.supports_foreign_keys and field.db_constraint:
            self.deferred_sql.append(self._create_fk_sql(model, field, "_fk_%(to_table)s_%(to_column)s"))
        # Reset connection if required
        if self.connection.features.connection_persists_old_columns:
            self.connection.close()

    def quote_value(self, value):
        return _quote_value(value)

    def create_model(self, model):
        """
        Takes a model and creates a table for it in the database.
        Will also create any accompanying indexes or unique constraints.
        """
        # Create column SQL, add FK deferreds if needed
        column_sqls = []
        params = []
        for field in model._meta.local_fields:
            # SQL
            definition, extra_params = self.column_sql(model, field)
            if definition is None:
                continue
            # Check constraints can go on the column SQL here
            db_params = field.db_parameters(connection=self.connection)
            if db_params['check']:
                # SQL Server requires a name for the check constraint
                definition += self._sql_check_constraint % {
                    "name": self._create_index_name(model._meta.db_table, [field.column], suffix="_check"),
                    "check": db_params['check']
                }
            # Autoincrement SQL (for backends with inline variant)
            col_type_suffix = field.db_type_suffix(connection=self.connection)
            if col_type_suffix:
                definition += " %s" % col_type_suffix
            params.extend(extra_params)
            # FK
            if field.remote_field and field.db_constraint:
                to_table = field.remote_field.model._meta.db_table
                to_column = field.remote_field.model._meta.get_field(field.remote_field.field_name).column
                if self.sql_create_inline_fk:
                    definition += " " + self.sql_create_inline_fk % {
                        "to_table": self.quote_name(to_table),
                        "to_column": self.quote_name(to_column),
                    }
                elif self.connection.features.supports_foreign_keys:
                    self.deferred_sql.append(self._create_fk_sql(model, field, "_fk_%(to_table)s_%(to_column)s"))
            # Add the SQL to our big list
            column_sqls.append("%s %s" % (
                self.quote_name(field.column),
                definition,
            ))
            # Autoincrement SQL (for backends with post table definition variant)
            if field.get_internal_type() in ("SmallAutoField", "AutoField", "BigAutoField"):
                autoinc_sql = self.connection.ops.autoinc_sql(model._meta.db_table, field.column)
                if autoinc_sql:
                    self.deferred_sql.extend(autoinc_sql)

        # Add any unique_togethers (always deferred, as some fields might be
        # created afterwards, like geometry fields with some backends)
        for fields in model._meta.unique_together:
            columns = [model._meta.get_field(field).column for field in fields]
            self.deferred_sql.append(self._create_unique_sql(model, columns))
        # Make the table
        sql = self.sql_create_table % {
            "table": self.quote_name(model._meta.db_table),
            "definition": ", ".join(column_sqls)
        }
        if model._meta.db_tablespace:
            tablespace_sql = self.connection.ops.tablespace_sql(model._meta.db_tablespace)
            if tablespace_sql:
                sql += ' ' + tablespace_sql
        # Prevent using [] as params, in the case a literal '%' is used in the definition
        self.execute(sql, params or None)

        # Add any field index and index_together's (deferred as SQLite3 _remake_table needs it)
        self.deferred_sql.extend(self._model_indexes_sql(model))

        # Make M2M tables
        for field in model._meta.local_many_to_many:
            if field.remote_field.through._meta.auto_created:
                self.create_model(field.remote_field.through)

    def delete_model(self, model):
        """
        Deletes a model from the database.
        """
        # Delete the foreign key constraints
        result = self.execute(
            self._sql_select_foreign_key_constraints % {
                "table": _quote_value(model._meta.db_table),
            },
        )

        for table, constraint in self.connection.connection._last_rows[:]:
            sql = self.sql_alter_column % {
                "table": self.quote_name(table),
                "changes": self.sql_alter_column_no_default % {
                    "column": self.quote_name(constraint),
                }
            }
            self.execute(sql)

        # Delete the table
        super().delete_model(model)
        # Remove all deferred statements referencing the deleted table.
        for sql in list(self.deferred_sql):
            if isinstance(sql, Statement) and sql.references_table(model._meta.db_table):
                self.deferred_sql.remove(sql)

    def prepare_default(self, value):
        return _quote_value(value)

    def remove_field(self, model, field):
        """
        Removes a field from a model. Usually involves deleting a column,
        but for M2Ms may involve deleting a table.
        """
        # Special-case implicit M2M tables
        if field.many_to_many and field.remote_field.through._meta.auto_created:
            return self.delete_model(field.remote_field.through)
        # It might not actually have a column behind it
        if field.db_parameters(connection=self.connection)['type'] is None:
            return
        # Drop any FK constraints, SQL Server requires explicit deletion
        with self.connection.cursor() as cursor:
            constraints = self.connection.introspection.get_constraints(cursor, model._meta.db_table)
        for name, infodict in constraints.items():
            if field.column in infodict['columns'] and infodict['foreign_key']:
                self.execute(self._delete_constraint_sql(self.sql_delete_fk, model, name))
        # Drop any indexes, SQL Server requires explicit deletion
        for name, infodict in constraints.items():
            if field.column in infodict['columns'] and infodict['index']:
                self.execute(self.sql_delete_index % {
                    "table": self.quote_name(model._meta.db_table),
                    "name": self.quote_name(name),
                })
        # Drop primary key constraint, SQL Server requires explicit deletion
        for name, infodict in constraints.items():
            if field.column in infodict['columns'] and infodict['primary_key']:
                self.execute(self.sql_delete_pk % {
                    "table": self.quote_name(model._meta.db_table),
                    "name": self.quote_name(name),
                })
        # Drop check constraints, SQL Server requires explicit deletion
        for name, infodict in constraints.items():
            if field.column in infodict['columns'] and infodict['check']:
                self.execute(self.sql_delete_check % {
                    "table": self.quote_name(model._meta.db_table),
                    "name": self.quote_name(name),
                })
        # Drop unique constraints, SQL Server requires explicit deletion
        for name, infodict in constraints.items():
            if field.column in infodict['columns'] and infodict['unique'] and not infodict['primary_key']:
                self.execute(self.sql_delete_unique % {
                    "table": self.quote_name(model._meta.db_table),
                    "name": self.quote_name(name),
                })
        # Delete the column
        sql = self.sql_delete_column % {
            "table": self.quote_name(model._meta.db_table),
            "column": self.quote_name(field.column),
        }
        self.execute(sql)
        # Reset connection if required
        if self.connection.features.connection_persists_old_columns:
            self.connection.close()
        # Remove all deferred statements referencing the deleted table.
        for sql in list(self.deferred_sql):
            if isinstance(sql, Statement) and sql.references_column(model._meta.db_table, field.column):
                self.deferred_sql.remove(sql)

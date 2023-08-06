import warnings

import minitds as Database

from django.db.backends.base.introspection import (
    BaseDatabaseIntrospection, FieldInfo, TableInfo,
)
from django.db.models.indexes import Index

SQL_AUTOFIELD = -777555
SQL_BIGAUTOFIELD = -777444


class DatabaseIntrospection(BaseDatabaseIntrospection):
    # Map type codes to Django Field types.
    data_types_reverse = {
        SQL_AUTOFIELD: 'AutoField',
        SQL_BIGAUTOFIELD: 'BigAutoField',
        Database.INTNTYPE: 'BigIntegerField',
        Database.BITNTYPE: 'BooleanField',
        Database.NCHARTYPE: 'CharField',
        Database.DECIMALNTYPE: 'DecimalField',
        Database.FLT8TYPE: 'FloatField',
        Database.FLT4TYPE: 'FloatField',
        Database.INT4TYPE: 'IntegerField',
        Database.INT8TYPE: 'BigIntegerField',
        Database.BIGBINARYTYPE: 'BinaryField',
        Database.FLTNTYPE: 'FloatField',
        Database.INT2TYPE: 'SmallIntegerField',
        Database.TIMENTYPE: 'TimeField',
        Database.DATENTYPE: 'DateField',
        Database.DATETIME2NTYPE: 'DateTimeField',
        Database.BIGVARBINTYPE: 'BinaryField',
        Database.NVARCHARTYPE: 'TextField',
        Database.BIGVARCHRTYPE: 'TextField',
        Database.NTEXTTYPE: 'TextField',
        Database.IMAGETYPE: 'BinaryField',
        Database.GUIDTYPE: 'UUIDField',
    }

    def get_field_type(self, data_type, description):
        field_type = super().get_field_type(data_type, description)
        # the max nvarchar length is described as 0 or 2**30-1
        # (it depends on the driver)
        size = description.internal_size
        if field_type == 'CharField':
            if size == 0 or size >= 2**30-1:
                field_type = "TextField"
        elif field_type == 'TextField':
            if size > 0 and size < 2**30-1:
                field_type = 'CharField'
        return field_type

    def get_table_list(self, cursor):
        """
        Returns a list of table and view names in the current database.
        """
        sql = 'SELECT TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = SCHEMA_NAME()'
        cursor.execute(sql)
        types = {'BASE TABLE': 't', 'VIEW': 'v'}
        r = [TableInfo(row[0], types.get(row[1])) for row in cursor.fetchall()]
        return r

    def get_table_description(self, cursor, table_name, identity_check=True):
        cursor.execute('EXEC sp_columns %s', (table_name, ))
        items = []

        for c in list(cursor.fetchall()):
            type_name = c[5].split()[0]
            cursor.execute('SELECT TYPE_ID(%s)', (type_name, ))
            type_id = cursor.fetchone()[0]
            ln = c[7]
            if ln and ln == c[15]:  # string
                ln //=2

            items.append(
                FieldInfo(c[3], type_id, ln, ln, c[6], c[8], bool(c[10]), c[12])
            )
        return items

    def get_sequences(self, cursor, table_name, table_fields=()):
        cursor.execute("""
            SELECT c.name FROM sys.columns c
            INNER JOIN sys.tables t ON c.object_id = t.object_id
            WHERE t.schema_id = SCHEMA_ID() AND t.name = %s AND c.is_identity = 1""",
            [table_name])
        # SQL Server allows only one identity column per table
        # https://docs.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql-identity-property
        row = cursor.fetchone()
        return [{'table': table_name, 'column': row[0]}] if row else []

    def get_relations(self, cursor, table_name):
        """
        Returns a dictionary of {field_name: (field_name_other_table, other_table)}
        representing all relationships to the given table.
        """
        # CONSTRAINT_COLUMN_USAGE: http://msdn2.microsoft.com/en-us/library/ms174431.aspx
        # CONSTRAINT_TABLE_USAGE:  http://msdn2.microsoft.com/en-us/library/ms179883.aspx
        # REFERENTIAL_CONSTRAINTS: http://msdn2.microsoft.com/en-us/library/ms179987.aspx
        # TABLE_CONSTRAINTS:       http://msdn2.microsoft.com/en-us/library/ms181757.aspx

        sql = """
SELECT e.COLUMN_NAME AS column_name,
  c.TABLE_NAME AS referenced_table_name,
  d.COLUMN_NAME AS referenced_column_name
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS a
INNER JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS b
  ON a.CONSTRAINT_NAME = b.CONSTRAINT_NAME AND a.TABLE_SCHEMA = b.CONSTRAINT_SCHEMA
INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE AS c
  ON b.UNIQUE_CONSTRAINT_NAME = c.CONSTRAINT_NAME AND b.CONSTRAINT_SCHEMA = c.CONSTRAINT_SCHEMA
INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS d
  ON c.CONSTRAINT_NAME = d.CONSTRAINT_NAME AND c.CONSTRAINT_SCHEMA = d.CONSTRAINT_SCHEMA
INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS e
  ON a.CONSTRAINT_NAME = e.CONSTRAINT_NAME AND a.TABLE_SCHEMA = e.TABLE_SCHEMA
WHERE a.TABLE_SCHEMA = SCHEMA_NAME() AND a.TABLE_NAME = %s AND a.CONSTRAINT_TYPE = 'FOREIGN KEY'"""
        cursor.execute(sql, (table_name,))
        return dict([[item[0], (item[2], item[1])] for item in cursor.fetchall()])

    def get_key_columns(self, cursor, table_name):
        """
        Returns a list of (column_name, referenced_table_name, referenced_column_name) for all
        key columns in given table.
        """
        key_columns = []
        cursor.execute("""
            SELECT c.name AS column_name, rt.name AS referenced_table_name, rc.name AS referenced_column_name
            FROM sys.foreign_key_columns fk
            INNER JOIN sys.tables t ON t.object_id = fk.parent_object_id
            INNER JOIN sys.columns c ON c.object_id = t.object_id AND c.column_id = fk.parent_column_id
            INNER JOIN sys.tables rt ON rt.object_id = fk.referenced_object_id
            INNER JOIN sys.columns rc ON rc.object_id = rt.object_id AND rc.column_id = fk.referenced_column_id
            WHERE t.schema_id = SCHEMA_ID() AND t.name = %s""", [table_name])
        key_columns.extend([tuple(row) for row in cursor.fetchall()])
        return key_columns

    def get_constraints(self, cursor, table_name):
        """
        Retrieves any constraints or keys (unique, pk, fk, check, index)
        across one or more columns.

        Returns a dict mapping constraint names to their attributes,
        where attributes is a dict with keys:
         * columns: List of columns this covers
         * primary_key: True if primary key, False otherwise
         * unique: True if this is a unique constraint, False otherwise
         * foreign_key: (table, column) of target, or None
         * check: True if check constraint, False otherwise
         * index: True if index, False otherwise.
         * orders: The order (ASC/DESC) defined for the columns of indexes
         * type: The type of the index (btree, hash, etc.)
        """
        constraints = {}
        # Loop over the key table, collecting things as constraints
        # This will get PKs, FKs, and uniques, but not CHECK
        cursor.execute("""
            SELECT
                kc.constraint_name,
                kc.column_name,
                tc.constraint_type,
                fk.referenced_table_name,
                fk.referenced_column_name
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kc
            INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc ON
                kc.table_schema = tc.table_schema AND
                kc.table_name = tc.table_name AND
                kc.constraint_name = tc.constraint_name
            LEFT OUTER JOIN (
                SELECT
                    ps.name AS table_schema,
                    pt.name AS table_name,
                    pc.name AS column_name,
                    rt.name AS referenced_table_name,
                    rc.name AS referenced_column_name
                FROM
                    sys.foreign_key_columns fkc
                INNER JOIN sys.tables pt ON
                    fkc.parent_object_id = pt.object_id
                INNER JOIN sys.schemas ps ON
                    pt.schema_id = ps.schema_id
                INNER JOIN sys.columns pc ON
                    fkc.parent_object_id = pc.object_id AND
                    fkc.parent_column_id = pc.column_id
                INNER JOIN sys.tables rt ON
                    fkc.referenced_object_id = rt.object_id
                INNER JOIN sys.schemas rs ON
                    rt.schema_id = rs.schema_id
                INNER JOIN sys.columns rc ON
                    fkc.referenced_object_id = rc.object_id AND
                    fkc.referenced_column_id = rc.column_id
            ) fk ON
                kc.table_schema = fk.table_schema AND
                kc.table_name = fk.table_name AND
                kc.column_name = fk.column_name
            WHERE
                kc.table_schema = SCHEMA_NAME() AND
                kc.table_name = %s
            ORDER BY
                kc.constraint_name ASC,
                kc.ordinal_position ASC
        """, [table_name])
        for constraint, column, kind, ref_table, ref_column in cursor.fetchall():
            # If we're the first column, make the record
            if constraint not in constraints:
                constraints[constraint] = {
                    "columns": [],
                    "primary_key": kind.lower() == "primary key",
                    "unique": kind.lower() in ["primary key", "unique"],
                    "foreign_key": (ref_table, ref_column) if kind.lower() == "foreign key" else None,
                    "check": False,
                    "index": False,
                }
            # Record the details
            constraints[constraint]['columns'].append(column)
        # Now get CHECK constraint columns
        cursor.execute("""
            SELECT kc.constraint_name, kc.column_name
            FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS kc
            JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS c ON
                kc.table_schema = c.table_schema AND
                kc.table_name = c.table_name AND
                kc.constraint_name = c.constraint_name
            WHERE
                c.constraint_type = 'CHECK' AND
                kc.table_schema = SCHEMA_NAME() AND
                kc.table_name = %s
        """, [table_name])
        for constraint, column in cursor.fetchall():
            # If we're the first column, make the record
            if constraint not in constraints:
                constraints[constraint] = {
                    "columns": [],
                    "primary_key": False,
                    "unique": False,
                    "foreign_key": None,
                    "check": True,
                    "index": False,
                }
            # Record the details
            constraints[constraint]['columns'].append(column)
        # Now get indexes
        cursor.execute("""
            SELECT
                i.name AS index_name,
                i.is_unique,
                i.is_primary_key,
                i.type,
                i.type_desc,
                ic.is_descending_key,
                c.name AS column_name
            FROM
                sys.tables AS t
            INNER JOIN sys.schemas AS s ON
                t.schema_id = s.schema_id
            INNER JOIN sys.indexes AS i ON
                t.object_id = i.object_id
            INNER JOIN sys.index_columns AS ic ON
                i.object_id = ic.object_id AND
                i.index_id = ic.index_id
            INNER JOIN sys.columns AS c ON
                ic.object_id = c.object_id AND
                ic.column_id = c.column_id
            WHERE
                t.schema_id = SCHEMA_ID() AND
                t.name = %s
            ORDER BY
                i.index_id ASC,
                ic.index_column_id ASC
        """, [table_name])
        indexes = {}
        for index, unique, primary, type_, desc, order, column in cursor.fetchall():
            if index not in indexes:
                indexes[index] = {
                    "columns": [],
                    "primary_key": primary,
                    "unique": unique,
                    "foreign_key": None,
                    "check": False,
                    "index": True,
                    "orders": [],
                    "type": Index.suffix if type_ in (1,2) else desc.lower(),
                }
            indexes[index]["columns"].append(column)
            indexes[index]["orders"].append("DESC" if order == 1 else "ASC")
        for index, constraint in indexes.items():
            if index not in constraints:
                constraints[index] = constraint
        return constraints

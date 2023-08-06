"""
MS SQL Servre database backend for Django.

Requires minitds: http://github.com/nakagami/minitds
"""
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.base.base import BaseDatabaseWrapper

try:
    import minitds as Database
except ImportError as e:
    raise ImproperlyConfigured("Error loading minitds module: %s" % e)


from .client import DatabaseClient                          # NOQA isort:skip
from .creation import DatabaseCreation                      # NOQA isort:skip
from .features import DatabaseFeatures                      # NOQA isort:skip
from .introspection import DatabaseIntrospection            # NOQA isort:skip
from .operations import DatabaseOperations                  # NOQA isort:skip
from .schema import DatabaseSchemaEditor                    # NOQA isort:skip
from .cursor import CursorWrapper                           # NOQA isort:skip


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'microsoft'
    display_name = 'SQL Server'

    data_types = {
        'SmallAutoField':    'smallint IDENTITY (1, 1)',
        'AutoField':         'int IDENTITY (1, 1)',
        'BigAutoField':      'bigint IDENTITY (1, 1)',
        'BigIntegerField':   'bigint',
        'BinaryField':       'varbinary(max)',
        'BooleanField':      'bit',
        'CharField':         'nvarchar(%(max_length)s)',
        'DateField':         'date',
        'DateTimeField':     'datetime2',
        'DecimalField':      'numeric(%(max_digits)s, %(decimal_places)s)',
        'DurationField':     'bigint',
        'FileField':         'nvarchar(%(max_length)s)',
        'FilePathField':     'nvarchar(%(max_length)s)',
        'FloatField':        'double precision',
        'IntegerField':      'int',
        'JSONFIeld':         'varbinary(max)',
        'IPAddressField':    'nvarchar(15)',
        'GenericIPAddressField': 'nvarchar(39)',
        'NullBooleanField':  'bit',
        'OneToOneField':     'int',
        'PositiveIntegerField': 'int',
        'PositiveSmallIntegerField': 'smallint',
        'SlugField':         'nvarchar(%(max_length)s)',
        'SmallIntegerField': 'smallint',
        'TextField':         'nvarchar(max)',
        'TimeField':         'time',
        'UUIDField':         'uniqueidentifier',
    }
    data_type_check_constraints = {
        'PositiveIntegerField': '[%(column)s] >= 0',
        'PositiveSmallIntegerField': '[%(column)s] >= 0',
    }
    operators = {
        # Since '=' is used not only for string comparision there is no way
        # to make it case (in)sensitive.
        'exact': '= %s',
        'iexact': "= UPPER(%s)",
        'contains': "LIKE %s ESCAPE '\\'",
        'icontains': "LIKE UPPER(%s) ESCAPE '\\'",
        'gt': '> %s',
        'gte': '>= %s',
        'lt': '< %s',
        'lte': '<= %s',
        'startswith': "LIKE %s ESCAPE '\\'",
        'endswith': "LIKE %s ESCAPE '\\'",
        'istartswith': "LIKE UPPER(%s) ESCAPE '\\'",
        'iendswith': "LIKE UPPER(%s) ESCAPE '\\'",
    }

    # The patterns below are used to generate SQL pattern lookup clauses when
    # the right-hand side of the lookup isn't a raw string (it might be an expression
    # or the result of a bilateral transformation).
    # In those cases, special characters for LIKE operators (e.g. \, *, _) should be
    # escaped on database side.
    #
    # Note: we use str.format() here for readability as '%' is used as a wildcard for
    # the LIKE operator.
    pattern_esc = r"REPLACE(REPLACE(REPLACE({}, '\', '[\]'), '%%', '[%%]'), '_', '[_]')"
    pattern_ops = {
        'contains': "LIKE '%%' + {} + '%%'",
        'icontains': "LIKE '%%' + UPPER({}) + '%%'",
        'startswith': "LIKE {} + '%%'",
        'istartswith': "LIKE UPPER({}) + '%%'",
        'endswith': "LIKE '%%' + {}",
        'iendswith': "LIKE '%%' + UPPER({})",
    }

    Database = Database
    SchemaEditorClass = DatabaseSchemaEditor
    # Classes instantiated in __init__().
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_connection_params(self):
        settings_dict = self.settings_dict
        if not settings_dict['NAME']:
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply the NAME value.")
        conn_params = {'database': settings_dict['NAME']}
        conn_params.update(settings_dict['OPTIONS'])
        if settings_dict['USER']:
            conn_params['user'] = settings_dict['USER']
        if settings_dict['PASSWORD']:
            conn_params['password'] = settings_dict['PASSWORD']
        if settings_dict['HOST']:
            conn_params['host'] = settings_dict['HOST']
        if settings_dict['PORT']:
            conn_params['port'] = settings_dict['PORT']
        conn_params['isolation_level'] = Database.ISOLATION_LEVEL_READ_COMMITTED
        return conn_params

    def get_new_connection(self, conn_params):
        connection = Database.connect(**conn_params)
#        with connection.cursor() as cur:
#            cur.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
#        connection.commit()
        return connection

    def init_connection_state(self):
        self._set_autocommit(self.get_autocommit())


    def _savepoint(self, sid):
        if self.get_autocommit():
            return
        return super()._savepoint(sid)

    def _savepoint_rollback(self, sid):
        if self.get_autocommit():
            return
        return super()._savepoint_rollback(sid)

    def _savepoint_commit(self, sid):
        pass

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            self.connection.set_autocommit(autocommit)
            self.autocommit = autocommit

    def create_cursor(self, name=None):
        cur = self.connection.cursor(factory=CursorWrapper)
        cur.autocommit = self.autocommit
        return cur

    def is_usable(self):
        return self.connection.is_connect()

    def close_if_unusable_or_obsolete(self):
        if self.errors_occurred:
            self.close()

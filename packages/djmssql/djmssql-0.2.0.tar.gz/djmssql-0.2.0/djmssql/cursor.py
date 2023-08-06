import datetime
import binascii
import enum
import collections
from django.utils import timezone
from django.db.utils import InterfaceError

try:
    import minitds as Database
except ImportError as e:
    raise ImproperlyConfigured("Error loading minitds module: %s" % e)


def _quote_value(v):
    if isinstance(v, enum.Enum):
        v = v.value

    if isinstance(v, datetime.datetime) and timezone.is_aware(v):
        return "'" + str(v.astimezone(timezone.utc).replace(tzinfo=None)) + "'"
    return Database.quote_value(v)

def convert_sql(query, params):
    if params is None:
        pass
    elif isinstance(params, dict):
        converted_params = {}
        for k, v in params.items():
            converted_params[k] = _quote_value(v)
        query = query % converted_params
    elif isinstance(params, (list, tuple)):
        escaped_params = tuple(_quote_value(param).replace('%', '%%') for param in params)
        s = query.replace('%', '%%').replace('%%s', '%s')
        s = s % escaped_params
        query = s.replace('%%', '%')

    return query


class CursorWrapper(Database.Cursor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.closed = False
        self.query = None

    def execute(self, query, params=None):
        if self.closed:
            raise InterfaceError('Cursor is closed')
        try:
            q = convert_sql(query, params)
            super().execute(q)
            self.query = q
        except Database.OperationalError as e:
            if e.err_num != 15225:
                raise e

    def executemany(self, query, param_list):
        if self.closed:
            raise InterfaceError('Cursor is closed')
        for params in param_list:
            super().execute(convert_sql(query, params))

    def close(self):
        super().close()
        self.closed = True

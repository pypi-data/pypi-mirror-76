import subprocess

from django.db.backends.base.client import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    executable_name = 'sqlcmd'

    @classmethod
    def settings_to_cmd_args(cls, settings_dict, parameters):

        args = [executable_name]

        if settings_dict['HOST']:
            args += ["-S", settings_dict['HOST']]
        if settings_dict['USER']:
            args += ["-U", settings_dict['USER']]
        if settings_dict['PASSWORD']:
            args += ["-P", settings_dict['PASSWORD']]

        args += ["-d", settings_dict['NAME']]

        return args

    def runshell(self, parameters):
        args = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict, parameters)
        subprocess.check_call(args)


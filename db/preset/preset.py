from .tables import (
    toaster_tables,
    toaster_settings_tables
)


class Preseter(object):
    """Cool presetter who knows how to do some things
    actions on the default MySQL database by calling
    just one function. Required, for example, for installation
    standard settings, tables, etc.
    """
    def __init__(self, connection, cursor):
        self.con = connection
        self.cur = cursor


    # add custom presets
    def deploy_toaster(self):
        """docstring
        """
        self.cur.execute('CREATE DATABASE IF NOT EXISTS toaster')
        self.cur.execute('CREATE DATABASE IF NOT EXISTS toaster_settings')

        for query in toaster_tables:
            self.cur.execute(query)

        for query in toaster_settings_tables:
            self.cur.execute(query)


    def conv_settings(self, conv_id: int):
        pass

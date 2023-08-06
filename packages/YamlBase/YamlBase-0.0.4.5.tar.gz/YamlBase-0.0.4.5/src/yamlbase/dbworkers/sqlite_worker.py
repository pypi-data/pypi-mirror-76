from .base import DBWorker
from yaml_worker import YamlDataBaseWorker
import os
from sql import SQLite


class SQLiteWorker(DBWorker):
    tables: list
    schemas: list

    def __init__(self, yaml: YamlDataBaseWorker):
        super().__init__(yaml)
        self.db_data = yaml
        self.conn = self.initialize_connection()
        self.db_identifier = f"{self.db_data.db_info['ip']}_{self.db_data.db_info['db_type']}_" \
                             f"{self.db_data.db_info['db_name']}"
        self.read_base_information()

    def check_if_used(self):
        return self.db_identifier in os.listdir('../scanned_bases')

    def initialize_connection(self) -> SQLite:
        return SQLite(self.db_data.db_info['ip'], self.db_data.db_info['db_name'])

    def insert_new_table(self, new_table):
        self.conn.create_table(new_table)
        self.tables = self.conn.get_table_list()

    def remove_table(self, table_obj):
        self.conn.remove_table(table_obj.table_name)

        self.tables = self.conn.get_table_list()

    def read_base_information(self):
        self.schemas = self.conn.get_schemas_list()
        self.tables = self.conn.get_table_list()

    def generate_config(self) -> dict:
        cfg = dict()
        cfg.update(self.db_data.db_info)

        cfg['schemas'] = {}
        cfg['schemas']['main'] = {}
        for table in self.tables:
            table_data = self.conn.get_table_data('main', table)
            cfg['schemas']['main'].update(table_data)

        return cfg

    def check_insert_table_possibility(self, new_table_name) -> bool:
        """
        :param new_table_name:name of new table
        :return: true if inserting is possible
        """
        # Check if table already exists
        for table in self.tables:
            if table == new_table_name:
                return False

        # Check if all tables that exists in base - defined in config
        for table in self.conn.get_table_schema_dict().values():
            if table not in [i.table_name for i in self.db_data.tables_info]:
                return False

        return True

    def check_remove_table_possibility(self, table_name_to_remove) -> bool:
        """
        :param table_name_to_remove: name of table to check
        :return: if table can be removed
        """

        return table_name_to_remove in self.tables

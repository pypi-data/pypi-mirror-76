from yaml_worker import YamlDataBaseWorker
from sql import SQLite, SQL


class DBWorker:

    def __init__(self, yaml: YamlDataBaseWorker):
        self.db_data = yaml
        self.conn = self.initialize_connection()
        self.db_identifier = f"{self.db_data.db_info['ip']}_{self.db_data.db_info['db_type']}_" \
                             f"{self.db_data.db_info['db_name']}"

    def check_if_used(self):
        pass

    def initialize_connection(self) -> SQL:
        pass

    def read_base_information(self):
        pass

    def check_base_updates(self):
        pass

    def remove_table(self, table_name):
        pass

    def insert_new_table(self, new_table):
        pass

    def generate_config(self):
        pass

    def check_insert_table_possibility(self, new_table_name):
        pass

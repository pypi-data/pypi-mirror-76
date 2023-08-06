"""Main module file of YamlBase"""


from dbworkers import SQLiteWorker
from yaml_worker import YamlDataBaseWorker
from exceptions import InsertActionImpossibleError, DataBaseTypeNotFound, ActionNotFound, \
    RemoveActionImpossibleError


class YBase:
    """Main class of YamlBase"""
    def __init__(self, path_to_yaml):
        """
        :param path_to_yaml: path to yaml representation of DataBase
        """
        self.yaml_config = YamlDataBaseWorker(path_to_yaml)
        self.db_worker = self.initialize_worker()

    def initialize_worker(self):
        if self.yaml_config.db_info['db_type'].lower() == 'sqlite':
            return SQLiteWorker(self.yaml_config)
        else:
            raise DataBaseTypeNotFound(self.yaml_config.db_info['db_type'])

    def detect_new_tables(self):
        """
        Search for new tables in yaml config
        :return: list of tables that was found in yaml but not in database
        """
        new_tables = []
        for table in self.yaml_config.tables_info:
            if table.table_name not in self.db_worker.tables:
                new_tables.append(table)
        return new_tables

    def detect_remove_tables(self):
        """
        Search for tables to remove in yaml config
        :return: list of tables that was found in base but not in yaml
        """
        remove_tables = []
        for table in self.db_worker.tables:
            if table.table_name not in [i.table_name for i in self.yaml_config.tables_info]:
                remove_tables.append(table)
        return remove_tables

    def do_action(self, action):
        """
        :param action:
        :return:
        """
        if action == 'insert':
            return self.insert_action()

        raise ActionNotFound(action)

    def check_action_possibility(self, action):
        action_is_possible = True
        if action == 'insert':
            for table in self.detect_new_tables():
                if not self.db_worker.check_insert_table_possibility(table):
                    action_is_possible = False
                # Condition for check optimization
                if not action_is_possible:
                    return action_is_possible
        if action == 'remove':
            for table in self.detect_remove_tables():
                if not self.db_worker.check_remove_table_possibility(table):
                    action_is_possible = False
                # Condition for check optimization
                if not action_is_possible:
                    return action_is_possible
        return action_is_possible

    def insert_action(self):
        if not self.check_action_possibility('insert'):
            raise InsertActionImpossibleError()

        self.db_worker.insert_new_tables(self.detect_new_tables())

    def remove_action(self):
        if not self.check_action_possibility('remove'):
            RemoveActionImpossibleError()

        self.db_worker.remove_tables(self.detect_new_tables())

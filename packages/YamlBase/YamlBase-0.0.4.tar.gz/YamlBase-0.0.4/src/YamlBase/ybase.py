"""Main module file of YamlBase"""


from dbworkers import SQLiteWorker
from yaml_worker import YamlDataBaseWorker, YamlActionsWorker
from exceptions import InsertActionImpossibleError, DataBaseTypeNotFound, ActionNotFound, \
    RemoveActionImpossibleError


class YBase:
    """Main class of YamlBase"""
    def __init__(self, path_to_yaml_db, path_to_yaml_actions):
        """
        :param path_to_yaml_db: path to yaml representation of DataBase
        :param path_to_yaml_actions: path to yaml with actions config
        """
        self.yaml_config = YamlDataBaseWorker(path_to_yaml_db)
        self.actions_config = YamlActionsWorker(path_to_yaml_actions)
        self.db_worker = self.initialize_worker()

    def initialize_worker(self):
        if self.yaml_config.db_info['db_type'].lower() == 'sqlite':
            return SQLiteWorker(self.yaml_config)
        else:
            raise DataBaseTypeNotFound(self.yaml_config.db_info['db_type'])

    def do_actions(self):
        for table, action in self.actions_config.action_table.items():
            try:
                self.do_action(action, self._filter_table(table))
                print(f"\nSUCCESS ACTION {action} on table {table}\n")
            except Exception as e:
                print(f"\nFAILED ACTION {action} on table {table}\nReason: {e}\n")

    def _filter_table(self, table_name):
        return [i for i in self.yaml_config.tables_info if i.table_name == table_name][0]

    def do_action(self, action, table_name):
        """
        :param action:
        :param table_name:
        :return:
        """
        if action == 'insert':
            return self.insert_action(table_name)
        elif action == 'remove':
            return self.remove_action(table_name)

        raise ActionNotFound(action)

    def check_action_possibility(self, action, table_obj):
        action_is_possible = True
        if action == 'insert':
            if not self.db_worker.check_insert_table_possibility(table_obj.table_name):
                action_is_possible = False
                # Condition for check optimization
                if not action_is_possible:
                    return action_is_possible
        if action == 'remove':
            if not self.db_worker.check_remove_table_possibility(table_obj.table_name):
                action_is_possible = False
                # Condition for check optimization
                if not action_is_possible:
                    return action_is_possible
        return action_is_possible

    def insert_action(self, new_table_name):
        if not self.check_action_possibility('insert', new_table_name):
            raise InsertActionImpossibleError()

        self.db_worker.insert_new_table(new_table_name)

    def remove_action(self, remove_table_name):
        if not self.check_action_possibility('remove', remove_table_name):
            raise RemoveActionImpossibleError()

        self.db_worker.remove_table(remove_table_name)

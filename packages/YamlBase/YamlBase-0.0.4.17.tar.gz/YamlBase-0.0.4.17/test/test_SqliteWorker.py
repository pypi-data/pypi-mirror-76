import sys
from sqlalchemy import create_engine
sys.path.extend(['../'])

from dbworkers import SQLiteWorker
from yaml_worker import YamlDataBaseWorker
import pytest


class TestSQLiteworker:

    def setup(self):
        self.cfg = YamlDataBaseWorker("test_base.yml")
        self.sqlite_connector = SQLiteWorker(self.cfg)

    def test_remove_tables(self):
        self.sqlite_connector.insert_new_table(self.cfg.tables_info[0])

        self.sqlite_connector.remove_table(self.cfg.tables_info[0])

        assert not self.sqlite_connector.tables

    def test_insert_new_tables(self):
        self.sqlite_connector.insert_new_table(self.cfg.tables_info[0])
        assert set(self.sqlite_connector.tables) <= set([i.table_name for i in self.cfg.tables_info])

        self.sqlite_connector.remove_table(self.cfg.tables_info[0])

    def test_check_insert_table_possibility(self):
        self.sqlite_connector.insert_new_table(self.cfg.tables_info[0])

        # Not to insert table that already exists
        assert not self.sqlite_connector.check_insert_table_possibility(self.cfg.tables_info[0].table_name)

        assert self.sqlite_connector.check_insert_table_possibility("test_name")

        self.sqlite_connector.remove_table(self.cfg.tables_info[0])

    def test_check_remove_table_possibility(self):
        self.sqlite_connector.insert_new_table(self.cfg.tables_info[0])

        # Not to insert table that already exists
        assert self.sqlite_connector.check_remove_table_possibility(self.cfg.tables_info[0].table_name)

        assert not self.sqlite_connector.check_remove_table_possibility("test_name")

        self.sqlite_connector.remove_table(self.cfg.tables_info[0])

    def test_read_base_information(self):
        self.sqlite_connector.insert_new_table(self.cfg.tables_info[0])
        self.sqlite_connector.read_base_information()

        assert self.sqlite_connector.schemas == ['main']
        assert self.cfg.tables_info[0].table_name in self.sqlite_connector.tables

        self.sqlite_connector.remove_table(self.cfg.tables_info[0])

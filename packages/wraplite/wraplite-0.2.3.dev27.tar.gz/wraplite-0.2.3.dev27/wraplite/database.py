import os
import sqlite3 as sql
from wraplite.table import Table, TableFormat

class Database():

    def __init__(self, name: str, folder_path: str) -> None:
        self.name = name
        self.folder_path = folder_path
        self.path = os.path.join(self.folder_path, self.name + '.db')
        self.con = sql.connect(self.path)
        for table_name in self.get_tables_list():
            setattr(self, table_name, Table(self.con, table_name))

    def __getattr__(self, name: str) -> None:
        table = Table(self.con, name).create()
        setattr(self, name, table)

    def __delattr__(self, name: str) -> None:
        table: Table = getattr(self, name)
        table.drop()
    
    def __str__(self) -> str:
        return 'database with tables: {}'.format(', '.join(self.get_tables_list()))

    def create_table(self, table_name: str, table_format: TableFormat) -> None:
        instruction = table_format.get_creation_instruction(table_name)
        setattr(self, table_name, Table(self.con, table_name).create(instruction))

    def get_tables_list(self) -> list:
        instruction = 'SELECT name FROM sqlite_master WHERE type=\'table\''
        with self.con:
            res = self.con.execute(instruction).fetchall()
            table_names = []
            for r in res:
                table_names.append(r[0])
            return table_names


import sqlite3 as sql
import datetime as dt
import pandas as pd
from wraplite import exceptions

class TableFormat(object):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) == 0: 
            raise ValueError('no values for row')
        for name, value in kwargs.items():
            setattr(self, name, value)
    
    def primary_keys(self, names: list) -> None:
        self._primary_keys = names
        return self
    
    def get_creation_instruction(self, table_name: str, error_if_exist: bool = True) -> str:
        self._table_name = table_name
        columns = []
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            column = key + ' '
            if value == str:
                column += 'TEXT'
            elif value == int:
                column += 'INTEGER'
            elif value == float:
                column += 'FLOAT'
            elif value == dt.datetime:
                column += 'DATETIME'
            else: 
                raise NotImplementedError()
            columns.append(column)
        if error_if_exist:
            main = 'CREATE TABLE'
        else:
            main = 'CREATE TABLE IF NOT EXISTS'

        return '{} {} ({}, PRIMARY KEY ({}) )'.format(
            main,
            self._table_name,
            ', '.join(columns),
            ', '.join(self._primary_keys)
        )

class Table():

    def __init__(self, con: sql.Connection, name: str) -> None:
        self.name = name
        self.con = con

    def __str__(self) -> str:
        return self.get_all().__str__()

    def create(self, instruction: str = None) -> None:
        if instruction is None:
            instruction = 'CREATE TABLE {} (id INTEGER NOT NULL PRIMARY KEY)'.format(self.name)
        with self.con:
            try:
                self.con.execute(instruction) 
            except Exception as e:
                print(e)
        return self
    
    def drop(self) -> None:
        instruction = 'DROP TABLE {}'.format(self.name)
        with self.con:
            self.con.execute(instruction)
            
    def drop_all(self) -> None:
        instruction = 'DELETE FROM {}'.format(self.name)
        with self.con:
            self.con.execute(instruction)
        return self
            
    def insert(self, df: pd.DataFrame) -> None:
        try:
            df.to_sql(name=self.name, con=self.con, if_exists='append', index=False)  
        except Exception as e:
            print(e)
            raise e

    def query(self, q: str) -> pd.DataFrame:
        if not q.upper().startswith('SELECT'):
            raise exceptions.NotSelectError()
        return pd.read_sql_query(q, self.con)

    def get_all(self) -> pd.DataFrame:
        return self.query('SELECT * FROM {}'.format(self.name))

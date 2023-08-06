import os
from wraplite import exceptions
from wraplite.database import Database

def get(name: str, folder_path: str = './', error_if_exist: bool = False) -> Database:
    if not os.path.isdir(folder_path):
        raise exceptions.FolderNotExistError()

    if error_if_exist:
        if os.path.exists(os.path.join(folder_path, name + '.db')):
            raise exceptions.DatabaseExistError()

    return Database(name, folder_path)
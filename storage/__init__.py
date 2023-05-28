from .base_storage import BaseStorage
from .db_storage import DBStorage
from .file_storage import FileStorage
from typing import Optional

class StorageFactory():

    storage_instance: Optional[BaseStorage]  = None

    __storages = {
        'db': DBStorage,
        'file': FileStorage
    }

    def __retrieve_storage(self, path:str, storage_type:str) -> None:
        ''' Retrieves storage instance '''
        self.storage_instance = self.__storages.get(storage_type)(path)

    def __init__(self, path:str, storage_type:str = 'file') -> None:
        ''' 
            Configures the cache path based on the storage 
            type of this cache instance 
        '''
        if not path:
            raise Exception('Path to storage must be provided')

        storage_type = 'db' if storage_type == 'database' else storage_type
        
        if storage_type != 'file' and storage_type != 'db':
            raise TypeError('Invalid storage type')

        self.__retrieve_storage(path, storage_type)
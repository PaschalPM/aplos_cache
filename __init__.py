from .storage.base_storage import BaseStorage
from .storage.file_storage import FileStorage
from .storage.db_storage import DBStorage
from .storage import StorageFactory
from os.path import abspath, join
from os import makedirs, unlink
from typing import Optional
import re

class Cache():

    storage_type: str = 'file'
    storage_dir: str = 'storage' # path to cache storage_directory
    file_name: str = 'cache'
    
    __cache_object: Optional[BaseStorage] = None

    def __init__(self, storage_type=None, storage_dir=None, file_name=None):
        '''.
            Configures the cache path based on the storage 
            type and sets cache object
        '''
        self.__configure(storage_type, storage_dir, file_name)
        

    def __configure(self, storage_type, storage_dir, file_name):
        ''' 
            Configures the cache path based on the storage 
            type of this cache instance 
        '''

        storage_type = storage_type if storage_type else Cache.storage_type

        storage_dir = storage_dir if storage_dir else Cache.storage_dir
        storage_dir = join(abspath('.'), storage_dir)
        makedirs(storage_dir, exist_ok=True)
        
        file_name = file_name if file_name else Cache.file_name
        file_name +='.db' if storage_type != 'file' else ''

        __cache_path = join(storage_dir, file_name)

        self.__cache_object = StorageFactory(__cache_path, storage_type).storage_instance

    def has(self, key):
        '''
            Checks if data (key, value) exists in file/db cache storage
            Returns: bool
        '''
        return self.__cache_object.has(key)

    def get(self, key):
        '''
            Retrieves data (key, value) if exists in file/db cache storage
            Returns: data | None
        '''
        return self.__cache_object.get(key)

    def put(self, key, value, exp_mins=10):
        '''
            Puts data (key, value) into the file/db cache storage
            Returns: bool
        '''
        return self.__cache_object.put(key, value, exp_mins=exp_mins)

    def pull(self, key):
        '''
            Deletes data (key, value) from file/db cache storage
            Returns: data | None
        '''
        return self.__cache_object.pull(key)

    def flush(self):
        '''
            Clears file/db cache storage
            Returns: bool
        '''
        return self.__cache_object.flush()


'''
Create a new Cache Storage Instance 
'''
cache = Cache()

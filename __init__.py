from .interface.file_cache import FileCache
from .interface.db_cache import DBCache
from os.path import abspath, join
from os import makedirs, unlink
import re

class Cache():

    storage_type = 'file'
    storage_dir = 'storage' # path to cache storage_directory
    file_name = 'cache'
    
    __cache_object = None
    __interface_register = {
        'file': FileCache,
        'db': DBCache
    }

    def __init__(self, storage_type=None, storage_dir=None, file_name=None):
        '''.
            Configures the cache path based on the storage 
            type and sets cache object
        '''
        self.__configure(storage_type, storage_dir, file_name)
        cache_interface =  Cache.__interface_register.get(self.storage_type)
        self.__cache_object = cache_interface(self.__cache_path)
        

    def __configure(self, storage_type, storage_dir, file_name):
        ''' 
            Configures the cache path based on the storage 
            type of this cache instance 
        '''

        self.storage_type = storage_type if storage_type else Cache.storage_type
        
        self.storage_type = 'db' if self.storage_type == 'database' else self.storage_type
        
        if self.storage_type != 'file' and self.storage_type != 'db':
            raise TypeError('Invalid storage type')

        self.storage_dir = storage_dir if storage_dir else Cache.storage_dir
        self.storage_dir = join(abspath('.'), self.storage_dir)
        makedirs(self.storage_dir, exist_ok=True)
        
        self.file_name = file_name if file_name else Cache.file_name
        self.file_name +='.db' if self.storage_type != 'file' else ''

        self.__cache_path = join(self.storage_dir, self.file_name)
    
    def has(self, key):
        '''
            Checks if data (key, value) exists in file/db cache storage
            Returns: bool
        '''
        return self.__cache_object._has(key)

    def get(self, key):
        '''
            Retrieves data (key, value) if exists in file/db cache storage
            Returns: data | None
        '''
        return self.__cache_object._get(key)

    def put(self, key, value, exp_mins=10):
        '''
            Puts data (key, value) into the file/db cache storage
            Returns: bool
        '''
        return self.__cache_object._put(key, value, exp_mins=exp_mins)

    def pull(self, key):
        '''
            Deletes data (key, value) from file/db cache storage
            Returns: data | None
        '''
        return self.__cache_object._pull(key)

    def flush(self):
        '''
            Clears file/db cache storage
            Returns: bool
        '''
        try:
            if self.storage_type != 'file':
                self.__cache_object._drop_connection()

            unlink(self.__cache_path)
            return (True)
    
        except Exception as e:
            return (False)


'''
Create a new Cache Storage Instance 
'''
cache = Cache()

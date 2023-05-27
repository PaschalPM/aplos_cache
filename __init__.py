from .src.file_cache import FileCache
from os.path import realpath, relpath, abspath, exists, join
from os import makedirs
import re

class Cache(FileCache):

    storage_dir = 'storage' # path to cache storage_directory
    file_name = 'cache'

    __cache_object = None

    def __init__(self, storage_dir=None, file_name=None):

        self.__configure(storage_dir, file_name)
        self.__cache_object = FileCache(self.storage_dir, self.file_name)
        

    def __configure(self, storage_dir, file_name):
        ''' Configures the storage_directory of this cache instance '''

        if not storage_dir:
            self.storage_dir = Cache.storage_dir
        else:
            self.storage_dir = storage_dir

        self.storage_dir = join(abspath('.'), self.storage_dir)

        makedirs(self.storage_dir, exist_ok=True)
        
        ''' Configures the storage file/db name of this cache instance '''
        if not file_name:
            self.file_name = Cache.file_name
        else:
            self.file_name = file_name

    
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

    def put(self, key, value, expiration=10):
        '''
            Puts data (key, value) into the file/db cache storage
            Returns: bool
        '''
        return self.__cache_object._put(key, value, expiration=expiration)

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
        return self.__cache_object._flush()


'''
Create a new Cache Storage Instance 
'''
cache = Cache()
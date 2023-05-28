from .base_storage import BaseStorage
from os import unlink
from os.path import exists, join
from time import time
from datetime import timedelta
from pickle import dump, load

class FileStorage(BaseStorage):
    __store: dict = {}
    __path: str = ''

    def __init__(self, path):
        self.__path = path

    def __commit(self) -> None:
        ''' Commits to the cache '''
        with open(self.__path, 'wb') as fp:
            dump(self.__store, fp)


    def _reload(self) -> None:
        '''
            Syncs cache store object with file store
        '''
        self.__store = {}
    
        if exists(self.__path):
            with open(self.__path, 'rb') as fp:
                cache = load(fp)
                cache_copy = cache.copy()
                if len(cache):
                    for key, val in cache_copy.items():
                        expiration = val.get('expiration')
                        cache.pop(key) if time() > expiration else None

                    self.__store = cache
                    self.__commit()
        

    def has(self, key) -> bool:
        '''
            Checks if data (key, value) exists in file cache storage
            Returns: bool
        '''
        self._reload()
        return True if self.__store.get(key, None) else False


    def get(self, key) -> list | dict | int | str:
        '''
            Retrieves data (key, value) if exists in file cache storage
            Returns: data | None
        '''
        self._reload()
        return self.__store.get(key, {}).get('value', None)
    

    def put(self, key, value, exp_mins=10) -> bool:
        '''
            Puts data (key, value) into file cache storage
            Returns: bool
        '''
        __expiration = timedelta(minutes=exp_mins).total_seconds()

        if (__expiration):
            self.__store[key] = {'value': value, 'expiration': time() + __expiration}
            self.__commit()
            return True

        return False


    def pull(self, key) -> list | dict | int | str:
        '''
            Deletes data (key, value) from file cache storage
            Returns: data | None
        '''
        self._reload()
        try:
            value, expiration = self.__store.pop(key).items()
            self.__commit()
            return value[1]
        except:
            return None

    def flush(self) -> bool:
        '''
            Clears file cache storage
            Returns: bool
        ''' 
        return self._unlink(self.__path)
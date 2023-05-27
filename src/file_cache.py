from os import unlink
from os.path import exists, join
from time import time
from datetime import timedelta
from pickle import dump, load

class FileCache:
    __cache_store = {}
    __cache_path = ''

    def __init__(self, cache_path):
        self.__cache_path = cache_path

    def __commit(self):
        ''' Commits to the cache '''
        with open(self.__cache_path, 'wb') as fp:
            dump(self.__cache_store, fp)


    def _reload(self):
        '''
            Syncs cache store object with file store
        '''
        self.__cache_store = {}
    
        if exists(self.__cache_path):
            with open(self.__cache_path, 'rb') as fp:
                cache = load(fp)
                cache_copy = cache.copy()
                if len(cache):
                    for key, val in cache_copy.items():
                        expiration = val.get('expiration')
                        cache.pop(key) if time() > expiration else None

                    self.__cache_store = cache
                    self.__commit()
        

    def _has(self, key):
        '''
            Checks if data (key, value) exists in file cache storage
            Returns: bool
        '''
        self._reload()
        return True if self.__cache_store.get(key, None) else False


    def _get(self, key):
        '''
            Retrieves data (key, value) if exists in file cache storage
            Returns: data | None
        '''
        self._reload()
        return self.__cache_store.get(key, {}).get('value', None)
    

    def _put(self, key, value, exp_mins=10):
        '''
            Puts data (key, value) into file cache storage
            Returns: bool
        '''
        __expiration = timedelta(minutes=exp_mins).total_seconds()

        if (__expiration):
            self.__cache_store[key] = {'value': value, 'expiration': time() + __expiration}
            self.__commit()
            return True

        return False


    def _pull(self, key):
        '''
            Deletes data (key, value) from file cache storage
            Returns: data | None
        '''
        self._reload()
        try:
            value, expiration = self.__cache_store.pop(key).items()
            self.__commit()
            return value[1]
        except:
            return None
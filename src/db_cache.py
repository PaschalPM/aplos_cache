import sqlite3
from os import unlink
from os.path import abspath, join
from time import time
from datetime import timedelta
from pickle import dumps, loads

class DBCache:
    __conn = None
    __cursor = None
    __cache_store = {}
    __cache_path = ''
    __last_sql = ''
    __last_params = {}

    def __init__(self, cache_dir, filename):
        self.__cache_path = join(cache_dir, filename)
        self.__conn = sqlite3.connect(self.__cache_path)
        self.__cursor = self.__conn.cursor()
        self.__create_table()
        self.__prune()
    
    def __create_table(self):
        ''' 
            Create the cache table
        '''
        self.__last_sql = '''
                CREATE TABLE IF NOT EXISTS cache(
                    key VARCHAR(256) NOT NULL UNIQUE PRIMARY KEY,
                    value BLOB(255) NOT NULL,
                    expiration FLOAT NOT NULL
                )
        '''
        self.__execute()

    def __execute(self):
        ''' Executes SQL Statements '''
        return self.__cursor.execute(self.__last_sql, self.__last_params)
    
    def __commit(self):
        ''' Commits to the cache '''
        self.__conn.commit()        


    def _has(self, key):
        '''
            Checks if data (key, value) exists in Database cache storage
            Returns: bool
        '''
        return True if self._get(key) else False

    def __prune(self):
        '''
            Prune away expired data from cache table
        '''
        self.__last_sql = 'DELETE FROM cache WHERE expiration < :now'
        self.__last_params = {'now': time()}
        self.__execute()
        self.__commit()
    

    def _get(self, key):
        '''
            Retrieves data (key, value) if exists in Database cache storage
            Returns: data | None
        '''
        self.__prune()
        self.__last_sql = 'SELECT * FROM cache where key = :key'
        self.__last_params = {'key': key}
        cursor = self.__execute()
        selected_row = cursor.fetchone()
        return loads(selected_row[1]) if selected_row else None

    def _put(self, key, value, exp_mins=10):
        '''
            Puts key, value, expiration into cache Database
            Returns: bool
        '''
        __expiration = timedelta(minutes=exp_mins).total_seconds()

        if __expiration:
            expiration = time() + __expiration
            value = dumps(value)
            self.__last_sql = '''
                INSERT OR REPLACE INTO cache(key, value, expiration) VALUES (:key, :value, :expiration)
            '''
            self.__last_params = {'key': key, 'value': value, 'expiration': expiration}
            self.__execute()
            self.__commit()
            return True

        return False

    def _pull(self, key):
        '''
            Deletes data (key, value) from Database cache storage
            Returns: data | None
        '''
        value = self._get(key)

        if value:
            self.__last_sql = 'DELETE FROM cache WHERE key = :key'
            self.__last_params = {'key': key}
            self.__execute()
            self.__commit()

        return value
    
    def _flush(self):
        '''
            Clears file cache storage
            Returns: bool
        '''
        pass

    def __del__(self):
        self.__conn.close()
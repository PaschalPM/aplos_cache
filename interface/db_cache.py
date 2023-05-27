import sqlite3
from os import unlink
from os.path import abspath, join
from time import time
from datetime import timedelta
from pickle import dumps, loads

class DBCache:
    _conn = None
    _is_connected = False
    __cursor = None
    __cache_path = ''
    __last_sql = ''
    __last_params = {}

    def __init__(self, cache_path):
        self.__cache_path = cache_path
        self._conn = sqlite3.connect(self.__cache_path, check_same_thread=False)
        self._is_connected = True
        self.__cursor = self._conn.cursor()
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
        self._conn.commit()        


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
        if self._is_connected:
            self.__last_sql = 'DELETE FROM cache WHERE expiration < :now'
            self.__last_params = {'now': time()}
            self.__execute()
            self.__commit()
    

    def _get(self, key):
        '''
            Retrieves data (key, value) if exists in Database cache storage
            Returns: data | None
        '''
        if self._is_connected:
            self.__prune()
            self.__last_sql = 'SELECT * FROM cache where key = :key'
            self.__last_params = {'key': key}
            cursor = self.__execute()
            selected_row = cursor.fetchone()
            return loads(selected_row[1]) if selected_row else None
    
        return None

    def _put(self, key, value, exp_mins=10):
        '''
            Puts key, value, expiration into cache Database
            Returns: bool
        '''
        __expiration = timedelta(minutes=exp_mins).total_seconds()

        if __expiration and self._is_connected:
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

        if value and self._is_connected:
            self.__last_sql = 'DELETE FROM cache WHERE key = :key'
            self.__last_params = {'key': key}
            self.__execute()
            self.__commit()

        return value
    
    def _drop_connection(self):
        '''
            Drops the connection to the database
        '''
        self._conn.close()
        self._is_connected = False

    def __del__(self):
        self._conn.close()

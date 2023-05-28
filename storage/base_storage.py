from abc import ABC, abstractmethod
from typing import Optional

class BaseStorage(ABC):
    __cache_path: str

    @abstractmethod
    def get(self, key) -> list | dict | int | str:
        pass
    
    @abstractmethod
    def has(self, key) -> bool:
        pass
    
    @abstractmethod
    def pull(self, key) -> list | dict | int | str:
        pass
    
    @abstractmethod
    def put(self, key, value, exp_mins=10) -> bool:
        pass

    @abstractmethod
    def flush(self) -> bool:
        pass

    def _unlink(self) -> bool:
        '''
            Clears db cache storage
            Returns: bool
        '''
        try:
            unlink(self.__cache_path)
            return (True)
    
        except Exception as e:
            return (False)
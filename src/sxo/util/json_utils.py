from typing import Dict
from typing import Any


class JsonError(Exception):
    ...

class JsonUtils:
    def __init__(self, _json:Dict[Any, Any]):
        self._json = _json

    def has_key(self, key:str) :
        return key in self._json

    def must_have(self, key:str) :
        if key not in self._json:
            raise JsonError(f'MISSING key in Json: {key}')
    
    
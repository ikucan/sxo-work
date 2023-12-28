from typing import Dict
from typing import Any

import numpy as np
import datetime as dt

class JsonError(Exception):
    ...

class JsonWrapperBase:
    def __init__(self, _json:Dict[Any, Any]):
        self._json = _json

    def raw_json(self,) :
        return self._json

    def has_key(self, key:str) :
        return key in self._json

    def must_have(self, key:str) :
        if key not in self._json:
            raise JsonError(f'MISSING key in Json: {key}')

    def set_str(self, key: str):
        ''' creates a string atribute on the class with the name key and value from json doc'''
        self.must_have(key)
        json_val = self._json[key]
        setattr(self, key, json_val)
    
    def set_int(self, key: str):
        ''' creates an int atribute'''
        self.must_have(key)
        json_val = self._json[key]
        setattr(self, key, int(json_val))

    def set_float(self, key: str):
        ''' creates a float atribute'''
        self.must_have(key)
        setattr(self, key, float(self._json[key]))

    def set_float_if(self, key: str):
        ''' creates a float atribute if present'''
        if self.has_key(key):
            setattr(self, key, float(self._json[key]))

    def set_bool(self, key: str):
        ''' creates a boolean atribute'''
        self.must_have(key)
        json_val = self._json[key]
        if isinstance(json_val, bool):
            setattr(self, key, json_val)
        elif isinstance(json_val, str):
            setattr(self, key, json_val.lower() == 'true')
        else:
            # this is dangerous but assume user knows what they are doing
            setattr(self, key, bool(json_val))

    def set_timestamp(self, key: str):
        ''' creates a timestamp atribute'''
        self.must_have(key)
        json_val = self._json[key]
        setattr(self, key, np.datetime64(json_val))

    def set_date(self,
                 key: str,
                 format: str = "%Y-%m-%d"):
        ''' creates a timestamp atribute'''
        self.must_have(key)
        json_val = self._json[key]
        aa = dt.datetime.strptime(json_val, format).date()

        setattr(self, key, np.datetime64(json_val))

import json
import time
from pathlib import Path
from functools import lru_cache

from typing import Any
from typing import Dict

def save(fnm: str, text: str):
    file = open(fnm, "w")
    file.write(text)
    file.close()

class JsonCacheError(Exception):
    ...

class JsonCache:

    @staticmethod
    @lru_cache
    def make(base:str|Path = None, make:bool = True):
        '''a cahced constructor wrapper'''
        return JsonCache(base, make)

    def __init__(self, base: str|Path, make:bool):
        if not base:
            if not make:
                raise JsonCacheError(f"ERROR, base path for Json Cache not specify")
            base = "/data/ref/"
        base_path = Path(base)
        
        if not base_path.exists():
            base_path.mkdir(True, True)

        self._base = base_path        

    def get(self,
            name:str| Path,
            max_age_s:int = 0,
            throw_if_missing:bool = False) -> Dict[Any, Any] | None:
        
        resource_path = self._base / name
        
        if not resource_path.exists():
            if throw_if_missing:
                raise JsonCacheError(f'ERROR. Name {resource_path} does not exist.')
            else:
                return None

        if time.time() - resource_path.stat().st_mtime > max_age_s:
            return None
        
        with open(resource_path.as_posix(), "r") as f:
            return json.load(f)

import json
import time
from pathlib import Path
from functools import lru_cache

from typing import Any
from typing import Dict


class JsonCacheError(Exception):
    ...

class JsonCache:

    @staticmethod
    @lru_cache
    def instance(base:str|Path = None, make:bool = True):
        '''a cahced constructor wrapper'''
        return JsonCache(base, make)

    def __init__(self, base: str|Path, make:bool):
        if not base:
            if not make:
                raise JsonCacheError(f"ERROR, base path for Json Cache not specify")
            base = "/data/ref/"
            print(f"WARNING. using default JsonCache location:: {base}")
        base_path = Path(base)
        
        base_path.mkdir(parents=True, exist_ok=True)

        self._base = base_path        

    def get(self,
            name:str | Path,
            max_age_s:int = -1,
            throw_if_missing:bool = False) -> Dict[Any, Any] | None:
        
        resource_path = self._base / name
        
        if not resource_path.exists():
            if throw_if_missing:
                raise JsonCacheError(f'ERROR. Name {resource_path} does not exist.')
            else:
                return None

        if (max_age_s >= 0 ) and (time.time() - resource_path.stat().st_mtime > max_age_s):
            return None
        
        with open(resource_path.as_posix(), "r") as f:
            try:
                return json.load(f)
            except Exception as e:
                print(f"ERROR reading cached JSON file at path {resource_path}. \n {e}")
                return None


    def put(self, name:str | Path, jsn: Dict[Any, Any]):

        resource_path = self._base / name
        
        resource_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(resource_path.as_posix(), "w") as f:
            json.dump(jsn, f, indent=2)

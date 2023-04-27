from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import TypeVar
from typing import Type

Json = Dict[Any, Any]

T = TypeVar('T')

Type Some[T] = Union[T, List[T]]


if __name__ == "__main__":
    print(123)
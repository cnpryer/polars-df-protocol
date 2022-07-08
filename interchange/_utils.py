from enum import IntEnum
from typing import Any


class DtypeKind(IntEnum):
    INT = 0
    UINT = 1
    FLOAT = 2
    BOOL = 20
    STRING = 21  # UTF-8
    DATETIME = 22
    CATEGORICAL = 23


DtypeKind_Primitive = {
    DtypeKind.INT,
    DtypeKind.UINT,
    DtypeKind.FLOAT,
    DtypeKind.BOOL,
}

CategoricalDescription = Any

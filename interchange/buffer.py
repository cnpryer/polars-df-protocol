from __future__ import annotations

from typing import Any

# TODO
BackedArray = Any


class Buffer:
    def __init__(self, arr: BackedArray, allow_copy: bool = False) -> Buffer:
        ...

    @property
    def bufsize(self) -> int:
        ...

    @property
    def ptr(self) -> int:
        ...

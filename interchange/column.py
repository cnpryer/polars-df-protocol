from __future__ import annotations

from typing import Any, Iterable, Optional

import polars as pl

from interchange._utils import CategoricalDescription, DtypeKind

ColumnBuffers = Any


class Column:
    ...

    def __init__(self, column: pl.Series, allow_copy: bool = True) -> None:
        ...

    @property
    def size(self) -> Optional[int]:
        ...

    @property
    def offset(self) -> int:
        ...

    @property
    def dtype(self) -> tuple[DtypeKind, int, str, str]:
        ...

    @property
    def describe_categorical(self) -> CategoricalDescription:
        ...

    @property
    def describe_null(self) -> tuple[DtypeKind, Any]:
        ...

    # TODO: why use cache here?
    @property
    def null_count(self) -> int:
        ...

    @property
    def metadata(self) -> dict[str, Any]:
        ...

    def num_chunks(self) -> int:
        ...

    def get_chunks(self, n_chunks: Optional[int] = None) -> Iterable[Column]:
        ...

    def get_buffers(
        self,
    ) -> ColumnBuffers:
        ...

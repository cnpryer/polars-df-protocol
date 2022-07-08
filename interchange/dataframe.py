from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

import polars as pl

from interchange.column import Column


class DataFrame:
    def __init__(
        self,
        df: pl.DataFrame,
        nan_as_null: bool = False,
        allow_copy: bool = True,
    ) -> None:
        ...

    def __dataframe__(
        self, nan_as_null: bool = False, allow_copy: bool = True
    ) -> DataFrame:
        ...

    @property
    def metadata(self) -> dict[str, Any]:
        ...

    def num_columns(self) -> int:
        ...

    def num_rows(self) -> int:
        ...

    def num_chunks(self) -> int:
        ...

    def column_names(self) -> Iterable[str]:
        ...

    def get_column(self, i: int) -> Column:
        ...

    def get_column_by_name(self, name: str) -> Column:
        ...

    def get_columns(self) -> Iterable[Column]:
        ...

    def select_columns(self, indices: Sequence[int]) -> DataFrame:
        ...

    def select_columns_by_name(self, names: Sequence[str]) -> DataFrame:
        ...

    def get_chunks(
        self, n_chunks: Optional[int] = None
    ) -> Iterable[DataFrame]:
        ...

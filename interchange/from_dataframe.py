"""An implementation of the DataFrame Intercahnge Protocol
``from_dataframe`` public function.

For more see https://data-apis.org/dataframe-protocol/latest/index.html
"""
from __future__ import annotations

import ctypes
from typing import Any, Optional, TypedDict

import polars as pl

from interchange._utils import DtypeKind, DtypeKind_Primitive
from interchange.buffer import Buffer
from interchange.column import Column
from interchange.dataframe import DataFrame

try:
    import numpy as np

    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False

# first pass uses numpy to hand the buffer data over to
# polars objects via ctypes.

# TODO: allow_copy True | False

BufferTypes = Any  # data, validity, offsets
BufferInterchangeRes = tuple[np.array, BufferTypes]

# numpy ctypes
_ints = {8: np.int8, 16: np.int16, 32: np.int32, 64: np.int64}
_uints = {8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64}
_floats = {32: np.float32, 64: np.float64}
_np_dtypes = {0: _ints, 1: _uints, 2: _floats, 20: {8: bool}}


def get_numpy_primitive_ctype(kind: DtypeKind, bitwidth: int) -> TypedDict:
    # takes dtype and bitwidth for numpy ctype
    column_dtype = _np_dtypes[kind][bitwidth]

    return column_dtype


def primitive_buffer_to_numpy_array(
    buffer: Buffer,
    dtype: DtypeKind,
    offset: int = 0,
    column_size: Optional[int] = None,
) -> np.array:
    # TODO: use offset and column_size

    # takes buffer (assuming just primitive types; caller handles)
    # TODO: should this be untyped?
    kind = dtype[0]
    bitwidth = dtype[1]

    # TODO: numpy decision
    column_dtype = get_numpy_primitive_ctype(kind, bitwidth)

    # No DLPack, so need to construct a new ndarray from the data pointer
    # and size in the buffer plus the dtype on the column
    ctypes_type = np.ctypeslib.as_ctypes_type(column_dtype)
    data_pointer = ctypes.cast(buffer.ptr, ctypes.POINTER(ctypes_type))

    # NOTE: `arr` does not own its memory, so the caller of this function must
    #       either make a copy or hold on to a reference of the column or
    #       buffer! (not done yet, this is pretty awful ...)
    # TODO: 8 might be better as a constant (is this bytes?)
    arr = np.ctypeslib.as_array(
        data_pointer, shape=(buffer.bufsize // (bitwidth // 8),)
    )

    return arr


def from_primitive_column(column: Column) -> BufferInterchangeRes:
    # takes column and returns numpy array with
    # the buffers from the column
    # TODO: numpy vs arrow vs pure python?
    buffers = column.get_buffers()
    data_buffer, data_dtype = buffers["data"]
    arr = primitive_buffer_to_numpy_array(
        data_buffer,
        dtype=data_dtype,
        offset=column.offset,
        column_size=column.size,
    )

    # TODO: apply validity
    # TODO: data_buffer of buffers? what about offsets?

    return arr, data_buffer


def from_chunk_to_polars_dataframe(chunk: DataFrame) -> pl.DataFrame:
    # takes dataframe interchange chunk and returns polars dataframe
    # assumes error handling is done by caller

    # data to instantiate polars dataframe with {col: vals}
    data = {}

    # buffers to retain during interchange
    buffers = []

    # {name: column} to perform interchange by column
    for name in chunk.column_names():
        column = chunk.get_column_by_name(name)
        kind = column.dtype[0]

        if kind in DtypeKind_Primitive:
            data[name], buffer = from_primitive_column(column)

        # TODO
        else:
            raise NotImplementedError(
                "Only primitive types are currently supported"
            )

        buffers.append(buffer)

    # TODO: use buffers
    res = pl.DataFrame(data)

    return res


def from_dataframe(df: DataFrame, allow_copy: bool = False) -> pl.DataFrame:
    # takes dataframe with interchange API and returns a polars dataframe
    if not _NUMPY_AVAILABLE:
        raise RuntimeError("numpy is required for the interchange")

    # TODO: must have numpy
    # TODO: must have pyarrow
    # TODO: must have __dataframe__
    # TODO: allow copy checks

    ix_df = df.__dataframe__(df, allow_copy=allow_copy)

    # concat chunks TODO: allow_copy
    dataframes = [
        from_chunk_to_polars_dataframe(ch) for ch in ix_df.get_chunks()
    ]
    res = pl.concat(dataframes)

    return res

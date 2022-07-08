# NOTE: __dataframe__ expected to come with 1.5.0
# target directly for now
import pandas as pd
import polars as pl

from interchange.from_dataframe import from_dataframe


def test_from_dataframe() -> None:
    # TODO: allow_copy = False
    pd_df = pd.DataFrame({"a": [0, 1]})
    pl_df = pl.DataFrame({"a": [0, 1]})

    pl.testing.assert_frame_equal(pl.from_pandas(pd_df), pl_df)

    expected = pl_df
    res = from_dataframe(pd_df)

    pl.testing.assert_frame_equal(res, expected)

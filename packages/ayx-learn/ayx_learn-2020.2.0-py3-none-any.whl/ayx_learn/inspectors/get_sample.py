# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Mixin implementation of sampling functionality used across several inspectors."""
from typing import Optional, Tuple, Union

from ayx_learn.typing import RandomStateLike

import pandas as pd

from typing_extensions import Protocol


class SupportsGetSample(Protocol):
    """Supports all of the attributes required for `get_sample` helper."""

    data: Union[pd.DataFrame, pd.Series]
    y: pd.Series
    max_samples: Optional[int]
    min_samples: int
    random_state: RandomStateLike


def get_sample(
    obj: SupportsGetSample
) -> Tuple[Union[pd.DataFrame, pd.Series], pd.Series]:
    """Run sampling on an object."""
    data_is_series = isinstance(obj.data, pd.Series)
    df = pd.concat(obj.data, obj.y)
    if obj.max_samples is not None and obj.max_samples < len(df):
        df = df.sample(obj.max_samples, obj.random_state)
        df.reset_index(drop=True, inplace=True)
    if obj.min_samples > len(df):
        df = df.sample(obj.min_samples, obj.random_state, replace=True)
        df.reset_index(drop=True, inplace=True)
    y = df.iloc[:, -1]
    X = df.iloc[:, :-1]
    if data_is_series:
        return X.iloc[:, 0], y
    else:
        return X, y

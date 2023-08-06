# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements array-like for type-checking.

For instancechecking, it's preferable to use `sklearn.utils.check_array`.
"""
from typing import Union

import numpy as np

import pandas as pd


ArrayLike = Union[pd.Series, pd.DataFrame, np.ndarray, list]

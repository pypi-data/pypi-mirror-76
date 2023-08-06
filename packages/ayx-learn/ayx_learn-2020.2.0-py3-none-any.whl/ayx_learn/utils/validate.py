# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Validation utility functions."""
import logging
from typing import Iterable, List

from ayx_learn.utils.constants import ColumnTypes
from ayx_learn.utils.exceptions import NullValueError

import pandas as pd

logger = logging.getLogger(__name__)


def validate_enum(value: str, enum: Iterable[str]):  # type: ignore
    """Validate value is in the enum.

    Parameters
    ----------
    value : str
        Value to be tested
    enum : Iterable[str]
        Enum to be tested

    Returns
    -------
    None
        If enum is valid.

    Raises
    ------
    TypeError
        If value is not in enum.
    """
    if value not in enum:
        raise TypeError(f"{value} is not a valid {enum}")


def validate_list_of_str(lst: List[str]):  # type: ignore
    """Validate that list consists of elements of type str.

    Parameters
    ----------
    lst : List[str]
        List of type str.

    Returns
    -------
    None
        If valid list.

    Raises
    ------
    TypeError
        If not a List or not all elements of list are of type str.
    """
    if not isinstance(lst, List):
        raise TypeError(f"{lst} is not a valid {List}")

    if not all(isinstance(elem, str) for elem in lst):
        raise TypeError(f"{lst} is not all of type str")


def validate_col_type(coltype: str) -> None:
    """Assert coltype is valid."""
    validate_enum(coltype, ColumnTypes)


def validate_no_nulls(df: pd.DataFrame) -> None:
    """Assert that a dataframe contains no null values."""
    names_of_columns_with_nulls = df.columns[df.isna().any()].to_list()

    if len(names_of_columns_with_nulls) > 0:
        err_str = (
            f"Dataframe contains null values in columns: {names_of_columns_with_nulls}"
        )
        logger.error(err_str)
        raise NullValueError(err_str, names_of_columns_with_nulls)  # type: ignore

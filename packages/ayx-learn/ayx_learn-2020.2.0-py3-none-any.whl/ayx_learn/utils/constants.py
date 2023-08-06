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
"""Constant values used throughout the ayx_learn library.

Attributes
----------
NA_PLACEHOLDER : str
    Value injected by default when a categorical value is imputed with "VALUE" method.
    In the context of an entire pipeline with OneHotEncoding, the actual value taken on is irrelevant

ColumnTypes : Iterable of str
    Iterable of ayx-learn acceptable column types (for use with ColumnTypeTransformer).

EncodingTypes : Iterable of str
    Iterable of ayx-learn acceptable encoding types.

"""
from enum import Enum as BaseEnum
from types import SimpleNamespace
from typing import Callable, Iterator, Union


class Enum(BaseEnum):
    """Enum definition that supports repr."""

    def __repr__(self) -> str:
        """Generate the representation of an enum."""
        return f"{self.__class__.__name__}({str(self)})"


class SimpleStringNamespace(SimpleNamespace):
    """SimpleNamespace-like wrapper for only strings."""

    def __init__(self, *strings: str):
        """Construct a simple string namespace.

        Parameters
        ----------
        *strings : str
            var args, each a string to be added as a SimpleNamespace of the form {string: string}

        """
        super().__init__(**{s: s for s in strings})

    @property
    def __iter__(self) -> Callable[[], Iterator[str]]:
        """Iterate over available strings."""
        return lambda: iter(self.__dict__.keys())

    def __call__(self, arg: Union[str, int]) -> str:
        """Effectively, validate that a string is inside the namespace."""
        try:
            # TODO: This is a hack to support the enum -> simplestringnamespace migration
            # between 20.1 and 20.2. Figure out a better way to handle this.
            if isinstance(arg, int):
                return list(self)[arg - 1]
            result = getattr(self, arg)  # type: str
            return result
        except AttributeError:
            raise ValueError(f"Unrecognized instance {arg}")


NA_PLACEHOLDER = "ayx_na_placeholder"


ColumnTypes = SimpleStringNamespace("CATEGORICAL", "NUMERIC", "BOOLEAN", "ID")


EncodingTypes = SimpleStringNamespace("ONE_HOT")

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
# flake8: noqa
"""Base objects for inspectors of data."""
from .base import BaseInspector
from .column_inspector import ColumnInspector
from .safe_inspect import SafeColInspectMixin
from .column_wise_inspector import ColumnWiseInspector
from .typing import ComputesMultiColumnInspection
from .combination import CombinationInspector


__all__ = [
    "BaseInspector",
    "ColumnInspector",
    "ColumnWiseInspector",
    "CombinationInspector",
    "ComputesMultiColumnInspection",
    "SafeColInspectMixin",
]

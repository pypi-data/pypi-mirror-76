# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
# flake8: noqa
"""Objects providing statistics, recommendations, and options."""
from .inspection import Inspection
from .column_inspection import ColumnInspection
from .force_drop import ForceDropInspection
from .failure import FailureInspection
from .multi_column import MultiColumnInspection


__all__ = [
    "ColumnInspection",
    "Inspection",
    "FailureInspection",
    "ForceDropInspection",
    "MultiColumnInspection",
]

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""ColumnInspection which forces dropping of a column."""
from typing import Any, Mapping, Optional

from ayx_learn.base.inspection.column_inspection import ColumnInspection
from ayx_learn.transformers import DropColumnTransformer


class ForceDropInspection(ColumnInspection):
    """Inspection to force dropping of column."""

    def __init__(
        self, column_name: str, statistics: Optional[Mapping[str, Any]] = None
    ):
        drop_column_transformer = DropColumnTransformer(column_name)
        super().__init__(column_name, drop_column_transformer, statistics=statistics)

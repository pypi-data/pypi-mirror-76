# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Base objects for inspectors columns."""
import abc
from typing import Optional

from ayx_learn.base.inspection import ColumnInspection
from ayx_learn.base.inspector.base import BaseInspector
from ayx_learn.base.pipeline import Pipeline

import pandas as pd


class ColumnInspector(BaseInspector):
    """Inspector for inspecting a single pandas.Series."""

    inspection: ColumnInspection

    def __init__(
        self,
        data: pd.Series,
        y: Optional[pd.Series] = None,
        upstream_pipeline: Optional[Pipeline] = None,
    ):
        """Construct the inspector.

        data : pd.Series
            data to inspect

        y : pd.Series (optional)
            target variable

        upstream_pipeline : Pipeline (default = Pipeline())
            previous actions on data

        """
        super().__init__(data=data, y=y, upstream_pipeline=upstream_pipeline)
        self.column_name = data.name

    # redefine for mypy
    @abc.abstractmethod
    def stateless_inspection(self) -> ColumnInspection:
        """Stateless computation of inspections.

        Returns
        -------
        Inspection object.
        """

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Base objects for running same column inspector on every column in dataset."""
from typing import Optional, Type

from ayx_learn.base.inspection import MultiColumnInspection
from ayx_learn.base.inspector.base import BaseInspector
from ayx_learn.base.inspector.column_inspector import ColumnInspector
from ayx_learn.base.pipeline import Pipeline

import pandas as pd


class ColumnWiseInspector(BaseInspector):
    """Inspector for running same inspector on every column in a dataframe."""

    def __init__(
        self,
        data: pd.DataFrame,
        column_inspector: Type[ColumnInspector],
        y: Optional[pd.Series] = None,
        upstream_pipeline: Optional[Pipeline] = None,
    ):
        """Construct the inspection.

        data : pd.DataFrame
            data to inspect

        column_inspector : ColumnInspector
            inspector to run on each column of data

        y : pd.Series (optional)
            target variable

        upstream_pipeline : Pipeline (default = Pipeline())
            previous actions on data

        """
        self.column_inspector = column_inspector
        self.inspectors = [
            self.column_inspector(
                data=data[name], y=y, upstream_pipeline=upstream_pipeline
            )
            for name in list(data)
        ]

    @property
    def inspection(self) -> MultiColumnInspection:  # type: ignore
        """Get the MultiColumnInspection housing all inspections for columns in data."""
        return MultiColumnInspection(
            [inspector.inspection for inspector in self.inspectors]
        )

    def stateless_inspection(self) -> MultiColumnInspection:
        """Compute stateless inspection.

        Returns
        -------
        MultiColumnInspection object.
        """
        if hasattr(self.column_inspector, "safe_inspect"):
            column_inspections = [
                inspector.safe_inspect().inspection  # type: ignore
                for inspector in self.inspectors
            ]
        else:
            column_inspections = [
                inspector.inspect().inspection for inspector in self.inspectors
            ]

        return MultiColumnInspection(column_inspections)

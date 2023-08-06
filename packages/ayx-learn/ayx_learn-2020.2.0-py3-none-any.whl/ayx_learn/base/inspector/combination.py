# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements base class for combining multiple inspectors."""
import abc
from typing import List, Tuple, Type

from ayx_learn.base.inspection import ColumnInspection, MultiColumnInspection
from ayx_learn.base.inspector.base import BaseInspector
from ayx_learn.base.inspector.typing import ComputesMultiColumnInspection

import pandas as pd


class CombinationInspector(BaseInspector):
    """Combines multiple inspectors."""

    dataframe_inspectors: Tuple[Type[ComputesMultiColumnInspection], ...]

    def __init__(self, data: pd.DataFrame, y: pd.Series):
        """Construct a combination inspector."""
        super().__init__(data=data, y=y)

    @property
    def column_names(self) -> List[str]:
        """Get the column names for the inspection."""
        return list(self.data)

    def stateless_inspection(self) -> MultiColumnInspection:
        """Run the inspection."""
        df_inspections = (
            inspector.stateless_inspection()  # type: ignore
            for inspector in self.dataframe_inspectors
        )
        inspection = MultiColumnInspection()
        for column in self.data:
            column_inspections = tuple(
                df_inspection.get_column_inspection(column)
                for df_inspection in df_inspections
            )
            inspection.add_column_inspection(
                self.combine_inspections(column_inspections)
            )
        return inspection

    @staticmethod
    @abc.abstractmethod
    def combine_inspections(
        inspections: Tuple[ColumnInspection, ...]
    ) -> ColumnInspection:
        """Combine a tuple of ColumnInspection objects."""
        pass

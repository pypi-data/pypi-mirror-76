# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Base inspector for combining absolute and relative importances."""
from typing import Tuple

from ayx_learn.base import ColumnInspection, CombinationInspector
from ayx_learn.transformers import DropColumnTransformer, IdentityTransformer
from ayx_learn.typing import SupportsTransform  # noqa F401


class CombinationImportanceInspector(CombinationInspector):
    """Combined importance inspector."""

    @staticmethod
    def combine_inspections(  # type: ignore  # supertype different api
        inspections: Tuple[ColumnInspection, ColumnInspection]
    ) -> ColumnInspection:
        """Combine two inspections into a single inspection."""
        relative, absolute = tuple(inspections)
        assert relative.column_name == absolute.column_name
        column_name = relative.column_name
        statistics = {
            "relative": relative.statistics["importance"],
            "absolute": absolute.statistics["importance"],
        }
        drop = DropColumnTransformer(relative.column_name)  # type: SupportsTransform
        keep = IdentityTransformer()  # type: SupportsTransform
        recommendation = (
            keep
            if CombinationImportanceInspector.keep(max(statistics.values()))
            else drop
        )
        options = {drop, keep}
        return ColumnInspection(column_name, recommendation, options, statistics)

    @staticmethod
    def keep(importance: float) -> bool:
        """Whether to recommend keeping a column based on its importance.

        Parameters
        ----------
        importance : float in [0, 1]

        """
        return 0.01 <= importance <= 0.75

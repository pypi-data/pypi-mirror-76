# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements inspector as container for multiple ColumnInspections."""
from collections.abc import Iterable
from itertools import product
from typing import Any, Dict, Iterable as IterableType, List, NoReturn, Optional, Set

from ayx_learn.base.inspection.inspection import Inspection
from ayx_learn.base.inspection.column_inspection import ColumnInspection  # noqa: I100
from ayx_learn.base.pipeline_step import PipelineStep


class MultiColumnInspection(Inspection):
    """Object to house a group of ColumnInspections."""

    def __init__(
        self, column_inspections: Optional[IterableType[ColumnInspection]] = None
    ):
        """Construct the inspector.

        Parameters
        ----------
        column_inspections : Iterable of ColumnInspection objects (default = [])
        """
        if not column_inspections:
            column_inspections = []
        self.column_inspections = column_inspections  # type: ignore #mypy setter issue

    @property
    def column_inspections(self) -> Dict[str, ColumnInspection]:
        """Get the column inspections."""
        return self.__column_inspections

    @column_inspections.setter
    def column_inspections(self, new: IterableType[ColumnInspection]) -> None:
        """Set the column inspections."""
        if not isinstance(new, Iterable) or not all(
            isinstance(elem, ColumnInspection) for elem in new
        ):
            raise TypeError(
                "column_inspections must be an Iterable of ColumnInspections."
            )
        self.__column_inspections: Dict[str, ColumnInspection] = {
            inspection.column_name: inspection for inspection in new
        }

    def add_column_inspection(
        self, column_inspection: ColumnInspection, if_exists: str = "update"
    ) -> None:
        """Add inspection for a column.

        Parameters
        ----------
        column_inspection : ColumnInspection
            inspection to add

        if_exists: str - "update", "keep", or "error"
            behavior if column inspection for the column already exists
                "update" - replace previous inspection for column with new one
                "keep" - keep previous inspection
                "error" - raise a ValueError

        """
        if if_exists not in {"keep", "update", "error"}:
            raise ValueError("unsupported value for if_exists")

        name = column_inspection.column_name
        exists = name in self.column_inspections.keys()

        if if_exists == "error" and exists:
            raise ValueError(f"Inspection for column {name} already exists.")
        elif if_exists == "keep" and exists:
            return
        else:
            self.__column_inspections[name] = column_inspection

    def get_column_inspection(self, column_name: str) -> ColumnInspection:
        """Get inspection for a column."""
        try:
            return self.__column_inspections[column_name]
        except KeyError:
            raise ValueError(f"No inspection for {column_name} exists.")

    @property
    def columns(self) -> List[str]:
        """All columns for which an inspection exists."""
        return list(self.column_inspections.keys())

    @property
    def recommendation(self) -> PipelineStep:
        """Get the recommendation."""
        return PipelineStep(
            {i.recommendation for i in self.column_inspections.values()}
        )

    # required because of python not allowing overriding of read-write with read-only
    @recommendation.setter
    def recommendation(self, new: Any) -> NoReturn:
        """Set the recommendation."""
        msg = "Property 'recommendation' of 'MultiColumnInspection' not writable."
        raise NotImplementedError(msg)

    @property
    def statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get the statistics."""
        return {
            column_name: inspection.statistics
            for column_name, inspection in self.column_inspections.items()
        }

    # required because of python not allowing overriding of read-write with read-only
    @statistics.setter
    def statistics(self, new: Any) -> NoReturn:
        """Set the statistics."""
        msg = "Property 'statistics' of 'MultiColumnInspection' not writable."
        raise NotImplementedError(msg)

    @property  # type: ignore
    def options(self) -> Set[PipelineStep]:  # type: ignore
        """Get the options for the transformer."""
        all_options = [
            inspection.options for inspection in self.column_inspections.values()
        ]
        combinations = product(*all_options)
        return {
            PipelineStep(combination) for combination in combinations  # type: ignore
        }

    # required because of python not allowing overriding of read-write with read-only
    @options.setter
    def options(self, new: Any) -> None:
        msg = "Property 'options' of 'MultiColumnInspection' not writable."
        raise RuntimeError(msg)

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Inspection object as a result of looking at a single column."""
from typing import AbstractSet, Any, Mapping, Optional, Set

from ayx_learn.base.inspection.inspection import Inspection
from ayx_learn.typing import SupportsTransform


class ColumnInspection(Inspection):
    """Inspection on single column.

    Recommended and allowable actions are transformers.
    """

    def __init__(
        self,
        column_name: str,
        recommendation: SupportsTransform,
        options: Optional[AbstractSet[SupportsTransform]] = None,
        statistics: Optional[Mapping[str, Any]] = None,
    ):
        """Construct the inspection.

        Parameters
        ----------
        column_name : str
            name of column of inspection

        recommendation : Transformer
            Recommended transformer to apply to a dataframe

        options : Set of Transformers, optional (default {recommendation})
            Set of all allowed transformers.
            Default is singleton set with recommended transformer.

        statistics : Mapping of names to values, optional (default: empty dict)
            Keys are names of properties, values are values.

        """
        self.column_name = column_name
        super().__init__(recommendation, options, statistics)

    @property
    def recommendation(self) -> SupportsTransform:
        """Recommended transformer to apply."""
        return self.__recommendation  # type: ignore

    @recommendation.setter
    def recommendation(self, new: SupportsTransform) -> None:
        """Set the recommendation."""
        self.__recommendation = new

    @property  # type: ignore  # not sure why these aren't compatible
    def options(self) -> Set[SupportsTransform]:  # type: ignore
        """Get the options."""
        return self.__options  # type: ignore

    @options.setter
    def options(self, new: AbstractSet[SupportsTransform]) -> None:
        """Set the options."""
        self.__options = set(new)

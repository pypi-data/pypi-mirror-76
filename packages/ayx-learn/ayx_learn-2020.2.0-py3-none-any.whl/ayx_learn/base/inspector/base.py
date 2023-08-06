# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Base class for inspectors of data."""
import abc
from typing import Optional, TypeVar

from ayx_learn.base.inspection import Inspection
from ayx_learn.base.pipeline import Pipeline
from ayx_learn.typing import ArrayLike


T = TypeVar("T", bound="BaseInspector")


class BaseInspector:
    """Abstract base inspector."""

    inspection: Inspection

    def __init__(
        self,
        data: ArrayLike,
        y: Optional[ArrayLike] = None,
        upstream_pipeline: Optional[Pipeline] = None,
    ):
        """Construct the inspector.

        data : array-like (e.g. pandas.Series, numpy.ndarray, pandas.DataFrame)
            data to inspect

        upstream_pipeline : Pipeline
            previous actions on data

        """
        self.data = data
        self.y = y
        if not upstream_pipeline:
            upstream_pipeline = Pipeline()
        self.upstream_pipeline = upstream_pipeline

    @abc.abstractmethod
    def stateless_inspection(self) -> Inspection:
        """Stateless computation of inspections.

        Returns
        -------
        Inspection object.
        """

    def inspect(self: T) -> T:
        """Perform inspection of object, mutating or replacing self.inspection."""
        self.inspection = self.stateless_inspection()
        return self

    def __repr__(self) -> str:
        """Generate a string representation of the object."""
        return (
            f"{self.__class__}("
            f"data={self.data}, "
            f"upstream_pipeline={self.upstream_pipeline})"
        )

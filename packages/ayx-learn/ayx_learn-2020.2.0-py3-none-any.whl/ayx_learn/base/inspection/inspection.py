# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements highest level inspection interface."""
from abc import ABC
from typing import AbstractSet, Any, Dict, Mapping, Optional, Set, Type, Union

from ayx_learn.typing import SupportsPredict, SupportsTransform


AnyStep = Union[SupportsTransform, SupportsPredict]


class Inspection(ABC):
    """Common interface for observing data and appending to a pipeline."""

    def __init__(
        self,
        recommendation: AnyStep,
        options: Optional[AbstractSet[AnyStep]] = None,
        statistics: Optional[Mapping[str, Any]] = None,
    ):
        """Construct the inspection.

        Parameters
        ----------
        recommendation : Transformer or Estimator
            Recommended action to apply to pipeline (e.g. Transformer, Estimator)

        options : Set of allowable actions to append to pipeline
            Set of all allowed transformers/ Estimators.
            Default is singleton set with recommended transformer.

        statistics : Dict mapping names to values, optional (default: empty dict)
            Keys are names of properties, values are values.

        """
        self.recommendation = recommendation

        if not options:
            options = {self.recommendation}
        self.options = options  # type: ignore # mypy doesn't check setter

        if not statistics:
            statistics = dict()
        self.statistics = statistics  # type: ignore # mypy doesn't check setter

    @classmethod
    def __subclasshook__(  # type: ignore # NotImplemented or bool
        cls: Type, C: Type  # noqa: N803
    ):
        """Check if class satisfies the inspection interface."""
        required_attrs = ["statistics", "recommendation", "options"]
        if cls is Inspection:
            for attr in required_attrs:
                if any(attr in B.__dict__ for B in C.__mro__):  # noqa: N806
                    continue
                return False
            return True
        return NotImplemented

    @property
    def recommendation(self) -> AnyStep:
        """Get the recommended step to apply."""
        return self.__recommendation

    @recommendation.setter
    def recommendation(self, new: AnyStep) -> None:
        """Set the recommended update."""
        self.__recommendation = new

    @property
    def options(self) -> Set[AnyStep]:
        """Get of allowed allowed steps."""
        return self.__options

    @options.setter
    def options(self, new: AbstractSet[AnyStep]) -> None:
        """Set the options for the transformer."""
        self.__options = set(new)

    @property
    def statistics(self) -> Dict[str, Any]:
        """Get the statistics."""
        return self.__statistics

    @statistics.setter
    def statistics(self, new: Mapping[str, Any]) -> None:
        """Set the statistics."""
        self.__statistics = dict(new)

    def __repr__(self) -> str:
        """Generate the string representation."""
        return (
            f"{self.__class__}("
            f"recommendation={self.recommendation}, "
            f"options={self.options}, "
            f"statistics={self.statistics})"
        )

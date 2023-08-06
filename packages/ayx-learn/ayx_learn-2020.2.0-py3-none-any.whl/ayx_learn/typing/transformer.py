# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Typehinting utilities for transformers."""
from abc import abstractmethod
from typing import Any, Optional, TypeVar

from ayx_learn.typing import ArrayLike

from typing_extensions import Protocol


A = TypeVar("A", bound="ArrayLike")
ST = TypeVar("ST", bound="SupportsTransform")


class SupportsTransform(Protocol):
    """Supports type-hinting of Transformers.

    Done via providing a minimal interface that a transformer must implement without
    need for explicit inheritance.

    Contrasts with the class Transformer which is useful for
    isinstance and issubclass checks.

    """

    @abstractmethod
    def fit(self: ST, X: ArrayLike, y: Optional[ArrayLike] = None, **kwargs: Any) -> ST:
        """Fit an arraylike object."""

    @abstractmethod
    def transform(self, X: A) -> A:
        """Transform an arraylike object."""

    @abstractmethod
    def fit_transform(
        self: ST, X: A, y: Optional[ArrayLike] = None, **fit_params: Any
    ) -> A:
        """Fit transform an arraylike object."""

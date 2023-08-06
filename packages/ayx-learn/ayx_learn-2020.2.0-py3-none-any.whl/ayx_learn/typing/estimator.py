# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Typehinting utilities for estimators."""
from abc import abstractmethod
from typing import Any, Optional

from ayx_learn.typing import ArrayLike

import numpy as np

from typing_extensions import Protocol


class SupportsPredict(Protocol):
    """Supports type-hinting of Estimator.

    Done via providing a minimal interface that an estimator must implement without
    need for explicit inheritance.

    Contrasts with the class Estimator which is useful for
    isinstance and issubclass checks.

    """

    @abstractmethod
    def fit(
        self, X: ArrayLike, y: Optional[ArrayLike], **kwargs: Any
    ) -> "SupportsPredict":
        """Fit an arraylike object."""

    @abstractmethod
    def predict(self, X: ArrayLike) -> ArrayLike:
        """Predict on an arraylike object."""


class SupportsImportances(Protocol):
    """Supports type-hinting of estimators with `.feature_importances_` attributes."""

    @property
    @abstractmethod
    def feature_importances_(self) -> np.array:
        """Get feature importances."""

    @abstractmethod
    def fit(
        self, X: ArrayLike, y: Optional[ArrayLike], **kwargs: Any
    ) -> "SupportsPredict":
        """Fit an arraylike object."""

    @abstractmethod
    def predict(self, X: ArrayLike) -> ArrayLike:
        """Predict on an arraylike object."""

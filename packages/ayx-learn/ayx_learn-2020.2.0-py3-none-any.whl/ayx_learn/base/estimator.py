# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements instancechecking, type-hinting of Estimators."""
from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from ayx_learn.typing import ArrayLike


class Estimator(ABC):
    """Supports instancechecking and subclasschecking of Estimator.

    An Estimator is defined as an object that implements fit and predict methods.

    Done via providing a minimal interface that an estimator must implement without
    need for explicit inheritance.

    Contrasts with the class SupportsPredict which is useful for static typechecking
    without runtime overhead.

    """

    @classmethod
    def __subclasshook__(  # type: ignore # NotImplemented or bool
        cls: Type, C: Type  # noqa: N803
    ):
        """Check that a class satisfies the estimator interface."""
        required_attrs = ["fit", "predict"]
        if cls is Estimator:
            for attr in required_attrs:
                if any(attr in B.__dict__ for B in C.__mro__):  # noqa: N806
                    continue
                return False
            return True
        return NotImplemented

    @abstractmethod
    def fit(self, X: ArrayLike, y: Optional[ArrayLike], **kwargs: Any) -> "Estimator":
        """Fit estimator.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Fitting dependent data

        y : pandas.Series or array-like, shape = (n_observations), optional
            Fitting target observations

        **kwargs :
            Additional arguments to pass to underlying transformers

        Returns
        -------
        self

        """

    @abstractmethod
    def predict(self, X: ArrayLike) -> ArrayLike:
        """Make predictions.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to predict.

        Returns
        -------
        Array-like, len: n_observations

        """

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements instancechecking, type-hinting of Transformers."""
from abc import ABC, abstractmethod
from typing import Any, Optional, Type, TypeVar

from ayx_learn.typing import ArrayLike


T = TypeVar("T", bound="Transformer")
A = TypeVar("A", bound="ArrayLike")


class Transformer(ABC):
    """Supports instancechecking and subclasschecking of Transformer.

    A Transformer is defined as an object that implements fit, transform, and fit_transform methods.

    Done via providing a minimal interface that a transformer must implement without
    need for explicit inheritance.

    Contrasts with the class SupportsTransform which is useful for static typechecking
    without runtime overhead.

    """

    @classmethod
    def __subclasshook__(  # type: ignore # NotImplemented or bool
        cls: Type, C: Type  # noqa: N803
    ):
        """Check if a class satisfies the transformer interface."""
        required_attrs = ["fit", "transform", "fit_transform"]
        if cls is Transformer:
            for attr in required_attrs:
                if any(attr in B.__dict__ for B in C.__mro__):  # noqa N806
                    continue
                return False
            return True
        return NotImplemented

    @abstractmethod
    def fit(self: T, X: ArrayLike, y: Optional[ArrayLike] = None, **kwargs: Any) -> T:
        """Fit transformer.

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
    def transform(self, X: A) -> A:
        """Transform data.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to transform.

        inplace : boolean, default = False
            Whether to transform the dataframe inplace.

        Returns
        -------
        ArrayLike, generally the same type as passed in as X

        """

    def fit_transform(
        self, X: A, y: Optional[ArrayLike] = None, **fit_params: Any
    ) -> A:
        """Fit, then transform data.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to transform.

        inplace : boolean, default = False
            Whether to transform the dataframe inplace.

        Returns
        -------
        ArrayLike, generally the same type as passed in as X

        """
        return self.fit(X=X, y=y, **fit_params).transform(X)

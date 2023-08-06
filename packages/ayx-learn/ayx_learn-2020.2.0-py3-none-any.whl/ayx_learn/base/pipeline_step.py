# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements pipeline as a sequence of transformers / model.

# TODO: consider use of sklearn.pipeline.FeatureUnion to handle parallel fitting
# TODO: and to get BaseEstimator interface
"""
from typing import Any, Iterator, MutableSet, Optional

from ayx_learn.typing import ArrayLike, SupportsTransform

from sklearn.base import TransformerMixin


class PipelineStep(TransformerMixin):
    """A collection of Transformers which can be fit and applied in any order.

    If the order of the transformers is important, use a pipeline instead.

    """

    def __init__(self, transformers: Optional[MutableSet[SupportsTransform]] = None):
        """Construct a pipeline step.

        Parameters
        ----------
        transformers : MutableSet of SupportsTransforms
            Set of objects that all implement fit, transform, and fit_transform.

        """
        if not transformers:
            transformers = set()
        self.transformers = set(transformers)

    def add_transformer(self, transformer: SupportsTransform) -> "PipelineStep":
        """Add a transformer to step.

        Parameters
        ----------
        transformer : SupportsTransform
            transformer to add

        Returns
        -------
        self

        """
        self.transformers.add(transformer)
        return self

    def fit(
        self, X: ArrayLike, y: Optional[ArrayLike] = None, **kwargs: Any
    ) -> "PipelineStep":
        """Fit step.

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
        for transformer in self.transformers:
            transformer.fit(X)
        return self

    def transform(self, X: ArrayLike, inplace: bool = False) -> ArrayLike:
        """Apply all transformers in step.

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
        X_new = X if inplace else X.copy()
        for t in self.transformers:
            X_new = t.transform(X_new)
        return X_new

    def __repr__(self) -> str:
        """Generate a string representation for this object."""
        separator = ",\n        "
        formatted_transformers = sorted(
            [repr(transformer) for transformer in self.transformers]
        )

        if len(formatted_transformers) == 0:
            formatted_kwargs = "transformers={}"
        else:
            formatted_kwargs = f"\n    transformers= {{\n        {separator.join(formatted_transformers)}\n    }}\n"
        return f"PipelineStep({formatted_kwargs})"

    def __hash__(self) -> int:
        """Generate a hash."""
        return hash(repr(self))

    def __eq__(self, other: Any) -> bool:
        """Check if another object is equal to this pipeline step."""
        if isinstance(other, PipelineStep):
            return repr(self) == repr(other)
        return NotImplemented

    def __iter__(self) -> Iterator[SupportsTransform]:
        """Provide an iterable for consumption."""
        for t in self.transformers:
            yield t

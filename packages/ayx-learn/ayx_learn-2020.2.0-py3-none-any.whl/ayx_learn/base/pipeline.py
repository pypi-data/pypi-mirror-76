# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements pipeline as a sequence of transformers / model."""
from collections.abc import Mapping, Sequence
from typing import (
    Any,
    Dict,
    List,
    Mapping as MappingType,
    Optional,
    Sequence as SequenceType,
    Tuple,
    TypeVar,
    Union,
)

from ayx_learn.base.estimator import Estimator
from ayx_learn.base.transformer import Transformer
from ayx_learn.typing import (
    AnyPipelineStep,
    NamedPipelineStep,
    NamedPipelineStepSequence,
    SupportsPredict,
    SupportsTransform,
)
from ayx_learn.utils.exceptions import (
    PredictWithoutClassificationEstimatorError,
    PredictWithoutEstimatorError,
)

import numpy as np

import pandas as pd

from sklearn.base import TransformerMixin
from sklearn.pipeline import (
    Pipeline as ScikitPipeline,
    make_pipeline as make_sklearn_pipeline,
)


P = TypeVar("P", bound="Pipeline")


class Pipeline(TransformerMixin, Sequence):
    """A sequence of transformers with an optional estimator at the end."""

    def __init__(self, steps: Optional[NamedPipelineStepSequence] = None):
        """Construct a pipeline."""
        if not steps:
            steps = []
        self.validate_steps(steps)
        self.steps = list(steps)

    @staticmethod
    def validate_steps(steps: NamedPipelineStepSequence) -> None:
        """Validate that the steps are a valid pipeline."""
        for name, step in steps[:-1]:
            if not isinstance(step, Transformer):
                raise ValueError("All non-final steps must be transformers.")
        for name, step in steps[-1:]:
            if not isinstance(step, (Transformer, Estimator)):
                raise ValueError("Final step must be transformer or estimator.")

    # ----------- Accessing steps -----------#

    @property
    def estimator(self) -> Optional[SupportsPredict]:
        """Get the estimator in the pipeline."""
        if self.steps and isinstance(self.steps[-1][1], Estimator):
            return self.steps[-1][1]
        return None

    @property
    def transformers(self) -> List[SupportsTransform]:
        """Get the transformers in the pipeline."""
        if not self.steps:
            return []
        transform_steps = self.steps[:-1] if self.estimator else self.steps
        return [s[1] for s in transform_steps]  # type: ignore

    @property
    def step_names(self) -> List[str]:
        """Get the step names."""
        return [s[0] for s in self.steps]

    @property
    def named_steps_list(self) -> List[NamedPipelineStep]:
        """Get the list of named steps."""
        return self.steps

    @property
    def named_steps_dict(self) -> Dict[str, AnyPipelineStep]:
        """Get the named steps of the pipeline."""
        return {s[0]: s[1] for s in self.steps}

    @property
    def unnamed_steps(self) -> List[AnyPipelineStep]:
        """Get the unnamed steps of the pipeline."""
        return [s[1] for s in self.steps]

    # ----------- FitTransform methods -----------#

    def fit(
        self: P, X: pd.DataFrame, y: Optional[pd.Series] = None, **kwargs: Any
    ) -> P:
        """Fit pipeline.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Fitting dependent data

        y : pandas.Series or array-like, shape = (n_observations), optional
            Fitting target observations

        **kwargs :
            Additional arguments to pass to underlying transformer

        """
        X_new = X.copy()
        if not self.steps:
            return self
        # Optimization - don't need to transform last step
        # Need to transform all previous ones to properly fit next one
        for step in self.unnamed_steps[:-1]:
            X_new = step.fit_transform(X_new, y=y, **kwargs)  # type: ignore
        self.unnamed_steps[-1].fit(X_new, y=y, **kwargs)
        return self

    def transform(self, X: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
        """Apply all transform steps in pipeline.

        Parameters
        ----------
        X : pandas.DataFrame, shape = (n_feature, n_observations)
            Data to transform.

        inplace : boolean, default = False
            Whether to transform the dataframe inplace.

        """
        X_new = X if inplace else X.copy()
        for t in self.transformers:
            X_new = t.transform(X_new)
        return X_new

    # ----------- Prediction methods -----------#

    def predict(self, X: pd.DataFrame) -> np.array:
        """Predicts results of pipeline for each observation in X.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to predict on.

        """
        X_new = self.transform(X)
        if self.estimator:
            return self.estimator.predict(X_new)
        else:
            msg = "Estimator must be at end of pipeline to predict."
            raise PredictWithoutEstimatorError(msg)

    def predict_proba(self, X: pd.DataFrame) -> np.array:
        """Predicts probabilities of classes of pipeline for each observation in X.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to predict on.

        """
        X_new = self.transform(X)
        if self.estimator and hasattr(self.estimator, "predict_proba"):
            return self.estimator.predict_proba(X_new)  # type: ignore
        else:
            msg = "Classifier must be at end of pipeline to predict."
            raise PredictWithoutClassificationEstimatorError(msg)

    def predict_with_proba(self, X: pd.DataFrame) -> Tuple[np.array, np.array]:
        """Efficiency wrapper to return predictions and probabilities but only tranform once.

        Parameters
        ----------
        X : pandas.DataFrame or array-like, shape = (n_feature, n_observations)
            Data to predict on.

        """
        X_new = self.transform(X)
        if self.estimator and hasattr(self.estimator, "predict_proba"):
            predictions = self.estimator.predict(X_new)
            probas = self.estimator.predict_proba(X_new)  # type: ignore
            return predictions, probas
        else:
            msg = "Classifier must be at end of pipeline to predict."
            raise PredictWithoutClassificationEstimatorError(msg)

    # ----------- Sequence methods -----------#

    def __getitem__(  # type: ignore
        self: P, val: Union[int, slice, str]
    ) -> Union[P, AnyPipelineStep]:
        """Return a sub-pipeline or a single step in the pipeline.

        Return type depends on the argument type for `val`.
            If int: return step object at position val.
            If str: return step object with name val.
            If slice: return new Pipeline object of same type with steps of slice.
                NOTE: only step size allowed for slicing pipeline is 1.

        """
        if isinstance(val, slice):
            if val.step not in (1, None):
                raise ValueError("Pipeline slicing only supports a step of 1")
            return self.__class__(self.steps[val])
        elif isinstance(val, int):
            return self.steps[val][1]
        else:
            return self.named_steps_dict[val]

    def __len__(self) -> int:
        """Get number of steps in pipeline."""
        return len(self.steps)

    # ----------- Conversions -----------#

    def make_sklearn_pipeline(self) -> ScikitPipeline:
        """Get an sklearn pipeline with same steps."""
        return ScikitPipeline(self.steps)

    # ----------- Misc -----------#

    def __repr__(self) -> str:
        """Get representation."""
        return f"{self.__class__}({repr(self.steps)})"

    def add_step(
        self: P, step: Any, idx: Optional[int] = None, name: Optional[str] = None
    ) -> P:
        """Add step to pipeline.

        Parameters
        ----------
        step : Transformer or Estimator to add

        idx : int, optional (default: None)
            numeric position to add step to.
            Defaults to end of pipeline.

        name : str, optional (default: idx)
            name of step, defaults to str(idx)

        Returns
        -------
        new pipeline object

        """
        if idx is None:
            idx = len(self)

        if name is None:
            name = str(idx)

        previous_steps = self.steps[:idx]
        current_step = (name, step)
        next_steps = self.steps[idx:]
        new_steps = previous_steps + [current_step] + next_steps
        return self.__class__(steps=new_steps)


SupportedConstructions = Optional[
    Union[
        SequenceType[NamedPipelineStep],
        SequenceType[AnyPipelineStep],
        MappingType[str, AnyPipelineStep],
        Pipeline,
        ScikitPipeline,
    ]
]


def _is_unnamed_step_sequence(obj: Any) -> bool:
    try:
        return all(isinstance(elem, (Transformer, Estimator)) for elem in obj)
    except Exception:
        return False


def _is_named_step_sequence(obj: Any) -> bool:
    try:
        return all(
            isinstance(elem, tuple)
            and len(elem) == 2
            and isinstance(elem[0], str)
            and isinstance(elem[1], ((Transformer, Estimator)))
            for elem in obj
        )
    except Exception:
        return False


def _is_step_mapping(obj: Any) -> bool:
    try:
        return _is_named_step_sequence(list(obj.items()))
    except Exception:
        return False


def make_pipeline(
    obj: SupportedConstructions = None, *sklearn_args: Any, **sklearn_kwargs: Any
) -> Pipeline:
    """Convert objects to a pipeline.

    Supports:
        - Sequence of Transformers / Estimators
        - Sequence of Tuples: (Name (str), Transformer / Estimator)
        - Mapping of names (str) to Transformer / Estimator
        - Pipeline
        - sklearn.pipeline.Pipeline
        - None
        - arguments to pass to sklearn pipeline constructor
    """
    if isinstance(obj, Pipeline):
        return obj
    elif isinstance(obj, ScikitPipeline):
        return Pipeline(obj.steps)
    elif obj is None:
        if sklearn_args or sklearn_kwargs:
            return make_pipeline(make_sklearn_pipeline(*sklearn_args, **sklearn_kwargs))
        else:
            return Pipeline()
    elif isinstance(obj, Sequence):
        if _is_named_step_sequence(obj):
            return Pipeline(obj)  # type: ignore
        elif _is_unnamed_step_sequence(obj):
            named_steps = [(str(i), step) for i, step in enumerate(obj)]
            return Pipeline(named_steps)  # type: ignore
        else:
            raise TypeError("Sequence must be all either named or unnamed steps.")
    elif isinstance(obj, Mapping):
        if _is_step_mapping(obj):
            named_steps = list(obj.items())
            return Pipeline(named_steps)  # type: ignore
        else:
            raise TypeError("Mapping must be names to steps.")
    else:
        raise TypeError("Unsupported type for make_pipeline.")

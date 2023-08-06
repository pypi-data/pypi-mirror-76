# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements base abstract strategy."""
import abc
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from ayx_learn.base.inspector import BaseInspector
from ayx_learn.base.pipeline import Pipeline
from ayx_learn.evaluations.evaluation import Evaluation
from ayx_learn.transformers import OneHotEncoderTransformer
from ayx_learn.typing import ArrayLike, SupportsPredict

import pandas as pd


P = TypeVar("P", bound="Pipeline")


class Strategy(abc.ABC):
    """Strategy abstract interface."""

    @property
    @abc.abstractmethod
    def estimators(self) -> List[Type[SupportsPredict]]:
        """Get estimators to make available."""
        pass

    @property
    @abc.abstractmethod
    def steps(self) -> Dict[str, Type[BaseInspector]]:
        """Get steps to make available.

        An inspector will generally act as a step with various options.
        TODO: make a transformer act a "hidden" inspector which provides one option.
        """
        pass

    def get_step(self, step_name: str) -> Type[BaseInspector]:
        """Get step by name.

        Parameters
        ----------
        step_name : str
            name of step

        Returns
        -------
        Inspector object

        Raises
        ------
        ValueError
            If step_name not in steps

        """
        try:
            return self.steps[step_name]
        except KeyError:
            raise ValueError(f"{step_name} not present in strategy steps.")

    def get_step_index(self, step_name: str) -> int:
        """Get numeric index of step.

        Parameters
        ----------
        step_name : str
            name of step

        Returns
        -------
        int (>= 0)
            numeric index of step

        Raises
        ------
        ValueError
            If step_name not in steps

        """
        for idx, name in enumerate(self.steps.keys()):
            if step_name == name:
                return idx
        raise ValueError(f"{step_name} not present in strategy steps.")

    def get_next_step_name(self, step_name: str) -> Union[str, None]:
        """Get the name of subsequent step.

        Parameters
        ----------
        step_name : str
            name of step

        Returns
        -------
        str : name of next step if step_name is before end of steps
        None : if step_name the last step

        Raises
        ------
        ValueError
            If step_name not in steps

        """
        if step_name not in self.steps.keys():
            raise ValueError(f"{step_name} not present in strategy steps.")
        try:
            idx = 1 + self.get_step_index(step_name)
            return list(self.steps.keys())[idx]
        except IndexError:
            return None

    def get_first_step_name(self) -> Union[str, None]:
        """Get name of first step.

        Returns
        -------
        str : name of first step if steps is not empty
        None : if there is no first step

        """
        try:
            return list(self.steps.keys())[0]
        except KeyError:
            return None

    @abc.abstractmethod
    def get_partition(
        self, fold_idx: int, *data: Tuple[ArrayLike, ...]
    ) -> Tuple[Tuple[ArrayLike, ...], ...]:
        """Given data and an index, get a partitioning of the data.

        Parameters
        ----------
        fold_idx : int
            index of fold

        *data
            additional data elements (e.g. X, y for supervised)

        """
        pass

    def build_pipeline(
        self, transform_pipeline: P, estimator: SupportsPredict, inplace: bool = True
    ) -> P:
        """Assemble pipeline of transforms with model.

        Parameters
        ----------
        transform_pipeline : Pipeline
            pipeline of transforms

        estimator : Estimator
            model to append to pipeline

        inplace : bool
            whether to mutate the `transform_pipeline` passed in

        Returns
        -------
        Pipeline with additional transform(s) and estimator appended.

        """
        # TODO: get rid of; using implicit steps (transformers) in steps property
        pipeline = transform_pipeline if inplace else deepcopy(transform_pipeline)
        ohe = OneHotEncoderTransformer(handle_unknown="ignore")
        pipeline.add_step(ohe)
        pipeline.add_step(estimator)
        return pipeline

    def fit(self, pipeline: Pipeline, *train_data: ArrayLike) -> Pipeline:
        """Train a pipeline."""
        pipeline.fit(*train_data)
        return pipeline

    @abc.abstractmethod
    def get_data(self, df: ArrayLike) -> Tuple[ArrayLike, ...]:
        """Get components of data given a dataframe."""
        pass

    @abc.abstractmethod
    def get_prediction_details(
        self, pipeline: Pipeline, test_data: Tuple[ArrayLike, ...], **kwargs: Any
    ) -> Dict[str, Any]:
        """Compute intermediate values used by ModelEvaluationEntity objects.

        Parameters
        ----------
        pipeline : PipelineEntity
            A previously-fit pipeline.

        *test_data
            Validation data (tuple of array-likes) for testing

        **kwargs :

        Returns
        -------
        dict : keys str
            Mapping of names to values

        """
        pass

    @property
    @abc.abstractmethod
    def evaluators(self) -> List[Type[Evaluation]]:
        """Get names of valid ModelEvaluation objects."""
        pass

    def create_evaluations(self, **prediction_details: Any) -> List[Evaluation]:
        """Generate Evaluation objects ready for evaluation.

        Parameters
        ----------
        prediction_details : dict
            as returned by get_prediction_details

        Returns
        -------
        List of Evaluation objects

        """
        return [evaluator(**prediction_details) for evaluator in self.evaluators]

    def run_evaluations(self, **prediction_details: Dict[str, Any]) -> List[Evaluation]:
        """Generate ModelEvaluationEntity objects and run them.

        Parameters
        ----------
        prediction_details : dict
            as returned by get_prediction_details

        Returns
        -------
        List of ModelEvaluation objects

        """
        evaluations = self.create_evaluations(**prediction_details)
        for evaluation in evaluations:
            evaluation.eval_fold(**prediction_details)  # type: ignore
        return evaluations

    @abc.abstractmethod
    def validate_df(self, df: pd.DataFrame) -> None:
        """Validate that df is a valid dataset for the particular strategy."""
        pass

    def get_inspector(
        self, df: pd.DataFrame, upstream_pipeline: Pipeline
    ) -> Optional[BaseInspector]:
        """Get next constructed inspector to run."""
        last_step = upstream_pipeline.step_names[-1]
        next_step_name = self.get_next_step_name(last_step)
        if not next_step_name:
            return None
        constructor = self.get_step(next_step_name)
        if hasattr(self, "target"):
            X = df.drop(columns=[self.target])  # type: ignore
            y = df[self.target]  # type: ignore
        else:
            X = df
            y = None
        return constructor(data=X, y=y, upstream_pipeline=upstream_pipeline)

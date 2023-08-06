# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements concrete strategy for multiclass classification."""
from typing import List, Type

from ayx_learn.classifiers import (
    DecisionTreeClassifier,
    RandomForestClassifier,
    XGBClassifier,
)
from ayx_learn.evaluations import (
    Accuracy,
    ClassificationImportance,
    ConfusionMatrix,
    Evaluation,
    LogLoss,
    M,
    ROC,
)
from ayx_learn.strategies.classification import ClassificationStrategy
from ayx_learn.typing import ArrayLike, SupportsPredict
from ayx_learn.utils.exceptions import TooManyLevelsError

import numpy as np

from sklearn.utils import check_array


class MulticlassStrategy(ClassificationStrategy):
    """Strategy for multiclass analyses."""

    _MAX_LEVELS = 10

    @property
    def evaluators(self) -> List[Type[Evaluation]]:
        """Get the supported evaluators."""
        return [Accuracy, ClassificationImportance, ConfusionMatrix, LogLoss, M, ROC]

    @property
    def estimators(self) -> List[Type[SupportsPredict]]:
        """Get the supported estimators."""
        return [DecisionTreeClassifier, RandomForestClassifier, XGBClassifier]

    def validate_target(self, target: ArrayLike) -> None:
        """Validate that target is suitable for multiclass classification."""
        target = check_array(target)
        nonnulls = target[~np.isnan(target)]
        n_unique = len(np.unique(nonnulls))
        if n_unique > self._MAX_LEVELS:
            raise TooManyLevelsError(
                f"For multiclass classification, target must have no more than {self._MAX_LEVELS} non-null unique values. Actual: {n_unique}."
            )

    def create_evaluations(self, levels, **prediction_details):  # type: ignore
        """Create the evaluations."""
        evaluations = []
        for evaluator in self.evaluators:
            if evaluator.__name__ == "ROC":
                # We want 1 ROC curve per level, but they're saved as separate evaluations.
                for level in levels:
                    params = prediction_details.copy()
                    params.update({"positive_class": level, "levels": levels})
                    evaluations.append(evaluator(**params))
            else:
                new_params = {
                    **{"levels": levels},
                    **prediction_details,
                }  # make mypy happy
                evaluations.append(evaluator(**new_params))

        return evaluations

# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements concrete strategy for binary classification."""
from typing import List, Type

from ayx_learn.classifiers import (
    DecisionTreeClassifier,
    LogisticRegressionClassifier,
    RandomForestClassifier,
    XGBClassifier,
)
from ayx_learn.evaluations import (
    AUC,
    Accuracy,
    ClassificationImportance,
    ConfusionMatrix,
    Evaluation,
    LogLoss,
    ROC,
)
from ayx_learn.strategies.classification import ClassificationStrategy
from ayx_learn.typing import ArrayLike, SupportsPredict
from ayx_learn.utils.exceptions import NonBinaryTargetError

import numpy as np

from sklearn.utils import check_array


class BinaryStrategy(ClassificationStrategy):
    """Strategy for binary classification."""

    @property
    def evaluators(self) -> List[Type[Evaluation]]:
        """Get the supported evaluations."""
        return [Accuracy, AUC, ClassificationImportance, ConfusionMatrix, LogLoss, ROC]

    @property
    def estimators(self) -> List[Type[SupportsPredict]]:
        """Get the supported estimators."""
        return [
            DecisionTreeClassifier,
            LogisticRegressionClassifier,
            RandomForestClassifier,
            XGBClassifier,
        ]

    def validate_target(self, target: ArrayLike) -> None:
        """Validate the target is suitable for binary classification."""
        target = check_array(target)
        nonnulls = target[~np.isnan(target)]
        n_unique = len(np.unique(nonnulls))
        if n_unique != 2:
            raise NonBinaryTargetError(
                f"For binary classification, target must have exactly 2 non-null unique values. Actual: {n_unique}."
            )

# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Adjusted R squared measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.evaluations.regression import RegressionEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np

from sklearn.metrics import r2_score


class AdjR2(RegressionEvaluation, MultiFoldEvaluation):
    """Adjusted R2 score supporting fold-independent evaluation and aggregation across folds.

    References
    ----------
    .. [1] Adjusted R squared: https://en.wikipedia.org/wiki/Coefficient_of_determination#Adjusted_R2

    """

    def __init__(self):  # type: ignore  # type: ignore
        """Construct the evaluation."""
        RegressionEvaluation.__init__(self)  # type: ignore
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, y_true, y_pred, pipeline, **kwargs):  # type: ignore
        """Run the evaluation."""
        # implementing reference [1]
        r2 = r2_score(y_true, y_pred)
        n = len(y_true)
        p = len(pipeline.model.predictors)
        if (n - p - 1) != 0:
            return 1 - (1 - r2) * (n - 1) / (n - p - 1)
        else:
            return 0

    def format(self, x):  # type: ignore
        """Run the format to external representation."""
        return x

    def inverse_format(self, x):  # type: ignore
        """Run the inverse format to internal representation."""
        return x

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        return np.mean(scores)

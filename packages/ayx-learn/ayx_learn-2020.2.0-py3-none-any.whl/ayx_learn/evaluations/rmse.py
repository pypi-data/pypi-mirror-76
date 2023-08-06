# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Root mean squared error measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.evaluations.regression import RegressionEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np


class RMSE(RegressionEvaluation, MultiFoldEvaluation):
    """Mean absolute error supporting fold-independent evaluation and aggregation across folds."""

    def __init__(self):  # type: ignore  # type: ignore
        """Construct the evaluation."""
        RegressionEvaluation.__init__(self)  # type: ignore
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, residuals, **kwargs):  # type: ignore
        """Run the evaluation."""
        return rmse(residuals)  # type: ignore

    def format(self, x):  # type: ignore
        """Run the format to external representation."""
        return x

    def inverse_format(self, x):  # type: ignore
        """Run the inverse format to internal representation."""
        return x

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        return np.sqrt(np.mean(np.square(self.scores)))


def rmse(residuals):  # type: ignore
    """Calculate the RMSE of residuals."""
    return np.sqrt(np.mean(np.square(residuals)))

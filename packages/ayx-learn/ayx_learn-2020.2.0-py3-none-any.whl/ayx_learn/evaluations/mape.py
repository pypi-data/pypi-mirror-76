# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Mean absolute percent error measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.evaluations.regression import RegressionEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np


class MAPE(RegressionEvaluation, MultiFoldEvaluation):
    """Mean absolute percent error supporting fold-independent evaluation and aggregation across folds."""

    def __init__(self):  # type: ignore  # type: ignore
        """Construct the evaluation."""
        RegressionEvaluation.__init__(self)  # type: ignore
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, y_true, residuals, **kwargs):  # type: ignore
        """Run the evaluation."""
        if np.all(y_true != 0):
            return mape_resids(residuals, y_true)  # type: ignore
        else:
            return None

    def format(self, x):  # type: ignore
        """Run the format to external representation."""
        return x

    def inverse_format(self, x):  # type: ignore
        """Run the inverse format to internal representation."""
        return x

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        try:
            return np.mean(scores)
        except TypeError:
            return None


def mape_resids(residuals, y_true):  # type: ignore
    """Mean absolute percent error calculation based on residuals and actuals."""
    return 100 * np.mean(np.divide(np.absolute(residuals), y_true))


def mape(y_true, y_pred):  # type: ignore
    """Mean absolute percent error calculation based on actual and fitted values."""
    residuals = y_true - y_pred
    return mape_resids(residuals, y_true)  # type: ignore

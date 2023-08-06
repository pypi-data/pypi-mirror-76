# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""R squared measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.evaluations.regression import RegressionEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np

from sklearn.metrics import r2_score


class R2(RegressionEvaluation, MultiFoldEvaluation):
    """R2 score supporting fold-independent evaluation and aggregation across folds."""

    def __init__(self):  # type: ignore  # type: ignore
        """Construct the evaluation."""
        RegressionEvaluation.__init__(self)  # type: ignore
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, y_true, y_pred, **kwargs):  # type: ignore
        """Run the evaluation."""
        return r2_score(y_true, y_pred)

    def format(self, x):  # type: ignore
        """Run the format to external representation."""
        return x

    def inverse_format(self, x):  # type: ignore
        """Run the inverse format to internal representation."""
        return x

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        return np.mean(self.scores)

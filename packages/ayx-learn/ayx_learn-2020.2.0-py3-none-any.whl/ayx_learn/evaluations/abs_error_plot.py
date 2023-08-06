# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Log Adjusted absolute residual error over multiple folds."""
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.evaluations.regression import RegressionEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np


# TODO refactor? multiple inheritance
# (esp. diamond inheritance) tends to create brittle designs


class AbsErrorPlot(RegressionEvaluation, MultiFoldEvaluation):
    """Absolute residual error plot support with fold-independent processing."""

    num_points = 101

    def __init__(self):  # type: ignore  # type: ignore
        """Construct the evaluation."""
        RegressionEvaluation.__init__(self)  # type: ignore
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, residuals, **kwargs):  # type: ignore
        """Run the evaluation."""
        absolute_residuals = np.absolute(residuals)
        normalized_residuals = np.log(1 + absolute_residuals)
        ys_actual = np.sort(normalized_residuals)
        xs_actual = np.linspace(1 / len(ys_actual), 1, len(ys_actual))
        xs_interp = np.linspace(0, 1, self.num_points)
        ys_interp = np.interp(xs_interp, xs_actual, ys_actual)
        return {"xs": xs_interp, "ys": ys_interp}

    def format(self, x):  # type: ignore
        """Run the format to external representation."""
        return x

    def inverse_format(self, x):  # type: ignore
        """Run the inverse format to internal representation."""
        return x

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        return {
            "xs": scores[0]["xs"],  # xs same across folds
            "ys": np.mean([score["ys"] for score in scores], axis=0),
        }

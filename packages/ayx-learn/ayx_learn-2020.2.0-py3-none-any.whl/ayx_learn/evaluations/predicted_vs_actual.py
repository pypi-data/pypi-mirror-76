# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Root mean squared error measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.evaluations.regression import RegressionEvaluation
from ayx_learn.evaluations.stratified_bin_sampler import StratifiedBinSampler
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np


SAMPLING_SAMPLE_SIZE = 500


def _sort_by_residuals(array_to_sort):  # type: ignore
    return array_to_sort[array_to_sort[:, 2].argsort()[::-1]]


class PredictedVsActual(RegressionEvaluation, MultiFoldEvaluation):
    """Predicted vs actual support with fold-independent processing."""

    def __init__(self):  # type: ignore
        """Construct the evaluation."""
        RegressionEvaluation.__init__(self)  # type: ignore
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(  # type: ignore
        self, y_pred, y_true, residuals, total_folds, **kwargs
    ):
        """Run the evaluation."""
        abs_residuals = np.absolute(residuals)
        array_to_sample_abs_residuals = np.array([y_pred, y_true, abs_residuals]).T
        sampler = StratifiedBinSampler(array_to_sample_abs_residuals)  # type: ignore

        predicted_vs_actual = (
            sampler.sample(
                round(SAMPLING_SAMPLE_SIZE / total_folds), _sort_by_residuals
            )
            if len(array_to_sample_abs_residuals)
            > round(SAMPLING_SAMPLE_SIZE / total_folds)
            else array_to_sample_abs_residuals
        )

        return {
            "predicted": predicted_vs_actual[:, 0],
            "actual": predicted_vs_actual[:, 1],
        }

    def format(self, score):  # type: ignore
        """Run the format to external representation."""
        return score

    def inverse_format(self, score):  # type: ignore
        """Run the inverse format to internal representation."""
        return score

    def _aggregate(self, scores):  # type: ignore
        if len(scores) == 0:
            raise NoFoldsEvaluatedError

        predicted = np.concatenate([score["predicted"] for score in scores])
        actual = np.concatenate([score["actual"] for score in scores])
        return {"predicted": predicted, "actual": actual}

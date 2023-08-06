# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements feature importance calculation with root mean squared error."""
from ayx_learn.evaluations.permutation_importance import BasePermutationImportance
from ayx_learn.evaluations.rmse import rmse


class RegressionImportance(BasePermutationImportance):
    """Permutation importance calculation that uses -rmse as the scoring function."""

    def _get_score(self, y_pred, y_true):  # type: ignore
        resids = y_pred - y_true
        # convert loss function into score by * -1
        return -1 * rmse(resids)  # type: ignore

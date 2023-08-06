# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements feature importance calculation with accuracy."""
from ayx_learn.evaluations.permutation_importance import BasePermutationImportance

from sklearn.metrics import accuracy_score


class ClassificationImportance(BasePermutationImportance):
    """Permutation importance calculation that uses accuracy as the scoring function."""

    def _get_score(self, y_pred, y_true):  # type: ignore
        return accuracy_score(y_true, y_pred)

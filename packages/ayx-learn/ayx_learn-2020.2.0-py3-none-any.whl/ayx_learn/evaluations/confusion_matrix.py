# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Confusion Matrix supporting aggregation over multiple folds."""
from ayx_learn.evaluations.classification import ClassificationEvaluation
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np

from sklearn.metrics import confusion_matrix


class ConfusionMatrix(ClassificationEvaluation, MultiFoldEvaluation):
    """Accuracy measure supporting fold-independent evaluation and aggregation across folds.

    Parameters
    ----------
    levels : array-like
        Collection of distinct values that appear in target

    encoded_levels (Optional) : array-like
        Numeric values corresponding to those in `levels`.
        Must have same length as `levels`.
        If not provided, assumed to be the same as `levels`.

    positive_class (Optional) : scalar
        If provided, should be an element of `levels` corresponding to class of interest
        If not provided, assumed to be first of `levels`

    """

    def __init__(  # type: ignore
        self, levels, encoded_levels=None, positive_class=None
    ):
        """Construct the evaluation."""
        ClassificationEvaluation.__init__(  # type: ignore
            self, levels, encoded_levels, positive_class
        )
        MultiFoldEvaluation.__init__(self)  # type: ignore

    def evaluate(self, y_true, y_pred, **kwargs):  # type: ignore
        """Run the evaluation."""
        return confusion_matrix(y_true, y_pred, self._encoded_levels)

    def format(self, cm):  # type: ignore
        """Run the format to external representation."""
        return [
            {"actual": self._levels[i], "predicted": self._levels[j], "count": cm[i][j]}
            for i in range(len(self._levels))
            for j in range(len(self._levels))
        ]

    def inverse_format(self, formatted_score):  # type: ignore
        """Run the inverse format to internal representation."""
        cm = np.zeros((len(self._levels), len(self._levels)))
        for cell in formatted_score:
            i = self._levels.index(cell["actual"])
            j = self._levels.index(cell["predicted"])
            if cm[i][j] != 0:
                raise ValueError("Repeated confusion matrix index")
            cm[i][j] = cell["count"]
        return cm

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        total = self._scores[0]
        for score in self._scores[1:]:
            total = np.add(total, score)
        return total

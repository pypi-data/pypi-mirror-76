# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""AUC measure supporting aggregation over multiple folds."""
import abc

from ayx_learn.evaluations.classification import ClassificationEvaluation
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np


class BaseAUC(ClassificationEvaluation, MultiFoldEvaluation):
    """Base class for AUC measure supporting fold-independent evaluation and aggregation across folds.

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

        if positive_class is None:
            self._positive_class = levels[0]
        else:
            level_type = type(levels[0])
            self._positive_class = level_type(positive_class)
            self._positive_class_index = levels.index(self._positive_class)
            self._positive_class_encoding = self._encoded_levels[
                self._positive_class_index
            ]

    @abc.abstractmethod
    def evaluate(  # type: ignore
        self, y_true, y_pred, y_pred_proba, model_level_encodings=None
    ):
        """Abstract method for computation for appropriate auc methodology."""

    def format(self, score):  # type: ignore
        """Run the format to external representation."""
        return score

    def inverse_format(self, formatted_score):  # type: ignore
        """Run the inverse format to internal representation."""
        return formatted_score

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError
        return np.mean(scores)

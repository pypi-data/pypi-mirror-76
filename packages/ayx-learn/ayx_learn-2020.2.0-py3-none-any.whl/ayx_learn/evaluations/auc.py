# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""AUC measure supporting aggregation over multiple folds."""
from ayx_learn.evaluations.base_auc import BaseAUC

from sklearn.metrics import roc_auc_score


class AUC(BaseAUC):
    """AUC measure supporting fold-independent evaluation and aggregation across folds.

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

    def evaluate(self, y_true, y_pred_proba, **kwargs):  # type: ignore
        """Run the evaluation."""
        auc_value = roc_auc_score(y_true, y_pred_proba[:, self._positive_class_index])
        auc_value = 1 - auc_value if self._positive_class_index == 0 else auc_value
        return auc_value

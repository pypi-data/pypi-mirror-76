# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Bivariate importance for regression via Goodman Kruskal Tau."""

from ayx_learn.base import SafeColInspectMixin
from ayx_learn.helpers.entropy_binning import entropy_bin_ids
from ayx_learn.helpers.goodman_kruskal_tau import gk_tau
from ayx_learn.inspectors.bivariate_importance import BivariateImportanceInspector

import pandas as pd


class GKTImportanceInspector(  # type: ignore
    SafeColInspectMixin, BivariateImportanceInspector
):
    """Importance calculator for classification via Goodman-Kruskal-Tau measure."""

    max_samples = 500

    @staticmethod
    def calc_importance(x: pd.Series, y: pd.Series) -> float:
        """Calculate the importance for a single column."""
        if pd.api.types.is_numeric_dtype(x):
            x = entropy_bin_ids(x.values, y.values)
            y = y.values
        else:
            x = x.values
            y = y.values
        return gk_tau(x, y)[0]

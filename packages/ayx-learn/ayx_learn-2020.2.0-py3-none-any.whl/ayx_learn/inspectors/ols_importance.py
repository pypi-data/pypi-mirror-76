# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Bivariate importance for regression via OLS."""
from ayx_learn.base import SafeColInspectMixin
from ayx_learn.inspectors.bivariate_importance import BivariateImportanceInspector
from ayx_learn.transformers import OneHotEncoderTransformer

import numpy as np

import pandas as pd

from sklearn.linear_model import LinearRegression


class OLSImportanceInspector(  # type: ignore
    SafeColInspectMixin, BivariateImportanceInspector
):
    """Importance calculator for regression via correlation of absolutes and predicteds from OLS."""

    # should use same sample size for everything since non-adjusted R2 being used
    min_samples = 500
    max_samples = 500
    x_encoder = OneHotEncoderTransformer()

    @staticmethod
    def calc_importance(x: pd.Series, y: pd.Series) -> float:
        """Calculate the importance of a single column."""
        X = pd.DataFrame(x)
        rgsr = LinearRegression(normalize=True).fit(X, y)
        y_pred = rgsr.predict(X)
        return abs(np.corrcoef(y, y_pred)[0, 1])  # type: ignore

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Inspector for calculating relative importance via a Regression Forest."""
from ayx_learn.inspectors.relative_importance import SurrogateImportanceInspector

from sklearn.ensemble import ExtraTreesRegressor


class RegressionForestInspector(SurrogateImportanceInspector):
    """Inspector for relative importance for regression for ExtraTreesRegressor."""

    surrogate = ExtraTreesRegressor(n_estimators=250, random_state=0)

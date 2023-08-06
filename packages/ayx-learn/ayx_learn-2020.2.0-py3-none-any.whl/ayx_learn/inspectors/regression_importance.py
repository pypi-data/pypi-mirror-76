# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Inspector for calculating importance for regression."""
from typing import Any

from ayx_learn.inspectors.combination_importance import CombinationImportanceInspector
from ayx_learn.inspectors.ols_importance import OLSImportanceInspector
from ayx_learn.inspectors.regression_forest_importance import RegressionForestInspector
from ayx_learn.typing import RandomStateLike

import pandas as pd

from sklearn.utils import check_random_state


class RegressionImportanceInspector(CombinationImportanceInspector):
    """Regression importance inspector."""

    dataframe_inspectors = (
        RegressionForestInspector,  # type: ignore
        OLSImportanceInspector,
    )

    def __init__(
        self,
        data: pd.DataFrame,
        y: pd.Series,
        random_state: RandomStateLike = 42,
        **kwargs: Any
    ):
        """Construct the inspector."""
        self.random_state = check_random_state(random_state)
        super().__init__(data, y)

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Inspector for calculating importance for classification."""
from typing import Any

from ayx_learn.inspectors.classification_forest_importance import (
    ClassificationForestInspector,
)
from ayx_learn.inspectors.combination_importance import CombinationImportanceInspector
from ayx_learn.inspectors.gkt_importance import GKTImportanceInspector
from ayx_learn.typing import RandomStateLike

import pandas as pd

from sklearn.utils import check_random_state


class ClassificationImportanceInspector(CombinationImportanceInspector):
    """Classification importance inspector."""

    dataframe_inspectors = (
        ClassificationForestInspector,  # type: ignore
        GKTImportanceInspector,
    )

    def __init__(
        self,
        data: pd.DataFrame,
        y: pd.Series,
        random_state: RandomStateLike = 42,
        **_: Any
    ):
        """Construct the inspector."""
        self.random_state = check_random_state(random_state)
        super().__init__(data, y)

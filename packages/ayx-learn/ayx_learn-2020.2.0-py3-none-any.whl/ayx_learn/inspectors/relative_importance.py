# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Base inspector for calculating relative importance via a surrogate estimator."""
from collections import defaultdict
from typing import Dict, Optional  # noqa: F401

from ayx_learn.base import BaseInspector, ColumnInspection, MultiColumnInspection
from ayx_learn.inspectors.get_sample import get_sample
from ayx_learn.transformers import (
    DropColumnTransformer,
    IdentityTransformer,
    OneHotEncoderTransformer,
)
from ayx_learn.typing import (  # noqa: F401
    RandomStateLike,
    SupportsImportances,
    SupportsTransform,
)

import pandas as pd

from sklearn.utils import check_random_state


class SurrogateImportanceInspector(BaseInspector):
    """Abstract base inspector for providing a feature importance via a surrogate estimator.

    Attributes
    ----------
    min_samples : int, default 1
        minimum records to use; records up-sampled if below

    max_samples : int, optional
        maximum samples to use; records down-sampled if above

    x_encoder : SupportsTransform
        encoder to use for predictors

    y_encoder : SupportsTransform
        encoder to use for target

    surrogate : sklearn.base.BaseEstimator
        Estimator with a .feature_importances_ attribute after fitting.

    """

    min_samples = 0
    max_samples = None  # type: Optional[int]
    x_encoder = OneHotEncoderTransformer()
    y_encoder = IdentityTransformer()
    surrogate: SupportsImportances

    def __init__(
        self, data: pd.DataFrame, y: pd.Series, random_state: RandomStateLike = None
    ):
        """Construct the inspector.

        data : pd.DataFrame
            data to inspect

        y : pd.Series
            target variable

        random_state : int | numpy.random.RandomState | None

        """
        super().__init__(data=data, y=y)
        self.random_state = check_random_state(random_state)

    @staticmethod
    def keep(importance: float) -> bool:
        """Whether to recommend keeping a column based on its importance.

        Parameters
        ----------
        importance : float in [0, 1]

        """
        return 0.01 <= importance <= 0.75

    def stateless_inspection(self) -> MultiColumnInspection:
        """Run the inspection."""
        X, y = get_sample(self)
        X = self.x_encoder.fit_transform(X)
        y = self.y_encoder.fit_transform(y)
        estimator = self.surrogate
        estimator.fit(X, y)
        relative_importances = defaultdict(float)  # type: Dict[str, float]
        link = self.x_encoder.get_link()
        for column_name, importance in zip(X.columns, estimator.feature_importances_):
            relative_importances[link[column_name]] += importance

        inspection = MultiColumnInspection()
        for column_name, importance in relative_importances.items():
            drop = DropColumnTransformer(column_name)  # type: SupportsTransform
            keep = IdentityTransformer()  # type: SupportsTransform

            column_inspection = ColumnInspection(
                column_name, keep if self.keep(importance) else drop, {keep, drop}
            )
            inspection.add_column_inspection(column_inspection)

        return inspection

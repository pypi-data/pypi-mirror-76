# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Base inspector for calculating bivariate feature importance."""
import abc
from typing import Optional  # noqa: F401

from ayx_learn.base import ColumnInspection, ColumnInspector
from ayx_learn.inspectors.get_sample import get_sample
from ayx_learn.transformers import DropColumnTransformer, IdentityTransformer
from ayx_learn.typing import RandomStateLike, SupportsTransform  # noqa: F401

import pandas as pd

from sklearn.utils import check_random_state


class BivariateImportanceInspector(ColumnInspector):
    """Abstract base inspector for providing a feature importance for the relationship between the target and a predictor.

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

    """

    min_samples = 0  # type: int
    max_samples = None  # type: Optional[int]
    x_encoder = IdentityTransformer()  # type: SupportsTransform
    y_encoder = IdentityTransformer()  # type: SupportsTransform

    def __init__(
        self, data: pd.Series, y: pd.Series, random_state: RandomStateLike = None
    ):
        """Construct the inspector.

        data : pd.Series
            data to inspect

        y : pd.Series
            target variable

        random_state : int | numpy.random.RandomState | None

        """
        super().__init__(data=data, y=y)
        self.random_state = check_random_state(random_state)

    @staticmethod
    @abc.abstractmethod
    def calc_importance(x: pd.Series, y: pd.Series) -> float:
        """Calculate bivariate importance.

        Parameters
        ----------
        x : pd.Series
            dependent variable

        y : pd.Series
            independent variable

        """
        pass

    @staticmethod
    def keep(importance: float) -> bool:
        """Whether to recommend keeping a column based on its importance.

        Parameters
        ----------
        importance : float in [0, 1]

        """
        return 0.01 <= importance <= 0.75

    def stateless_inspection(self) -> ColumnInspection:
        """Run the inspection."""
        x, y = get_sample(self)
        x = self.x_encoder.fit_transform(x)
        y = self.y_encoder.fit_transform(y)
        importance = self.calc_importance(x, y)
        drop = DropColumnTransformer(self.column_name)
        keep = IdentityTransformer()
        return ColumnInspection(
            column_name=self.column_name,
            recommendation=keep if self.keep(importance) else drop,  # type: ignore
            options={drop, keep},
            statistics={"importance": importance},
        )

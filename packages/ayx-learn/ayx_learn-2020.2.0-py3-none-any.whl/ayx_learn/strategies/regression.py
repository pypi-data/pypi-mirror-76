# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements base abstract strategy for classification analyses."""
from typing import Any, Dict, List, Tuple, Type

from ayx_learn.base import BaseInspector, Pipeline
from ayx_learn.evaluations import (
    AbsErrorPlot,
    AdjR2,
    Evaluation,
    MAE,
    MRE,
    PredictedVsActual,
    R2,
    RMSE,
    RegressionImportance,
)
from ayx_learn.inspectors import (
    DataFrameNullsInspector,
    DataFrameTypeInspector,
    RegressionImportanceInspector,
)
from ayx_learn.regressors import (
    DecisionTreeRegressor,
    LinearRegression,
    RandomForestRegressor,
)
from ayx_learn.strategies.supervised import SupervisedStrategy
from ayx_learn.typing import SupportsPredict
from ayx_learn.utils.exceptions import NonNumericTargetError

import pandas as pd

from sklearn.model_selection import KFold


class RegressionStrategy(SupervisedStrategy):
    """Base strategy for regression analyses."""

    n_splits = 3
    splitter_rng = 42

    @property
    def partitioner(self):  # type: ignore
        """Get the paritioner for this strategy."""
        return KFold(
            n_splits=self.n_splits, shuffle=True, random_state=self.splitter_rng
        )

    def get_prediction_details(  # type: ignore # mypy errors on test_data restrictive
        self,
        pipeline: Pipeline,
        test_data: Tuple[pd.DataFrame, pd.Series],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Get prediction details of pipeline.

        Parameters
        ----------
        pipeline : Pipeline

        test_data : Tuple[ArrayLike]
            X, y data held out from training

        **kwargs : mop-up

        Returns
        -------
        dict of str names to values

        """
        X_test, y_test = test_data
        y_pred = pipeline.predict(X_test)
        resids = y_test - y_pred
        return {
            "y_pred": y_pred,
            "y_true": y_test,
            "residuals": resids,
            "pipeline": pipeline,
            "x_test": X_test,
            "total_folds": self.n_splits,
        }

    @property
    def evaluators(self) -> List[Type[Evaluation]]:
        """Get the supported evaluators."""
        return [
            AbsErrorPlot,
            AdjR2,
            MAE,
            MRE,
            PredictedVsActual,
            R2,
            RegressionImportance,
            RMSE,
        ]

    @property
    def estimators(self) -> List[Type[SupportsPredict]]:
        """Get the supported estimators."""
        return [DecisionTreeRegressor, LinearRegression, RandomForestRegressor]

    @property
    def steps(self) -> Dict[str, Type[BaseInspector]]:
        """Get the inspectors for a given problem type.

        Returns
        -------
        Dictionary mapping PipelineStep type to an Inspector / Transformer

        """
        return {
            "COLUMN_TYPING": DataFrameTypeInspector,
            "NA_HANDLING": DataFrameNullsInspector,
            "FEATURE_IMPORTANCE": RegressionImportanceInspector,
        }

    def validate_target(self, target: pd.Series) -> None:
        """Validate that target is numeric."""
        try:
            target.astype(float)
        except ValueError:
            raise NonNumericTargetError(
                "Target not coercible to a numeric value. Invalid target for regression."
            )

    def get_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Get components of data given a dataframe."""
        X, y = super().get_data(df)
        return X, y.astype(float)

# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""XGBoost classification algorithm."""
import pandas as pd

from xgboost.sklearn import XGBClassifier as XGBoostClassifier


class XGBClassifier(XGBoostClassifier):
    """Wrapper for xgboost classifier sklearn api.

    Provides additional support for xgboost unsupported column names containing '[', ']' and '<'.

    """

    def __init__(  # type: ignore
        self,
        max_depth=3,
        learning_rate=0.1,
        n_estimators=100,
        objective="binary:logistic",
        booster="gbtree",
        gamma=0,
        min_child_weight=1,
        subsample=1,
        colsample_bytree=1,
        colsample_bylevel=1,
        colsample_bynode=1,
        random_state=10,
        missing=None,
        n_jobs=1,
    ):
        """Construct an xgboost classifier.

        For more information, see xgboost classifier documentation [1]

        [1]: https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier

        """
        super().__init__(
            max_depth=max_depth,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            objective=objective,
            booster=booster,
            gamma=gamma,
            min_child_weight=min_child_weight,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            colsample_bylevel=colsample_bylevel,
            colsample_bynode=colsample_bynode,
            random_state=random_state,
            missing=missing,
            n_jobs=n_jobs,
        )

    def fit(self, x, y, *args, **kwargs):  # type: ignore
        """Fit a model on training data."""
        x = self._convert_data(x)  # type: ignore
        return super().fit(x, y, *args, **kwargs)

    def predict(self, x, *args, **kwargs):  # type: ignore
        """Get predictions on test data."""
        x = self._convert_data(x)  # type: ignore
        return super().predict(x, *args, **kwargs)

    def predict_proba(self, x, *args, **kwargs):  # type: ignore
        """Get predictions with probabilities on test data."""
        x = self._convert_data(x)  # type: ignore
        return super().predict_proba(x, *args, **kwargs)

    @staticmethod
    def _convert_data(x):  # type: ignore
        """
        Convert incoming data to correct numpy array format if it's a dataframe.

        The XGBoost packages doesn't allow dataframes with [, ], or < in the column name.
        To avoid this issue, just use the underlying numpy ndarray as the training data.
        """
        if isinstance(x, pd.DataFrame):
            return x.values

        return x

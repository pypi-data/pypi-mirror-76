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
"""Random forest regression algorithm."""

from sklearn.ensemble import ExtraTreesRegressor


class RandomForestRegressor(ExtraTreesRegressor):
    """Wrapper for sklearn ExtraTreesClassifier."""

    def __init__(  # type: ignore
        self,
        n_estimators=100,
        criterion="mse",
        max_depth=10,
        min_samples_split=2,
        min_weight_fraction_leaf=0.0,
        max_features="auto",
        min_impurity_decrease=0.0,
        bootstrap=True,
        random_state=10,
    ):
        """Construct a random forest regressor using extra-random trees.

        For more information, see sklearn ExtraTreesRegressor documentation [1]

        [1]: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html

        """
        super().__init__(
            n_estimators=n_estimators,
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_features=max_features,
            min_impurity_decrease=min_impurity_decrease,
            bootstrap=bootstrap,
            random_state=random_state,
        )

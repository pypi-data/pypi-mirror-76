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
"""Decision tree regression algorithm."""

from sklearn.tree import DecisionTreeRegressor


class DecisionTreeRegressor(DecisionTreeRegressor):  # type: ignore
    """Wrapper for sklearn DecisionTreeRegressor."""

    def __init__(  # type: ignore
        self,
        criterion="mse",
        splitter="best",
        max_depth=10,
        min_samples_split=2,
        min_weight_fraction_leaf=0.0,
        max_features="auto",
        random_state=10,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        presort=False,
    ):
        """Construct a decision tree regressor.

        For more information, see sklearn DecisionTreeRegressor documentation [1]

        [1]: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html

        """
        super().__init__(
            criterion=criterion,
            splitter=splitter,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            random_state=random_state,
            min_impurity_decrease=min_impurity_decrease,
            presort=presort,
        )

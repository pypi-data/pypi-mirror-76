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
"""Linear regression algorithm."""

from sklearn.linear_model import ElasticNet


class LinearRegression(ElasticNet):
    """Wrapper for sklearn ElasticNet regressor."""

    def __init__(  # type: ignore # noqa: N803
        self, fit_intercept=True, normalize=True, random_state=10
    ):
        """Construct a linear regression model.

        For more information, see sklearn ElasticNet documentation [1]

        [1]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html

        """
        super().__init__(
            alpha=0.01,
            l1_ratio=0.9,
            fit_intercept=fit_intercept,
            normalize=normalize,
            random_state=random_state,
        )

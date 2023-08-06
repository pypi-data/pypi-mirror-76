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
"""Logistic regression classification algorithm."""

from sklearn.linear_model import LogisticRegression


class LogisticRegressionClassifier(LogisticRegression):
    """Wrapper for sklearn LogisticRegression classifier."""

    def __init__(  # type: ignore
        self,
        penalty="l2",
        dual=False,
        tol=1e-4,
        C=1.0,  # noqa: N803
        fit_intercept=True,
        intercept_scaling=1,
        class_weight=None,
        random_state=10,
        solver="liblinear",
        max_iter=100,
        multi_class="auto",
        verbose=0,
    ):
        """Construct a logistic regression classifier.

        For more information, see sklearn LogisticRegression documentation [1]

        [1]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

        """
        super().__init__(
            penalty=penalty,
            dual=dual,
            tol=tol,
            C=C,
            fit_intercept=fit_intercept,
            intercept_scaling=intercept_scaling,
            class_weight=class_weight,
            random_state=random_state,
            solver=solver,
            max_iter=max_iter,
            multi_class=multi_class,
            verbose=verbose,
        )

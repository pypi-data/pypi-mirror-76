# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Make pipeline wrapper."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sklearn.base import BaseEstimator
    from sklearn.pipeline import Pipeline


def make_pipeline(*steps: "BaseEstimator") -> "Pipeline":
    """Make an ayx_learn pipeline object from a list of steps.

    For more info, see sklearn make_pipeline documentation [1]

    [1]: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.make_pipeline.html

    """
    from sklearn.pipeline import make_pipeline

    return make_pipeline(*steps)

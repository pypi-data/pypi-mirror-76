# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Inspector for calculating relative importance via a Classification Forest."""
from ayx_learn.inspectors.relative_importance import SurrogateImportanceInspector

from sklearn.ensemble import ExtraTreesClassifier


class ClassificationForestInspector(SurrogateImportanceInspector):
    """Inspector for relative importance for classification for ExtraTreesClassifier."""

    surrogate = ExtraTreesClassifier(n_estimators=250, random_state=0)

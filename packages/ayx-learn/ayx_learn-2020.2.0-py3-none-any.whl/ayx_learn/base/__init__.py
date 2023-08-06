# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Base domain objects."""

# flake8: noqa  # input order is essential to avoid circular imports

# Building blocks don't require other base components
from .estimator import Estimator
from .transformer import Transformer

# Only require building blocks
from .pipeline import Pipeline, make_pipeline
from .pipeline_step import PipelineStep
from .inspection import (
    FailureInspection,
    Inspection,
    ColumnInspection,
    ForceDropInspection,
    MultiColumnInspection,
)

# Consider pipelines and return inspections
from .inspector import (
    BaseInspector,
    ColumnInspector,
    ColumnWiseInspector,
    ComputesMultiColumnInspection,
    SafeColInspectMixin,
    CombinationInspector,
)

# Combine inspecting with pipeline components
from .strategy import Strategy


__all__ = [
    "Estimator",
    "Transformer",
    "Pipeline",
    "PipelineStep",
    "Inspection",
    "FailureInspection",
    "ColumnInspection",
    "ForceDropInspection",
    "MultiColumnInspection",
    "BaseInspector",
    "ColumnInspector",
    "ColumnWiseInspector",
    "CombinationInspector",
    "ComputesMultiColumnInspection",
    "SafeColInspectMixin",
    "Strategy",
]

# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Typehinting utilities for pipeline objects."""
from typing import Sequence, Tuple, Union

from ayx_learn.typing.estimator import SupportsPredict
from ayx_learn.typing.transformer import SupportsTransform

AnyPipelineStep = Union[SupportsTransform, SupportsPredict]
NamedPipelineStep = Tuple[str, AnyPipelineStep]
NamedPipelineStepSequence = Sequence[NamedPipelineStep]

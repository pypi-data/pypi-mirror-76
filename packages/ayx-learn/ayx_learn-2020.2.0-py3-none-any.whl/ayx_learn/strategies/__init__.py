# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Ayx-supplied strategies for building and evaluating pipelines."""
from .binary import BinaryStrategy
from .continuous import ContinuousStrategy
from .multiclass import MulticlassStrategy


__all__ = ["BinaryStrategy", "ContinuousStrategy", "MulticlassStrategy"]

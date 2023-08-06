# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""FailureInspection tracking an error."""
from ayx_learn.base.inspection.force_drop import ForceDropInspection


class FailureInspection(ForceDropInspection):
    """Inspection for unsuccessful inspects."""

    def __init__(self, column_name: str, error: Exception):
        super().__init__(column_name)
        self.error = error

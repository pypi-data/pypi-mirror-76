# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Optional safe_inspect functionality."""
import logging
from typing import TypeVar

from ayx_learn.base.inspection import ColumnInspection, FailureInspection
from ayx_learn.base.inspector.column_inspector import ColumnInspector  # noqa: F401


T2 = TypeVar("T2", bound="ColumnInspector")


logger = logging.getLogger(__name__)


class SafeColInspectMixin:
    """Optional 'safe_inspect' functionality for ColumnInspector.

    Any errors will result in an inspection that only allows dropping columns.
    """

    inspection: ColumnInspection

    def safe_inspect(self: T2) -> T2:  # type: ignore
        """Safe (will not throw exception) wrapper for self.inspect.

        Instead of throwing an error, will return a failure inspection.

        """
        try:
            self.inspect()
        except Exception as e:
            logger.exception(e)
            self.inspection = FailureInspection(self.column_name, e)
        return self

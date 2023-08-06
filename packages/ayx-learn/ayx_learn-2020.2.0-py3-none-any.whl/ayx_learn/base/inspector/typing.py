# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Extra support for typehinting with inspectors."""
import abc

from ayx_learn.base.inspection import MultiColumnInspection

from typing_extensions import Protocol


class ComputesMultiColumnInspection(Protocol):
    """Supports typehinting of objects that compute multicolumn inspections."""

    @abc.abstractmethod
    def stateless_inspection(self) -> MultiColumnInspection:
        """Run a stateless inspection."""
        pass

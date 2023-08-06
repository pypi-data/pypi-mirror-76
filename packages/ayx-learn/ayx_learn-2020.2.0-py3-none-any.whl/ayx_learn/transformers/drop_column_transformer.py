# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Light wrapper around ColumnSelectorTransformer for dropping single column."""
from ayx_learn.transformers.column_selector_transformer import ColumnSelectorTransformer


class DropColumnTransformer(ColumnSelectorTransformer):
    """Light wrapper around ColumnSelectorTransformer for dropping single column."""

    def __init__(self, column_name: str, inplace: bool = False):
        """Construct transformer.

        Parameters
        ----------
        column_name : str
            Name of column to drop.

        inplace : bool (default: False)
            whether .transform is applied inplace

        """
        self.column_name = column_name
        self.inplace = inplace
        super().__init__([column_name], select_not_deselect=False)

# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Inspector / Inspection for inspecting data for null values."""
from collections.abc import Iterable
from typing import Any, Optional, Set, Union

from ayx_learn.base import (
    ColumnInspection,
    ColumnInspector,
    ColumnWiseInspector,
    ForceDropInspection,
    Pipeline,
    SafeColInspectMixin,
)
from ayx_learn.transformers import (
    ColumnTypeTransformer,
    DropColumnTransformer,
    ImputeTransformer,
)
from ayx_learn.transformers.impute_transformer import ImputeMethods
from ayx_learn.typing import SupportsTransform
from ayx_learn.utils.constants import ColumnTypes, NA_PLACEHOLDER

import pandas as pd


def _get_column_type(column_name: str, obj: Any) -> Optional[str]:
    if isinstance(obj, ColumnTypeTransformer) and obj.colname == column_name:
        return obj.coltype
    elif isinstance(obj, Iterable):
        try:
            # use last because if order is important, we want the most recent type change
            return [_get_column_type(column_name, obj_i) for obj_i in obj if obj_i][-1]
        except IndexError:
            return None
    else:
        return None


class ColumnNullsInspector(SafeColInspectMixin, ColumnInspector):  # type: ignore
    """Inspects a column for null values.

    Attributes
    ----------
    drop_threshold : float
        Fraction
    """

    drop_threshold = 0.8

    def __init__(self, data: pd.Series, upstream_pipeline: Pipeline):
        """Construct an inspector."""
        super().__init__(data=data, upstream_pipeline=upstream_pipeline)
        column_type = _get_column_type(self.column_name, self.upstream_pipeline)
        if column_type:
            self.column_type = column_type
        else:
            self.column_type = self._infer_column_type(self.data)

    @staticmethod
    def _infer_column_type(column: pd.Series) -> str:
        if pd.api.types.is_bool_dtype(column):
            return ColumnTypes.BOOLEAN  # type: ignore
        elif pd.api.types.is_numeric_dtype(column):
            return ColumnTypes.NUMERIC  # type: ignore
        elif pd.api.types.is_categorical_dtype(column):
            return ColumnTypes.CATEGORICAL  # type: ignore
        else:
            raise ValueError("Couldn't infer column type.")

    def stateless_inspection(self) -> ColumnInspection:
        """Run the inspection."""
        n_missing = self.data.isnull().sum()  # type: ignore
        try:
            frac_missing = n_missing / len(self.data)
        except ZeroDivisionError:
            frac_missing = 1

        statistics = {
            "n_missing": n_missing,
            "frac_missing": frac_missing,
            "length": len(self.data),
            "n_nonnull": len(self.data) - n_missing,
        }

        if frac_missing == 1:
            return ForceDropInspection(self.column_name, statistics)
        else:
            return ColumnInspection(
                column_name=self.column_name,
                recommendation=self.get_recommendation(frac_missing),
                options=self.get_options(),
                statistics=statistics,
            )

    def get_recommendation(self, frac_missing: float) -> SupportsTransform:
        """Get the recommended transformer."""
        type_method_map = {
            ColumnTypes.CATEGORICAL: ImputeMethods.VALUE,
            ColumnTypes.NUMERIC: ImputeMethods.MEDIAN,
            ColumnTypes.BOOLEAN: ImputeMethods.MODE,
        }
        drop_transformer = DropColumnTransformer(self.column_name)
        if frac_missing > self.drop_threshold:
            return drop_transformer
        else:
            return ImputeTransformer(
                method=type_method_map[self.column_type],
                value=NA_PLACEHOLDER,
                colname=self.column_name,
            )

    def get_options(self) -> Set[Union[ImputeTransformer, DropColumnTransformer]]:
        """Get the available options for the transformers."""
        type_method_set_map = {
            ColumnTypes.CATEGORICAL: {ImputeMethods.VALUE, ImputeMethods.MODE},
            ColumnTypes.NUMERIC: {
                ImputeMethods.MEDIAN,
                ImputeMethods.MODE,
                ImputeMethods.MEDIAN,
            },
            ColumnTypes.BOOLEAN: {ImputeMethods.MODE},
        }
        options = {
            ImputeTransformer(
                method=method, value=NA_PLACEHOLDER, colname=self.column_name
            )
            for method in type_method_set_map[self.column_type]
        }
        options.add(DropColumnTransformer(self.column_name))
        return options


class DataFrameNullsInspector(ColumnWiseInspector):
    """Inspector that runs ColumnNullsInspector on every column in dataframe."""

    def __init__(self, data: pd.DataFrame, upstream_pipeline: Pipeline, **_: Any):
        """Construct the inspector.

        Parameters
        ----------
        data : pd.DataFrame
            data to inspect each column of

        """
        super().__init__(
            data, ColumnNullsInspector, upstream_pipeline=upstream_pipeline
        )

# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Inspector / Inspection for inspecting data for column types."""
from typing import Any, List, Mapping, Set

from ayx_learn.base import (
    ColumnInspection,
    ColumnInspector,
    ColumnWiseInspector,
    SafeColInspectMixin,
)
from ayx_learn.transformers import ColumnTypeTransformer, DropColumnTransformer
from ayx_learn.typing import SupportsTransform
from ayx_learn.utils.constants import ColumnTypes
from ayx_learn.utils.exceptions import UnaryColumnError

import numpy as np

import pandas as pd


DEFAULT_BOOLEAN_MAP = {
    "1": True,
    "1.0": True,
    "TRUE": True,
    "T": True,
    "Y": True,
    "YES": True,
    "0": False,
    "0.0": False,
    "FALSE": False,
    "F": False,
    "N": False,
    "NO": False,
}


class ColumnTypeInspector(SafeColInspectMixin, ColumnInspector):  # type: ignore
    """Inspector for column typing."""

    numeric_score_threshold = 0.98
    string_score_threshold = 1 - numeric_score_threshold
    numeric_score_exponent = np.log(0.5) / np.log(numeric_score_threshold)
    string_score_exponent = np.log(0.5) / np.log(string_score_threshold)
    id_unique_exponent = 1
    n_cat_unique_threshold = 60

    def __init__(
        self,
        data: pd.Series,
        bool_map: Mapping[str, bool] = DEFAULT_BOOLEAN_MAP,
        chunk_size: int = 1000,
    ):
        """Construct the inspector.

        Parameters
        ----------
        data : pd.Series
            column to inspect

        bool_map : Mapping[str, bool] (default = DEFAULT_BOOLEAN_MAP)
            allowed boolean strings and their boolean values
            case insensitive

        chunk_size : int (default = 1000)
            number of rows to process at a time

        """
        super().__init__(data=data)
        col = self.data
        self.column_len = col.size  # type: ignore
        self.nonnulls = col.dropna()  # type: ignore
        self.n_nonnulls = self.nonnulls.size
        self.n_nulls = self.column_len - self.n_nonnulls
        self.chunk_size = chunk_size
        self.chunks_processed = 0
        self.frac_processed = 0
        self.n_unique = self.nonnulls.nunique()
        # If the entire column is null, then set frac_unique to zero.
        self.frac_unique = (
            (self.n_unique / self.nonnulls.size) if self.nonnulls.size > 0 else 0
        )
        if len(self.nonnulls) > 0:
            self.nonnulls = self.nonnulls.sample(frac=1).reset_index(drop=True)
        self.bool_map = bool_map

    def stateless_inspection(self):  # type: ignore
        """Run inspection."""

    def inspect(self) -> "ColumnTypeInspector":
        """Run inspection."""
        if self.n_unique == 1:
            raise UnaryColumnError
        elif self.n_nonnulls == 0:
            # All columns are null. Fall back to "categorical"
            self.scores = {
                ColumnTypes.BOOLEAN: 0,
                ColumnTypes.CATEGORICAL: 1,
                ColumnTypes.NUMERIC: 0,
                ColumnTypes.ID: 0,
            }
            self.allowed_types = self._get_all_types()
            self.n_valid_numerics = 0
            self.n_invalid_numerics = 0
        elif self.n_unique == 2 and self._all_valid_bools(self.n_nonnulls):
            self.scores = {
                ColumnTypes.BOOLEAN: 1,
                ColumnTypes.CATEGORICAL: 0,
                ColumnTypes.NUMERIC: 0,
                ColumnTypes.ID: 0,
            }
            self.allowed_types = self._get_all_types()
        else:
            self.resolved = False
            self.n_valid_numerics = 0
            self.n_invalid_numerics = 0
            while not self.resolved:
                self._process_chunk()
        assert np.isclose(sum(self.scores.values()), 1)
        for score in self.scores.values():
            assert score >= 0
            assert score <= 1
        statistics = {
            "confidence": {k: v for k, v in self.scores.items()},
            "length": self.column_len,
            "n_missing": self.n_nulls,
            "n_nonnull": self.n_nonnulls,
            "n_unique": self.n_unique,
        }
        self.inspection = ColumnInspection(
            statistics=statistics,
            recommendation=self._get_recommended_transformer(self.scores),
            options=self._get_permissible_transformers(self.allowed_types),
            column_name=self.column_name,
        )
        return self

    @staticmethod
    def _get_all_types() -> List[str]:
        return [
            ColumnTypes.ID,
            ColumnTypes.BOOLEAN,
            ColumnTypes.NUMERIC,
            ColumnTypes.CATEGORICAL,
        ]

    def _get_permissible_transformers(
        self, allowed_types: List[str]
    ) -> Set[ColumnTypeTransformer]:
        permissible = set()
        # always allow column dropping
        permissible.add(DropColumnTransformer(self.column_name))
        for t in self.allowed_types:
            if t == ColumnTypes.ID:
                pass  # already allow column dropping
            else:
                permissible.add(
                    ColumnTypeTransformer(coltype=t, colname=self.column_name)
                )
        return permissible

    def _get_recommended_transformer(
        self, scores: Mapping[str, float]
    ) -> SupportsTransform:
        top_scoring_type = max(self.scores, key=self.scores.get)
        if top_scoring_type == ColumnTypes.ID:
            return DropColumnTransformer(self.column_name)
        else:
            return ColumnTypeTransformer(top_scoring_type, self.column_name)

    def _process_chunk(self) -> None:
        chunk_start = self.chunks_processed * self.chunk_size
        chunk_end = min((self.chunks_processed + 1) * self.chunk_size, self.n_nonnulls)
        chunk = self.nonnulls[chunk_start:chunk_end]
        self.chunks_processed = self.chunks_processed + 1
        frac_processed = chunk_end / self.n_nonnulls
        numerics = pd.to_numeric(chunk, errors="coerce").dropna()
        self.n_valid_numerics = numerics.size + self.n_valid_numerics
        frac_valid_numerics = self.n_valid_numerics / chunk_end
        frac_invalid_numerics = 1 - frac_valid_numerics
        numeric_score = frac_valid_numerics ** (1 / frac_processed)
        string_score = frac_invalid_numerics ** (1 / frac_processed)
        if numeric_score >= self.numeric_score_threshold:
            self._process_numeric_col_scores(
                numerics, frac_valid_numerics, frac_processed
            )
            self.resolved = True
        elif string_score >= self.string_score_threshold:
            self._process_string_col_scores(chunk, frac_valid_numerics, frac_processed)
            self.resolved = True

    def _all_valid_bools(self, col: pd.Series) -> bool:
        for val in col:
            if str(val).strip().upper() not in self.bool_map.keys():
                return False
        return True

    def _process_numeric_col_scores(
        self, vals: pd.Series, frac_valid_numerics: float, frac_processed: float
    ) -> None:
        if self._contains_decimals(vals):
            self._process_decimal_col_scores(frac_valid_numerics, frac_processed)
        else:
            self._process_int_col_scores(frac_valid_numerics, frac_processed)

    def _process_decimal_col_scores(
        self, raw_numeric_score: float, frac_processed: float
    ) -> None:
        numeric_score = (
            raw_numeric_score ** frac_processed
        ) ** self.numeric_score_exponent
        numeric_score = max(numeric_score, 0.5)
        if self.n_unique <= self.n_cat_unique_threshold:
            distributed_uncertainty = (1 - numeric_score) * (1 / 3)
            self.scores = {
                ColumnTypes.NUMERIC: numeric_score + distributed_uncertainty,
                ColumnTypes.CATEGORICAL: 2
                * distributed_uncertainty
                * (1 - self.frac_unique),
                ColumnTypes.ID: 2 * distributed_uncertainty * self.frac_unique,
                ColumnTypes.BOOLEAN: 0,
            }
        else:
            distributed_uncertainty = (1 - numeric_score) * (1 / 2)
            self.scores = {
                ColumnTypes.NUMERIC: numeric_score
                + 2 * distributed_uncertainty * (1 - self.frac_unique),
                ColumnTypes.CATEGORICAL: 0,
                ColumnTypes.ID: 2 * distributed_uncertainty * self.frac_unique,
                ColumnTypes.BOOLEAN: 0,
            }
        self.allowed_types = self._get_numeric_allowed_types()

    def _process_int_col_scores(
        self, raw_numeric_score: float, frac_processed: float
    ) -> None:
        numeric_score = (
            raw_numeric_score ** frac_processed
        ) ** self.numeric_score_exponent
        numeric_score = max(numeric_score, 0.5)
        numeric_score = min(numeric_score, 0.7)  # natural uncertainty
        unique_score = self.frac_unique ** self.id_unique_exponent
        if self.n_unique <= self.n_cat_unique_threshold:
            distributed_uncertainty = (1 - numeric_score) * (1 / 3)
            self.scores = {
                ColumnTypes.NUMERIC: numeric_score + distributed_uncertainty,
                ColumnTypes.CATEGORICAL: 2
                * distributed_uncertainty
                * (1 - unique_score),
                ColumnTypes.ID: 2 * distributed_uncertainty * unique_score,
                ColumnTypes.BOOLEAN: 0,
            }
        else:
            distributed_uncertainty = (1 - numeric_score) * (1 / 2)
            self.scores = {
                ColumnTypes.NUMERIC: numeric_score
                + 2 * distributed_uncertainty * (1 - unique_score),
                ColumnTypes.CATEGORICAL: 0,
                ColumnTypes.ID: 2 * distributed_uncertainty * unique_score,
                ColumnTypes.BOOLEAN: 0,
            }
        self.allowed_types = self._get_numeric_allowed_types()

    def _process_string_col_scores(
        self, vals: pd.Series, raw_numeric_score: float, frac_processed: float
    ) -> None:
        raw_string_score = 1 - raw_numeric_score
        string_score = (
            raw_string_score ** frac_processed
        ) ** self.string_score_exponent
        string_score = max(string_score, 2 / 3)
        numeric_score = 1 - string_score
        unique_score = self.frac_unique ** self.id_unique_exponent
        if self.n_unique <= self.n_cat_unique_threshold:
            self.scores = {
                ColumnTypes.ID: string_score * unique_score,
                ColumnTypes.CATEGORICAL: string_score * (1 - unique_score),
                ColumnTypes.NUMERIC: numeric_score,
                ColumnTypes.BOOLEAN: 0,
            }
        else:
            self.scores = {
                ColumnTypes.ID: string_score,
                ColumnTypes.NUMERIC: numeric_score,
                ColumnTypes.CATEGORICAL: 0,
                ColumnTypes.BOOLEAN: 0,
            }
        self.allowed_types = [t for t, score in self.scores.items() if score != 0]

    def _contains_decimals(self, numerics: pd.Series) -> bool:
        for x in numerics:
            if x != round(x):
                return True
        return False

    def _get_numeric_allowed_types(self) -> List[str]:
        types = [ColumnTypes.NUMERIC, ColumnTypes.ID]
        if self.n_unique <= self.n_cat_unique_threshold:
            types.append(ColumnTypes.CATEGORICAL)
        return types


class DataFrameTypeInspector(ColumnWiseInspector):
    """Inspector that runs ColumnTypeInspector for every column in dataframe."""

    def __init__(self, data: pd.DataFrame, **_: Any):
        """Construct the inspector.

        Parameters
        ----------
        data : pd.DataFrame
            data to inspect each column of

        **kwargs
            arguments to mop up
        """
        super().__init__(data, ColumnTypeInspector)

# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Exception definitions for ayx-learn."""


class DataScienceException(Exception):
    """Base exception for data science objects."""


class OheUnexpectedLevelsException(DataScienceException):
    """Exception for unexpected level in One Hot Encoding."""

    def __init__(self, message, errors):  # type: ignore
        self.levels, self.column_name = errors
        super().__init__(message)


class NullValueError(DataScienceException):
    """Exception for a dataframe containing null values."""

    def __init__(self, message, column_names):  # type: ignore
        self.column_names = column_names
        super().__init__(message)


class ImputationError(DataScienceException):
    """Exception for an issue when performing null value imputation."""

    def __init__(self, message, column_name):  # type: ignore
        self.column_names = column_name
        super().__init__(message)


class DegenerateDFError(Exception):
    """Degenerate dataframe."""


class NoRowsDFError(DegenerateDFError):
    """No rows in dataframe."""


class NoColsDFError(DegenerateDFError):
    """No columns in dataframe."""


class InvalidMinimalDFError(Exception):
    """Invalid minimal dataframe."""


class InsufficientRowsDFError(InvalidMinimalDFError):
    """Insufficient rows in dataframe."""


class InsufficientColsDFError(InvalidMinimalDFError):
    """Insufficient columns in dataframe."""


class InvalidTargetError(Exception):
    """Invalid target."""


class NonBinaryTargetError(InvalidTargetError):
    """Non binary target."""


class TooManyLevelsError(InvalidTargetError):
    """Too many levels."""


class NonNumericTargetError(InvalidTargetError):
    """Target is not numeric."""


class NoFoldsEvaluatedError(Exception):
    """No folds evaluated."""


class OneDimensionalTypeError(Exception):
    """One dimensional type error."""


class TwoDimensionalTypeError(Exception):
    """Two dimensional type error."""


class PositiveClassNotInTargetError(Exception):
    """Positive class not found in the target."""


class TargetPredictedLengthMatchError(Exception):
    """Mismatch in length of predictions."""


class UnaryColumnError(Exception):
    """Column contains a single unique value."""


class PipelineShapeError(Exception):
    """Invalid structure to pipeline for an expected operation."""


class PredictWithoutEstimatorError(PipelineShapeError):
    """Attempting to call a predict-like method on pipeline without estimator."""


class PredictWithoutClassificationEstimatorError(PipelineShapeError):
    """Attempting to call a predict-like method on pipeline without classification estimator."""

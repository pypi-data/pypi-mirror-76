# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Data science objects for evaluations on models."""
from .abs_error_plot import AbsErrorPlot
from .accuracy import Accuracy
from .adjr2 import AdjR2
from .auc import AUC
from .classification import ClassificationEvaluation
from .classification_importance import ClassificationImportance
from .confusion_matrix import ConfusionMatrix
from .evaluation import Evaluation
from .log_loss import LogLoss
from .m_auc import M, a_metric, m_auc
from .mae import MAE
from .mape import MAPE
from .mre import MRE
from .predicted_vs_actual import PredictedVsActual
from .r2 import R2
from .regression import RegressionEvaluation
from .regression_importance import RegressionImportance
from .rmse import RMSE
from .roc import ROC


__all__ = [
    "AbsErrorPlot",
    "Accuracy",
    "AdjR2",
    "AUC",
    "a_metric",
    "ClassificationEvaluation",
    "ClassificationImportance",
    "ConfusionMatrix",
    "Evaluation",
    "LogLoss",
    "M",
    "MAE",
    "MAPE",
    "MRE",
    "m_auc",
    "PredictedVsActual",
    "R2",
    "RegressionEvaluation",
    "RegressionImportance",
    "RMSE",
    "ROC",
    "a_metric",
    "m_auc",
]

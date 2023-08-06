# Copyright (c) 2019, Alteryx Inc.
"""Computation for goodman-kruskal-tau metric."""
from typing import Tuple

import numpy as np

import pandas as pd


def gk_tau(x: np.array, y: np.array) -> Tuple[float, float]:
    """Calculate the Goodman Kruskal tau statistics between categorical variables.

    Parameters
    ----------
    x : np.array (1-D)

    y : np.array (1-D)

    """
    assert x.size == y.size
    n = x.size
    contingency_pcts = pd.crosstab(x, y).values / n

    col_pcts = np.sum(contingency_pcts, axis=0)
    row_pcts = np.sum(contingency_pcts, axis=1)
    v_x = 1 - np.dot(row_pcts, row_pcts)
    v_y = 1 - np.dot(col_pcts, col_pcts)

    square_pcts = np.square(contingency_pcts)
    ev_x_y = 1 - np.sum(np.sum(square_pcts, axis=0) / col_pcts)
    ev_y_x = 1 - np.sum(np.sum(square_pcts, axis=1) / row_pcts)

    tau_xy = (v_x - ev_x_y) / v_x
    tau_yx = (v_y - ev_y_x) / v_y

    return tau_xy, tau_yx

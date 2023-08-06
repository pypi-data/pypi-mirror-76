# Copyright (c) 2019, Alteryx Inc.
"""Methods for binning numeric values based on entropy.

Implementation based on
Fayyad, Usama M.; Irani, Keki B. (1993) "Multi-Interval Discretization of Continuous-Valued Attributes for Classification Learning" (PDF). hdl:2014/35171., Proc. 13th Int. Joint Conf. on Artificial Intelligence (Q334 .I571 1993), pp. 1022-1027

"""
from functools import partial
from typing import Callable, List, Optional, Tuple

import numpy as np

EPS = 10e-16


def safe_log(x: np.float, base: np.float = np.exp(1)) -> np.float:
    """Take logarithm of base. Invalid values evaluate to 0.

    This is done rather than try/catch for efficiency (noticeable when vectorized)
    and because try/catch by callers would lead to excessive duplication.

    Parameters
    ----------
    x : numeric
        Numeric value to take logarithm of

    base : numeric (> 0)
        Log base

    Returns
    -------
    double

    """
    return safe_log_arr(np.array([x]), base=base, copy=False)[0]


def safe_log_arr(
    x: np.array, base: np.float = np.exp(1), copy: bool = True
) -> np.array:
    """Take element-wise logarithm of base. Invalid values evaluate to 0.

    Parameters
    ----------
    x : np.array, numeric
        Numeric values to take logarithm of

    base : numeric (> 0)
        Log base

    copy : bool
        make a copy before operating on array

    Returns
    -------
    Array of log values

    NOTE: not leaving `copy`=True may cause mutations to the input `x`

    """
    if copy:
        x = x.copy()
    # values <= 0 are invalid; make them evaluate (via log) to 0
    x[x <= 0] = 1
    return np.true_divide(np.log(x), np.log(base))


def entropy(x: np.array) -> np.float:
    """Calculate entropy of array.

    Parameters
    ----------
    x : np.array

    Returns
    -------
    entropy calculation (numeric scalar)

    """
    _, counts = np.unique(x, return_counts=True)
    percentages = np.true_divide(counts, x.size)
    return -np.dot(percentages, safe_log_arr(percentages, base=2))


def order_by(by: np.array, *arrays_to_order: np.array) -> Tuple[np.array, ...]:
    """Order several arrays in terms of a single one.

    by : np.array
        This array's sorting order will be used to order each in arrays_to_order.

    arrays_to_order : np.array s
        Arrays to sort.

    Returns
    -------
    tuple of arrays, one for each array in arrays_to_order,
    all sorted in terms of the values in `by`

    """
    index_order = np.argsort(by)
    return tuple(arr[index_order] for arr in arrays_to_order)


def split_at(arr: np.array, index: int) -> Tuple[np.array, np.array]:
    """Split array into 2 arrays at index. Index-element in right split.

    Parameters
    ----------
    arr : array
        array to sort split

    index : int >= 0
        index to split arr at

    Returns
    -------
    2 element tuple:
        array of first `index` elements of arr,
        array of rest of arr

    """
    return arr[:index], arr[index:]


def tree_split_score(
    var: np.array, position: int, criterion: Callable[[np.array], np.float] = entropy
) -> np.float:
    """Calculate the score of a tree split, based on given criterion.

    var[position] is last element in left branch.

    Parameters
    ----------
    var : array
        to score

    position : int >= 0
        index to split at

    criterion : function
        scoring function to use on splits

    Returns
    -------
    double : score value of split
    """
    left, right = split_at(var, position + 1)
    left_pct = left.size / var.size
    right_pct = 1 - left_pct
    return left_pct * criterion(left) + right_pct * criterion(right)


class NoValidSplitException(Exception):
    """No valid split based on a splitting criterion."""


def split(
    x: np.array,
    y: np.array,
    total_size: int,
    criterion: Callable[[np.array], np.float] = entropy,
    ordered: bool = False,
) -> Tuple[int, np.float, Optional[np.float]]:
    """Split x based on y, minimizing a splitting function `criterion`.

    Parameters
    ----------
    x : np.array
        to split

    y : np.array
        determines where to split x

    total_size : int
        original total size of array

    criterion : function
        splitting function to use. defaults to entropy

    ordered : bool
        Whether x and y are already ordered by x.

    Returns
    -------
    index : int (>= 0)
        Index of split. Left split in [:index].
        Note: this is not relevant when ordered = False,
        as the index is based on sorted array

    min_score : double
        Minimum score

    gain : double or None
        double if gain >= threshold, else None

    """
    assert x.size == y.size
    if not ordered:
        x, y = order_by(x, x, y)

    valid_split_indices = _get_valid_split_indices(x, y)
    if len(valid_split_indices):
        # need info for minimum criterion split
        score_calculator = np.vectorize(
            partial(tree_split_score, var=y, criterion=criterion), otypes=[float]
        )
        scores = score_calculator(position=valid_split_indices)
        min_index = np.argmin(scores)
        min_score = scores[min_index]
        split_index = valid_split_indices[min_index]

        log2 = partial(safe_log, base=2)
        # compute results

        delta, base_score = _compute_delta_and_base(y, split_index, criterion)

        threshold = log2(y.size - 1) / y.size + delta / y.size

        gain = base_score - min_score
        # use dampening factor on threshold that always results in >= 2 bins
        if gain < threshold * (1 - y.size / total_size):
            raise NoValidSplitException

    else:
        raise NoValidSplitException

    return split_index, min_score, gain


def _compute_delta_and_base(
    y: np.array, split_index: int, scoring_function: Callable[[np.array], np.float]
) -> Tuple[np.float, np.float]:
    y_n_uniques = np.unique(y).size
    base_score = scoring_function(y)
    base_norm_score = y_n_uniques * base_score
    left, right = split_at(y, split_index + 1)
    left_score = _compute_norm_score(left, scoring_function)
    right_score = _compute_norm_score(right, scoring_function)
    delta = (
        safe_log(3 ** y_n_uniques, base=2) - base_norm_score + left_score + right_score
    )
    return delta, base_score


def _index_is_valid_split(
    i: int, ordered_unique_indices: np.array, ys: np.array
) -> bool:
    try:
        start_of_this_x = ordered_unique_indices[i - 1] + 1 if i >= 0 else 0
        end_of_next_x = ordered_unique_indices[i + 1]
        ys = ys[start_of_this_x : (end_of_next_x + 1)]
        return np.unique(ys).size > 1  # type: ignore
    except Exception:
        return False


def _get_valid_split_indices(xs: np.array, ys: np.array) -> np.array:
    # Assumes x and y sorted by x, same length
    ordered_unique_indices = np.nonzero(xs[:-1] != xs[1:])[0]
    validity_checker = np.vectorize(
        partial(
            _index_is_valid_split, ordered_unique_indices=ordered_unique_indices, ys=ys
        ),
        otypes=[bool],
    )
    return ordered_unique_indices[validity_checker(range(len(ordered_unique_indices)))]


def _compute_norm_score(
    values: np.array, scoring_function: Callable[[np.array], np.float]
) -> np.float:
    """Scoring function on values / number of uniques in values."""
    # if n_uniques already determined (allowed for efficiency),
    # use that instead of re-counting
    n_uniques = np.unique(values).size
    return n_uniques * scoring_function(values)


def split_bin(
    xs: np.array,
    ys: np.array,
    lower_bound: np.float,
    upper_bound: np.float,
    total_size: int,
) -> List[Tuple[np.float, np.float]]:
    """Split the bin based on entropy-splitting.

    xs and ys should be ORDERED np.arrays

    Splitting occurs recursively as long as a "useful" (per entropy gain)
    split is found


    Parameters
    ----------
    xs : np.array
        should be ordered. Bin these

    ys : np.array
        should be ordered. Bin based on these

    lower_bound : double
        Lower bound for x

    upper_bound : double
        Upper bound for x

    total_size : int
        Original total size of x (or y)

    Returns
    -------
    list of bins
    bins are defined as 2-element tuples of the form lower_bound, upper_bound
    and are of the form [lower, upper)

    """
    try:
        x_index, _, gain = split(xs, ys, total_size, ordered=True)
        # add epsilon so that split in left
        middle_bin_edge = np.mean(xs[(x_index - 1) : (x_index + 1)]) + EPS
        # now, "cut" the bin (lower_bound, upper_bound) into
        # (lower_bound, middle_bin_edge) and (middle_bin_edge, upper_bound)
        # recursively attempting to split
        in_lower = xs < middle_bin_edge
        in_upper = np.logical_not(in_lower)
        lower_bins = split_bin(
            xs[in_lower], ys[in_lower], lower_bound, middle_bin_edge, total_size
        )
        upper_bins = split_bin(
            xs[in_upper], ys[in_upper], middle_bin_edge, upper_bound, total_size
        )
        return lower_bins + upper_bins
    except NoValidSplitException:
        return [(lower_bound, upper_bound)]


def entropy_bins(x: np.array, y: np.array) -> List[Tuple[np.float, np.float]]:
    """Get bin edges, based on entropy.

    Term n will be the lower bound of bin n and the upper bound of bin n-1.
    Bins are of the form [lower_bound, upper_bound] except the last, which is closed.

    """
    assert x.size == y.size
    # for efficiency, just sort (x and y in terms of x) once up front
    x, y = order_by(x, x, y)

    # start with single bin covering full range of x
    initial_bin = (x[0], x[-1] + EPS)
    # recursively split as long as allowed
    bins = split_bin(x, y, *initial_bin, total_size=x.size)

    # the standard way (i.e. numpy) to output bins is to output their edges.
    _, upper_bound = bins[-1]
    bin_edges = [lower_bound for lower_bound, _ in bins] + [upper_bound]
    return bin_edges


def entropy_bin_ids(x: np.array, y: np.array) -> List[int]:
    """Get bin ids, based on entropy."""
    return np.digitize(x, entropy_bins(x, y), True)  # type: ignore

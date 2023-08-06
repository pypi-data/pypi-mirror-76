# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements base class for calculating permutation importance."""
import abc
from typing import Dict

from ayx_learn.base import Pipeline
from ayx_learn.evaluations.multi_fold_evaluation import MultiFoldEvaluation
from ayx_learn.transformers.one_hot_encoder_transformer import OneHotEncoderTransformer
from ayx_learn.utils.exceptions import NoFoldsEvaluatedError

import numpy as np

from sklearn.utils import check_random_state


# ---------- HELPERS ------------#

_DEFAULT_RANDOM_SEED = 97121120


# ---------- PERMUTATION IMPORTANCE ------------#


class BasePermutationImportance(abc.ABC, MultiFoldEvaluation):
    """Base permutation importance class."""

    def __init__(self, random_state=_DEFAULT_RANDOM_SEED):  # type: ignore
        """Construct a permutation importance evaluation.

        Parameters
        ----------
        random_state :
            int, numpy.random.RandomState, or None
            If int, seed to use to seed numpy RandomState object;
            If RandomState object, object to used
            If None, numpy's RandomState will be used

        """
        super().__init__()  # type: ignore
        self.random_state = check_random_state(random_state)

    def _aggregate(self, scores):  # type: ignore
        if self.n_folds == 0:
            raise NoFoldsEvaluatedError

        def average_score_values(column_scores):  # type: ignore
            return {
                "column_name": column_scores[0]["column_name"],
                "value": np.mean([d["value"] for d in column_scores]),
            }

        return [
            average_score_values(column_scores)  # type: ignore
            for column_scores in zip(*scores)
        ]

    def get_shufflers(self, link: Dict):  # type: ignore
        """Get shufflers that respect encodings.

        Parameters
        ----------
        link : dict
            mapping between post-OHE column names and pre-OHE column names

        Returns
        -------
        dict
            Mapping between pre-OHE column names and shuffle functions.
            A shuffle function transforms a 2-D numpy array into a 2-D numpy array with the same shape, shuffling a collection of columns identically (with respect to index)

        """
        shufflers = dict()
        columns_without_shufflers = list(link.keys())
        while columns_without_shufflers:
            encoded_colnames = [
                encoded_name
                for encoded_name, original_name in link.items()
                if original_name == link[columns_without_shufflers[0]]
            ]
            shufflers[link[encoded_colnames[0]]] = self.get_shuffler(  # type: ignore
                encoded_colnames
            )
            columns_without_shufflers = [
                x for x in columns_without_shufflers if x not in encoded_colnames
            ]
        return shufflers

    def get_shuffler(self, colnames):  # type: ignore
        """Get the shuffling method."""

        def shuffle(df, copy=True):  # type: ignore
            col_nums = [i for i, x in enumerate(list(df)) if x in colnames]
            x = df.copy().values if copy else df.values
            x[:, col_nums] = self.random_state.permutation(x[:, col_nums])
            return x

        return shuffle

    def shuffle_score(  # type: ignore  # type: ignore
        self, link: Dict, score_func, df_x
    ):
        """Shuffle and score each column."""
        shufflers = self.get_shufflers(link)
        base_score = score_func(df_x)
        score_decreases = {
            colname: base_score - score_func(shuffler(df_x))
            for colname, shuffler in shufflers.items()
        }
        return score_decreases

    @abc.abstractmethod
    def _get_score(self, y_pred, y_true):  # type: ignore
        pass

    def _get_shuffle_scorer(self, y_true, estimator):  # type: ignore
        def score_x_test(x_test):  # type: ignore
            return self._get_score(estimator.predict(x_test), y_true)  # type: ignore

        return score_x_test

    def evaluate(  # type: ignore
        self, pipeline: Pipeline, x_test, y_true, *args, **kwargs
    ):
        """Run the evaluation."""
        column_names = list(x_test)

        encoder_idx = None
        for idx, step in enumerate(pipeline.pipeline_transform_steps):
            if isinstance(step, OneHotEncoderTransformer):
                encoder_idx = idx

        if encoder_idx is None:
            # if there's no one-hot-encoder we can simply transform via the pipeline
            x_final = pipeline.transform(x_test)
            link = {x: x for x in column_names}
        else:
            x_pre_encoding = x_test.copy()
            # in order to shuffle and respect one-hot-encodings
            # we need to get the columns going into the one-hot-encoder
            # in the form of a "link"
            for step in pipeline.pipeline_transform_steps[:encoder_idx]:
                x_pre_encoding = step.transform(x_pre_encoding)
            encoder = pipeline.pipeline_transform_steps[encoder_idx]
            link = encoder.get_link()
            x_final = x_pre_encoding
            for step in pipeline.pipeline_transform_steps[encoder_idx:]:
                x_final = step.transform(x_final)

        scorer = self._get_shuffle_scorer(y_true, pipeline.model)  # type: ignore
        shuffle_scores = self.shuffle_score(link=link, score_func=scorer, df_x=x_final)

        return [
            {"column_name": column_name, "value": score}
            for column_name, score in shuffle_scores.items()
        ]

    def format(self, score):  # type: ignore
        """Run the format to external representation."""
        return score

    def inverse_format(self, formatted_score):  # type: ignore
        """Run the inverse format to internal representation."""
        return formatted_score

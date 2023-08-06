# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Abstract class for model evaluations over multiple folds."""
import abc

from ayx_learn.evaluations.evaluation import Evaluation


class MultiFoldEvaluation(Evaluation):
    """Abstract class to define methods that evaluations must implement to support fold-independent evaluation and aggregation."""

    def __init__(self):  # type: ignore  # type: ignore
        """Construct the evaluation."""
        Evaluation.__init__(self)  # type: ignore
        self._scores = []

    def add_score(self, score):  # type: ignore
        """Add score for fold to collection of scores.

        Returns
        -------
        `self`

        """
        self._scores.append(score)
        return self

    def eval_fold(self, *args, **kwargs):  # type: ignore
        """Evaluate new data for new fold.

        Parameters
        ----------
        *args :
            positional args to pass to `Evaluation.evaluate`
        **kwargs :
            named args to pass to `Evaluation.evaluate`

        Returns
        -------
        `self`

        """
        self.add_score(self.evaluate(*args, **kwargs))  # type: ignore
        return self

    @property
    def n_folds(self):  # type: ignore
        """Get the number of folds."""
        return len(self._scores)

    @n_folds.setter
    def n_folds(self, n):  # type: ignore
        """Update `n_folds` without changing aggregated score.

        If folds are added, new folds' score is aggregated score.
        If folds are removed, all folds' score is aggregated score.

        Parameters
        ----------
        n : int (>= 0)
            number of folds

        """
        if n < self.n_folds:
            self._scores = [self.aggregate(self.scores)] * n  # type: ignore
        else:
            self._scores = self.scores + [
                self.aggregate(self.scores)  # type: ignore
            ] * (n - self.n_folds)

    @property
    def scores(self):  # type: ignore
        """List of scores, one per fold."""
        return self._scores

    @scores.setter
    def scores(self, scores):  # type: ignore
        """List of scores, one per fold."""
        self._scores = scores

    @abc.abstractmethod
    def _aggregate(self, scores):  # type: ignore
        """Aggregate list of scores, combining into single score of same type as elements of `scores`.

        Parameters
        ----------
        scores : list
            List of scores - one per fold

        Returns
        -------
        Object of same type as elements of `scores`; result of aggregating scores over all folds

        """

    @property
    def score(self):  # type: ignore
        """Single score, achieved by aggregating scores from folds.

        If set, it may change the scores of individual folds but will not change the aggregated result.
        """
        return self._aggregate(self.scores)  # type: ignore

    @score.setter
    def score(self, x):  # type: ignore
        """Single score, achieved by aggregating scores from folds.

        If set, it may change the scores of individual folds but will not change the aggregated result.
        """
        n_folds = max(self.n_folds, 1)
        self.scores = [x]
        self.n_folds = n_folds

    @property
    def formatted_scores(self):  # type: ignore
        """List of scores formatted for outputting, one for each fold."""
        return [self.format(s) for s in self.scores]  # type: ignore

    @formatted_scores.setter
    def formatted_scores(self, scores):  # type: ignore
        """List of scores formatted for outputting, one for each fold."""
        self.scores = [self.inverse_format(s) for s in scores]  # type: ignore

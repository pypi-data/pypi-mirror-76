# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements abstract base class for model evaluations."""
import abc


class Evaluation(metaclass=abc.ABCMeta):
    """Abstract Base class for model evaluations."""

    def __init__(self, **kwargs):  # type: ignore  # type: ignore
        """Construct the evaluation."""

    @property  # type: ignore
    @abc.abstractmethod
    def score(self):  # type: ignore  # type: ignore
        """Obtain score of evaluation."""

    @score.setter  # type: ignore
    @abc.abstractmethod
    def score(self, score):  # type: ignore
        """Set score of evaluation."""

    @abc.abstractmethod
    def format(self, score):  # type: ignore
        """Return formatted score."""

    @property
    def formatted_score(self):  # type: ignore
        """Score formatted for output."""
        return self.format(self.score)  # type: ignore

    @abc.abstractmethod
    def inverse_format(self, formatted_score):  # type: ignore
        """Return take formatted score and return score."""

    @formatted_score.setter  # type: ignore  # type: ignore  # type: ignore
    @property
    def formatted_score(self, f_score):  # type: ignore  # type: ignore
        """Take formatted_score as input and manipulate `self.score` accordingly.

        Parameters
        ----------
        f_score :
            formatted score, as returned, for example, by `self.format`

        """
        self.score = self.inverse_formatter(f_score)  # type: ignore  # type: ignore

    @abc.abstractmethod
    def evaluate(self, *args, **kwargs):  # type: ignore
        """Evaluate data, manipulating score."""

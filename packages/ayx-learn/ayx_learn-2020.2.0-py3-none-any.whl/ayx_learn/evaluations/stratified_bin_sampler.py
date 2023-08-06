# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
"""Implements the ``model-evaluations`` resource."""
import numpy as np

import sklearn


SAMPLING_RANDOM_SEED = 1943


class StratifiedBinSampler:
    """Stratified bin sampler object."""

    def __init__(  # type: ignore
        self, array_to_sample, random_state=SAMPLING_RANDOM_SEED
    ):
        """Construct the sampler."""
        self.array_to_sample = array_to_sample
        self.random_generator = sklearn.utils.check_random_state(SAMPLING_RANDOM_SEED)

    def sample(self, sample_size, sorter=np.sort):  # type: ignore
        """Run the sampling."""
        strata_sizes = self.make_strata_sizes(  # type: ignore
            len(self.array_to_sample), sample_size
        )
        cumulative_sizes = np.zeros(sample_size + 1)
        cumulative_sizes[1:] = np.add.accumulate(strata_sizes)
        cumulative_sizes = cumulative_sizes.astype(int)
        strata_start_indices = cumulative_sizes[:-1]
        strata_stop_indices = cumulative_sizes[1:]
        sorted_a = sorter(self.array_to_sample)

        def elements_within_strata(strata_index):  # type: ignore
            return sorted_a[
                strata_start_indices[strata_index] : strata_stop_indices[strata_index]
            ]

        def choose_random_strata_index(strata_index):  # type: ignore
            return self.random_generator.choice(
                elements_within_strata(strata_index).shape[0]  # type: ignore
            )

        sample_shape = (sample_size,) + sorted_a.shape[1:]

        return self.new_vector(  # type: ignore
            sample_shape,
            lambda i: elements_within_strata(i)[choose_random_strata_index(i)],
        )

    def make_strata_sizes(self, population_size, sample_size):  # type: ignore
        """Generate the stratifcation sizes."""
        # if we made evenly-sized strata, there'd be left-overs
        extras = population_size % sample_size
        # randomly choose which strata indices to add the left-overs to
        strata_to_increase = set(
            self.random_generator.choice(range(sample_size), size=extras, replace=False)
        )
        # all of the strata should be approximately-evenly-sized
        return [
            np.floor(population_size / sample_size) + (i in strata_to_increase)
            for i in range(sample_size)
        ]

    def new_vector(self, sample_shape, item_function):  # type: ignore
        """Create a new vector filled with items from a callable."""
        new_arr = np.zeros(sample_shape)
        for idx in range(sample_shape[0]):
            new_arr[idx] = item_function(idx)
        return new_arr

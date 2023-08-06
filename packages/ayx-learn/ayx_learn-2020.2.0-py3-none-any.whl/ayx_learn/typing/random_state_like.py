# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
"""Implements random-state-like for type-checking.

For consolidation and instancechecking, use `sklearn.utils.check_random_state`.
"""
from typing import Optional, Union

import numpy as np


RandomStateLike = Optional[Union[np.random.RandomState, int]]

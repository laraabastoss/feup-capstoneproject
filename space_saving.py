from __future__ import annotations

import math
import random
import typing

import numpy as np

from river import base


class SpaceSaving(base.Base):

    """Space-Saving algorithm for finding heavy hitters.

    The Space-Saving algorithm is designed to find the heavy hitters in a data stream using a
    fixed amount of memory. It keeps track of the frequency of each item and ensures that only
    the most frequent items are stored, discarding less frequent ones when necessary.

    Parameters
    ----------
    k
        The maximum number of heavy hitters to store.

    Attributes
    ----------
    counts : dict
        A dictionary to store the counts of items.

    Methods
    -------
    update(x, w=1)
        Update the counts with the given element.
    __getitem__(x) -> int
        Get the count of the given element.
    __len__() -> int
        Return the number of elements stored.
    total() -> int
        Return the total count.
    most_common() -> int
        Return the number of heavy hitters stored.

    Examples
    --------
    >>> ss = SpaceSaving(k=10)
    >>> for i in range(100):
    ...     ss.update(i % 10)
    ...
    >>> len(ss)
    10
    >>> ss.total()
    100
    >>> ss.most_common()
    10

    References
    ----------
    - Metwally, A., Agrawal, D., & Abbadi, A. E. (2005). Efficient computation of frequent and top-k
    elements in data streams. In Proceedings of the 10th International Conference on Database Theory
    (ICDT'05) (pp. 398-412). Springer-Verlag.
    """
    


    def __init__(self, k: int):
        self.k = k
        self.counts = {}

    def update(self, x: typing.Hashable, w: int = 1):

        """Update the counts with the given element."""
        if x in self.counts:
            self.counts[x] += w

        elif len(self.counts) > self.k:
            min_count_key = min(self.counts, key=self.counts.get)
            self.counts[x] = self.counts.get(min_count_key) + 1
            del self.counts[min_count_key]

        else:
            self.counts[x] = w

    def __getitem__(self, x) -> int:
        """Get the count of the given element."""
        return self.counts.get(x, 0)
    
    def __len__(self):
        """Return the number of elements stored."""
        return len(self.counts)
    
    def total(self) -> int:
        """Return the total count."""
        return sum(self.counts.values())
    
    @property
    def most_common(self) -> int:
        """Return the number of heavy hitters stored."""
        return min(len(self.counts), self.k)

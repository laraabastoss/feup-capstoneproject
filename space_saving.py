from __future__ import annotations

import math
import random
import typing

import numpy as np

from river import base


class SpaceSaving(base.Base):


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

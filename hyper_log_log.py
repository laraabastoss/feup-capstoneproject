from __future__ import annotations

import math
import typing

from river import base

class HyperLogLog(base.Base):
    def __init__(self, b: int):
        self.b = b
        self.m = 2 ** b
        self.alpha = self.get_alpha(self.m)
        self.registers = [0] * self.m

    @staticmethod
    def get_alpha(m: int) -> float:
        if m == 16:
            return 0.673
        if m == 32:
            return 0.697
        if m == 64:
            return 0.709
        return 0.7213 / (1 + 1.079 / m)

    @staticmethod
    def left_most_one(w: int) -> int:
        return len(bin(w)) - bin(w).rfind('1') - 1

    def update(self, x: typing.Hashable):
        hash_val = hash(x)
        j = hash_val & (self.m - 1)
        w = hash_val >> self.b
        self.registers[j] = max(self.registers[j], self.left_most_one(w))

    
    def count(self) -> int:
        est = self.alpha * self.m ** 2 / sum(2 ** (-reg) for reg in self.registers)

        # correction
        if est <= 5 / 2 * self.m:
            v = self.registers.count(0)
            if v != 0:
                return round(self.m * math.log(self.m / v))
        elif est <= 1 / 30 * 2 ** 32:
            return round(est)
        else:
            return round(-2 ** 32 * math.log(1 - est / 2 ** 32))

    def __len__(self) -> int:
        return self.count()

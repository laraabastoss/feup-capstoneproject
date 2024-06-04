from __future__ import annotations

import math
import typing

from river import base

class HyperLogLog(base.Base):

    """HyperLogLog algorithm for cardinality estimation.

    The HyperLogLog algorithm is designed to estimate cardinality of a data set with the aid
    of m bytes of auxiliary memory, know as registers.

    Firstly, each element in the data set is hashed into a binary string, ensuring data is
    uniformly distributed and simulating random distribution. The algorithm hashes each element 
    into a binary string and then organizes these binary representations into registers. 

    Hyper LogLog, represents an improvement over the original LogLog algorithm by utilizing a 
    technique called harmonic mean to estimate the cardinality.

    Parameters
    ----------
    b : int
        The precision parameter which determines the number of registers used (m = 2^b).
        Higher values of b provide more accurate estimates but use more memory.

    Attributes
    ----------
    b : int
        The precision parameter.
    m : int
        The number of registers (2^b).
    alpha : float
        A constant used in the cardinality estimation formula, which depends on m.
    registers : list of int
        A list of size m to store the maximum number of leading zeroes observed in the hash values.

    Methods
    -------
    update(x)
        Update the registers with the given element.
    count() -> int
        Estimate the number of distinct elements.
    __len__() -> int
        Return the estimated number of distinct elements.
    get_alpha(m) -> float
        Compute the bias correction constant alpha based on the number of registers.
    left_most_one(w) -> int
        Find the position of the left-most 1-bit in the binary representation of a number.


    Examples
    --------

    >>> from river import sketch

    >>> hll = sketch.HyperLogLog(b=15)

    >>> for i in range(100):
    ...     hll.update(i)

    >>> hyperloglog.count()
    100 

    >>> len(hyperloglog)
    100 

    References
    ----------

    - [^1]: Marianne Durand and Philippe Flajolet. Loglog counting of large cardinalities (extended abstract). Algorithms Project, INRIA–Rocquencourt, 2003.
    - [^2]: Philippe Flajolet,  ́Eric Fusy, Olivier Gandouet, and Fr ́ed ́eric Meunier. Hyperloglog: the analysis of a near-optimal cardinality estimation algorithm. Algorithms Project, IN-RIA–Rocquencourt. 

    """
    

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

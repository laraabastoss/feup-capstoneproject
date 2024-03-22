import collections
import random
from river import sketch
from space_saving import SpaceSaving
from hyper_log_log import HyperLogLog

# Create an instance of SpaceSaving with k=1000
spacesaving = SpaceSaving(k=1000)

# Create an instance of HyperLogLog with b=8 (number of bits for registers)
hyperloglog = HyperLogLog(b=8)

# Create a random number generator
rng = random.Random(7)

# Create a Counter to compare results
counter = collections.Counter()

# Generate random values and update the SpaceSaving, HyperLogLog, and Counter
vals = []
for v in range(100000):
    spacesaving.update(v)
    hyperloglog.update(v)
    counter[v] += 1
   # vals.append(v)

# Print some results for comparison
print("SpaceSaving counts:")
print(spacesaving.counts)
print("HyperLogLog count:")
print(hyperloglog.count())
print("Counter counts:")
print(counter)

# Test some specific values
print("Count of 333 in Counter:", counter[333])
print("Count of 333 in SpaceSaving:", spacesaving[333])

print("Count of 532 in Counter:", counter[532])
print("Count of 532 in SpaceSaving:", spacesaving[532])


# Print lengths of Counter and SpaceSaving
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", spacesaving.total())
print("Length of HyperLogLog:", hyperloglog.count())

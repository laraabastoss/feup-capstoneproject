import collections
import random
from river import sketch
from space_saving import SpaceSaving
from hyper_log_log import HyperLogLog
from hierarchical_heavy_hitters import HierarchicalHeavyHitters

# Create an instance of SpaceSaving with k=1000
spacesaving = SpaceSaving(k=100000)

# Create an instance of HyperLogLog with b=8 (number of bits for registers)
hyperloglog = HyperLogLog(b=8)

# Create an instance of HierarchicalHeavyHitters with k=10, epsilon=0.01, and threshold_ratio=0.5
hierarchical_hh = HierarchicalHeavyHitters(k=10, epsilon=0.01, threshold_ratio=0.5)

# Create a random number generator
rng = random.Random(7)

# Create a Counter to compare results
counter = collections.Counter()

# Generate random values and update the SpaceSaving, HyperLogLog, HierarchicalHeavyHitters, and Counter
for v in [1,2,3,4,5,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,1,23,4,5,6,1,2,3,4,5]:
    spacesaving.update(v)
    hyperloglog.update(v)
    hierarchical_hh.update(str(v))
    counter[v] += 1

# Print some results for comparison
# print("SpaceSaving counts:")
# print(spacesaving.counts)
# print("HyperLogLog count:")
# print(hyperloglog.count())
print("HierarchicalHeavyHitters counts:")
print(hierarchical_hh.output(phi=100))
print("Counter counts:")
# print(counter)

# Test some specific values
print("Count of 2 in Counter:", counter[2])
print("Count of 2 in SpaceSaving:", spacesaving[2])
print("Count of 2 in HierarchicalHeavyHitters:", hierarchical_hh[str(2)])




print("Count of 7 in Counter:", counter[7])
print("Count of 7 in SpaceSaving:", spacesaving[7])
print("Count of 7 in HierarchicalHeavyHitters:", hierarchical_hh[str(7)])

# Print lengths of Counter and SpaceSaving
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", spacesaving.total())
print("Length of HyperLogLog:", hyperloglog.count())

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
for v in [12,23,35,45,55,16,25,36,36,36,36,36]:
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

print(hierarchical_hh)

phi = 100

# Extract heavy hitters
heavy_hitters = hierarchical_hh.output(phi)

# Print the heavy hitters
print("Heavy Hitters:")
for item in heavy_hitters:
    print(item)



print("Count of 36665 in Counter:", counter[36])
print("Count of 36665 in SpaceSaving:", spacesaving[36])
print("Count of 36665 in HierarchicalHeavyHitters:", hierarchical_hh[str(36)])

# Print lengths of Counter and SpaceSaving
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", spacesaving.total())
print("Length of HyperLogLog:", hyperloglog.count())

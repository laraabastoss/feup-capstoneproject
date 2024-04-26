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
hierarchical_hh = HierarchicalHeavyHitters(k=10, epsilon=0.25)

# Create a random number generator
rng = random.Random(7)


counter = collections.Counter()

with open('data/chess.txt', 'r') as f:
    lines = f.readlines()


for line in [1,2,21,31,34,212,3]:

    hierarchical_hh.update(str(line))

'''
print("HierarchicalHeavyHitters counts:")
print(hierarchical_hh.output(phi=100))
'''

print(hierarchical_hh)

phi = 0.1


# Extract heavy hitters
heavy_hitters = hierarchical_hh.output(phi)

# Print the heavy hitters
print(hierarchical_hh.totals())
print(heavy_hitters)

for item in heavy_hitters:
    print(item)



print("Count of 36665 in Counter:", counter[34])
print("Count of 36665 in SpaceSaving:", spacesaving[34])
print("Count of 36665 in HierarchicalHeavyHitters:", hierarchical_hh[str(2)])

# Print lengths of Counter and SpaceSaving
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", spacesaving.total())
print("Length of HyperLogLog:", hyperloglog.count())

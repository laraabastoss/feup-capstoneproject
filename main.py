import collections
import random
from river import sketch
from space_saving import SpaceSaving
from hyper_log_log import HyperLogLog
from hierarchical_heavy_hitters import HierarchicalHeavyHitters


counter = sketch.Counter()
# Create an instance of SpaceSaving with k=1000
spacesaving = SpaceSaving(k=70)

# Create an instance of HyperLogLog with b=8 (number of bits for registers)
hyperloglog = HyperLogLog(b=8)

# Create an instance of HierarchicalHeavyHitters with k=10, epsilon=0.01, and threshold_ratio=0.5
hierarchical_hh = HierarchicalHeavyHitters(k=10, epsilon=0.25)

# Create a random number generator
rng = random.Random(7)


counter = collections.Counter()

'''
for line in [1,2,21,31,34,212,3,24]:

    hierarchical_hh.update(str(line))
'''

with open('data/chess.txt', 'r') as f:
    for line in f:
        elements = line.strip().split()
        for element in elements:
            counter.update(element)
            spacesaving.update(element, 1)
            #hierarchical_hh.update(element)


# SpaceSaving tests
print(spacesaving.counts)

'''
print("HierarchicalHeavyHitters counts:")
print(hierarchical_hh.output(phi=100))
print(hierarchical_hh)
phi = 0.1
heavy_hitters = hierarchical_hh.output(phi)
print(hierarchical_hh.totals())
print(heavy_hitters)
for item in heavy_hitters:
    print(item)

'''





print("Count of 62 in Counter:", counter['61'])
print("Count of 62 in SpaceSaving:", spacesaving['61'])
#print("Count of 36665 in HierarchicalHeavyHitters:", hierarchical_hh[str(2)])

# Print lengths of Counter and SpaceSaving
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", spacesaving.total())
#print("Length of HyperLogLog:", hyperloglog.count())

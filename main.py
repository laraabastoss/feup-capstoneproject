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
hyperloglog = HyperLogLog(b=15)


'''
for i in range(100):
    hyperloglog.update(i)

print("Estimated number of distinct elements:", len(hyperloglog))
'''
def custom_parent_func(x, i):
    
    if i == len(x)+1:
        return None  # Define the root value
    return x[:i + 1]  # Custom parent function


def custom_parent_func2(x, i):
    if i == x:
        return str(0)  # Define the root value
    return str(int(x) - i) # Custom parent function

# Create an instance of HierarchicalHeavyHitters with the new parent function and root value
hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.001, parent_func=custom_parent_func, root_value=None)

# Create a random number generator
rng = random.Random(7)


counter = collections.Counter()


for line in [ 1,21,31,34,212,3,24]:

    hierarchical_hh.update(str(line))


with open('data/chess.txt', 'r') as f:
    for line in f:
        elements = line.strip().split()
        for element in elements:
            counter.update(element)
            spacesaving.update(element, 1)
            hyperloglog.update(element)
            #hierarchical_hh.update(element)


# SpaceSaving tests
#print(spacesaving.counts)


#print( hierarchical_hh['21'])
#print(hierarchical_hh.output(phi=100))
print(hierarchical_hh)
phi = 0.01
#heavy_hitters = hierarchical_hh.output(phi)
#print(hierarchical_hh.totals())
#print(heavy_hitters)
#print(heavy_hitters)



#print("Count of 61 in Counter:", counter['61'])
#print("Count of 61 in SpaceSaving:", spacesaving['61'])
#print("Count of 61 in SpaceSaving:", hyperloglog['61'])
#print("Count of 36665 in HierarchicalHeavyHitters:", hierarchical_hh[str(2)])

# Print lengths of Counter and SpaceSaving

"""
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", spacesaving.total())
print("Length of HyperLogLog:", hyperloglog.count())
"""
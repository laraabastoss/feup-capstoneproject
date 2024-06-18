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


'''
for i in range(100):
    hyperloglog.update(i)

print("Estimated number of distinct elements:", len(hyperloglog))
'''

def custom_parent_func(x, i): 
    if i > len(x):
         return None 
    return x[:i]

def custom_parent_func2(x, i):
    if i == x:
        return str(0)  # Define the root value
    return str(int(x) - i) # Custom parent function

def custom_parent_func3(x, i):
    parts = x.split('.')
    if i >= len(parts):
        return None  
    return '.'.join(parts[:i+1])

# Create an instance of HierarchicalHeavyHitters with the new parent function and root value
hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.00001)

# Create a random number generator
rng = random.Random(7)


counter = collections.Counter()


for line in [ 1,2,3,4,5,6,7,8,9,1,2,3,4,45454,45454,66]:
    #hyperloglog.update(line)
    hierarchical_hh.update(str(line))


with open('data/chess.txt', 'r') as f:
    for line in f:
        elements = line.strip().split()
        for element in elements:
            counter.update(element)
            #spacesaving.update(element, 1)
            #hyperloglog.update(element)
            #hierarchical_hh.update(element)


# SpaceSaving tests
#print(spacesaving.counts)


#print( hyperloglog.count())
#print(hierarchical_hh.output(phi=100))
print(hierarchical_hh)
phi = 0.01
heavy_hitters = hierarchical_hh.output(phi)
#print(hierarchical_hh.totals())
print(heavy_hitters)
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
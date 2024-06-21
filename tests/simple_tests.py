import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from space_saving import SpaceSaving
from hyper_log_log import HyperLogLog
from hierarchical_heavy_hitters import HierarchicalHeavyHitters


# Space Saving

print("Space Saving")

# Create an instance of SpaceSaving with k=70

spacesaving = SpaceSaving(k=10)

# Test Case 1

for i in range(100):
    spacesaving.update(i % 10)

print(len(spacesaving))

print(spacesaving.total())

print(spacesaving.heavy_hitters)

print(spacesaving[10])

# Test Case 2

spacesaving = SpaceSaving(k=10)

list = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,10,100,1000]
for i in list:

    spacesaving.update(i )

print(len(spacesaving))

print(spacesaving.total())

print(spacesaving.heavy_hitters)

print(spacesaving[1])
print(list.count(1))

print(spacesaving[2])
print(list.count(2))

print(spacesaving[4])
print(list.count(4))

print(spacesaving[9])
print(list.count(9))

# ------------------------------------------------------------------------------------------------------

# Hyper Log Log

print("Hyper Log Log")

hyperloglog = HyperLogLog(b=15)

for i in range(100):
    hyperloglog.update(i)

print(hyperloglog.count())

hyperloglog = HyperLogLog(b=15)

for i in range(100):
    hyperloglog.update(i%10)

print(hyperloglog.count())

# ------------------------------------------------------------------------------------------------------

# Hierarchical Heavy Hitters

print("Hierarchical Heavy Hitters")

def custom_parent_func(x, i): 
    if i > len(x):
         return None 
    return x[:i]

def custom_parent_func2(x, i):
    parts = x.split('.')
    if i >= len(parts):
        return None  
    return '.'.join(parts[:i+1])

hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.00001)

for line in [1,2,21,31,34,212,3,24]:
    hierarchical_hh.update(str(line))

print(hierarchical_hh)
  
print( hierarchical_hh['212'])

phi = 0.01
heavy_hitters = hierarchical_hh.output(phi)
print(heavy_hitters)


hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.00001, parent_func = custom_parent_func)

for line in [1,2,21,31,34,212,3,24]:
    hierarchical_hh.update(str(line))

print(hierarchical_hh)

print( hierarchical_hh['212'])

phi = 0.01
heavy_hitters = hierarchical_hh.output(phi)
print(heavy_hitters)

hierarchical_hh = HierarchicalHeavyHitters(k=10, epsilon=0.001, parent_func=custom_parent_func2, root_value=None)

for line in ["123.456","123.123", "456.123", "123", "123"]:
    hierarchical_hh.update(line)

print(hierarchical_hh)

heavy_hitters = hierarchical_hh.output(phi)
print(heavy_hitters)

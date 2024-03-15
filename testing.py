import collections
import random
from river import sketch
from spacesaving import SpaceSaving


# Create an instance of SpaceSaving with k=5
spacesaving = SpaceSaving(k=5)

# Create a random number generator
rng = random.Random(7)

# Create a Counter to compare results
counter = collections.Counter()

# Generate random values and update the SpaceSaving and Counter
vals = [1,2,3,4,5,2,2,6,7,8,9,10,11]
for v in vals:
    spacesaving.update(v)
    counter[v] += 1

# Print some results for comparison
print("SpaceSaving counts:")
print(spacesaving.counts)
print("Counter counts:")
print(counter)

# Test some specific values
print("Count of 2 in Counter:", counter[2])
print("Count of 2 in SpaceSaving:", spacesaving[2])
print("Count of 5 in Counter:", counter[5])
print("Count of 5 in SpaceSaving:", spacesaving[5])

# Print lengths of Counter and SpaceSaving
print("Length of Counter:", len(counter))
print("Length of SpaceSaving:", len(spacesaving))







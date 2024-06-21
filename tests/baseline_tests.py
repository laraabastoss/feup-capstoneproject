import sys
import os
import time
import resource

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from space_saving import SpaceSaving
from hyper_log_log import HyperLogLog
from hierarchical_heavy_hitters import HierarchicalHeavyHitters

# Initialize the algorithms
space_saving = SpaceSaving(k=100)
hyper_log_log = HyperLogLog(b=15)
hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.00001)

# Data Stream file path 
file_path = '../data/chess.txt'

# Start time
start_time = time.time()

# Measure Memory
def get_memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


initial_mem_usage = get_memory_usage()
space_saving_mem_usage = initial_mem_usage
hyper_log_log_mem_usage = initial_mem_usage
hierarchical_hh_mem_usage = initial_mem_usage

with open(file_path, 'r') as f:
    for line in f:
        elements = line.strip().split()
        for element in elements:
 
            space_saving_mem_usage = max(space_saving_mem_usage, get_memory_usage())
            hyper_log_log_mem_usage = max(hyper_log_log_mem_usage, get_memory_usage())
            hierarchical_hh_mem_usage = max(hierarchical_hh_mem_usage, get_memory_usage())


            space_saving.update(element, 1)
            hyper_log_log.update(element)
            hierarchical_hh.update(element)


total_time = time.time() - start_time

# Performance
print("Space Saving Algorithm:")
print(f"Memory Usage: {space_saving_mem_usage / 1024} MB")  
print(f"Execution Time: {total_time} seconds")

print("\nHyperLogLog Algorithm:")
print(f"Memory Usage: {hyper_log_log_mem_usage / 1024} MB") 
print(f"Execution Time: {total_time} seconds")

print("\nHierarchical Heavy Hitters Algorithm:")
print(f"Memory Usage: {hierarchical_hh_mem_usage / 1024} MB")  
print(f"Execution Time: {total_time} seconds")

# Some values to compare
print("\nAdditional Outputs:")
print("Space Saving Heavy Hitters:", space_saving.heavy_hitters)
print("HyperLogLog Estimated Count:", hyper_log_log.count())
phi = 0.01
heavy_hitters = hierarchical_hh.output(phi)
print("Hierarchical Heavy Hitters Heavy Hitters:", heavy_hitters)

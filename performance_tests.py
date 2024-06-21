import numpy as np
import matplotlib.pyplot as plt
from pympler import asizeof
import time
from space_saving import SpaceSaving
from hyper_log_log import HyperLogLog
from hierarchical_heavy_hitters import HierarchicalHeavyHitters

# Customizable parameters

k_space_saving = 100
b_hyper_log_log = 20
skew = 2.0

# ------------------------------------------------------------------------------------------------------

# Auxiliar Function

# Generate true cardinality from stream
def generate_ground_truth(stream):
    true_cardinality = len(set(stream))  
    return true_cardinality

# Generate keys for HHH heavy hitters
def get_keys_from_heavy_hitters(heavy_hitters):
    keys = [int(key) for key, _ in heavy_hitters]
    return keys

# Generate true Heavy Hitters from stream
def get_actual_heavy_hitters(stream, k):
    from collections import Counter
    counter = Counter(stream)
    return set(dict(counter.most_common(k)).keys())

# Generate Stream
def generate_zipf_data(size, skew):
    return np.random.zipf(skew, size)

# Measure speed
def measure_speed(algorithm, stream):
    start_time = time.time()
    for item in stream:
        algorithm.update(item)
 
    end_time = time.time()
    if (type(algorithm) is HyperLogLog):
        return end_time - start_time, algorithm.count()
    
    elif (type(algorithm) is SpaceSaving):

        filtered_hitters = {key: count for key, count in algorithm.heavy_hitters.items() if count != 1}
        return end_time - start_time, filtered_hitters
    
    else:
        return end_time - start_time, algorithm.output(0.01)

# Measure memory
def get_memory_usage(obj):
    return asizeof.asizeof(obj)

# ------------------------------------------------------------------------------------------------------

# Initialize Auxiliar Variables 
sizes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000] 
accuracy_hyperloglog = []
accuracy_spacesaving = []
accuracy_hierarchicalhh = []
speed_results = []
memory_results = []
recall_spacesaving = []
recall_hyperloglog = []
recall_hierarchicalhh = []
re_spacesaving = []
re_hyperloglog = []
re_hierarchicalhh = []

# ------------------------------------------------------------------------------------------------------

# Iterate through sizes
for size in sizes:
    stream = generate_zipf_data(size, skew)
 
    # Initialize algorithms
    space_saving = SpaceSaving(k=k_space_saving)
    hyper_log_log = HyperLogLog(b=b_hyper_log_log)
    hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.00001)

    # Measure speed
    speed_space_saving, heavy_hitters = measure_speed(space_saving, stream)
    speed_hyper_log_log, count = measure_speed(hyper_log_log, stream)
    speed_hierarchical_hh, heavy_hitters_hhh = measure_speed(hierarchical_hh, stream)
    speed_results.append((speed_space_saving, speed_hyper_log_log, speed_hierarchical_hh))

    # Measure memory
    memory_space_saving = get_memory_usage(space_saving)
    memory_hyper_log_log = get_memory_usage(hyper_log_log)
    memory_hierarchical_hh = get_memory_usage(hierarchical_hh)
    memory_results.append((memory_space_saving, memory_hyper_log_log, memory_hierarchical_hh))

    # Calculate accuracy for SpaceSaving
    ground_truth_heavy_hitters = get_actual_heavy_hitters(stream, k=len(heavy_hitters))
    print(len(set(heavy_hitters.keys()).intersection(ground_truth_heavy_hitters)))
    accuracy = len(set(heavy_hitters.keys()).intersection(ground_truth_heavy_hitters)) / len(heavy_hitters)
    accuracy_spacesaving.append( accuracy)

    # Calculate accuracy for HyperLogLog
    ground_truth = generate_ground_truth(stream)
    accuracy_hll = 1 - abs(count - ground_truth) / ground_truth
    accuracy_hyperloglog.append(accuracy_hll)

    # Calculate accuracy for HHH
    ground_truth = get_actual_heavy_hitters(stream,len(heavy_hitters_hhh))
    accuracy_hhh = len(set(get_keys_from_heavy_hitters(heavy_hitters_hhh)).intersection(ground_truth))/ len(heavy_hitters_hhh)
    accuracy_hierarchicalhh.append( accuracy_hhh)

    # Calculate recall for SpaceSaving
    actual_heavy_hitters = np.array(list(ground_truth_heavy_hitters))
    recall_space_saving = len(set(heavy_hitters.keys()).intersection(actual_heavy_hitters)) / len(actual_heavy_hitters)
    recall_spacesaving.append(recall_space_saving)
    
    # Calculate recall for HyperLogLog (assuming all unique)
    recall_hyper_log_log = count / len(set(stream))
    recall_hyperloglog.append(recall_hyper_log_log)
    
    # Calculate recall for HHH
    recall_hierarchical_hh = len(set(get_keys_from_heavy_hitters(heavy_hitters_hhh)).intersection(actual_heavy_hitters)) / len(actual_heavy_hitters)
    recall_hierarchicalhh.append(recall_hierarchical_hh)
    
    # Calculate RE for SpaceSaving
    re_space_saving = 1 - accuracy
    re_spacesaving.append(re_space_saving)

    # Calculate RE for HyperLogLog
    re_hyper_log_log = 1 - accuracy_hll
    re_hyperloglog.append(re_hyper_log_log)

    # Calculate RE for HHH
    re_hierarchical_hh = 1- accuracy_hhh
    re_hierarchicalhh.append(re_hierarchical_hh)
  
   
speed_space_saving, speed_hyper_log_log, speed_hierarchical_hh = zip(*speed_results)
memory_space_saving, memory_hyper_log_log, memory_hierarchical_hh = zip(*memory_results)

# ------------------------------------------------------------------------------------------------------

# Plot the graphs

plt.rc('font', family='times new roman')

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(sizes, speed_space_saving, marker='o', linestyle='-', color='black', label='Space Saving')
plt.plot(sizes, speed_hyper_log_log, marker='s', linestyle='--', color='black', label='HyperLogLog')
plt.plot(sizes, speed_hierarchical_hh, marker='^', linestyle=':', color='black', label='Hierarchical Heavy Hitters')
plt.xlabel('Stream Size', fontsize=12)
plt.ylabel('Speed (seconds)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.xlim(min(sizes), max(sizes))
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(sizes, memory_space_saving, marker='o', linestyle='-', color='black', label='Space Saving')
plt.plot(sizes, memory_hyper_log_log, marker='s', linestyle='--', color='black', label='HyperLogLog')
plt.plot(sizes, memory_hierarchical_hh, marker='^', linestyle=':', color='black', label='Hierarchical Heavy Hitters')
plt.xlabel('Stream Size', fontsize=12)
plt.ylabel('Memory (bytes)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.xlim(min(sizes), max(sizes))
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(sizes, accuracy_spacesaving, marker='o', linestyle='-', color='black', label='Space Saving')
plt.plot(sizes, accuracy_hyperloglog, marker='s', linestyle='--', color='black', label='HyperLogLog')
plt.plot(sizes, accuracy_hierarchicalhh, marker='^', linestyle=':', color='black', label='Hierarchical Heavy Hitters')
plt.xlabel('Stream Size', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.xlim(min(sizes), max(sizes))
plt.ylim(0, 1.1)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(sizes, recall_spacesaving, marker='o', linestyle='-', color='black', label='Space Saving')
plt.plot(sizes, recall_hyperloglog, marker='s', linestyle='--', color='black', label='HyperLogLog')
plt.plot(sizes, recall_hierarchicalhh, marker='^', linestyle=':', color='black', label='Hierarchical Heavy Hitters')
plt.xlabel('Stream Size', fontsize=12)
plt.ylabel('Recall', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.xlim(min(sizes), max(sizes))
plt.ylim(0, 1.1)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6), dpi=100)
plt.plot(sizes, re_spacesaving, marker='o', linestyle='-', color='black', label='Space Saving')
plt.plot(sizes, re_hyperloglog, marker='s', linestyle='--', color='black', label='HyperLogLog')
plt.plot(sizes, re_hierarchicalhh, marker='^', linestyle=':', color='black', label='Hierarchical Heavy Hitters')
plt.xlabel('Stream Size', fontsize=12)
plt.ylabel('Relative Error (RE)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.xlim(min(sizes), max(sizes))
plt.ylim(0, 1.1) 
plt.tight_layout()
plt.show()
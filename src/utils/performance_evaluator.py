import time
import tracemalloc
import numpy as np
import logging
import yaml
from utils.config_loader import load_config

# Set up logging to a file
logging.basicConfig(filename="debug.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

config = load_config('config/settings.yaml')

def load_settings():
    with open('config/settings.yaml', 'r') as file:
        return yaml.safe_load(file)

settings = load_settings()
thresholds = settings['evaluation_metrics']['thresholds']

def track_execution_time(func):
    """Decorator to measure execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f'Execution time for {func.__name__}: {execution_time:.6f} seconds')
        return result, execution_time
    return wrapper

def track_memory_usage(func):
    """Decorator to measure memory usage of a function."""
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logging.info(f'Memory usage for {func.__name__}: {peak_memory} bytes')
        return result, peak_memory
    return wrapper

def calculate_path_length(path):
    """Calculates the length of the computed path."""
    if path is None or len(path) == 0:
        return 0
    return len(path)

def get_threshold(maze_size, thresholds):
    if maze_size <= 20:
        return thresholds['small']
    elif maze_size <= 50:
        return thresholds['medium']
    else:
        return thresholds['large']

def calculate_convergence_rate(iterations, maze_size):
    """Records the number of iterations needed to converge."""
    return iterations


def calculate_optimality(path, optimal_path):
    """Determines if the path found is optimal."""
    if not optimal_path:
        return 0
    return 1 if len(path) == len(optimal_path) else 0

def run(func, runs=config['evaluation_metrics']['runs'], algorithm_type=None, *args, **kwargs):
    """Executes the algorithm multiple times and records performance metrics."""
    results_list = []  # Store each run separately

    # Extract invalid maze attempts and failed paths from kwargs (but don't pass them to func)
    invalid_maze_attempts = kwargs.pop('invalid_maze_attempts', 0)
    failed_paths = kwargs.pop('failed_paths', 0)
    
    for _ in range(runs):
        # Track execution time and memory usage separately
        result, execution_time = track_execution_time(func)(*args, **kwargs)
        _, memory_usage = track_memory_usage(func)(*args, **kwargs)  # Separate call to get memory
        
        iterations = 0 # MDP algorithms
        nodes_expanded = 0 # Search algorithms
        # Handle nodes expanded tracking
        if algorithm_type == 'search':
            path, nodes_expanded = result
        elif algorithm_type == 'mdp':
            path, policy, iterations = result
            nodes_expanded = None

        path_length = calculate_path_length(path)
        optimality = calculate_optimality(path, kwargs.get('optimal_path', path))  # Use the found path as the optimal path if not provided

        # Store this run's metrics as a separate dictionary
        run_metrics = {
            'execution_times': execution_time,
            'memory_usages': memory_usage,
            'path_lengths': path_length,
            'convergence_rates': iterations if algorithm_type == "mdp" else None,
            'optimalities': optimality,
            'nodes_expanded': nodes_expanded if algorithm_type == "search" else None,
            'invalid_maze_attempts': invalid_maze_attempts,
            'failed_paths': failed_paths,
        }
        results_list.append(run_metrics)  # Append each run separately

    return results_list  # Return a list of dictionaries instead of a single aggregated dictionary



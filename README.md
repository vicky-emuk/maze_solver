# Maze Solver and Performance Evaluator

This project implements various search and MDP (Markov Decision Process) algorithms to solve mazes and evaluate their performance. The performance metrics are saved to a CSV file and visualised using Jupyter notebooks. The project includes functionalities for generating mazes, solving them using different algorithms, and analysing the performance of these algorithms.

## Modules

### `src/algorithms/search_algorithms.py`
Contains implementations of search algorithms:
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- A* Search

### `src/algorithms/mdp_algorithms.py`
Contains implementations of MDP algorithms:
- Value Iteration
- Policy Iteration

### `src/utils/config_loader.py`
Loads configuration settings from a YAML file.

### `src/utils/maze_generator.py`
Generates random mazes of specified sizes.

### `src/utils/maze_loader.py`
Loads mazes and finds start and goal positions.

### `src/utils/maze_visualiser.py`
Visualises mazes and solution paths.

### `src/utils/performance_evaluator.py`
Evaluates the performance of algorithms and saves metrics to a CSV file.

### `src/main.py`
Main entry point for the program. Handles command-line arguments and runs the selected algorithm on generated mazes.

## How to Run the Program

### Command Line Mode

1. Navigate to the `src` directory:
    ```sh
    cd /path/to/maze_solver/src
    ```

2. Run the program with the desired parameters:
    ```sh
    python main.py <maze_size> <algorithm_type> <algorithm> [runs]
    ```

    Example:
    ```sh
    python main.py 50 search dfs 5
    ```

    - `maze_size`: Size of the maze (e.g., 50 for 50x50)
    - `algorithm_type`: Type of algorithm to use (`search` or `mdp`)
    - `algorithm`: Algorithm to use (`dfs`, `bfs`, `astar`, `value`, `policy`)
    - `runs` (optional): Number of runs for performance evaluation

### Curses UI Mode

1. Run the program without command-line arguments:
    ```sh
    python main.py
    ```

2. Follow the prompts to select maze size, algorithm type, and algorithm.

## Visualising Performance

### Exploratory Analysis

1. Open the Jupyter notebook:
    ```sh
    jupyter notebook /path/to/maze_solvernotebooks/exploratory_analysis.ipynb
    ```

2. Run the cells to perform exploratory analysis on the performance metrics

### Performance Visualisation

1. Open the Jupyter notebook:
    ```sh
    jupyter notebook /path/to/maze_solver/notebooks/performance_visualisation.ipynb
    ```

2. Run the cells to generate visualisations comparing the performance of different algorithms

## Configuration

Configuration settings are stored in `config/settings.yaml`. You can modify this file to change evaluation metrics, file paths, and other settings

```
evaluation_metrics:
  runs: 5
  thresholds:
    small: 0.1
    medium: 0.5
    large: 1.0
file_paths:
  solution_path_file: ../data/mazes/solution_path.txt
  performance_metrics_file: ../data/results/performance_metrics.csv
```

## License

This project is licensed under the MIT License.
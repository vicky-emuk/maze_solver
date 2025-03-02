import os
import csv
import curses
import time
import uuid
import logging
import argparse
from datetime import datetime
from threading import Thread
from utils.config_loader import load_config
from utils.maze_loader import find_start_goal
from utils.maze_visualiser import save_solution_path, mark_solution_path, display_maze, display_maze_with_policy
from utils.performance_evaluator import run
from utils.maze_generator import generate_maze
from algorithms.search_algorithms import dfs, bfs, astar
from algorithms.mdp_algorithms import define_mdp_components, value_iteration, policy_iteration, apply_policy_to_maze

# Load configuration
config = load_config(os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml'))
thresholds = config['evaluation_metrics']['thresholds']

# ------------- Utility functions

# Determine convergence based on maze size
def get_threshold(maze_size, thresholds):
    threshold = thresholds['small'] if maze_size <= 20 else thresholds['medium'] if maze_size <= 50 else thresholds['large']
    return threshold

# Run the selected search algorithm
def run_search_algorithm(algorithm, maze, start, goal):
    algorithms = {"dfs": dfs, "bfs": bfs, "astar": astar}
    return algorithms[algorithm](maze, start, goal)

# Run the selected MDP algotithm
def run_mdp_algorithm(algorithm, maze, start):
    states, actions, transitions, rewards, gamma = define_mdp_components(maze)
    mdp_algorithms = {
        "value": value_iteration,
        "policy": policy_iteration
    }
    policy, iterations = mdp_algorithms[algorithm](states, actions, transitions, rewards, gamma)
    return apply_policy_to_maze(maze, policy, start), policy, iterations

# Add the metrics to the performance_metrics.csv file
def save_metrics_to_csv(metrics_list, maze_size, algorithm_type, algorithm, maze_id, timestamp):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'performance_metrics.csv')
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Maze ID', 'Timestamp', 'Maze Size', 'Algorithm Type', 'Algorithm', 'Run Index', 
                             'Execution Time', 'Memory Usage', 'Path Length', 'Convergence Rate', 'Optimality', 'Nodes Expanded',
                             'Invalid Maze Attempts', 'Failed Paths'])

        # Ensure metrics_list is a list of dictionaries
        if isinstance(metrics_list, dict):
            metrics_list = [metrics_list]

        for run_index, metrics in enumerate(metrics_list, start=1):
            writer.writerow([
                maze_id,
                timestamp,
                maze_size,
                algorithm_type,
                algorithm,
                run_index, 
                metrics.get('execution_times', None),
                metrics.get('memory_usages', None),
                metrics.get('path_lengths', None),
                metrics.get('convergence_rates', None),
                metrics.get('optimalities', None),
                metrics.get('nodes_expanded', None),
                metrics.get('invalid_maze_attempts', 0),
                metrics.get('failed_paths', 0)
            ])

        logging.info(f"Saved {len(metrics_list)} runs for Maze ID: {maze_id} in performance_metrics.csv")

# Generate a maze until a valid one is found
def generate_valid_maze(maze_size, maze_count):
    logging.info(f"Generating maze {maze_count}...")
    maze_size = int(maze_size)
    
    invalid_maze_attempts = 0
    while True:
        maze = generate_maze(maze_size)
        start, goal = find_start_goal(maze)
        
        if start and goal:
            break
        invalid_maze_attempts += 1
        logging.warning(f"Generated maze is invalid. Retrying... (Attempt {invalid_maze_attempts})")

    return maze, start, goal, invalid_maze_attempts

# ------------- Main functions

# Main entry point for command line mode
def main(stdscr=None):
    parser = argparse.ArgumentParser(
        description="Maze Generator and Solver",
        usage="python main.py <maze_size> <algorithm_type> <algorithm> [runs]\n"
              "Example: python main.py 50 search dfs 5"
        )
    parser.add_argument("maze_size", type=int, help="Size of the maze (e.g., 50 for 50x50)")
    parser.add_argument("algorithm_type", choices=["search", "mdp"], help="Type of algorithm to use (search or mdp)")
    parser.add_argument("algorithm", choices=["dfs", "bfs", "astar", "value", "policy"], help="Algorithm to use")
    parser.add_argument("runs", type=int, nargs="?", help="Number of runs for performance evaluation")
    try:
        args = parser.parse_args()
    except SystemExit:
        exit(1)

    # Use config value if runs argument is not provided
    runs = args.runs if args.runs is not None else config["evaluation_metrics"]["runs"]

    if args.maze_size and args.algorithm_type and args.algorithm:
        maze_size = args.maze_size
        algorithm_type = args.algorithm_type
        algorithm = args.algorithm
        maze_count = 1

        logging.info(f"Selected maze size: {maze_size}, Algorithm type: {algorithm_type}, Algorithm: {algorithm}, Runs: {runs}")
        total_invalid_maze_attempts = 0
        failed_paths = 0
        # Maze Generation Time
        maze_start_time = time.time()
        # Keep regenerating the maze until a valid path is found
        while True:
            # Generate a valid maze
            maze, start, goal, invalid_maze_attempts = generate_valid_maze(maze_size, maze_count)
            maze_end_time = time.time()
            maze_generation_time = maze_end_time - maze_start_time
            total_invalid_maze_attempts += invalid_maze_attempts
            maze_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logging.info(f"Maze ID: {maze_id}, Timestamp: {timestamp}, Start: {start}, Goal: {goal}")

            # Algorithm Execution Time
            algorithm_start_time = time.time()
            # Execute the selected algorithm
            if algorithm_type == "search":
                path, nodes_expanded = run_search_algorithm(algorithm, maze, start, goal)
            elif algorithm_type == "mdp":
                path, policy, iterations = run_mdp_algorithm(algorithm, maze, start)

            # If a valid path is found, break the loop
            if path:
                logging.info(f"Path found for Maze ID: {maze_id}, Path: {path}")
                break  # Exit the loop when a valid path is found
            else:
                logging.warning(f"No valid path found for Maze ID: {maze_id}. Regenerating maze...")
                failed_paths += 1
        # Once a valid maze and path are found, save and analyse it
        algorithm_end_time = time.time()
        algorithm_execution_time = algorithm_end_time - algorithm_start_time
        save_solution_path(path, config["file_paths"]["solution_path_file"])
        mark_solution_path(maze, path)

        # Processing time
        # Evaluate performance
        post_processing_start_time = time.time()
        if algorithm_type == "search":
            metrics_list = run(
                run_search_algorithm,
                runs=runs,  # Uses updated runs value
                algorithm_type=algorithm_type,
                algorithm=algorithm,
                maze=maze,
                start=start,
                goal=goal,
                invalid_maze_attempts=total_invalid_maze_attempts,
                failed_paths=failed_paths,
            )
        else:
            metrics_list = run(
                run_mdp_algorithm,
                runs=runs,  # Uses updated runs value
                algorithm_type=algorithm_type,
                algorithm=algorithm,
                maze=maze,
                start=start,
                invalid_maze_attempts=total_invalid_maze_attempts,
                failed_paths=failed_paths,
            )
        save_metrics_to_csv(metrics_list, maze_size, algorithm_type, algorithm, maze_id, timestamp)
        post_processing_end_time = time.time()
        post_processing_time = post_processing_end_time - post_processing_start_time
        logging.info(f"Metrics saved for Maze ID: {maze_id}, Metrics: {metrics_list}")
        total_time = maze_generation_time + algorithm_execution_time + post_processing_time
        logging.info(f"Maze Generation Time: {maze_generation_time:.4f} sec, Algorithm Time: {algorithm_execution_time:.4f} sec, Post-processing Time: {post_processing_time:.4f} sec, Total Runtime: {total_time:.4f} sec")
        
        # Display the maze with the solution path
        maze_window_title = f"Maze {maze_count}: {maze_size} - {algorithm_type} - {algorithm}"
        if algorithm_type == "search":
            display_maze(maze, maze_window_title)
        elif algorithm_type == "mdp":
            display_maze_with_policy(maze, policy, path, maze_window_title)
    else:
        # Curses UI mode
        curses.wrapper(curses_main)

# Main entry point for curses UI mode
def curses_main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    title = "Maze Generator and Solver"
    stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)

    maze_size = None
    algorithm_type = None
    algorithm = None
    maze_count = 1

    while True:
        # Maze size prompt
        if maze_size is None:
            stdscr.clear()
            stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
            maze_size_prompt = "Enter the maze size (e.g., 50 for 50x50) or type 'exit' to quit: "
            stdscr.addstr(3, 2, maze_size_prompt)
            curses.echo()
            maze_size_input = stdscr.getstr(4, 2, 10).decode('utf-8')
            curses.noecho()
            if maze_size_input.lower() == 'exit':
                stdscr.addstr(5, 2, "Exiting the program...")
                stdscr.refresh()
                curses.napms(2000)
                return
            if maze_size_input.isdigit() and int(maze_size_input) > 0:
                maze_size = maze_size_input
            else:
                stdscr.addstr(6, 2, "Invalid input. Please enter a positive number.")
                stdscr.refresh()
                curses.napms(2000)
                continue

        # Algorithm type prompt
        if algorithm_type is None:
            stdscr.clear()
            stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
            stdscr.addstr(3, 2, f"Selected maze size: {maze_size}")
            algorithm_type_prompt = "Select the algorithm type:"
            stdscr.addstr(5, 2, algorithm_type_prompt)
            algorithm_types = ["search", "mdp", "go back"]
            current_type = 0

            while True:
                for i, alg_type in enumerate(algorithm_types):
                    if i == current_type:
                        stdscr.addstr(6 + i, 4, f"> {alg_type}", curses.A_REVERSE)
                    else:
                        stdscr.addstr(6 + i, 4, f"  {alg_type}")
                key = stdscr.getch()
                if key == curses.KEY_UP and current_type > 0:
                    current_type -= 1
                elif key == curses.KEY_DOWN and current_type < len(algorithm_types) - 1:
                    current_type += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if algorithm_types[current_type] == "go back":
                        maze_size = None
                        break
                    algorithm_type = algorithm_types[current_type]
                    break

            if maze_size is None:
                continue

        # Algorithm selection prompt
        if algorithm is None:
            stdscr.clear()
            stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
            stdscr.addstr(3, 2, f"Selected maze size: {maze_size}")
            stdscr.addstr(4, 2, f"Selected algorithm type: {algorithm_type}")

            if algorithm_type == "search":
                algorithm_prompt = "Select the search algorithm:"
                algorithms = ["dfs", "bfs", "astar", "go back"]
            else:
                algorithm_prompt = "Select the MDP algorithm:"
                algorithms = ["value", "policy", "go back"]

            stdscr.addstr(5, 2, algorithm_prompt)
            current_alg = 0

            while True:
                for i, alg in enumerate(algorithms):
                    if i == current_alg:
                        stdscr.addstr(6 + i, 4, f"> {alg}", curses.A_REVERSE)
                    else:
                        stdscr.addstr(6 + i, 4, f"  {alg}")
                key = stdscr.getch()
                if key == curses.KEY_UP and current_alg > 0:
                    current_alg -= 1
                elif key == curses.KEY_DOWN and current_alg < len(algorithms) - 1:
                    current_alg += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if algorithms[current_alg] == "go back":
                        algorithm_type = None
                        break
                    algorithm = algorithms[current_alg]
                    break

            if algorithm_type is None:
                continue
        
        logging.info(f'Selected maze size: {maze_size}, Algorithm type: {algorithm_type}, Algorithm: {algorithm}')
        # Track invalid mazes & failed paths
        total_invalid_maze_attempts = 0
        failed_paths = 0
        
        # Generate a valid maze
        stdscr.clear()
        stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
        message = f"Generating Maze {maze_count}. Note: This may take a while for large mazes."
        stdscr.addstr(9, 2, message)
        stdscr.refresh()
        logging.info(message)
        maze_start_time = time.time()
        maze, start, goal, invalid_maze_attempts = generate_valid_maze(maze_size, maze_count)
        maze_end_time = time.time()
        maze_generation_time = maze_end_time - maze_start_time
        total_invalid_maze_attempts += invalid_maze_attempts
        maze_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        logging.info(f'Maze ID: {maze_id}, Timestamp: {timestamp}, Start: {start}, Goal: {goal}')

        maze_window_title = f"Maze {maze_count}: {maze_size} - {algorithm_type} - {algorithm}"
        algorithm_start_time = time.time()
        # Execute the selected algorithm
        if algorithm_type == "search":
            path, nodes_expanded = run_search_algorithm(algorithm, maze, start, goal)
        elif algorithm_type == "mdp":
            path, policy, iterations = run_mdp_algorithm(algorithm, maze, start)
        if path:
            algorithm_end_time = time.time()
            algorithm_execution_time = algorithm_end_time - algorithm_start_time
            save_solution_path(path, config['file_paths']['solution_path_file'])
            mark_solution_path(maze, path)
            logging.info(f'Path found for Maze ID: {maze_id}, Path: {path}')

            post_processing_start_time = time.time()
            # Evaluate performance
            if algorithm_type == "search":
                metrics_list = run(run_search_algorithm, 
                            runs=config['evaluation_metrics']['runs'], 
                            algorithm_type=algorithm_type,
                            algorithm=algorithm, maze=maze, start=start, goal=goal, 
                            invalid_maze_attempts=total_invalid_maze_attempts, failed_paths=failed_paths)
            else:
                metrics_list = run(run_mdp_algorithm, 
                            runs=config['evaluation_metrics']['runs'], 
                            algorithm_type=algorithm_type,
                            algorithm=algorithm, maze=maze, start=start, 
                            invalid_maze_attempts=total_invalid_maze_attempts, failed_paths=failed_paths)
            post_processing_end_time = time.time()
            post_processing_time = post_processing_end_time - post_processing_start_time
            # Save metrics
            save_metrics_to_csv(metrics_list, maze_size, algorithm_type, algorithm, maze_id, timestamp)
            logging.info(f'Metrics saved for Maze ID: {maze_id}, Metrics: {metrics_list}')
            
            stdscr.clear()
            stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
            # Display maze generated message
            message = f"Maze {maze_count} generated. Please wait for the maze to be displayed."
            stdscr.addstr(9, 2, message)
            stdscr.refresh()
            logging.info(message)
            total_time = maze_generation_time + algorithm_execution_time + post_processing_time
            logging.info(f"Maze Generation Time: {maze_generation_time:.4f} sec, Algorithm Time: {algorithm_execution_time:.4f} sec, Post-processing Time: {post_processing_time:.4f} sec, Total Runtime: {total_time:.4f} sec")
            # Display the maze with the solution path
            if algorithm_type == "search":
                Thread(target=display_maze, args=(maze, maze_window_title)).start()
            elif algorithm_type == "mdp":
                thread = Thread(target=display_maze_with_policy, args=(maze, policy, path, maze_window_title))
                thread.daemon = True  # Ensure thread does not block execution
                thread.start()
                thread.join(timeout=0.1)
        else:
            logging.warning(f'No valid path found for Maze ID: {maze_id}')
            failed_paths += 1
            continue

        # Increment maze count after each run
        maze_count += 1

        # Prompt user for next action
        options = ["Run with same values", "New input", "Exit"]
        current_option = 0

        while True:
            stdscr.clear()
            stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
            stdscr.addstr(3, 2, f"Selected maze size: {maze_size}")
            stdscr.addstr(4, 2, f"Selected algorithm type: {algorithm_type}")
            stdscr.addstr(5, 2, f"Selected algorithm: {algorithm}")
            stdscr.addstr(7, 2, "Select an option:")

            for i, option in enumerate(options):
                if i == current_option:
                    stdscr.addstr(8 + i, 4, f"> {option}", curses.A_REVERSE)
                else:
                    stdscr.addstr(8 + i, 4, f"  {option}")

            key = stdscr.getch()
            if key == curses.KEY_UP and current_option > 0:
                current_option -= 1
            elif key == curses.KEY_DOWN and current_option < len(options) - 1:
                current_option += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if options[current_option] == "Run with same values":
                    break
                elif options[current_option] == "New input":
                    maze_size = None
                    algorithm_type = None
                    algorithm = None
                    maze_count = 1
                    break
                elif options[current_option] == "Exit":
                    return

if __name__ == "__main__":
    main()
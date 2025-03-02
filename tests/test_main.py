import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import curses

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import main, generate_valid_maze, run_search_algorithm, run_mdp_algorithm

class TestMain(unittest.TestCase):

    @patch('main.curses.wrapper')
    def test_main_flow(self, mock_wrapper):
        # Mock the curses window
        mock_stdscr = MagicMock()
        mock_wrapper.return_value = mock_stdscr

        # Simulate user inputs
        inputs = [
            '50',  # Maze size
            curses.KEY_DOWN, curses.KEY_ENTER,  # Select "search"
            curses.KEY_DOWN, curses.KEY_ENTER,  # Select "dfs"
            curses.KEY_DOWN, curses.KEY_ENTER,  # Select "Run with same values"
            'exit'  # Exit
        ]
        mock_stdscr.getch.side_effect = inputs

        # Run the main function
        curses.wrapper(main)

        # Verify that the main function ran without errors
        mock_stdscr.addstr.assert_any_call(1, unittest.mock.ANY, unittest.mock.ANY)

    @patch('main.dfs')
    @patch('main.bfs')
    @patch('main.astar')
    def test_run_search_algorithm(self, mock_astar, mock_bfs, mock_dfs):
        # Mock the search algorithms
        mock_dfs.return_value = [(0, 0), (0, 1), (0, 2)]
        mock_bfs.return_value = [(0, 0), (0, 1), (0, 2)]
        mock_astar.return_value = [(0, 0), (0, 1), (0, 2)]

        # Test DFS
        path = run_search_algorithm('dfs', [['S', 'P', 'G']], (0, 0), (0, 2))
        self.assertEqual(path, [(0, 0), (0, 1), (0, 2)])

        # Test BFS
        path = run_search_algorithm('bfs', [['S', 'P', 'G']], (0, 0), (0, 2))
        self.assertEqual(path, [(0, 0), (0, 1), (0, 2)])

        # Test A*
        path = run_search_algorithm('astar', [['S', 'P', 'G']], (0, 0), (0, 2))
        self.assertEqual(path, [(0, 0), (0, 1), (0, 2)])

    @patch('main.value_iteration')
    @patch('main.policy_iteration')
    @patch('main.apply_policy_to_maze')
    def test_run_mdp_algorithm(self, mock_apply_policy_to_maze, mock_policy_iteration, mock_value_iteration):
        # Mock the MDP algorithms
        mock_value_iteration.return_value = {'policy': 'value'}
        mock_policy_iteration.return_value = {'policy': 'policy'}
        mock_apply_policy_to_maze.return_value = [(0, 0), (0, 1), (0, 2)], {'policy': 'value'}

        # Test Value Iteration
        path, policy = run_mdp_algorithm('value', [['S', 'P', 'G']], (0, 0))
        self.assertEqual(run_mdp_algorithm('value', [['S', 'P', 'G']], (0, 0)), ([(0, 0), (0, 1), (0, 2)], {'policy': 'value'}))

        # Test Policy Iteration
        path, policy = run_mdp_algorithm('policy', [['S', 'P', 'G']], (0, 0))
        self.assertEqual(path, [(0, 0), (0, 1), (0, 2)])
        self.assertEqual(policy, {'policy': 'value'})

    @patch('main.curses.wrapper')
    def test_invalid_maze_size(self, mock_wrapper):
        # Mock the curses window
        mock_stdscr = MagicMock()
        mock_wrapper.return_value = mock_stdscr

        # Simulate user inputs
        inputs = [
            '-1',  # Invalid maze size
        ]
        mock_stdscr.getstr.side_effect = inputs

        # Run the main function
        curses.wrapper(main)

        # Verify that the main function handled the invalid input
        self.assertTrue(mock_stdscr.addstr.called)

    @patch('main.curses.wrapper')
    def test_user_exits_early(self, mock_wrapper):
        # Mock the curses window
        mock_stdscr = MagicMock()
        mock_wrapper.return_value = mock_stdscr

        # Simulate user inputs
        inputs = [
            'exit'  # Exit early
        ]
        mock_stdscr.getstr.side_effect = inputs

        # Run the main function
        curses.wrapper(main)

        # Verify that the main function handled the early exit
        self.assertTrue(mock_stdscr.addstr.called)

if __name__ == '__main__':
    unittest.main()

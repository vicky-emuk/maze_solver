import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from utils.maze_loader import find_start_goal
from utils.maze_visualiser import display_maze, display_maze_with_policy
from utils.maze_generator import generate_maze

class TestMazeGeneration(unittest.TestCase):

    @patch('utils.maze_visualiser.Tk')
    def test_display_maze(self, mock_tk):
        # Mock the Tkinter window
        mock_window = MagicMock()
        mock_tk.return_value = mock_window

        # Create a simple maze
        maze = [
            ['S', 'P', 'G'],
            ['P', 'w', 'P'],
            ['P', 'P', 'P']
        ]

        # Display the maze
        display_maze(maze, "DFS Maze Display")

        # Verify that the window was created and displayed
        self.assertTrue(mock_window.mainloop.called)

    @patch('utils.maze_visualiser.Tk')
    def test_display_maze_with_policy(self, mock_tk):
        # Mock the Tkinter window
        mock_window = MagicMock()
        mock_tk.return_value = mock_window

        # Create a simple maze and policy
        maze = [
            ['S', 'P', 'G'],
            ['P', 'w', 'P'],
            ['P', 'P', 'P']
        ]
        policy = {
            (0, 0): 'R',
            (0, 1): 'R',
            (0, 2): 'D',
            (1, 2): 'D',
            (2, 2): 'L',
            (2, 1): 'L',
            (2, 0): 'U',
            (1, 0): 'R' 
        }
        path = [(0, 0), (0, 1), (0, 2)]

        # Display the maze with policy
        display_maze_with_policy(maze, policy, path, "MDP Maze Display")

        # Verify that the window was created and displayed
        self.assertTrue(mock_window.mainloop.called)

if __name__ == '__main__':
    unittest.main()

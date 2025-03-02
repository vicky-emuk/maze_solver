import unittest
import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from utils.maze_loader import find_start_goal, find_neighbours

class TestMazeLoader(unittest.TestCase):

    def setUp(self):
        self.maze = [
            ['S', 'P', 'P', 'w', 'G'],
            ['w', 'w', 'P', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'w', 'w', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P']
        ]

    def test_find_start_goal(self):
        start, goal = find_start_goal(self.maze)
        self.assertEqual(start, (0, 0))
        self.assertEqual(goal, (0, 4))

    def test_find_neighbours(self):
        neighbours = find_neighbours(self.maze, (2, 2))
        expected_neighbours = [(1, 2), (2, 1), (2, 3)]
        self.assertCountEqual(neighbours, expected_neighbours)

    def test_invalid_maze(self):
        maze = [
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'P', 'P', 'P', 'P']
        ]
        start, goal = find_start_goal(maze)
        self.assertIsNone(start)
        self.assertIsNone(goal)

    def test_different_maze_sizes(self):
        maze_small = [['S', 'G']]
        start, goal = find_start_goal(maze_small)
        self.assertEqual(start, (0, 0))
        self.assertEqual(goal, (0, 1))

        maze_large = [['P' for _ in range(50)] for _ in range(50)]
        maze_large[0][0] = 'S'
        maze_large[49][49] = 'G'
        start, goal = find_start_goal(maze_large)
        self.assertEqual(start, (0, 0))
        self.assertEqual(goal, (49, 49))

if __name__ == '__main__':
    unittest.main()

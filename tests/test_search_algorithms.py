import unittest
import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from algorithms.search_algorithms import dfs, bfs, astar
from utils.maze_loader import find_start_goal

class TestSearchAlgorithms(unittest.TestCase):

    def setUp(self):
        self.maze = [
            ['S', 'P', 'P', 'w', 'G'],
            ['w', 'w', 'P', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'w', 'w', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P']
        ]
        self.start, self.goal = find_start_goal(self.maze)

    def test_dfs(self):
        path = dfs(self.maze, self.start, self.goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.start)
        self.assertEqual(path[-1], self.goal)

    def test_bfs(self):
        path = bfs(self.maze, self.start, self.goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.start)
        self.assertEqual(path[-1], self.goal)

    def test_astar(self):
        path = astar(self.maze, self.start, self.goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.start)
        self.assertEqual(path[-1], self.goal)

    def test_no_path(self):
        maze = [
            ['S', 'w', 'w', 'w', 'G'],
            ['w', 'w', 'w', 'w', 'w'],
            ['w', 'w', 'w', 'w', 'w'],
            ['w', 'w', 'w', 'w', 'w'],
            ['w', 'w', 'w', 'w', 'w']
        ]
        start, goal = find_start_goal(maze)
        self.assertIsNone(dfs(maze, start, goal))
        self.assertIsNone(bfs(maze, start, goal))
        self.assertIsNone(astar(maze, start, goal))

    def test_multiple_paths(self):
        maze = [
            ['S', 'P', 'P', 'P', 'G'],
            ['P', 'w', 'w', 'P', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'w', 'w', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P']
        ]
        start, goal = find_start_goal(maze)
        path_dfs = dfs(maze, start, goal)
        path_bfs = bfs(maze, start, goal)
        path_astar = astar(maze, start, goal)
        self.assertIsNotNone(path_dfs)
        self.assertIsNotNone(path_bfs)
        self.assertIsNotNone(path_astar)
        self.assertEqual(path_dfs[0], start)
        self.assertEqual(path_bfs[0], start)
        self.assertEqual(path_astar[0], start)
        self.assertEqual(path_dfs[-1], goal)
        self.assertEqual(path_bfs[-1], goal)
        self.assertEqual(path_astar[-1], goal)

    def test_large_maze(self):
        maze = [['P' for _ in range(50)] for _ in range(50)]
        maze[0][0] = 'S'
        maze[49][49] = 'G'
        start, goal = find_start_goal(maze)
        path_dfs = dfs(maze, start, goal)
        path_bfs = bfs(maze, start, goal)
        path_astar = astar(maze, start, goal)
        self.assertIsNotNone(path_dfs)
        self.assertIsNotNone(path_bfs)
        self.assertIsNotNone(path_astar)
        self.assertEqual(path_dfs[0], start)
        self.assertEqual(path_bfs[0], start)
        self.assertEqual(path_astar[0], start)
        self.assertEqual(path_dfs[-1], goal)
        self.assertEqual(path_bfs[-1], goal)
        self.assertEqual(path_astar[-1], goal)

if __name__ == '__main__':
    unittest.main()

import unittest
import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from algorithms.mdp_algorithms import define_mdp_components, value_iteration, policy_iteration, apply_policy_to_maze
from utils.maze_loader import find_start_goal

class TestMDPAlgorithms(unittest.TestCase):

    def setUp(self):
        self.maze = [
            ['S', 'P', 'P', 'w', 'G'],
            ['w', 'w', 'P', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'w', 'w', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P']
        ]
        self.start, self.goal = find_start_goal(self.maze)
        self.states, self.actions, self.transitions, self.rewards, self.gamma = define_mdp_components(self.maze)

    def test_value_iteration(self):
        policy = value_iteration(self.states, self.actions, self.transitions, self.rewards, self.gamma)
        self.assertIsNotNone(policy)
        path = apply_policy_to_maze(self.maze, policy, self.start)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], self.start)
        self.assertEqual(path[-1], self.goal)

    def test_policy_iteration(self):
        policy = policy_iteration(self.states, self.actions, self.transitions, self.rewards, self.gamma)
        self.assertIsNotNone(policy)
        path = apply_policy_to_maze(self.maze, policy, self.start)
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
        states, actions, transitions, rewards, gamma = define_mdp_components(maze)
        policy = value_iteration(states, actions, transitions, rewards, gamma)
        path = apply_policy_to_maze(maze, policy, start)
        self.assertIsNone(path)

    def test_goal_state(self):
        self.assertIn(self.goal, self.states)
        for action in self.actions:
            self.assertIn(action, self.transitions[self.goal])
            self.assertEqual(self.rewards[self.goal][action], 0)

    def test_different_gamma(self):
        gamma_values = [0.5, 0.9, 0.99]
        for gamma in gamma_values:
            policy = value_iteration(self.states, self.actions, self.transitions, self.rewards, gamma)
            self.assertIsNotNone(policy)
            path = apply_policy_to_maze(self.maze, policy, self.start)
            self.assertIsNotNone(path)
            self.assertEqual(path[0], self.start)
            self.assertEqual(path[-1], self.goal)

    def test_multiple_optimal_policies(self):
        maze = [
            ['S', 'P', 'P', 'P', 'G'],
            ['P', 'w', 'w', 'P', 'P'],
            ['P', 'P', 'P', 'P', 'P'],
            ['P', 'w', 'w', 'w', 'P'],
            ['P', 'P', 'P', 'P', 'P']
        ]
        start, goal = find_start_goal(maze)
        states, actions, transitions, rewards, gamma = define_mdp_components(maze)
        policy_value = value_iteration(states, actions, transitions, rewards, gamma)
        policy_policy = policy_iteration(states, actions, transitions, rewards, gamma)
        path_value = apply_policy_to_maze(maze, policy_value, start)
        path_policy = apply_policy_to_maze(maze, policy_policy, start)
        self.assertIsNotNone(path_value)
        self.assertIsNotNone(path_policy)
        self.assertEqual(path_value[0], start)
        self.assertEqual(path_policy[0], start)
        self.assertEqual(path_value[-1], goal)
        self.assertEqual(path_policy[-1], goal)

if __name__ == '__main__':
    unittest.main()

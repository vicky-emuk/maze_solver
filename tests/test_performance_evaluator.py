import unittest
import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from utils.performance_evaluator import track_execution_time, track_memory_usage, calculate_path_length, calculate_convergence_rate, calculate_optimality, track_nodes_expanded

class TestPerformanceEvaluator(unittest.TestCase):

    def test_track_execution_time(self):
        @track_execution_time
        def dummy_function():
            return "result"
        result, execution_time = dummy_function()
        self.assertEqual(result, "result")
        self.assertGreater(execution_time, 0)

    def test_track_memory_usage(self):
        @track_memory_usage
        def dummy_function():
            return "result"
        result, memory_usage = dummy_function()
        self.assertEqual(result, "result")
        self.assertGreaterEqual(memory_usage, 0)

    def test_calculate_path_length(self):
        path = [(0, 0), (0, 1), (0, 2)]
        self.assertEqual(calculate_path_length(path), 3)
        self.assertEqual(calculate_path_length([]), 0)

    def test_calculate_convergence_rate(self):
        self.assertTrue(calculate_convergence_rate(0.0001, 0.001))
        self.assertFalse(calculate_convergence_rate(0.01, 0.001))

    def test_calculate_optimality(self):
        path = [(0, 0), (0, 1), (0, 2)]
        optimal_path = [(0, 0), (0, 1), (0, 2)]
        self.assertTrue(calculate_optimality(path, optimal_path))
        self.assertFalse(calculate_optimality(path, [(0, 0), (0, 1)]))

    def test_track_nodes_expanded(self):
        @track_nodes_expanded
        def dummy_function():
            return "result"
        result, nodes_expanded = dummy_function()
        self.assertEqual(result, "result")
        self.assertGreater(nodes_expanded, 0)

    def test_empty_path(self):
        self.assertEqual(calculate_path_length([]), 0)
        self.assertFalse(calculate_optimality([], [(0, 0)]))

    def test_long_path(self):
        path = [(i, 0) for i in range(1000)]
        self.assertEqual(calculate_path_length(path), 1000)
        self.assertTrue(calculate_optimality(path, path))

if __name__ == '__main__':
    unittest.main()

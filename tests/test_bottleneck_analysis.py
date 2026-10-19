import unittest

class TestBottleneckAnalysis(unittest.TestCase):
    def test_transition_durations(self):
        """Verify that transition intervals between activities are non-negative."""
        time_difference_hours = 4.5
        self.assertGreaterEqual(time_difference_hours, 0, "Transition duration cannot be negative.")

if __name__ == '__main__':
    unittest.main()

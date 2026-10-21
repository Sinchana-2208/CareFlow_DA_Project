import unittest

import pandas as pd

from src.activity_transition_analysis import analyze_activity_transitions


class TestActivityTransitionAnalysis(unittest.TestCase):

    def setUp(self):
        self.events = pd.DataFrame({
            "case_id": ["A", "A", "A", "B", "B"],
            "activity": [
                "Registration",
                "Triage",
                "Treatment",
                "Registration",
                "Triage",
            ],
            "timestamp": [
                "2026-01-01 09:00:00",
                "2026-01-01 09:15:00",
                "2026-01-01 10:00:00",
                "2026-01-02 08:00:00",
                "2026-01-02 08:20:00",
            ],
        })

    def test_counts_repeated_transitions(self):
        result = analyze_activity_transitions(self.events)
        row = result[
            (result["from_activity"] == "Registration")
            & (result["to_activity"] == "Triage")
        ].iloc[0]
        self.assertEqual(row["transition_count"], 2)

    def test_calculates_elapsed_time(self):
        result = analyze_activity_transitions(self.events)
        row = result[
            (result["from_activity"] == "Registration")
            & (result["to_activity"] == "Triage")
        ].iloc[0]
        self.assertAlmostEqual(row["average_elapsed_minutes"], 17.5)
        self.assertAlmostEqual(row["median_elapsed_minutes"], 17.5)

    def test_does_not_connect_different_cases(self):
        result = analyze_activity_transitions(self.events)
        pairs = list(zip(result["from_activity"], result["to_activity"]))
        self.assertNotIn(("Treatment", "Registration"), pairs)

    def test_transition_percentages_total_100(self):
        result = analyze_activity_transitions(self.events)
        self.assertAlmostEqual(result["transition_percentage"].sum(), 100.0)

    def test_empty_input_returns_empty_summary(self):
        empty = pd.DataFrame(columns=["case_id", "activity", "timestamp"])
        result = analyze_activity_transitions(empty)
        self.assertTrue(result.empty)
        self.assertIn("transition_count", result.columns)

    def test_missing_required_column_raises_error(self):
        invalid = pd.DataFrame({"case_id": ["A"], "activity": ["Triage"]})
        with self.assertRaises(ValueError):
            analyze_activity_transitions(invalid)


if __name__ == "__main__":
    unittest.main()

"""
Automated tests for CareFlow transition-time analysis.

These tests use synthetic timestamps and do not require
the actual project dataset.
"""

import unittest

import pandas as pd

from src.transition_time_analysis import calculate_transition_times


class TestTransitionTimeAnalysis(unittest.TestCase):

    def setUp(self):
        """Create a small synthetic event log for testing."""

        self.event_log = pd.DataFrame({
            "case_id": [
                "CASE_001",
                "CASE_001",
                "CASE_001",
                "CASE_002",
                "CASE_002",
            ],
            "activity": [
                "Registration",
                "Triage",
                "Blood Test",
                "Registration",
                "Triage",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01 08:00:00",
                    "2026-01-01 08:15:00",
                    "2026-01-01 08:45:00",
                    "2026-01-02 09:00:00",
                    "2026-01-02 10:00:00",
                ],
                utc=True,
            ),
        })

    def test_transition_count(self):
        """Each case's first event should have no preceding transition."""

        transitions = calculate_transition_times(self.event_log)

        # CASE_001 has 3 events and 2 transitions.
        # CASE_002 has 2 events and 1 transition.
        self.assertEqual(len(transitions), 3)

    def test_elapsed_time_calculation(self):
        """Elapsed minutes should match the known timestamps."""

        transitions = calculate_transition_times(self.event_log)

        case_001 = transitions[
            transitions["case_id"] == "CASE_001"
        ]

        case_002 = transitions[
            transitions["case_id"] == "CASE_002"
        ]

        self.assertEqual(
            case_001["elapsed_minutes"].tolist(),
            [15.0, 30.0],
        )

        self.assertEqual(
            case_002["elapsed_minutes"].tolist(),
            [60.0],
        )

    def test_transition_labels(self):
        """Each transition should identify the two activities."""

        transitions = calculate_transition_times(self.event_log)

        expected_transitions = [
            "Registration -> Triage",
            "Triage -> Blood Test",
            "Registration -> Triage",
        ]

        self.assertEqual(
            transitions["transition"].tolist(),
            expected_transitions,
        )

    def test_no_transition_between_different_cases(self):
        """Events from separate cases must not be connected."""

        transitions = calculate_transition_times(self.event_log)

        self.assertEqual(
            transitions["case_id"].tolist(),
            [
                "CASE_001",
                "CASE_001",
                "CASE_002",
            ],
        )

        self.assertNotIn(
            "Blood Test -> Registration",
            transitions["transition"].tolist(),
        )


if __name__ == "__main__":
    unittest.main()
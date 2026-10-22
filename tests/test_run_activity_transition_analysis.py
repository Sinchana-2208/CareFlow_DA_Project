import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestActivityTransitionRunner(unittest.TestCase):
    def test_runner_creates_transition_summary_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "test_events.xlsx"
            output_file = temp_path / "transition_summary.csv"

            events = pd.DataFrame(
                {
                    "case_id": ["P1", "P1", "P2", "P2"],
                    "event_index": [1, 2, 1, 2],
                    "activity": [
                        "Registration",
                        "Triage",
                        "Registration",
                        "Treatment",
                    ],
                    "timestamp": [
                        "2026-01-01 09:00:00",
                        "2026-01-01 09:10:00",
                        "2026-01-02 10:00:00",
                        "2026-01-02 10:30:00",
                    ],
                }
            )

            with pd.ExcelWriter(input_file) as writer:
                events.to_excel(
                    writer,
                    sheet_name="Event Log Visual",
                    index=False,
                )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "src.run_activity_transition_analysis",
                    "--input",
                    str(input_file),
                    "--sheet",
                    "Event Log Visual",
                    "--output",
                    str(output_file),
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=60,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=f"Runner failed:\n{result.stdout}\n{result.stderr}",
            )
            self.assertTrue(output_file.exists())

            summary = pd.read_csv(output_file)

            self.assertEqual(len(summary), 2)
            self.assertEqual(
                set(summary["from_activity"]),
                {"Registration"},
            )
            self.assertEqual(
                set(summary["to_activity"]),
                {"Triage", "Treatment"},
            )
            self.assertEqual(
                int(summary["transition_count"].sum()),
                2,
            )


if __name__ == "__main__":
    unittest.main()


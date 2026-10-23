import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestWorkflowReportRunner(unittest.TestCase):
    def test_runner_creates_all_report_csv_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "test_events.xlsx"
            output_dir = temp_path / "outputs"

            events = pd.DataFrame(
                {
                    "case_id": ["P1", "P1", "P1", "P2", "P2"],
                    "event_index": [1, 2, 3, 1, 2],
                    "activity": [
                        "Registration",
                        "Triage",
                        "Treatment",
                        "Registration",
                        "Triage",
                    ],
                    "timestamp": [
                        "2026-01-01 09:00:00",
                        "2026-01-01 09:10:00",
                        "2026-01-01 09:30:00",
                        "2026-01-02 10:00:00",
                        "2026-01-02 10:15:00",
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
                    "src.run_workflow_report",
                    "--input",
                    str(input_file),
                    "--sheet",
                    "Event Log Visual",
                    "--output-dir",
                    str(output_dir),
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

            overview_file = output_dir / "workflow_overview.csv"
            variants_file = output_dir / "pathway_variants.csv"
            transitions_file = output_dir / "activity_transition_summary.csv"

            self.assertTrue(overview_file.exists())
            self.assertTrue(variants_file.exists())
            self.assertTrue(transitions_file.exists())

            overview = pd.read_csv(overview_file)
            variants = pd.read_csv(variants_file)
            transitions = pd.read_csv(transitions_file)

            metrics = overview.set_index("metric")["value"]

            self.assertEqual(int(metrics["valid_event_records"]), 5)
            self.assertEqual(int(metrics["patient_cases"]), 2)
            self.assertEqual(int(metrics["unique_activities"]), 3)
            self.assertEqual(int(metrics["unique_pathway_variants"]), 2)
            self.assertEqual(int(metrics["unique_activity_transitions"]), 2)

            self.assertEqual(int(variants["case_count"].sum()), 2)
            self.assertEqual(int(transitions["transition_count"].sum()), 3)


if __name__ == "__main__":
    unittest.main()


import json
from pathlib import Path
import sys
import tempfile
import unittest

# Resolve workspace paths
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from audit_event_log import audit_event_log  # noqa: E402
from run_pm4py_discovery import export_native_artifacts, load_events  # noqa: E402


class TestCareflowPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = ROOT_DIR / "careflow_data"
        cls.log_path = cls.data_dir / "clean_event_log.csv"
        cls.dbt_root = ROOT_DIR / "careflow_dbt"

    def test_audit_passes_for_current_synthetic_log(self):
        metrics = audit_event_log(self.log_path)
        self.assertTrue(metrics.get("passed"))
        self.assertEqual(
            (metrics.get("case_count"), metrics.get("xray_to_triage_cases")),
            (500, 200),
        )

    def test_process_discovery_native_exports_are_created(self):
        log_records = load_events(self.log_path)
        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_path = Path(tmp_dir)
            stats = export_native_artifacts(log_records, dest_path)

            self.assertEqual(stats["event_count"], 3900)
            self.assertEqual(stats["process_variant_count"], 2)
            self.assertAlmostEqual(stats["xray_to_triage_rate_percent"], 40.0, places=1)

            expected_csvs = {
                "native_directly_follows.csv",
                "native_process_variants.csv",
                "baseline_conformance_results.csv",
            }
            for filename in expected_csvs:
                self.assertTrue((dest_path / filename).is_file(), f"Missing file: {filename}")

            summary_doc = json.loads((dest_path / "process_discovery_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary_doc.get("case_count"), 500)

    def test_dbt_project_and_model_files_exist(self):
        for config_file in ("dbt_project.yml", "profiles.yml.example"):
            self.assertTrue((self.dbt_root / config_file).is_file(), f"{config_file} not found")

        required_models = {
            "stg_careflow__events.sql",
            "int_careflow__ordered_events.sql",
            "int_careflow__event_transitions.sql",
            "fct_patient_cases.sql",
            "fct_transition_bottlenecks.sql",
            "fct_triage_loopbacks.sql",
            "fct_process_variants.sql",
            "fct_conformance_results.sql",
        }
        discovered_models = {item.name for item in (self.dbt_root / "models").glob("**/*.sql")}
        self.assertTrue(required_models.issubset(discovered_models))


if __name__ == "__main__":
    unittest.main(verbosity=2)

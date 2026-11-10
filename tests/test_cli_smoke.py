"""In-process CLI smoke tests: every script must run end-to-end on the synthetic log."""
import runpy
import sys

import pytest

SCRIPTS = "scripts"


def run_cli(project_root, script, argv):
    old = sys.argv
    sys.argv = [script, *argv]
    try:
        runpy.run_path(str(project_root / SCRIPTS / script), run_name="__main__")
    except SystemExit as exit_:
        return exit_.code or 0
    finally:
        sys.argv = old
    return 0


CSV = "careflow_data/clean_event_log.csv"


def test_audit_cli(project_root, tmp_path):
    assert run_cli(project_root, "audit_event_log.py", [str(project_root / CSV), "--json-out", str(tmp_path / "a.json")]) == 0
    assert (tmp_path / "a.json").is_file()


def test_discovery_cli(project_root, tmp_path):
    assert run_cli(project_root, "run_pm4py_discovery.py", [str(project_root / CSV), "--output-dir", str(tmp_path)]) == 0
    assert (tmp_path / "native_process_variants.csv").is_file()


def test_week3_cli(project_root, tmp_path):
    assert run_cli(project_root, "week3_bottleneck_metrics.py", ["--input", str(project_root / CSV), "--output-dir", str(tmp_path)]) == 0
    assert (tmp_path / "week3_kpi_summary.json").is_file()
    assert run_cli(project_root, "week3_bottleneck_metrics.py", ["--input", str(tmp_path / "nope.csv"), "--output-dir", str(tmp_path)]) == 1


def test_week4_cli(project_root, tmp_path):
    assert run_cli(project_root, "week4_conformance.py", ["--input", str(project_root / CSV), "--output-dir", str(tmp_path)]) == 0
    assert (tmp_path / "week4_kpi_summary.json").is_file()


def test_pm4py_conformance_cli(project_root, tmp_path):
    pytest.importorskip("pm4py")
    run_cli(project_root, "run_pm4py_conformance.py", ["--input", str(project_root / CSV), "--output-dir", str(tmp_path)])
    assert (tmp_path / "pm4py_conformance_summary.json").is_file()


def test_dashboard_cli(project_root, tmp_path):
    run_cli(project_root, "build_dashboard.py", ["--input", str(project_root / CSV), "--output", str(tmp_path / "d.html")])
    assert (tmp_path / "d.html").stat().st_size > 10_000


def test_bi_export_cli(project_root, tmp_path):
    run_cli(project_root, "export_bi_datasets.py", ["--data-dir", str(project_root / "careflow_data"), "--output-dir", str(tmp_path)])
    assert (tmp_path / "bi_kpis.csv").is_file()


def test_loader_dry_run_in_process(project_root):
    assert run_cli(project_root, "load_synthetic_to_bigquery.py", ["--dry-run"]) == 0

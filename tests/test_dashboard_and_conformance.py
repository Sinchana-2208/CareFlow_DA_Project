import json
import pandas as pd
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "careflow_data" / "clean_event_log.csv"


def test_dashboard_case_builder_matches_known_rates():
    from build_dashboard import build_cases
    cases = build_cases(DATA)
    assert len(cases) == 500
    assert sum(c["loop"] for c in cases) == 200
    assert sum(c["conf"] for c in cases) == 300


def test_dashboard_html_is_written(tmp_path):
    from build_dashboard import TEMPLATE, build_cases
    out = tmp_path / "d.html"
    out.write_text(TEMPLATE.replace("__DATA__", json.dumps(build_cases(DATA))), encoding="utf-8")
    assert "CareFlow" in out.read_text(encoding="utf-8")
    assert "__DATA__" not in out.read_text(encoding="utf-8")


def test_pm4py_alignment_conformance(tmp_path):
    pytest.importorskip("pm4py")
    from run_pm4py_conformance import run
    summary = run(DATA, tmp_path)
    assert summary["cases"] == 500
    assert summary["baseline_conforming_cases"] == 300
    assert (tmp_path / "pm4py_alignment_by_case.csv").exists()


def test_bi_export_labels_have_no_blank_reason(tmp_path):
    from export_bi_datasets import export
    kpis = export(ROOT / "careflow_data", tmp_path)
    cases = pd.read_csv(tmp_path / "bi_cases.csv")
    assert kpis["Loopback_Rate_Percent"] == 40.0
    assert cases["Loopback_Reason"].notna().all()
    assert set(cases["Conformance_Status"]) == {"Conforming", "Deviating"}

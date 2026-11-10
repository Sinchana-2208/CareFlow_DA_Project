import pandas as pd
import pytest

from careflow_analysis import (analyze_csv, build_transition_summary, main,
                               summarize_loopbacks_by_group, validate_event_log)


def log(rows):
    return pd.DataFrame(rows, columns=["Case_ID", "Activity_Name", "Timestamp", "Arrival_Shift"])


GOOD = [
    ("C1", "Registration", "2026-01-01 09:00", "Morning"),
    ("C1", "X-Ray", "2026-01-01 09:10", "Morning"),
    ("C1", "Triage", "2026-01-01 09:25", "Morning"),
    ("C2", "Registration", "2026-01-01 20:00", "Night"),
    ("C2", "Discharge", "2026-01-01 20:40", "Night"),
]


def test_validate_counts():
    out = validate_event_log(log(GOOD))
    assert out["case_count"] == 2 and out["event_count"] == 5 and out["passed"]


def test_whitespace_is_trimmed_before_duplicate_check():
    rows = [("A", "Triage", "2026-01-01", "x"), (" A ", " Triage", "2026-01-01", "x")]
    with pytest.raises(ValueError, match="duplicate"):
        validate_event_log(log(rows))


def test_blank_and_bad_timestamp_report_csv_rows():
    rows = [("A", "Triage", "2026-01-01", "x"), ("", "Triage", "2026-01-02", "x"), ("B", "X", "oops", "x")]
    with pytest.raises(ValueError) as err:
        validate_event_log(log(rows))
    assert "row(s): 3" in str(err.value) and "row(s): 4" in str(err.value)


def test_missing_column_and_empty():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_event_log(pd.DataFrame({"Case_ID": ["A"]}))
    with pytest.raises(ValueError, match="empty"):
        validate_event_log(log([]))
    with pytest.raises(TypeError):
        validate_event_log([1, 2])


def test_transition_minutes():
    t = build_transition_summary(log(GOOD))
    row = t[t["Transition"] == "X-Ray → Triage"].iloc[0]
    assert row["Mean_Elapsed_Minutes"] == 15.0


def test_loopback_by_group_counts_each_case_once():
    s = summarize_loopbacks_by_group(log(GOOD), "Arrival_Shift").set_index("Arrival_Shift")
    assert s.loc["Morning", "Loopback_Cases"] == 1 and s.loc["Night", "Loopback_Cases"] == 0
    with pytest.raises(ValueError):
        summarize_loopbacks_by_group(log(GOOD), "Nope")


def test_analyze_csv_and_cli(tmp_path, project_root):
    src = project_root / "careflow_data" / "clean_event_log.csv"
    result = analyze_csv(src, tmp_path)
    assert result["validation"]["case_count"] == 500
    assert main(["--input", str(src), "--output-dir", str(tmp_path)]) == 0
    assert main(["--input", str(tmp_path / "missing.csv")]) == 1

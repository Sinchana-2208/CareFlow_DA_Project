import subprocess
import sys

import pandas as pd


def run(project_root, *args):
    return subprocess.run([sys.executable, str(project_root / "scripts" / "load_synthetic_to_bigquery.py"), *args],
                          capture_output=True, text=True)


def test_dry_run_needs_no_cloud(project_root):
    r = run(project_root, "--dry-run")
    assert r.returncode == 0 and "no cloud client" in r.stdout


def test_refuses_non_synthetic_rows(project_root, tmp_path):
    df = pd.read_csv(project_root / "careflow_data" / "raw_event_log.csv")
    df.loc[0, "Is_Synthetic"] = False
    bad = tmp_path / "bad.csv"
    df.to_csv(bad, index=False)
    r = run(project_root, "--dry-run", "--csv", str(bad))
    assert r.returncode != 0 and "Is_Synthetic" in r.stderr


def test_requires_project_without_dry_run(project_root, monkeypatch):
    r = subprocess.run([sys.executable, str(project_root / "scripts" / "load_synthetic_to_bigquery.py")],
                       capture_output=True, text=True, env={"PATH": ""})
    assert r.returncode != 0

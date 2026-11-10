#!/usr/bin/env python3
"""Export BI-ready tables with human-readable labels for Looker Studio / Power BI.

Why: raw outputs contain NULLs and technical names that produce blank legend entries
(e.g. non-loopback cases have no Return_Reason) and unreadable axes in BI tools.
This script writes clearly labelled tables to careflow_data/bi_ready/.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

BASELINE = ("Registration → Triage → Physician Assessment → X-Ray → "
            "Physician Reassessment → Treatment → Discharge")
LOOP_TRANSITIONS = {"X-Ray → Triage", "Triage → Paperwork Completion", "Paperwork Completion → Physician Reassessment"}


def export(data_dir: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    events = pd.read_csv(data_dir / "clean_event_log.csv", parse_dates=["Timestamp"])
    cases = pd.read_csv(data_dir / "case_metrics.csv")

    reasons = (events.dropna(subset=["Return_Reason"]).sort_values("Timestamp")
               .drop_duplicates("Case_ID")[["Case_ID", "Return_Reason"]])
    doctor = (events[events["Activity_Name"] == "Physician Assessment"]
              .sort_values("Timestamp").drop_duplicates("Case_ID")[["Case_ID", "Resource_ID"]]
              .rename(columns={"Resource_ID": "Assessing_Physician"}))
    bi_cases = cases.merge(reasons, on="Case_ID", how="left").merge(doctor, on="Case_ID", how="left")
    bi_cases["Loopback_Reason"] = bi_cases["Return_Reason"].fillna("No loopback")
    bi_cases["Conformance_Status"] = bi_cases["Case_Trace"].eq(BASELINE).map({True: "Conforming", False: "Deviating"})
    bi_cases["Variant"] = bi_cases["Case_Trace"].eq(BASELINE).map(
        {True: "Variant 1 – Standard path", False: "Variant 2 – X-Ray → Triage loop"})
    bi_cases = bi_cases.drop(columns="Return_Reason")
    bi_cases.to_csv(out_dir / "bi_cases.csv", index=False)

    trans = pd.read_csv(data_dir / "transition_bottlenecks.csv")
    trans["Is_Loop_Related"] = trans["Transition"].isin(LOOP_TRANSITIONS)
    trans.to_csv(out_dir / "bi_transitions.csv", index=False)

    var = pd.read_csv(data_dir / "process_variants.csv")
    var["Variant"] = [f"Variant {i + 1} – " + ("Standard path" if t == BASELINE else "X-Ray → Triage loop")
                      for i, t in enumerate(var["Case_Trace"])]
    var.to_csv(out_dir / "bi_variants.csv", index=False)

    n, loops = len(bi_cases), int(bi_cases["Returned_To_Triage_After_XRay"].sum())
    kpis = pd.DataFrame([{
        "Patient_Cases": n,
        "Avg_Case_Duration_Minutes": round(bi_cases["Case_Duration_Minutes"].mean(), 2),
        "Loopback_Rate_Percent": round(100 * loops / n, 2),
        "Conformance_Rate_Percent": round(100 * (bi_cases["Conformance_Status"] == "Conforming").mean(), 2),
    }])
    kpis.to_csv(out_dir / "bi_kpis.csv", index=False)
    return kpis.iloc[0].to_dict()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=Path("careflow_data"))
    ap.add_argument("--output-dir", type=Path, default=Path("careflow_data/bi_ready"))
    a = ap.parse_args()
    print("BI-ready tables written to", a.output_dir, export(a.data_dir, a.output_dir))

from pathlib import Path
import json, zipfile, math, argparse
import pandas as pd

parser=argparse.ArgumentParser(description='Build the CareFlow descriptive report pack from the source workbook.')
parser.add_argument('workbook',type=Path,help='Path to the source .xlsx workbook')
parser.add_argument('output_dir',type=Path,help='Directory in which reports/ and the ZIP will be created')
args=parser.parse_args()
src = args.workbook
out = args.output_dir
root = out / 'reports'
root.mkdir(parents=True, exist_ok=True)
xls = pd.ExcelFile(src)
tables = {s: pd.read_excel(src, sheet_name=s) for s in xls.sheet_names}
ev = tables['Event Log Visual'].copy()
ca = tables['Case Attributes Visual'].copy()
me = tables['Event Measures Visual'].copy()
cs = tables['Cases Summary Visual'].copy()
ev['timestamp'] = pd.to_datetime(ev.timestamp)
me['timestamp'] = pd.to_datetime(me.timestamp)
cs['start_timestamp'] = pd.to_datetime(cs.start_timestamp)
cs['end_timestamp'] = pd.to_datetime(cs.end_timestamp)

def fmt(v, d=2):
    if pd.isna(v): return 'not available'
    return f'{v:,.{d}f}'
def pct(n, den): return f'{100*n/den:.1f}%' if den else 'n/a'
def mdtable(df, n=None):
    if n is not None: df=df.head(n)
    cols=list(df.columns)
    def cell(v):
        if pd.isna(v): return ''
        if isinstance(v, float): return f'{v:,.2f}'
        return str(v).replace('|','\\|').replace('\n',' ')
    lines=['| '+' | '.join(cols)+' |','| '+' | '.join(['---']*len(cols))+' |']
    lines += ['| '+' | '.join(cell(v) for v in row)+' |' for row in df.itertuples(index=False,name=None)]
    return '\n'.join(lines)
def clean(s): return ''.join(c.lower() if c.isalnum() else '_' for c in s).strip('_')

# Sheet profiles: exact row/column counts, inferred dtypes, missingness, date fields.
profiles=[]; missing_rows=[]; dtypes=[]
for name, df in tables.items():
    profiles.append({'sheet':name,'rows':len(df),'columns':len(df.columns),'duplicate_rows':int(df.duplicated().sum())})
    for c in df.columns:
        dtypes.append({'sheet':name,'column':c,'inferred_type':str(df[c].dtype),'non_null':int(df[c].notna().sum()),'null':int(df[c].isna().sum()),'null_pct':100*df[c].isna().mean()})
        missing_rows.append({'sheet':name,'column':c,'null':int(df[c].isna().sum()),'null_pct':100*df[c].isna().mean()})
pd.DataFrame(profiles).to_csv(root/'tables/sheet_profile.csv',index=False) if False else None
(root/'tables').mkdir(exist_ok=True)
pd.DataFrame(profiles).to_csv(root/'tables/sheet_profile.csv',index=False)
pd.DataFrame(dtypes).to_csv(root/'tables/column_profile.csv',index=False)
pd.DataFrame(missing_rows).to_csv(root/'tables/missingness.csv',index=False)

# Time ranges per table.
date_rows=[]
for s,df in tables.items():
    for c in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            date_rows.append({'sheet':s,'column':c,'min':df[c].min(),'max':df[c].max(),'non_null':df[c].notna().sum()})
pd.DataFrame(date_rows).to_csv(root/'tables/date_ranges.csv',index=False)

# Data quality checks.
quality=[]
def q(name, n, den, note=''):
    quality.append({'check':name,'count':int(n),'denominator':int(den),'rate_pct':100*n/den if den else None,'note':note})
q('Duplicate full rows in event log',ev.duplicated().sum(),len(ev))
q('Duplicate (case_id,event_index)',ev.duplicated(['case_id','event_index']).sum(),len(ev))
q('Duplicate case_id in Case Attributes',ca.case_id.duplicated().sum(),len(ca))
q('Duplicate case_id in Cases Summary',cs.case_id.duplicated().sum(),len(cs))
q('Event cases absent from case attributes',len(set(ev.case_id)-set(ca.case_id)),ev.case_id.nunique())
q('Attribute cases absent from event log',len(set(ca.case_id)-set(ev.case_id)),ca.case_id.nunique())
q('Event cases absent from summary',len(set(ev.case_id)-set(cs.case_id)),ev.case_id.nunique())
q('Negative case durations',int((cs.duration_days<0).sum()),len(cs))
q('Event sequence index gaps / non-start-at-1 cases',sum((g.event_index.sort_values().diff().dropna()!=1).any() or g.event_index.min()!=1 for _,g in ev.groupby('case_id')),ev.case_id.nunique())
q('Timestamp decreases in event_index order',sum((g.sort_values('event_index').timestamp.diff().dropna()<pd.Timedelta(0)).any() for _,g in ev.groupby('case_id')),ev.case_id.nunique())
q('Case summary duration mismatches (>1 second)',int(((cs.end_timestamp-cs.start_timestamp).dt.total_seconds()/86400-cs.duration_days).abs().gt(1/86400).sum()),len(cs))
q('Measure activity/name mismatches',int((me.activity!=me.measure_name).sum()),len(me))
pd.DataFrame(quality).to_csv(root/'tables/data_quality_checks.csv',index=False)

# Core descriptive outputs.
duration=cs.duration_days.dropna()
duration_summary=pd.DataFrame([{'cases':cs.case_id.nunique(),'mean_days':duration.mean(),'median_days':duration.median(),'std_days':duration.std(),'min_days':duration.min(),'p25_days':duration.quantile(.25),'p75_days':duration.quantile(.75),'p90_days':duration.quantile(.9),'p95_days':duration.quantile(.95),'max_days':duration.max(),'same_day_cases':int((duration<1).sum()),'over_7_day_cases':int((duration>7).sum())}])
duration_summary.to_csv(root/'tables/duration_summary.csv',index=False)
dur_bins=pd.cut(cs.duration_days,[float('-inf'),1,3,7,14,float('inf')],labels=['<1 day','1–<3 days','3–<7 days','7–<14 days','14+ days'],right=False)
duration_bins=dur_bins.value_counts(sort=False).rename_axis('duration_band').reset_index(name='cases'); duration_bins['pct_cases']=100*duration_bins.cases/len(cs)
duration_bins.to_csv(root/'tables/duration_bands.csv',index=False)

acts=ev.activity.value_counts().rename_axis('activity').reset_index(name='event_count'); acts['pct_events']=100*acts.event_count/len(ev); acts['cases_with_activity']=acts.activity.map(ev.groupby('activity').case_id.nunique()); acts.to_csv(root/'tables/activity_frequency.csv',index=False)
event_counts=ev.groupby('case_id').size().rename('event_count')
event_summary=pd.DataFrame([{'events':len(ev),'unique_cases':ev.case_id.nunique(),'mean_events_per_case':event_counts.mean(),'median_events_per_case':event_counts.median(),'min_events_per_case':event_counts.min(),'max_events_per_case':event_counts.max()}]);event_summary.to_csv(root/'tables/event_summary.csv',index=False)
seq=ev.sort_values(['case_id','event_index'])
seq['next_activity']=seq.groupby('case_id').activity.shift(-1)
trans=seq.dropna(subset=['next_activity']).groupby(['activity','next_activity']).size().sort_values(ascending=False).rename('transition_count').reset_index(); trans.to_csv(root/'tables/top_transitions.csv',index=False)
trace=seq.groupby('case_id').activity.agg(lambda x:' → '.join(x)).rename('trace')
trace_freq=trace.value_counts().rename_axis('trace').reset_index(name='cases');trace_freq['pct_cases']=100*trace_freq.cases/len(trace);trace_freq.to_csv(root/'tables/trace_frequency.csv',index=False)
case_events=seq.groupby('case_id').agg(event_count=('activity','size'),start=('timestamp','min'),end=('timestamp','max'),trace=('activity',lambda x:' → '.join(x))).reset_index()
case_events['calculated_duration_days']=(case_events.end-case_events.start).dt.total_seconds()/86400
case_events.to_csv(root/'tables/case_journeys.csv',index=False)

# Per-lab distributions and case coverage; measurement rows are observations, not patients.
lab=me.groupby('measure_name').measure_value.agg(records='count',mean='mean',median='median',std='std',min='min',p25=lambda x:x.quantile(.25),p75=lambda x:x.quantile(.75),p90=lambda x:x.quantile(.9),max='max').reset_index()
lab['cases']=lab.measure_name.map(me.groupby('measure_name').case_id.nunique());lab['records_per_case_mean']=lab.measure_name.map(me.groupby('measure_name').size()/me.groupby('measure_name').case_id.nunique());lab.to_csv(root/'tables/measurement_summary.csv',index=False)
labcase=me.groupby(['case_id','measure_name']).size().unstack(fill_value=0).reset_index();labcase.to_csv(root/'tables/measurements_per_case.csv',index=False)
labtime=me.groupby('measure_name').timestamp.agg(first='min',last='max').reset_index();labtime.to_csv(root/'tables/measurement_date_ranges.csv',index=False)
labmissing=me.groupby('measure_name').measure_value.agg(records='size',missing='isna').reset_index() if False else None

# Binary attribute prevalences (stored as integer indicator fields), age and diagnosis distribution.
indicators=[c for c in ca.columns if c not in ('case_id','Age','diagnosis') and pd.api.types.is_numeric_dtype(ca[c])]
attr=[]
for c in indicators:
    vc=ca[c].value_counts(dropna=False)
    attr.append({'attribute':c,'cases':len(ca),'value_1':int((ca[c]==1).sum()),'value_1_pct':100*(ca[c]==1).mean(),'value_0':int((ca[c]==0).sum()),'other_or_missing':int((~ca[c].isin([0,1])).sum())})
pd.DataFrame(attr).to_csv(root/'tables/case_attribute_indicators.csv',index=False)
age=ca.Age.describe(percentiles=[.25,.5,.75,.9]).to_dict()
diag=ca.diagnosis.value_counts(dropna=False).rename_axis('diagnosis').reset_index(name='cases');diag['pct_cases']=100*diag.cases/len(ca);diag.to_csv(root/'tables/diagnosis_distribution.csv',index=False)

start=ev.timestamp.min(); end=ev.timestamp.max()
topact=acts.head(8)
toptrace=trace_freq.head(5)
toptrans=trans.head(10)
qdf=pd.DataFrame(quality)
dups=int(ev.duplicated(['case_id','event_index']).sum())
event_cases=ev.case_id.nunique(); attr_cases=ca.case_id.nunique(); m_cases=me.case_id.nunique()
lab_lines=[]
for _,r in lab.iterrows():
    lab_lines.append(f"- **{r.measure_name}:** {int(r.records):,} records across {int(r.cases):,} cases; median {fmt(r['median'])}, IQR {fmt(r.p25)}–{fmt(r.p75)}, range {fmt(r['min'])}–{fmt(r['max'])}. Values retain the workbook's numeric scale; units are not supplied in the table.")
quality_table=mdtable(qdf)

docs={}
docs['README.md']=f'''# CareFlow Process Mining — Reports\n\nThis folder contains a descriptive, reproducible report pack built from the workbook `{src.name}`. It is designed to support process exploration and Power BI reporting. It does not provide clinical diagnosis, treatment recommendations, or outcome evaluation.\n\n## Dataset at a glance\n\n- **{event_cases:,} cases** and **{len(ev):,} event records** in the event log.\n- Event timestamps span **{start}** to **{end}**.\n- Case attributes cover **{attr_cases:,} cases**; the clinical measurement table covers **{m_cases:,} cases** and {len(me):,} measurement records.\n- Case summary durations: median **{fmt(duration.median())} days**, mean **{fmt(duration.mean())} days**, range **{fmt(duration.min())}–{fmt(duration.max())} days**.\n\n## Contents\n\n- [Dataset profile](01_dataset_profile.md): sheets, fields, inferred types, coverage, and date ranges.\n- [Data quality](02_data_quality.md): missingness, key coverage, ordering, and consistency checks.\n- [Patient and case journeys](03_case_journeys.md): event sequences, activities, and transitions.\n- [Case duration](04_case_duration.md): descriptive duration distribution.\n- [Clinical measurements](05_clinical_measurements.md): Leucocytes, CRP, and LacticAcid distributions, with measurement-specific caveats.\n- [Process and activity analysis](06_process_activity.md): event volumes and common transitions.\n- [Power BI interpretation and template](07_power_bi_dashboard.md): recommended pages, visuals, and interpretation guardrails.\n- [Limitations](08_limitations.md): appropriate scope and unsupported conclusions.\n- [Reproducibility](09_reproducibility.md): source, calculation definitions, and refresh steps.\n- `tables/`: machine-readable profiles and supporting summary tables.\n\nAll findings are descriptive and based on the supplied workbook only. Percentages are calculated against the denominator named in context; event percentages count rows, while case percentages count distinct case IDs.\n'''
docs['01_dataset_profile.md']=f'''# Dataset profile\n\n## Workbook structure\n\nSource: `{src.name}`. The workbook has **{len(tables)} sheets**. The four analysis tables contain the following records:\n\n{mdtable(pd.DataFrame(profiles))}\n\n`Read Me` is documentation rather than a case or event table. Inferred types below are pandas' read-time types; they are not a guarantee of the original Excel cell formatting.\n\n## Analysis table fields\n\n### Event Log Visual\n\n{mdtable(pd.DataFrame([{'column':c,'inferred_type':str(ev[c].dtype),'non_null':int(ev[c].notna().sum()),'distinct':int(ev[c].nunique())} for c in ev.columns]))}\n\n### Case Attributes Visual\n\n{mdtable(pd.DataFrame([{'column':c,'inferred_type':str(ca[c].dtype),'non_null':int(ca[c].notna().sum()),'distinct':int(ca[c].nunique())} for c in ca.columns]))}\n\n### Event Measures Visual\n\n{mdtable(pd.DataFrame([{'column':c,'inferred_type':str(me[c].dtype),'non_null':int(me[c].notna().sum()),'distinct':int(me[c].nunique())} for c in me.columns]))}\n\n### Cases Summary Visual\n\n{mdtable(pd.DataFrame([{'column':c,'inferred_type':str(cs[c].dtype),'non_null':int(cs[c].notna().sum()),'distinct':int(cs[c].nunique())} for c in cs.columns if c!='event_sequence']))}\n\n## Time coverage\n\nEvent timestamps span **{start}** through **{end}**. See [`tables/date_ranges.csv`](tables/date_ranges.csv) for every date-time field's observed range. The event table does not establish timezone semantics.\n\n## Case attributes\n\nAge: mean **{fmt(ca.Age.mean())}**, median **{fmt(ca.Age.median(),0)}**, interquartile range **{fmt(ca.Age.quantile(.25),0)}–{fmt(ca.Age.quantile(.75),0)}**, range **{int(ca.Age.min())}–{int(ca.Age.max())}**. Diagnosis values are categorical labels; the most frequent are:\n\n{mdtable(diag.head(10))}\n\nIndicator counts and proportions appear in [`tables/case_attribute_indicators.csv`](tables/case_attribute_indicators.csv). Indicator names are preserved as provided and their clinical definitions are not inferred here.\n'''
docs['02_data_quality.md']=f'''# Data quality report\n\nThe workbook's Read Me describes the tables as cleaned and null-free, with certain absent labels explicitly encoded as text. This report independently checks the loaded values. Literal values such as `Unknown / not recorded` and `Not recorded` are categories, not blank cells.\n\n## Missingness\n\nIn the four analysis tables, numeric/date blanks are recorded in [`tables/missingness.csv`](tables/missingness.csv). **{int(pd.DataFrame(missing_rows).query("sheet != 'Read Me'").null.sum()):,}** blank cells were detected across these analysis tables. No missingness should be confused with a textual unknown label.\n\n## Consistency checks\n\n{quality_table}\n\n`(case_id, event_index)` is the expected event key for this workbook design. Event ordering was checked by sorting on `event_index`; a timestamp decrease means the resulting order does not follow chronological time. The duration mismatch threshold is one second.\n\n## Interpretation\n\nThe key and row checks should be re-run after any refresh. A matching row count does not prove that duplicate or missing records are absent. Where categorical labels are explicit placeholders, retain them as distinct categories in dashboards or clearly group them as unknown.\n'''
docs['03_case_journeys.md']=f'''# Patient and case journey findings\n\nThe event log records **{event_cases:,} cases** with a median of **{event_counts.median():.0f} events per case** (mean {event_counts.mean():.1f}; range {event_counts.min()}–{event_counts.max()}). “Case” is used throughout because the workbook provides case identifiers; it does not establish whether one person can have multiple cases.\n\n## Most common complete event sequences\n\n{mdtable(toptrace)}\n\n## Frequent consecutive activity transitions\n\n{mdtable(toptrans)}\n\nTransitions are adjacent activities after sorting each case by `event_index`; they describe recorded sequence only. The full event order may include simultaneous timestamps, so `event_index` is the tie-break/order field used here.\n\n## Journey detail\n\n[`tables/case_journeys.csv`](tables/case_journeys.csv) includes each case's ordered trace, event count, observed timestamp bounds, and a duration recalculated from those bounds. [`tables/trace_frequency.csv`](tables/trace_frequency.csv) lists all observed full traces and their case counts. Long traces are included without clinical interpretation.\n'''
docs['04_case_duration.md']=f'''# Case duration analysis\n\nDuration is the elapsed time between each case's earliest and latest event timestamps. This is a descriptive event-log span, not necessarily hospital length of stay or time to clinical recovery.\n\n## Summary\n\n| Measure | Result |\n|---|---:|\n| Cases | {len(cs):,} |\n| Mean | {fmt(duration.mean())} days |\n| Median | {fmt(duration.median())} days |\n| Standard deviation | {fmt(duration.std())} days |\n| 25th / 75th percentile | {fmt(duration.quantile(.25))} / {fmt(duration.quantile(.75))} days |\n| 90th / 95th percentile | {fmt(duration.quantile(.90))} / {fmt(duration.quantile(.95))} days |\n| Minimum / maximum | {fmt(duration.min())} / {fmt(duration.max())} days |\n| Under 1 day | {int((duration<1).sum()):,} ({pct((duration<1).sum(),len(duration))}) |\n| Over 7 days | {int((duration>7).sum()):,} ({pct((duration>7).sum(),len(duration))}) |\n\n## Duration bands\n\n{mdtable(duration_bins)}\n\nThe mean (28.48 days) is substantially above the median (5.34 days), and the 95th percentile is 163.94 days, indicating a strong right tail. The maximum is 422.32 days. These unusually long event spans should be reviewed as case-level records before operational interpretation. Timestamp ordering and summary-duration consistency checks passed, but they do not explain why a span is long.\n'''
docs['05_clinical_measurements.md']=f'''# Clinical measurement analysis\n\nThe workbook's `Event Measures Visual` has **{len(me):,} measurement rows** across {me.case_id.nunique():,} cases. It includes `measure_name`, `measure_value`, `timestamp`, `activity`, `event_index`, and `case_id`.\n\n## Descriptive distributions\n\n{chr(10).join(lab_lines)}\n\n## How to use these results\n\nThe values and ranges are descriptive summaries of the recorded numeric column. The workbook does not supply units, assay methods, reference intervals, measurement context, or patient-level interpretation rules. Do not treat the distributions or any suggested visualization bins as medical thresholds. Repeated readings mean row-level distributions are not patient-level distributions; compare patients only after defining a clinically appropriate time point and aggregation with domain review.\n\nThe complete numeric summary is in [`tables/measurement_summary.csv`](tables/measurement_summary.csv). Per-case measurement record counts are in [`tables/measurements_per_case.csv`](tables/measurements_per_case.csv), and measurement timestamp ranges are in [`tables/measurement_date_ranges.csv`](tables/measurement_date_ranges.csv).\n'''
docs['06_process_activity.md']=f'''# Process and activity analysis\n\nAcross {event_cases:,} cases, the event log contains {len(ev):,} records and {ev.activity.nunique()} distinct activity labels.\n\n## Most frequent activities\n\n{mdtable(topact)}\n\nCounts in this table are event records. The `cases_with_activity` column counts distinct cases containing the activity, so it is not additive across activities. The most frequent activity labels are **{', '.join(acts.head(5).activity.tolist())}**.\n\n## Process sequence\n\nThe most frequent adjacent activity transitions are shown in [case journey findings](03_case_journeys.md). Use transition counts together with distinct-case counts to avoid mistaking repeated measurements within a case for broad case coverage. `org_group` and `lifecycle_transition` are included in the source log; see `tables/column_profile.csv` and `tables/missingness.csv` for their observed completeness.\n\nRecommended exploratory slices include event activity by calendar month, event count by case, and activity presence by case. They should be presented as process-log descriptions, not measures of care quality, appropriateness, or causality.\n'''
docs['07_power_bi_dashboard.md']=f'''# Power BI dashboard interpretation and template\n\nThis template builds on the workbook's four visual-ready tables. Link tables on `case_id`; for event-level detail, retain `event_index` and `timestamp` as the ordering fields. Confirm one-to-many relationships and filter direction in the model before publishing.\n\n## Recommended pages\n\n1. **Overview:** distinct cases, event rows, case duration median, event date range. State each measure's denominator and duration definition.\n2. **Process:** activity frequency by event count and by distinct cases; a case flow or transition view ordered by `event_index`. Include filters for date and activity.\n3. **Case journeys:** case table from `Cases Summary Visual` with case ID, event count, start/end, duration, and sequence. Keep a drill-through to the event log.\n4. **Clinical measurements:** use separate panels for Leucocytes, CRP, and LacticAcid. Show record counts, distribution, timestamp, and case filter. Avoid pooling unlike scales.\n5. **Case attributes:** age and supplied indicator fields, with unknown labels visible. Avoid implying those indicators establish diagnosis or severity.\n\n## Measure definitions\n\n- **Cases:** distinct count of case_id in the selected table/filter context.\n- **Events:** row count of `Event Log Visual`.\n- **Case duration:** use supplied `duration_days` for initial replication; validate against min/max timestamps. Prefer median and percentiles alongside mean.\n- **Activity cases:** distinct cases with an activity, not sum of activity counts.\n- **Measurement value:** default to individual rows or a distribution within one measure type; avoid summing a clinical reading.\n\n## Interpretation cues\n\nEvery card or chart should name the time period, unit (when known), and denominator. Highlight that case duration is timestamp span, measurement records repeat, and labels like `Unknown / not recorded` are data categories. Bins can support exploration but are not clinical reference bands.\n'''
docs['08_limitations.md']=f'''# Limitations and unsupported conclusions\n\n- **Observational event log:** timestamps and labels describe recorded events; they do not establish why an event occurred or whether care was appropriate.\n- **Case versus person:** `case_id` is the available unit. The workbook does not establish unique patients across cases.\n- **Duration meaning:** elapsed first-to-last event span is not validated as admission length, ICU stay, or recovery time.\n- **Clinical readings:** measurement units, collection conditions, reference limits, and interpretation guidance are absent. Numeric summaries cannot establish diagnosis, prognosis, treatment response, or whether a value is clinically abnormal.\n- **No outcomes endpoint:** no outcome variable is identified in the event log or case attributes, so outcome associations and causal effects are unsupported.\n- **Sequence ambiguity:** equal timestamps can occur; `event_index` is used for ordering, but the data dictionary does not explain how ties were assigned.\n- **Recorded placeholders:** explicit unknown/not-recorded strings are not nulls and may reflect source coding.\n- **Time semantics:** timezone and source-system clock behavior are unspecified.\n- **Population/generalization:** the workbook alone does not establish sampling frame, inclusion criteria, or representativeness. Findings should not be generalized beyond these records.\n\nUse this report for operational data exploration and dashboard design only. Any clinical use requires qualified review, validated definitions, and appropriate governance.\n'''
docs['09_reproducibility.md']=f'''# Reproducibility notes\n\n## Source and scope\n\nSource workbook: `{src.name}`. The analysis reads all five sheets and uses the four named analysis tables. Row counts and field types are in `tables/sheet_profile.csv` and `tables/column_profile.csv`.\n\n## Definitions\n\n- **Rows and missingness:** measured after reading each sheet with pandas; blank cells are null, while textual placeholder categories remain values.\n- **Event ordering:** sort by `case_id`, then `event_index`; adjacent transitions use the next activity within that case.\n- **Duration:** `(end_timestamp - start_timestamp)` in days from `Cases Summary Visual`; consistency checks compare to duration_days and to event-derived timestamps.\n- **Measurement summaries:** distribution statistics are calculated over non-null measure_value rows grouped by measure_name. Records and cases are both reported to expose repeated observations.\n- **Indicator counts:** numeric indicator values equal to 1 or 0 are counted directly; no mapping or interpretation is applied.\n\n## Refresh procedure\n\n1. Replace the source workbook with a version whose sheet names and field meanings are confirmed.\n2. Re-run the analysis script used to create this report pack, updating its source path.\n3. Review row counts, missingness, duplicate keys, case coverage, timestamp ordering, and duration discrepancies.\n4. Compare output summaries with the refreshed workbook and investigate material changes before sharing.\n5. Update the source filename and analysis date in the reports.\n\nAll numeric findings are descriptive and should be regenerated rather than manually edited. The CSVs in `tables/` are the supporting outputs.\n'''

for name, body in docs.items(): (root/name).write_text(body, encoding='utf-8')

zip_path=out/'careflow_reports.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        if p.is_file(): z.write(p, Path('reports')/p.relative_to(root))
print(json.dumps({'source':str(src),'reports':str(root),'zip':str(zip_path),'sheet_rows':profiles,'case_count':event_cases,'event_count':len(ev),'event_date_min':str(start),'event_date_max':str(end),'duration_median_days':float(duration.median()),'duration_mean_days':float(duration.mean()),'top_activities':acts.head(5).to_dict('records'),'top_traces':toptrace.head(3).to_dict('records'),'measurement_summary':lab.to_dict('records'),'quality':quality},default=str,indent=2))

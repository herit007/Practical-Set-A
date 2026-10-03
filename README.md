# Delivery Delay Analysis — Data Analysis Set A

**Student name:** Tanna Herit  
**Student ID:** 11431
**Assigned set:** Set A

## Business objective
Determine which service type has the greatest delivery-delay burden and which hub needs priority attention.

## Two business questions answered
1. Which service type has the greatest delivery-delay burden?
2. Which hub has the greatest summed delay burden?

## Verified analysis findings
- Clean fact records: **12** (13 supplied rows, one exact duplicate removed).
- Overall total delay_days: **34.00**.
- Standard service_type: **22.00** total delay_days; **5/6 = 83.33%** delay incidence.
- Express service_type: **12.00** total delay_days; **4/6 = 66.67%** delay incidence.
- Highest-delay hub: **Mumbai = 15.00**; Delhi = 14.00; Chennai = 5.00.
- Highest-delay route: **R4 / Rural Feeder = 14.00**, which is **41.18%** of overall delay_days.
- Monthly totals: **Jan 8.00, Feb 9.00, Mar 17.00**.
- Routes exceeding 8 summed delay_days: **R4 Rural Feeder = 14.00; R1 Metro Link = 9.00**.
- Top two hubs by summed delay_days: **Mumbai = 15.00; Delhi = 14.00**.
- Diagnostic unmatched route rows: **0**.

## Recommendation and limitation
**Recommendation:** Prioritize operational review of the Mumbai hub and the Standard-service routes, especially Rural Feeder (R4), because these areas have the largest summed delay_days in this dataset.

**Limitation:** Each row is a month-end route/hub delivery summary; summed delay_days represents cumulative record-level delay and is not a count of unique parcels requiring expedited action.

## Metric definitions
- `delay_days = MAX(actual_days - promised_days, 0)`
- Delay incidence rate = records where `actual_days > promised_days` / all records.
- Rates are calculated from underlying counts, not averaged subgroup percentages.

## Data dictionary
| Column | Type | Meaning |
|---|---|---|
| record_id | integer | Delivery-summary record identifier |
| month | text/category | Jan, Feb, Mar; preserve this order |
| route_id | text | Route lookup key |
| hub | text | Hub name |
| promised_days | numeric | Promised delivery duration |
| actual_days | numeric | Actual delivery duration |
| route | text | Route name from lookup |
| service_type | text | Express or Standard |
| delay_days | numeric | Non-negative delivery delay |

## Cleaning
1. Preserve the supplied raw 13-row deliveries file.
2. Remove the one exact duplicate record (`record_id=12`) from analysis data.
3. Merge routes onto deliveries using `route_id` as the lookup key.
4. Validate 12 clean rows and zero unmatched service_type values.
5. Derive delay_days using the required formula.

## Repository structure
```text
data-analysis-set-a/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── raw/
│       ├── deliveries.csv
│       └── routes.csv
├── excel/
│   └── analysis.xlsx
├── sql/
│   ├── setup.sql
│   └── queries.sql
├── python/
│   └── analysis.py
├── powerbi/
│   ├── dashboard.pbix
│   ├── DAX_measures.txt
│   └── PowerBI_build_steps.md
└── outputs/
    ├── clean_data.csv
    ├── python_summary.csv
    ├── python_chart.png
    ├── powerbi_dashboard.png
    └── sql/
        ├── s2a_delay_by_service_type.csv
        ├── s2b_routes_over_8.csv
        ├── s2c_top_two_hubs.csv
        └── s3_unmatched_route_diagnostic.csv
```

## SQL setup and execution
SQL dialect: **MySQL 8.0.36**.  
Run `sql/setup.sql` first, then `sql/queries.sql`.

Expected:
- S2a: Standard 22.00, Express 12.00.
- S2b: R4 Rural Feeder 14.00, R1 Metro Link 9.00.
- S2c: Mumbai 15.00, Delhi 14.00.
- Diagnostic: 0 unmatched route rows.

## Python setup and run
```bash
pip install -r requirements.txt
python python/analysis.py
```

The script uses repository-relative paths and exports the clean data, service summary, and monthly chart.

## Excel sheet guide
- **Raw:** original 13-row deliveries data unchanged.
- **Lookup:** 4-row routes lookup.
- **Clean:** 12 unique records, XLOOKUP service_type, delay_days formula, before/after counts.
- **Summary:** hub SUMIFS and service-type × month summary with Jan → Feb → Mar order and chart.

## Power BI refresh
The report should use the two CSV files under `data/raw/`. After cloning, update the source paths in Power Query to the local repository paths, then Refresh. Keep the model relationship and measures described in `powerbi/PowerBI_build_steps.md`.

## Cross-tool reconciliation
Aggregate selected: **Standard service_type total delay_days = 22.00**.
- Excel Summary: 22.00
- SQL S2a: 22.00
- Python service summary: 22.00
- Power BI Standard-filtered Total Delay Days: expected 22.00

No rounding difference is expected for this aggregate.

## Video
**Video URL:** [PASTE ACCESSIBLE YOUTUBE/GOOGLE DRIVE LINK]  
**Duration:** [ENTER 5–10 MINUTES]

The video should show face + screen throughout and explain the dataset, duplicate handling, Excel formulas/PivotTable, one SQL query, Python merge/assertion/derivation/chart, Power BI measure and slicer, two numeric findings, one recommendation, one limitation, and repository structure.

## Tools and versions
- Excel: Microsoft 365 / Excel 2019+
- Power BI Desktop: latest available version
- SQL: MySQL 8.0.36
- Python: 3.x
- pandas / matplotlib: see `requirements.txt`

## Authorship
All work in this repository is my own except where cited.

## Final submission fields
- Public repository URL: [PASTE URL]
- Final commit hash: [PASTE HASH]

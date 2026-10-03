from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DELIVERIES_PATH = ROOT / "data" / "raw" / "deliveries.csv"
ROUTES_PATH = ROOT / "data" / "raw" / "routes.csv"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

deliveries = pd.read_csv(DELIVERIES_PATH)
routes = pd.read_csv(ROUTES_PATH)

# Required numeric types
deliveries["record_id"] = pd.to_numeric(deliveries["record_id"], errors="raise").astype("int64")
deliveries["promised_days"] = pd.to_numeric(deliveries["promised_days"], errors="raise")
deliveries["actual_days"] = pd.to_numeric(deliveries["actual_days"], errors="raise")

# Remove the exact duplicate and merge with the lookup
deliveries = deliveries.drop_duplicates().copy()
merged = deliveries.merge(routes, on="route_id", how="left", validate="many_to_one")

assert len(merged) == 12, f"Expected 12 clean rows, got {len(merged)}"
assert merged["service_type"].isna().sum() == 0, "Unmatched route_id found after merge"

# Derived metric
merged["delay_days"] = (merged["actual_days"] - merged["promised_days"]).clip(lower=0)
merged["month"] = pd.Categorical(merged["month"], categories=["Jan","Feb","Mar"], ordered=True)

# Service-type summary
summary = (
    merged.assign(delayed=merged["actual_days"] > merged["promised_days"])
    .groupby("service_type", observed=True)
    .agg(
        total_delay_days=("delay_days","sum"),
        records=("record_id","count"),
        delayed_records=("delayed","sum")
    )
    .reset_index()
)
summary["delay_incidence_rate"] = summary["delayed_records"] / summary["records"]
summary["delay_incidence_rate_pct"] = summary["delay_incidence_rate"] * 100

# Single route with greatest summed delay and its share
route_totals = merged.groupby(["route_id","route"], as_index=False)["delay_days"].sum()
max_delay = route_totals["delay_days"].max()
top_routes = route_totals[route_totals["delay_days"] == max_delay]
assert len(top_routes) == 1, "Expected a single route with greatest summed delay"
top_route = top_routes.iloc[0]
top_route_share_pct = top_route["delay_days"] / merged["delay_days"].sum() * 100

print("Top route:", top_route["route_id"], top_route["route"])
print("Top route delay_days:", int(top_route["delay_days"]))
print("Top route share of overall delay (%):", round(top_route_share_pct, 2))

# Monthly chart, explicitly ordered Jan -> Feb -> Mar
monthly = merged.groupby("month", observed=True)["delay_days"].sum().reindex(["Jan","Feb","Mar"])
ax = monthly.plot(kind="bar", title="Monthly Total Delay Days")
ax.set_xlabel("Month")
ax.set_ylabel("Total Delay Days")
plt.tight_layout()
plt.savefig(OUTPUTS / "python_chart.png", dpi=160)
plt.close()

merged.to_csv(OUTPUTS / "clean_data.csv", index=False)
summary.to_csv(OUTPUTS / "python_summary.csv", index=False)

# Reconciliation assertion
assert int(summary.loc[summary.service_type=="Standard","total_delay_days"].iloc[0]) == 22
assert int(summary.loc[summary.service_type=="Express","total_delay_days"].iloc[0]) == 12
assert int(merged["delay_days"].sum()) == 34

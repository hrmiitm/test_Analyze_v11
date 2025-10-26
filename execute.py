#!/usr/bin/env python3
"""
Data Analysis Script
Reads data.csv (or data.xlsx if CSV missing) and performs revenue analysis
Outputs JSON to stdout.
"""

from pathlib import Path
import json
import sys
import pandas as pd


def read_data():
    csv = Path("data.csv")
    xlsx = Path("data.xlsx")
    if csv.exists():
        return pd.read_csv(csv)
    if xlsx.exists():
        return pd.read_excel(xlsx)
    raise FileNotFoundError("Neither 'data.csv' nor 'data.xlsx' found in working directory.")


def main() -> None:
    try:
        df = read_data()

        if df.empty:
            results = {"error": "Input data is empty", "total_records": 0}
            print(json.dumps(results, indent=2))
            return

        required = {"Revenue", "Region", "Product"}
        missing = required - set(df.columns)
        if missing:
            results = {"error": f"Missing required columns: {sorted(list(missing))}", "columns": list(df.columns)}
            print(json.dumps(results, indent=2))
            return

        # Ensure Revenue is numeric; coerce errors to NaN then fill with 0
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)

        # Total revenue
        total_revenue = df["Revenue"].sum()

        # Average revenue by Region and Product
        region_revenue = df.groupby("Region")["Revenue"].mean().to_dict()
        product_revenue = df.groupby("Product")["Revenue"].mean().to_dict()

        # Top region by total revenue
        totals_by_region = df.groupby("Region")["Revenue"].sum()
        top_region = totals_by_region.idxmax() if not totals_by_region.empty else None

        results = {
            "total_revenue": float(total_revenue),
            "avg_revenue_by_region": {str(k): float(v) for k, v in region_revenue.items()},
            "avg_revenue_by_product": {str(k): float(v) for k, v in product_revenue.items()},
            "top_region": str(top_region) if top_region is not None else None,
            "total_records": int(len(df)),
        }

        print(json.dumps(results, indent=2))

    except Exception as exc:  # keep broad except to guarantee JSON output in CI
        # Print error as JSON so CI step (python execute.py > result.json) always produces a JSON file
        print(json.dumps({"error": str(exc)}))
        return


if __name__ == "__main__":
    main()

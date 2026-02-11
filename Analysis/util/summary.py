import pandas as pd
from pathlib import Path


def generate_success_rate_summary(df, bool_cols, out_dir, warnings):
    """Generate a summary table (CSV) of success rates by scenario."""
    if not bool_cols:
        warnings.append("Build/Run/Exploit columns not found; skipping success rate summary.")
        return None

    # Group by dataset and type
    datasets = sorted(df["dataset"].dropna().unique())
    types = sorted(df["type"].dropna().unique())
    
    if not datasets or not types:
        warnings.append("Missing Dataset or Type values; skipping success rate summary.")
        return None

    # Create summary data
    summary_data = []

    for dataset in datasets:
        for dtype in types:
            subset = df[(df["dataset"] == dataset) & (df["type"] == dtype)]
            
            row = {"Scenario": f"{dataset} – {dtype}"}
            
            if subset.empty:
                for col in bool_cols:
                    row[f"{col.title()} %"] = 0.0
            else:
                for col in bool_cols:
                    val = float(subset[col].mean()) * 100.0
                    row[f"{col.title()} %"] = round(val, 2)
            
            summary_data.append(row)

    # Save summary table as CSV
    summary_df = pd.DataFrame(summary_data)
    summary_csv = out_dir / "success_rate_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    
    return summary_csv

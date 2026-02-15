#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from pathlib import Path
from util.plots import *
from util.summary import generate_success_rate_summary
from util.tables import (
    generate_functional_outcomes_table,
    generate_success_rate_per_strategy_table,
    generate_change_impact_summary_table,
    generate_automation_summary_table,
    generate_quadrant_occupancy_table,
    generate_paired_comparison_summary_table,
)
from util.config import (
    CHANGECLASS_WEIGHTS,
    AUTOMATION_WEIGHTS,
    FONT_FAMILY,
    FONT_SERIF,
    FONT_TITLE_SIZE,
    FONT_AXES_LABEL_SIZE,
    FONT_TICK_SIZE,
    FONT_LEGEND_SIZE,
    CHANGECLASS_DISTRIBUTION_FIGURE,
    AUTOMATION_DISTRIBUTION_FIGURE,
    IMPACT_VS_AUTOMATION_FIGURE
)

import pandas as pd
import matplotlib


EXPECTED_COLUMNS = [
    "cve_id",
    "type",
    "errormessage",
    "stage",
    "categoryid",
    "categoryname",
    "changeclass",
    "automationchallenge",
    "changenote",
    "explanation",
]


def ensure_venv_and_deps(venv_dir: Path) -> bool:
    """Create venv and install deps. Return True if deps should be available."""
    in_venv = getattr(sys, "base_prefix", sys.prefix) != sys.prefix
    if in_venv:
        return True

    if not venv_dir.exists():
        print(f"[setup] Creating venv at {venv_dir}...")
        import venv

        builder = venv.EnvBuilder(with_pip=True)
        try:
            builder.create(venv_dir)
        except Exception as exc:
            print(f"[setup] Failed to create venv: {exc}")
            return False

    python_exe = venv_python(venv_dir)
    if not python_exe.exists():
        print("[setup] venv python not found. Please recreate the venv.")
        return False

    try:
        subprocess.check_call([str(python_exe), "-m", "pip", "--version"])
    except Exception:
        print("[setup] pip is unavailable in the venv.")
        print(
            "[setup] Please ensure pip is installed, then run:\n"
            f"  {python_exe} -m pip install -U pip pandas openpyxl matplotlib"
        )
        return False

    print("[setup] Installing deps in venv (pandas, openpyxl, matplotlib)...")
    subprocess.check_call(
        [str(python_exe), "-m", "pip", "install", "-U", "pip", "pandas", "openpyxl", "matplotlib"]
    )
    print(
        "[setup] Done. Re-run this script using:\n"
        f"  {python_exe} {Path(__file__).name}"
    )
    return False


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    def norm(col: str) -> str:
        col = col.strip().lower()
        out = []
        for ch in col:
            if ch.isalnum():
                out.append(ch)
            else:
                out.append("_")
        return "_".join("".join(out).split("_"))

    df = df.copy()
    df.columns = [norm(c) for c in df.columns]

    rename_map = {
        "cve_id": "cve_id",
        "cveid": "cve_id",
        "type": "type",
        "errormessage": "errormessage",
        "error_message": "errormessage",
        "stage": "stage",
        "categoryid": "categoryid",
        "category_id": "categoryid",
        "categoryname": "categoryname",
        "category_name": "categoryname",
        "changeclass": "changeclass",
        "change_class": "changeclass",
        "automationchallenge": "automationchallenge",
        "automation_challenge": "automationchallenge",
        "changenote": "changenote",
        "change_note": "changenote",
        "explanation": "explanation",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df


def detect_boolean_columns(df: pd.DataFrame):
    present = []
    for col in ["compile", "run", "exploit"]:
        if col in df.columns:
            present.append(col)
    return present


def normalize_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0).astype(float).astype(int).astype(bool)
    if pd.api.types.is_string_dtype(s):
        mapping = {
            "true": True,
            "t": True,
            "1": True,
            "yes": True,
            "y": True,
            "false": False,
            "f": False,
            "0": False,
            "no": False,
            "n": False,
        }
        return s.fillna("").str.strip().str.lower().map(mapping).fillna(False).astype(bool)
    return s.fillna(False).astype(bool)


def add_weights(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["changeclass"] = df["changeclass"].astype(str).str.strip().str.lower()
    df["automationchallenge"] = df["automationchallenge"].astype(str).str.strip().str.lower()
    df["impact_weight"] = df["changeclass"].map(CHANGECLASS_WEIGHTS).fillna(0).astype(int)
    df["automation_weight"] = df["automationchallenge"].map(AUTOMATION_WEIGHTS).fillna(0).astype(int)
    return df


def aggregate_per_cve(df: pd.DataFrame, bool_cols):
    group_cols = ["cve_id", "type", "dataset"]
    agg = (
        df.groupby(group_cols, dropna=False)
        .agg(
            TotalImpact=("impact_weight", "sum"),
            TotalAutomation=("automation_weight", "sum"),
            ChangeCount=("impact_weight", "size"),
        )
        .reset_index()
    )
    for col in bool_cols:
        rates = df.groupby(group_cols)[col].mean().reset_index().rename(columns={col: f"{col}_rate"})
        agg = agg.merge(rates, on=group_cols, how="left")
    return agg


def standard_style():
    matplotlib.rcParams.update(
        {
            "font.family": FONT_FAMILY,
            "font.serif": FONT_SERIF,
            "axes.titlesize": FONT_TITLE_SIZE,
            "axes.labelsize": FONT_AXES_LABEL_SIZE,
            "xtick.labelsize": FONT_TICK_SIZE,
            "ytick.labelsize": FONT_TICK_SIZE,
            "legend.fontsize": FONT_LEGEND_SIZE,
        }
    )





def load_excel(path: Path, dataset_label: str, warnings):
    """Load classified Excel files (with changeclass and automationchallenge columns)."""
    if not path.exists():
        warnings.append(f"Missing file: {path}")
        return pd.DataFrame()

    xls = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    frames = []
    for sheet_name, df in xls.items():
        df = normalize_columns(df)
        # Only include sheets that have the required classification columns
        if "changeclass" not in df.columns or "automationchallenge" not in df.columns:
            continue
        df["dataset"] = dataset_label
        df["sheet"] = sheet_name
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def load_summary_excel(path: Path, dataset_label: str, warnings):
    """Load summary Excel files (without classification columns filtering)."""
    if not path.exists():
        warnings.append(f"Missing file: {path}")
        return pd.DataFrame()

    xls = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    frames = []
    for sheet_name, df in xls.items():
        df = normalize_columns(df)
        df["dataset"] = dataset_label
        df["sheet"] = sheet_name
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description="Phase2 figures and aggregates.")
    parser.add_argument(
        "--web",
        default="Phase2RawAnalysis_Web_Classified.xlsx",
        help="Path to Web classified Excel file",
    )
    parser.add_argument(
        "--services",
        default="Phase2RawAnalysis_Services_Classified.xlsx",
        help="Path to Services classified Excel file",
    )
    parser.add_argument(
        "--web-summary",
        default="Phase2TableSummaryWeb.xlsx",
        help="Path to Web summary Excel file for functional success charts",
    )
    parser.add_argument(
        "--services-summary",
        default="Phase2TableSummaryServices.xlsx",
        help="Path to Services summary Excel file for functional success charts",
    )
    parser.add_argument(
        "--outdir",
        default="figures_paper",
        help="Output directory for figures and CSVs",
    )
    parser.add_argument(
        "--vector",
        action="store_true",
        help="Also save PDF/SVG versions of figures",
    )
    parser.add_argument(
        "--skip-venv",
        action="store_true",
        help="Skip venv creation and dependency install",
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help="Generate only tables (skip figures)",
    )
    args = parser.parse_args()

    if not args.skip_venv:
        ok = ensure_venv_and_deps(Path(".venv"))
        if not ok:
            return 0

    warnings = []
    standard_style()

    df_web = load_excel(Path(args.web), "Web", warnings)
    df_services = load_excel(Path(args.services), "Services", warnings)
    df = pd.concat([df_web, df_services], ignore_index=True)
    if df.empty:
        print("No data loaded. Check input files.")
        return 1
    
    # Load summary data for functional success charts
    df_web_summary = load_summary_excel(Path(args.web_summary), "Web", warnings)
    df_services_summary = load_summary_excel(Path(args.services_summary), "Services", warnings)
    df_summary = pd.concat([df_web_summary, df_services_summary], ignore_index=True)

    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        warnings.append(f"Missing expected columns: {', '.join(missing_cols)}")

    bool_cols = detect_boolean_columns(df)
    for col in bool_cols:
        df[col] = normalize_bool_series(df[col])
    
    # Prepare summary data for functional success charts
    bool_cols_summary = detect_boolean_columns(df_summary)
    for col in bool_cols_summary:
        df_summary[col] = normalize_bool_series(df_summary[col])
    
    # Verify all three metrics are present
    expected_metrics = ["compile", "run", "exploit"]
    missing_metrics = [m for m in expected_metrics if m not in bool_cols_summary]
    if missing_metrics:
        warnings.append(f"Missing metrics in summary data: {', '.join(missing_metrics)}")
        warnings.append(f"Available columns: {', '.join(df_summary.columns.tolist())}")

    df = add_weights(df)
    agg = aggregate_per_cve(df, bool_cols)

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Create tables directory
    tables_dir = Path("tables_paper")
    tables_dir.mkdir(parents=True, exist_ok=True)

    agg_csv = out_dir / "aggregated_per_cve.csv"
    agg.to_csv(agg_csv, index=False)

    saved = [agg_csv]
    
    # Generate tables
    table_path = generate_functional_outcomes_table(df_summary, tables_dir, warnings)
    if table_path:
        saved.append(table_path)
    
    table_path = generate_success_rate_per_strategy_table(df_summary, tables_dir, warnings)
    if table_path:
        saved.append(table_path)
    
    table_path = generate_change_impact_summary_table(df, agg, tables_dir, warnings)
    if table_path:
        saved.append(table_path)
    
    table_path = generate_automation_summary_table(df, agg, tables_dir, warnings)
    if table_path:
        saved.append(table_path)
    
    table_path = generate_quadrant_occupancy_table(agg, tables_dir, warnings)
    if table_path:
        saved.append(table_path)
    
    table_path = generate_paired_comparison_summary_table(agg, tables_dir, warnings)
    if table_path:
        saved.append(table_path)
    
    # Success rate summary table (CSV) - using summary data
    csv_path = generate_success_rate_summary(df_summary, bool_cols_summary, out_dir, warnings)
    if csv_path:
        saved.append(csv_path)
    
    # Skip figures if --tables flag is set
    if args.tables:
        print("\nSkipping figures (--tables flag set)")
        print("\nSaved files:")
        for p in saved:
            print(f"  - {p}")
        if warnings:
            print("\nWarnings:")
            for w in warnings:
                print(f"  - {w}")
        return 0
    
    # Figure 1: Overall functional success rates - using summary data
    path = plot_overall_success(df_summary, bool_cols_summary, out_dir, args.vector, warnings)
    if path:
        saved.append(path)
    
    # Figure 2a: Services functional success (Package vs Source) - using summary data
    path = plot_services_success(df_summary, bool_cols_summary, out_dir, args.vector, warnings)
    if path:
        saved.append(path)
    
    # Figure 2b: Web functional success (Compose vs Source) - using summary data
    path = plot_web_success(df_summary, bool_cols_summary, out_dir, args.vector, warnings)
    if path:
        saved.append(path)
    
    path = plot_functional_success(agg, bool_cols, out_dir, args.vector, warnings)
    if path:
        saved.append(path)
    
    # Figure 3: Change Impact class distribution
    path = plot_changeclass_impact_distribution(df, out_dir, args.vector, warnings)
    if path:
        saved.append(path)
    
    # Figure 4: Automation Challenge class distribution
    path = plot_automation_challenge_distribution(df, out_dir, args.vector, warnings)
    if path:
        saved.append(path)
    
    path = plot_stacked_distribution(
        df,
        "changeclass",
        out_dir / CHANGECLASS_DISTRIBUTION_FIGURE,
        # title="ChangeClass Distribution by Type",
        title="",
        also_vector=args.vector,
        warnings=warnings,
    )
    if path:
        saved.append(path)
    path = plot_stacked_distribution(
        df,
        "automationchallenge",
        out_dir / AUTOMATION_DISTRIBUTION_FIGURE,
        # title="AutomationChallenge Distribution by Type",
        title="",
        also_vector=args.vector,
        warnings=warnings,
    )
    if path:
        saved.append(path)
    path = plot_scatter(agg, out_dir / IMPACT_VS_AUTOMATION_FIGURE, args.vector, warnings)
    if path:
        saved.append(path)
    saved.extend(plot_boxplots(agg, out_dir, args.vector, warnings))
    path = plot_paired_delta_hist(
        agg, out_dir / PAIRED_DELTA_FIGURE, args.vector, warnings
    )
    if path:
        saved.append(path)
    
    # Figure 7: Error category frequency by stage
    path = plot_error_category_by_stage(df, out_dir, args.vector, warnings)
    if path:
        saved.append(path)

    print("\nSaved files:")
    for p in saved:
        print(f"  - {p}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - {w}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

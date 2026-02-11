"""
Generate CSV tables for paper.
"""
import pandas as pd
from pathlib import Path


def generate_functional_outcomes_table(df_summary, out_dir: Path, warnings):
    """
    Generate table with Build/Run/Exploit success rates.
    
    Table structure:
    - Rows: Overall, Services Package, Services Source, Web Compose, Web Bundle
    - Columns: % Build success, % Run success, % Exploit success
    """
    if df_summary.empty:
        warnings.append("No summary data for functional outcomes table.")
        return None
    
    # Check required columns
    required_cols = ["compile", "run", "exploit", "type", "dataset"]
    missing = [c for c in required_cols if c not in df_summary.columns]
    if missing:
        warnings.append(f"Missing columns for functional outcomes table: {', '.join(missing)}")
        return None
    
    results = []
    
    # Overall success rates
    total = len(df_summary)
    if total > 0:
        build_pct = (df_summary["compile"].sum() / total) * 100
        run_pct = (df_summary["run"].sum() / total) * 100
        exploit_pct = (df_summary["exploit"].sum() / total) * 100
        results.append({
            "Category": "Overall",
            "Build Success (%)": round(build_pct, 1),
            "Run Success (%)": round(run_pct, 1),
            "Exploit Success (%)": round(exploit_pct, 1),
        })
    
    # Services breakdowns
    services_df = df_summary[df_summary["dataset"].str.lower() == "services"]
    for type_name in ["Package", "Source"]:
        subset = services_df[services_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            build_pct = (subset["compile"].sum() / len(subset)) * 100
            run_pct = (subset["run"].sum() / len(subset)) * 100
            exploit_pct = (subset["exploit"].sum() / len(subset)) * 100
            results.append({
                "Category": f"Services {type_name}",
                "Build Success (%)": round(build_pct, 1),
                "Run Success (%)": round(run_pct, 1),
                "Exploit Success (%)": round(exploit_pct, 1),
            })
    
    # Web breakdowns
    web_df = df_summary[df_summary["dataset"].str.lower() == "web"]
    for type_name in ["Compose", "Bundle"]:
        subset = web_df[web_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            build_pct = (subset["compile"].sum() / len(subset)) * 100
            run_pct = (subset["run"].sum() / len(subset)) * 100
            exploit_pct = (subset["exploit"].sum() / len(subset)) * 100
            results.append({
                "Category": f"Web {type_name}",
                "Build Success (%)": round(build_pct, 1),
                "Run Success (%)": round(run_pct, 1),
                "Exploit Success (%)": round(exploit_pct, 1),
            })
    
    if not results:
        warnings.append("No data to generate functional outcomes table.")
        return None
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_functional_outcomes.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path


def generate_success_rate_per_strategy_table(df_summary, out_dir: Path, warnings):
    """
    Generate table with Build/Run/Exploit success rates per strategy.
    
    Table structure (Table 1 — Functional success rates):
    - Rows: Services Package, Services Source, Webapps Compose, Webapps Source/Bundle
    - Columns: Build %, Run %, Exploit %
    """
    if df_summary.empty:
        warnings.append("No summary data for success rate per strategy table.")
        return None
    
    # Check required columns
    required_cols = ["compile", "run", "exploit", "type", "dataset"]
    missing = [c for c in required_cols if c not in df_summary.columns]
    if missing:
        warnings.append(f"Missing columns for success rate per strategy table: {', '.join(missing)}")
        return None
    
    results = []
    
    # Services breakdowns
    services_df = df_summary[df_summary["dataset"].str.lower() == "services"]
    for type_name in ["Package", "Source"]:
        subset = services_df[services_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            build_pct = (subset["compile"].sum() / len(subset)) * 100
            run_pct = (subset["run"].sum() / len(subset)) * 100
            exploit_pct = (subset["exploit"].sum() / len(subset)) * 100
            results.append({
                "Scenario": f"Services – {type_name}",
                "Build %": round(build_pct, 1),
                "Run %": round(run_pct, 1),
                "Exploit %": round(exploit_pct, 1),
            })
    
    # Webapps breakdowns - try Source first, then Bundle, then Compose
    web_df = df_summary[df_summary["dataset"].str.lower() == "web"]
    for type_name in ["Compose", "Source", "Bundle"]:
        subset = web_df[web_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            build_pct = (subset["compile"].sum() / len(subset)) * 100
            run_pct = (subset["run"].sum() / len(subset)) * 100
            exploit_pct = (subset["exploit"].sum() / len(subset)) * 100
            results.append({
                "Scenario": f"Webapps – {type_name}",
                "Build %": round(build_pct, 1),
                "Run %": round(run_pct, 1),
                "Exploit %": round(exploit_pct, 1),
            })
    
    if not results:
        warnings.append("No data to generate success rate per strategy table.")
        return None
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_success_rate_per_strategy.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path


def generate_change_impact_summary_table(df, agg, out_dir: Path, warnings):
    """
    Generate table with Change Impact class distribution and median total impact.
    
    Table structure (Table 2 — Change Impact aggregates):
    - Rows: Services Package, Services Source, Webapps Compose, Webapps Source/Bundle
    - Columns: % C0, % C1, % C2, Median Total Impact
    """
    if df.empty:
        warnings.append("No classified data for change impact summary table.")
        return None
    
    # Check required columns
    required_cols = ["changeclass", "type", "dataset"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        warnings.append(f"Missing columns for change impact summary table: {', '.join(missing)}")
        return None
    
    if agg.empty or "TotalImpact" not in agg.columns:
        warnings.append("No aggregated data with TotalImpact for change impact summary table.")
        return None
    
    results = []
    
    # Services breakdowns
    services_df = df[df["dataset"].str.lower() == "services"]
    services_agg = agg[agg["dataset"].str.lower() == "services"]
    
    for type_name in ["Package", "Source"]:
        subset = services_df[services_df["type"].str.lower() == type_name.lower()]
        subset_agg = services_agg[services_agg["type"].str.lower() == type_name.lower()]
        
        if len(subset) > 0:
            # Calculate percentage of each changeclass
            total_count = len(subset)
            c0_count = (subset["changeclass"] == "c0").sum()
            c1_count = (subset["changeclass"] == "c1").sum()
            c2_count = (subset["changeclass"] == "c2").sum()
            
            c0_pct = (c0_count / total_count) * 100 if total_count > 0 else 0
            c1_pct = (c1_count / total_count) * 100 if total_count > 0 else 0
            c2_pct = (c2_count / total_count) * 100 if total_count > 0 else 0
            
            # Calculate median TotalImpact from aggregated data
            median_impact = subset_agg["TotalImpact"].median() if len(subset_agg) > 0 else 0
            
            results.append({
                "Scenario": f"Services – {type_name}",
                "% C0": round(c0_pct, 1),
                "% C1": round(c1_pct, 1),
                "% C2": round(c2_pct, 1),
                "Median Total Impact": round(median_impact, 1),
            })
    
    # Webapps breakdowns
    web_df = df[df["dataset"].str.lower() == "web"]
    web_agg = agg[agg["dataset"].str.lower() == "web"]
    
    for type_name in ["Compose", "Source", "Bundle"]:
        subset = web_df[web_df["type"].str.lower() == type_name.lower()]
        subset_agg = web_agg[web_agg["type"].str.lower() == type_name.lower()]
        
        if len(subset) > 0:
            # Calculate percentage of each changeclass
            total_count = len(subset)
            c0_count = (subset["changeclass"] == "c0").sum()
            c1_count = (subset["changeclass"] == "c1").sum()
            c2_count = (subset["changeclass"] == "c2").sum()
            
            c0_pct = (c0_count / total_count) * 100 if total_count > 0 else 0
            c1_pct = (c1_count / total_count) * 100 if total_count > 0 else 0
            c2_pct = (c2_count / total_count) * 100 if total_count > 0 else 0
            
            # Calculate median TotalImpact from aggregated data
            median_impact = subset_agg["TotalImpact"].median() if len(subset_agg) > 0 else 0
            
            results.append({
                "Scenario": f"Webapps – {type_name}",
                "% C0": round(c0_pct, 1),
                "% C1": round(c1_pct, 1),
                "% C2": round(c2_pct, 1),
                "Median Total Impact": round(median_impact, 1),
            })
    
    if not results:
        warnings.append("No data to generate change impact summary table.")
        return None
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_change_impact_summary.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path


def generate_automation_summary_table(df, agg, out_dir: Path, warnings):
    """
    Generate table with Automation Challenge class distribution and median total automation.
    
    Table structure (Table 3 — Automation Challenge aggregates):
    - Rows: Services Package, Services Source, Webapps Compose, Webapps Source/Bundle
    - Columns: % A0, % A1, % A2, Median Total Automation
    """
    if df.empty:
        warnings.append("No classified data for automation summary table.")
        return None
    
    # Check required columns
    required_cols = ["automationchallenge", "type", "dataset"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        warnings.append(f"Missing columns for automation summary table: {', '.join(missing)}")
        return None
    
    if agg.empty or "TotalAutomation" not in agg.columns:
        warnings.append("No aggregated data with TotalAutomation for automation summary table.")
        return None
    
    results = []
    
    # Services breakdowns
    services_df = df[df["dataset"].str.lower() == "services"]
    services_agg = agg[agg["dataset"].str.lower() == "services"]
    
    for type_name in ["Package", "Source"]:
        subset = services_df[services_df["type"].str.lower() == type_name.lower()]
        subset_agg = services_agg[services_agg["type"].str.lower() == type_name.lower()]
        
        if len(subset) > 0:
            # Calculate percentage of each automationchallenge
            total_count = len(subset)
            a0_count = (subset["automationchallenge"] == "a0").sum()
            a1_count = (subset["automationchallenge"] == "a1").sum()
            a2_count = (subset["automationchallenge"] == "a2").sum()
            
            a0_pct = (a0_count / total_count) * 100 if total_count > 0 else 0
            a1_pct = (a1_count / total_count) * 100 if total_count > 0 else 0
            a2_pct = (a2_count / total_count) * 100 if total_count > 0 else 0
            
            # Calculate median TotalAutomation from aggregated data
            median_automation = subset_agg["TotalAutomation"].median() if len(subset_agg) > 0 else 0
            
            results.append({
                "Scenario": f"Services – {type_name}",
                "% A0": round(a0_pct, 1),
                "% A1": round(a1_pct, 1),
                "% A2": round(a2_pct, 1),
                "Median Total Automation": round(median_automation, 1),
            })
    
    # Webapps breakdowns
    web_df = df[df["dataset"].str.lower() == "web"]
    web_agg = agg[agg["dataset"].str.lower() == "web"]
    
    for type_name in ["Compose", "Source", "Bundle"]:
        subset = web_df[web_df["type"].str.lower() == type_name.lower()]
        subset_agg = web_agg[web_agg["type"].str.lower() == type_name.lower()]
        
        if len(subset) > 0:
            # Calculate percentage of each automationchallenge
            total_count = len(subset)
            a0_count = (subset["automationchallenge"] == "a0").sum()
            a1_count = (subset["automationchallenge"] == "a1").sum()
            a2_count = (subset["automationchallenge"] == "a2").sum()
            
            a0_pct = (a0_count / total_count) * 100 if total_count > 0 else 0
            a1_pct = (a1_count / total_count) * 100 if total_count > 0 else 0
            a2_pct = (a2_count / total_count) * 100 if total_count > 0 else 0
            
            # Calculate median TotalAutomation from aggregated data
            median_automation = subset_agg["TotalAutomation"].median() if len(subset_agg) > 0 else 0
            
            results.append({
                "Scenario": f"Webapps – {type_name}",
                "% A0": round(a0_pct, 1),
                "% A1": round(a1_pct, 1),
                "% A2": round(a2_pct, 1),
                "Median Total Automation": round(median_automation, 1),
            })
    
    if not results:
        warnings.append("No data to generate automation summary table.")
        return None
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_automation_summary.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path


def generate_quadrant_occupancy_table(agg, out_dir: Path, warnings):
    """
    Generate table with quadrant occupancy based on TotalImpact vs TotalAutomation.
    
    Table structure (Table 4 — Quadrant occupancy):
    - Quadrants based on median TotalImpact and TotalAutomation
    - Rows: Easy, Engineering-difficult, Automation-difficult, Hard
    - Columns: Quadrant, # CVEs, %
    """
    if agg.empty:
        warnings.append("No aggregated data for quadrant occupancy table.")
        return None
    
    # Check required columns
    if "TotalImpact" not in agg.columns or "TotalAutomation" not in agg.columns:
        warnings.append("Missing TotalImpact or TotalAutomation columns for quadrant occupancy table.")
        return None
    
    # Calculate medians
    median_impact = agg["TotalImpact"].median()
    median_automation = agg["TotalAutomation"].median()
    
    # Classify CVEs into quadrants
    def classify_quadrant(row):
        if row["TotalImpact"] <= median_impact and row["TotalAutomation"] <= median_automation:
            return "Easy"
        elif row["TotalImpact"] > median_impact and row["TotalAutomation"] <= median_automation:
            return "Engineering-difficult"
        elif row["TotalImpact"] <= median_impact and row["TotalAutomation"] > median_automation:
            return "Automation-difficult"
        else:  # high impact, high automation
            return "Hard"
    
    agg["Quadrant"] = agg.apply(classify_quadrant, axis=1)
    
    # Count CVEs per quadrant
    quadrant_counts = agg["Quadrant"].value_counts()
    total_cves = len(agg)
    
    # Define quadrant order
    quadrant_order = ["Easy", "Engineering-difficult", "Automation-difficult", "Hard"]
    
    results = []
    for quadrant in quadrant_order:
        count = quadrant_counts.get(quadrant, 0)
        percentage = (count / total_cves * 100) if total_cves > 0 else 0
        results.append({
            "Quadrant": quadrant,
            "# CVEs": count,
            "%": round(percentage, 1),
        })
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_quadrant_occupancy.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path


def generate_paired_comparison_summary_table(agg, out_dir: Path, warnings):
    """
    Generate table with paired comparison summary (Package vs Source).
    
    Table structure (Table 5 — Paired comparison summary):
    - Rows: Median, Mean
    - Columns: Metric, Package (Impact), Source (Impact), Δ Change impact, 
               Package (Automation), Source (Automation), Δ Automation challenge
    """
    if agg.empty:
        warnings.append("No aggregated data for paired comparison summary table.")
        return None
    
    # Check required columns
    required_cols = ["TotalImpact", "TotalAutomation", "type", "dataset", "cve_id"]
    missing = [c for c in required_cols if c not in agg.columns]
    if missing:
        warnings.append(f"Missing columns for paired comparison summary table: {', '.join(missing)}")
        return None
    
    # Filter for Services dataset
    services_agg = agg[agg["dataset"].str.lower() == "services"].copy()
    
    # Find CVEs that have both Package and Source
    package_cves = set(services_agg[services_agg["type"].str.lower() == "package"]["cve_id"])
    source_cves = set(services_agg[services_agg["type"].str.lower() == "source"]["cve_id"])
    paired_cves = package_cves & source_cves
    
    if not paired_cves:
        warnings.append("No paired CVEs (Package + Source) found for paired comparison summary.")
        # Try Web dataset as fallback
        web_agg = agg[agg["dataset"].str.lower() == "web"].copy()
        compose_cves = set(web_agg[web_agg["type"].str.lower() == "compose"]["cve_id"])
        bundle_cves = set(web_agg[web_agg["type"].str.lower() == "bundle"]["cve_id"])
        paired_cves = compose_cves & bundle_cves
        
        if not paired_cves:
            warnings.append("No paired CVEs found in Web dataset either.")
            return None
        
        # Use Web data instead
        df_type_a = web_agg[web_agg["cve_id"].isin(paired_cves) & (web_agg["type"].str.lower() == "compose")]
        df_type_b = web_agg[web_agg["cve_id"].isin(paired_cves) & (web_agg["type"].str.lower() == "bundle")]
        type_a_name = "Compose"
        type_b_name = "Bundle"
    else:
        df_type_a = services_agg[services_agg["cve_id"].isin(paired_cves) & (services_agg["type"].str.lower() == "package")]
        df_type_b = services_agg[services_agg["cve_id"].isin(paired_cves) & (services_agg["type"].str.lower() == "source")]
        type_a_name = "Package"
        type_b_name = "Source"
    
    results = []
    
    # Calculate statistics for Median
    pkg_impact_median = df_type_a["TotalImpact"].median()
    src_impact_median = df_type_b["TotalImpact"].median()
    delta_impact_median = src_impact_median - pkg_impact_median
    
    pkg_auto_median = df_type_a["TotalAutomation"].median()
    src_auto_median = df_type_b["TotalAutomation"].median()
    delta_auto_median = src_auto_median - pkg_auto_median
    
    results.append({
        "Metric": "Median",
        f"{type_a_name} (Impact)": round(pkg_impact_median, 1),
        f"{type_b_name} (Impact)": round(src_impact_median, 1),
        "Δ Change Impact": round(delta_impact_median, 1),
        f"{type_a_name} (Automation)": round(pkg_auto_median, 1),
        f"{type_b_name} (Automation)": round(src_auto_median, 1),
        "Δ Automation Challenge": round(delta_auto_median, 1),
    })
    
    # Calculate statistics for Mean
    pkg_impact_mean = df_type_a["TotalImpact"].mean()
    src_impact_mean = df_type_b["TotalImpact"].mean()
    delta_impact_mean = src_impact_mean - pkg_impact_mean
    
    pkg_auto_mean = df_type_a["TotalAutomation"].mean()
    src_auto_mean = df_type_b["TotalAutomation"].mean()
    delta_auto_mean = src_auto_mean - pkg_auto_mean
    
    results.append({
        "Metric": "Mean",
        f"{type_a_name} (Impact)": round(pkg_impact_mean, 1),
        f"{type_b_name} (Impact)": round(src_impact_mean, 1),
        "Δ Change Impact": round(delta_impact_mean, 1),
        f"{type_a_name} (Automation)": round(pkg_auto_mean, 1),
        f"{type_b_name} (Automation)": round(src_auto_mean, 1),
        "Δ Automation Challenge": round(delta_auto_mean, 1),
    })
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_paired_comparison_summary.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path

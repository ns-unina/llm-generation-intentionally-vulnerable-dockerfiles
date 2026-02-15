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
        build_count = df_summary["compile"].sum()
        run_count = df_summary["run"].sum()
        exploit_count = df_summary["exploit"].sum()
        build_pct = (build_count / total) * 100
        run_pct = (run_count / total) * 100
        exploit_pct = (exploit_count / total) * 100
        results.append({
            "Category": "Overall",
            "Build Success": f"{build_count}/{total} ({build_pct:.1f}%)",
            "Run Success": f"{run_count}/{total} ({run_pct:.1f}%)",
            "Exploit Success": f"{exploit_count}/{total} ({exploit_pct:.1f}%)",
        })
    
    # Services breakdowns
    services_df = df_summary[df_summary["dataset"].str.lower() == "services"]
    for type_name in ["Package", "Source"]:
        subset = services_df[services_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            total_sub = len(subset)
            build_count = subset["compile"].sum()
            run_count = subset["run"].sum()
            exploit_count = subset["exploit"].sum()
            build_pct = (build_count / total_sub) * 100
            run_pct = (run_count / total_sub) * 100
            exploit_pct = (exploit_count / total_sub) * 100
            results.append({
                "Category": f"Services {type_name}",
                "Build Success": f"{build_count}/{total_sub} ({build_pct:.1f}%)",
                "Run Success": f"{run_count}/{total_sub} ({run_pct:.1f}%)",
                "Exploit Success": f"{exploit_count}/{total_sub} ({exploit_pct:.1f}%)",
            })
    
    # Web breakdowns
    web_df = df_summary[df_summary["dataset"].str.lower() == "web"]
    for type_name in ["Compose", "Bundle"]:
        subset = web_df[web_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            total_sub = len(subset)
            build_count = subset["compile"].sum()
            run_count = subset["run"].sum()
            exploit_count = subset["exploit"].sum()
            build_pct = (build_count / total_sub) * 100
            run_pct = (run_count / total_sub) * 100
            exploit_pct = (exploit_count / total_sub) * 100
            results.append({
                "Category": f"Web {type_name}",
                "Build Success": f"{build_count}/{total_sub} ({build_pct:.1f}%)",
                "Run Success": f"{run_count}/{total_sub} ({run_pct:.1f}%)",
                "Exploit Success": f"{exploit_count}/{total_sub} ({exploit_pct:.1f}%)",
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
            total_sub = len(subset)
            build_count = subset["compile"].sum()
            run_count = subset["run"].sum()
            exploit_count = subset["exploit"].sum()
            build_pct = (build_count / total_sub) * 100
            run_pct = (run_count / total_sub) * 100
            exploit_pct = (exploit_count / total_sub) * 100
            results.append({
                "Scenario": f"Services – {type_name}",
                "Build": f"{build_count}/{total_sub} ({build_pct:.1f}%)",
                "Run": f"{run_count}/{total_sub} ({run_pct:.1f}%)",
                "Exploit": f"{exploit_count}/{total_sub} ({exploit_pct:.1f}%)",
            })
    
    # Webapps breakdowns - try Source first, then Bundle, then Compose
    web_df = df_summary[df_summary["dataset"].str.lower() == "web"]
    for type_name in ["Compose", "Source", "Bundle"]:
        subset = web_df[web_df["type"].str.lower() == type_name.lower()]
        if len(subset) > 0:
            total_sub = len(subset)
            build_count = subset["compile"].sum()
            run_count = subset["run"].sum()
            exploit_count = subset["exploit"].sum()
            build_pct = (build_count / total_sub) * 100
            run_pct = (run_count / total_sub) * 100
            exploit_pct = (exploit_count / total_sub) * 100
            results.append({
                "Scenario": f"Webapps – {type_name}",
                "Build": f"{build_count}/{total_sub} ({build_pct:.1f}%)",
                "Run": f"{run_count}/{total_sub} ({run_pct:.1f}%)",
                "Exploit": f"{exploit_count}/{total_sub} ({exploit_pct:.1f}%)",
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
                "C0": f"{c0_count}/{total_count} ({c0_pct:.1f}%)",
                "C1": f"{c1_count}/{total_count} ({c1_pct:.1f}%)",
                "C2": f"{c2_count}/{total_count} ({c2_pct:.1f}%)",
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
                "C0": f"{c0_count}/{total_count} ({c0_pct:.1f}%)",
                "C1": f"{c1_count}/{total_count} ({c1_pct:.1f}%)",
                "C2": f"{c2_count}/{total_count} ({c2_pct:.1f}%)",
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
                "A0": f"{a0_count}/{total_count} ({a0_pct:.1f}%)",
                "A1": f"{a1_count}/{total_count} ({a1_pct:.1f}%)",
                "A2": f"{a2_count}/{total_count} ({a2_pct:.1f}%)",
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
                "A0": f"{a0_count}/{total_count} ({a0_pct:.1f}%)",
                "A1": f"{a1_count}/{total_count} ({a1_pct:.1f}%)",
                "A2": f"{a2_count}/{total_count} ({a2_pct:.1f}%)",
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
            "CVEs": f"{count}/{total_cves} ({percentage:.1f}%)",
        })
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_quadrant_occupancy.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path


def generate_paired_comparison_summary_table(agg, out_dir: Path, warnings):
    """
    Generate combined table with paired comparison summary for Services and Web.
    
    Table structure:
    - Rows: Change Impact (Source vs Package), Change Impact (Bundle vs Compose),
            Automatic Challenge (Source vs Package), Automatic Challenge (Bundle vs Compose)
    - Columns: Metric, Scenario 1, Scenario 2, Mean, Median, Delta (Mean/Median)
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
    
    results = []
    
    # Process Services dataset (Package vs Source)
    services_agg = agg[agg["dataset"].str.lower() == "services"].copy()
    package_cves = set(services_agg[services_agg["type"].str.lower() == "package"]["cve_id"])
    source_cves = set(services_agg[services_agg["type"].str.lower() == "source"]["cve_id"])
    services_paired_cves = package_cves & source_cves
    
    if services_paired_cves:
        df_package = services_agg[services_agg["cve_id"].isin(services_paired_cves) & (services_agg["type"].str.lower() == "package")]
        df_source = services_agg[services_agg["cve_id"].isin(services_paired_cves) & (services_agg["type"].str.lower() == "source")]
        
        # Change Impact
        impact_mean = round(df_source["TotalImpact"].mean(), 1)
        impact_median = round(df_source["TotalImpact"].median(), 1)
        impact_delta = round(impact_mean - round(df_package["TotalImpact"].mean(), 1), 1)
        
        results.append({
            "Metric": "Change Impact",
            "Scenario 1": "Source",
            "Scenario 2": "Package",
            "Mean": impact_mean,
            "Median": impact_median,
            "Delta (Mean/Median)": impact_delta,
        })
        
        # Automatic Challenge
        auto_mean = round(df_source["TotalAutomation"].mean(), 1)
        auto_median = round(df_source["TotalAutomation"].median(), 1)
        auto_delta = round(auto_mean - round(df_package["TotalAutomation"].mean(), 1), 1)
        
        results.append({
            "Metric": "Automatic Challenge",
            "Scenario 1": "Source",
            "Scenario 2": "Package",
            "Mean": auto_mean,
            "Median": auto_median,
            "Delta (Mean/Median)": auto_delta,
        })
    
    # Process Web dataset (Bundle vs Compose)
    web_agg = agg[agg["dataset"].str.lower() == "web"].copy()
    compose_cves = set(web_agg[web_agg["type"].str.lower() == "compose"]["cve_id"])
    bundle_cves = set(web_agg[web_agg["type"].str.lower() == "bundle"]["cve_id"])
    web_paired_cves = compose_cves & bundle_cves
    
    if web_paired_cves:
        df_compose = web_agg[web_agg["cve_id"].isin(web_paired_cves) & (web_agg["type"].str.lower() == "compose")]
        df_bundle = web_agg[web_agg["cve_id"].isin(web_paired_cves) & (web_agg["type"].str.lower() == "bundle")]
        
        # Change Impact
        impact_mean = round(df_bundle["TotalImpact"].mean(), 1)
        impact_median = round(df_bundle["TotalImpact"].median(), 1)
        impact_delta = round(impact_mean - round(df_compose["TotalImpact"].mean(), 1), 1)
        
        results.append({
            "Metric": "Change Impact",
            "Scenario 1": "Bundle",
            "Scenario 2": "Compose",
            "Mean": impact_mean,
            "Median": impact_median,
            "Delta (Mean/Median)": impact_delta,
        })
        
        # Automatic Challenge
        auto_mean = round(df_bundle["TotalAutomation"].mean(), 1)
        auto_median = round(df_bundle["TotalAutomation"].median(), 1)
        auto_delta = round(auto_mean - round(df_compose["TotalAutomation"].mean(), 1), 1)
        
        results.append({
            "Metric": "Automatic Challenge",
            "Scenario 1": "Bundle",
            "Scenario 2": "Compose",
            "Mean": auto_mean,
            "Median": auto_median,
            "Delta (Mean/Median)": auto_delta,
        })
    
    if not results:
        warnings.append("No paired CVEs found for paired comparison summary.")
        return None
    
    # Create DataFrame and save
    table_df = pd.DataFrame(results)
    table_path = out_dir / "tab_results_paired_comparison_summary.csv"
    table_df.to_csv(table_path, index=False)
    
    return table_path

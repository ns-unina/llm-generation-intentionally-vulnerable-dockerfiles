import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from pathlib import Path
from .config import (
    COLORS_3,
    COLORS_4,
    COLORS_BUILD_RUN_EXPLOIT,
    FIGURE_SIZE_WIDE,
    FIGURE_SIZE_MEDIUM,
    FIGURE_SIZE_PLOT,
    FIGURE_SIZE_BOX,
    BAR_WIDTH,
    GREEN_COLOR,
    GROUP_SPACING,
    ORANGE_COLOR,
    RED_COLOR,
    SCATTER_ALPHA,
    SCATTER_EDGE_COLOR,
    SCATTER_EDGE_WIDTH,
    HIST_ALPHA,
    LEGEND_COLUMNS_DEFAULT,
    LEGEND_COLUMNS_SCATTER,
    LEGEND_TICKER_SIZE,
    BOXPLOT_SHOW_FLIERS,
    HISTOGRAM_BINS,
    TITLE_FUNCTIONAL_SUCCESS,
    TITLE_IMPACT_VS_AUTOMATION,
    TITLE_PAIRED_DELTA,
    TITLE_BOXPLOT_IMPACT,
    TITLE_BOXPLOT_AUTOMATION,
    TITLE_OVERALL_SUCCESS,
    TITLE_SERVICES_SUCCESS,
    TITLE_WEB_SUCCESS,
    TITLE_CHANGECLASS_IMPACT,
    TITLE_AUTOMATION_CHALLENGE,
    TITLE_ERROR_CATEGORY_STAGE,
    CHANGECLASS_COLORS,
    AUTOMATION_COLORS,
    FONT_DATA_LABEL_SIZE,
    GAP_BETWEEN_GROUPS,
    OVERALL_SUCCESS_FIGURE,
    SERVICES_SUCCESS_FIGURE,
    WEB_SUCCESS_FIGURE,
    CHANGECLASS_IMPACT_FIGURE,
    AUTOMATION_CHALLENGE_FIGURE,
    IMPACT_VS_AUTOMATION_FIGURE,
    PAIRED_DELTA_FIGURE,
    ERROR_CATEGORY_BUILD_FIGURE,
    ERROR_CATEGORY_RUN_FIGURE,
    ERROR_CATEGORY_EXPLOIT_FIGURE,
    FUNCTIONAL_SUCCESS_FIGURE,
    CHANGECLASS_DISTRIBUTION_FIGURE,
    AUTOMATION_DISTRIBUTION_FIGURE,
    BOXPLOT_IMPACT_FIGURE,
    BOXPLOT_AUTOMATION_FIGURE,
)

def save_figure(fig, path: Path, also_vector: bool):
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    if also_vector:
        fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
        fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def plot_chart_three_level(scenario_labels, bar_data, bool_cols, title, out_path, also_vector, total_cves=None):
    """Helper function to create a 3-level bar chart for Build/Run/Exploit."""
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)
    
    # Ensure we have colors for all metrics
    num_metrics = len(bool_cols)
    colors = COLORS_BUILD_RUN_EXPLOIT[:num_metrics] if num_metrics <= 3 else COLORS_BUILD_RUN_EXPLOIT
    
    if len(scenario_labels) == 1:
        # Single scenario: simple bar chart with all metrics
        x = range(len(bool_cols))
        ax.bar(x, [bar_data[col][0] for col in bool_cols], color=colors)
        ax.set_xticks(x)
        ax.set_xticklabels([col.title() for col in bool_cols])
    else:
        # Multiple scenarios: grouped bar chart
        x = range(len(scenario_labels))
        # Adjust width based on number of metrics (narrower for 3 bars)
        width = 0.28 / (num_metrics / 2.5) if num_metrics > 2 else 0.25
        
        for i, col in enumerate(bool_cols):
            # Center the bars around each scenario position
            offset = (i - (num_metrics - 1) / 2) * width
            ax.bar(
                [xi + offset for xi in x],
                bar_data[col],
                width=width,
                label=col.title(),
                color=colors[i],
            )
        
        ax.set_xticks(x)
        ax.set_xticklabels(scenario_labels, rotation=0)
        ax.legend()
    
    ax.set_ylabel("Number of CVEs")
    # ax.set_title(title)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Set y-axis ticks to integer values from 0 to total_cves
    if total_cves is not None:
        max_val = total_cves
    else:
        max_val = max([max(bar_data[col]) if bar_data[col] else 0 for col in bool_cols] + [0])
    ax.set_yticks(range(0, int(max_val) + 1))
    
    save_figure(fig, out_path, also_vector)
    return out_path


def plot_overall_success(df, bool_cols, out_dir, also_vector, warnings, title=None):
    """Figure 1: Overall functional success rates (Build/Run/Exploit) across all data."""
    if not bool_cols:
        warnings.append("Build/Run/Exploit columns not found; skipping overall success chart.")
        return None
    if len(bool_cols) < 3:
        warnings.append(f"Warning: Only {len(bool_cols)} metrics found for overall success: {bool_cols}")
    
    # Calculate global success counts (number of CVEs)
    bar_data = {col: [int(df[col].sum())] for col in bool_cols}
    scenario_labels = ["Overall"]
    total_cves = df['cve_id'].nunique() if 'cve_id' in df.columns else None
    
    chart_path = out_dir / OVERALL_SUCCESS_FIGURE
    return plot_chart_three_level(
        scenario_labels, bar_data, bool_cols,
        title or TITLE_OVERALL_SUCCESS,
        chart_path, also_vector, total_cves=total_cves
    )


def plot_services_success(df, bool_cols, out_dir, also_vector, warnings, title=None):
    """Figure 2a: Functional success (Build/Run/Exploit) for Services (Package vs Source)."""
    if not bool_cols:
        warnings.append("Build/Run/Exploit columns not found; skipping services success chart.")
        return None
    if len(bool_cols) < 3:
        warnings.append(f"Warning: Only {len(bool_cols)} metrics found for services: {bool_cols}")
    
    # Filter for Services dataset
    services_df = df[df["dataset"].str.lower() == "services"]
    if services_df.empty:
        warnings.append("No Services data found; skipping services success chart.")
        return None
    
    bar_data = {col: [] for col in bool_cols}
    scenario_labels = []
    
    for dtype in ["Package", "Source"]:
        subset = services_df[services_df["type"].str.lower() == dtype.lower()]
        if not subset.empty:
            scenario_labels.append(dtype)
            for col in bool_cols:
                val = int(subset[col].sum())
                bar_data[col].append(val)
    
    if not scenario_labels:
        warnings.append("No Package/Source data found for Services; skipping services success chart.")
        return None
    
    total_cves = services_df['cve_id'].nunique() if 'cve_id' in services_df.columns else None
    chart_path = out_dir / SERVICES_SUCCESS_FIGURE
    return plot_chart_three_level(
        scenario_labels, bar_data, bool_cols,
        title or TITLE_SERVICES_SUCCESS,
        chart_path, also_vector, total_cves=total_cves
    )


def plot_web_success(df, bool_cols, out_dir, also_vector, warnings, title=None):
    """Figure 2b: Functional success (Build/Run/Exploit) for Web Applications (Compose vs Source)."""
    if not bool_cols:
        warnings.append("Build/Run/Exploit columns not found; skipping web success chart.")
        return None
    if len(bool_cols) < 3:
        warnings.append(f"Warning: Only {len(bool_cols)} metrics found for web: {bool_cols}")
    
    # Filter for Web dataset
    web_df = df[df["dataset"].str.lower() == "web"]
    if web_df.empty:
        warnings.append("No Web data found; skipping web success chart.")
        return None
    
    bar_data = {col: [] for col in bool_cols}
    scenario_labels = []
    
    # Look for Compose/Bundle and Source
    for dtype in ["Compose", "Bundle", "Source"]:
        subset = web_df[web_df["type"].str.lower() == dtype.lower()]
        if not subset.empty:
            scenario_labels.append(dtype)
            for col in bool_cols:
                val = int(subset[col].sum())
                bar_data[col].append(val)
    
    if not scenario_labels:
        # Debug: show what types are available
        available_types = web_df["type"].unique().tolist()
        warnings.append(f"No Compose/Bundle/Source data found for Web. Available types: {available_types}")
        return None
    
    total_cves = web_df['cve_id'].nunique() if 'cve_id' in web_df.columns else None
    chart_path = out_dir / WEB_SUCCESS_FIGURE
    return plot_chart_three_level(
        scenario_labels, bar_data, bool_cols,
        title or TITLE_WEB_SUCCESS,
        chart_path, also_vector, total_cves=total_cves
    )


def plot_success_rate_summary(df, bool_cols, out_dir, also_vector, warnings, title=None):
    """Deprecated: Use plot_overall_success, plot_services_success, plot_web_success instead."""
    return plot_overall_success(df, bool_cols, out_dir, also_vector, warnings, title)


def plot_functional_success(agg, bool_cols, out_dir, also_vector, warnings, title=None):
    if not bool_cols:
        warnings.append("Build/Run/Exploit columns not found; skipping functional success chart.")
        return None

    types = sorted(agg["type"].dropna().unique())
    datasets = sorted(agg["dataset"].dropna().unique())
    if not types or not datasets:
        warnings.append("Missing Type or Dataset values; skipping functional success chart.")
        return None

    metrics = [f"{c}_rate" for c in bool_cols]
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

    width = BAR_WIDTH
    group_spacing = GROUP_SPACING
    x_positions = []
    labels = []
    base = 0.0
    for t in types:
        x_positions.append(base)
        labels.append(t)
        base += len(datasets) * len(metrics) * width + group_spacing

    colors = COLORS_3
    for ti, t in enumerate(types):
        base_x = x_positions[ti]
        for di, d in enumerate(datasets):
            for mi, metric in enumerate(metrics):
                subset = agg[(agg["type"] == t) & (agg["dataset"] == d)]
                if subset.empty:
                    val = 0.0
                else:
                    val = float(subset[metric].mean()) * 100.0
                x = base_x + (di * len(metrics) + mi) * width
                ax.bar(
                    x,
                    val,
                    width=width,
                    color=colors[mi % len(colors)],
                    label=f"{metric.replace('_rate','').title()} ({d})" if ti == 0 else None,
                )

    ax.set_ylabel("Success Rate (%)")
    ax.set_xticks([p + (len(datasets) * len(metrics) * width) / 2 - width for p in x_positions])
    ax.set_xticklabels(labels, rotation=0)
    # ax.set_title(title or TITLE_FUNCTIONAL_SUCCESS)
    ax.set_ylim(0, 100)
    ax.legend(ncol=LEGEND_COLUMNS_DEFAULT)

    path = out_dir / FUNCTIONAL_SUCCESS_FIGURE
    save_figure(fig, path, also_vector)
    return path


def plot_changeclass_impact_distribution(df, out_dir, also_vector, warnings, title=None):
    """Figure 3: Distribution of Change Impact classes (C0, C1, C2) by Type and Dataset as stacked percentage bar chart."""
    if "changeclass" not in df.columns or "type" not in df.columns or "dataset" not in df.columns:
        if warnings:
            warnings.append("Missing changeclass, type, or dataset column; skipping changeclass impact chart.")
        return None
    
    # Normalize changeclass to lowercase
    df = df.copy()
    df["changeclass"] = df["changeclass"].astype(str).str.strip().str.lower()
    
    # Create combined labels: "Services – Package", "Services – Source", "Web – Compose", "Web – Bundle"
    df["scenario"] = df["dataset"].str.capitalize() + " – " + df["type"]
    
    # Count occurrences of each changeclass per scenario
    counts = df.groupby(["scenario", "changeclass"]).size().reset_index(name="count")
    
    if counts.empty:
        if warnings:
            warnings.append("No changeclass data for distribution chart.")
        return None
    
    # Calculate totals per scenario
    scenario_totals = counts.groupby("scenario")["count"].sum().reset_index(name="total")
    counts = counts.merge(scenario_totals, on="scenario")
    
    # Pivot to get changeclass as columns (using counts instead of percentages)
    pivot = counts.pivot_table(index="scenario", columns="changeclass", values="count", fill_value=0)
    
    # Define the order of scenarios and changeclass categories
    scenario_order = ["Services – Package", "Services – Source", "Web – Compose", "Web – Bundle"]
    changeclass_order = ["c0", "c1", "c2"]
    
    # Filter to only scenarios that exist in data
    scenario_order = [s for s in scenario_order if s in pivot.index]
    
    # Reindex pivot table
    pivot = pivot.reindex(scenario_order)
    pivot = pivot.reindex(columns=changeclass_order, fill_value=0)
    
    # Create stacked bar chart with spacing between groups
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)
    
    # Create x positions with spacing between Services and Web groups
    x_positions = []
    x_pos = 0
    for i, scenario in enumerate(pivot.index):
        # Add gap before Web group
        if i == 2:  # Before Web – Compose
            x_pos += GAP_BETWEEN_GROUPS  # Gap between Services and Web groups
        x_positions.append(x_pos)
        x_pos += 1
    
    bottom = None
    labels = {"c0": "C0 (trivial)", "c1": "C1 (local/config)", "c2": "C2 (architectural/systemic)"}
    
    for cat in changeclass_order:
        vals = pivot[cat].values
        color = CHANGECLASS_COLORS.get(cat, "#cccccc")
        if bottom is None:
            ax.bar(x_positions, vals, label=labels[cat], color=color, width=0.6)
            bottom = vals.copy()
        else:
            ax.bar(x_positions, vals, bottom=bottom, label=labels[cat], color=color, width=0.6)
            bottom = bottom + vals
    
    ax.set_xticks(x_positions)
    
    # Create simplified labels (just type: Source, Package, Compose, Bundle)
    type_labels = []
    type_map = {"Package": "Package", "Source": "Source", "Compose": "Compose", "Bundle": "Bundle"}
    
    for scenario in pivot.index:
        # Split "Services – Package" into dataset and type
        parts = scenario.split(" – ")
        if len(parts) == 2:
            dataset, type_ = parts
            type_labels.append(type_map.get(type_, type_))
        else:
            type_labels.append(scenario)
    
    ax.set_xticklabels(type_labels, rotation=0)
    
    # Add dataset labels (Services, Web) centered above groups
    if len(x_positions) >= 2:
        # Services center (between Package and Source)
        services_center = (x_positions[0] + x_positions[1]) / 2
        ax.text(services_center, ax.get_ylim()[1] * 0.95, "Services", 
                ha='center', va='top', style='italic', fontsize=11, weight='normal')
    
    if len(x_positions) >= 4:
        # Web center (between Compose and Bundle)
        web_center = (x_positions[2] + x_positions[3]) / 2
        ax.text(web_center, ax.get_ylim()[1] * 0.95, "Web", 
                ha='center', va='top', style='italic', fontsize=11, weight='normal')
    
    ax.set_ylabel("Count")
    # ax.set_title(title or TITLE_CHANGECLASS_IMPACT)
    ax.legend()
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    chart_path = out_dir / CHANGECLASS_IMPACT_FIGURE
    save_figure(fig, chart_path, also_vector)
    return chart_path


def plot_automation_challenge_distribution(df, out_dir, also_vector, warnings, title=None):
    """Figure 4: Distribution of Automation Challenge classes (A0, A1, A2) by Type and Dataset as stacked percentage bar chart."""
    if "automationchallenge" not in df.columns or "type" not in df.columns or "dataset" not in df.columns:
        if warnings:
            warnings.append("Missing automationchallenge, type, or dataset column; skipping automation challenge chart.")
        return None
    
    # Normalize automationchallenge to lowercase
    df = df.copy()
    df["automationchallenge"] = df["automationchallenge"].astype(str).str.strip().str.lower()
    
    # Create combined labels: "Services – Package", "Services – Source", "Web – Compose", "Web – Bundle"
    df["scenario"] = df["dataset"].str.capitalize() + " – " + df["type"]
    
    # Count occurrences of each automationchallenge per scenario
    counts = df.groupby(["scenario", "automationchallenge"]).size().reset_index(name="count")
    
    if counts.empty:
        if warnings:
            warnings.append("No automationchallenge data for distribution chart.")
        return None
    
    # Calculate totals per scenario
    scenario_totals = counts.groupby("scenario")["count"].sum().reset_index(name="total")
    counts = counts.merge(scenario_totals, on="scenario")
    
    # Pivot to get automationchallenge as columns (using counts instead of percentages)
    pivot = counts.pivot_table(index="scenario", columns="automationchallenge", values="count", fill_value=0)
    
    # Define the order of scenarios and automationchallenge categories
    scenario_order = ["Services – Package", "Services – Source", "Web – Compose", "Web – Bundle"]
    automation_order = ["a0", "a1", "a2"]
    
    # Filter to only scenarios that exist in data
    scenario_order = [s for s in scenario_order if s in pivot.index]
    
    # Reindex pivot table
    pivot = pivot.reindex(scenario_order)
    pivot = pivot.reindex(columns=automation_order, fill_value=0)
    
    # Create stacked bar chart with spacing between groups
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)
    
    # Create x positions with spacing between Services and Web groups
    x_positions = []
    x_pos = 0
    for i, scenario in enumerate(pivot.index):
        # Add gap before Web group
        if i == 2:  # Before Web – Compose
            x_pos += 1.5  # Gap between Services and Web groups
        x_positions.append(x_pos)
        x_pos += 1
    
    bottom = None
    labels = {"a0": "A0 — Easily automatable", "a1": "A1 — Partially automatable", "a2": "A2 — Hard to automate"}
    
    for cat in automation_order:
        vals = pivot[cat].values
        color = AUTOMATION_COLORS.get(cat, "#cccccc")
        if bottom is None:
            ax.bar(x_positions, vals, label=labels[cat], color=color, width=0.6)
            bottom = vals.copy()
        else:
            ax.bar(x_positions, vals, bottom=bottom, label=labels[cat], color=color, width=0.6)
            bottom = bottom + vals
    
    ax.set_xticks(x_positions)
    
    # Create simplified labels (just type: Source, Package, Compose, Bundle)
    type_labels = []
    type_map = {"Package": "Package", "Source": "Source", "Compose": "Compose", "Bundle": "Bundle"}
    
    for scenario in pivot.index:
        # Split "Services – Package" into dataset and type
        parts = scenario.split(" – ")
        if len(parts) == 2:
            dataset, type_ = parts
            type_labels.append(type_map.get(type_, type_))
        else:
            type_labels.append(scenario)
    
    ax.set_xticklabels(type_labels, rotation=0)
    
    # Add dataset labels (Services, Web) centered above groups
    if len(x_positions) >= 2:
        # Services center (between Package and Source)
        services_center = (x_positions[0] + x_positions[1]) / 2
        ax.text(services_center, ax.get_ylim()[1] * 0.95, "Services", 
                ha='center', va='top', style='italic', fontsize=11, weight='normal')
    
    if len(x_positions) >= 4:
        # Web center (between Compose and Bundle)
        web_center = (x_positions[2] + x_positions[3]) / 2
        ax.text(web_center, ax.get_ylim()[1] * 0.95, "Web", 
                ha='center', va='top', style='italic', fontsize=11, weight='normal')
    
    ax.set_ylabel("Count")
    # ax.set_title(title or TITLE_AUTOMATION_CHALLENGE)
    ax.legend()
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    chart_path = out_dir / AUTOMATION_CHALLENGE_FIGURE
    save_figure(fig, chart_path, also_vector)
    return chart_path


def plot_stacked_distribution(df, column, out_path, title=None, also_vector=False, warnings=None):
    if warnings is None:
        warnings = []
    if column not in df.columns:
        warnings.append(f"Missing {column} column; skipping {title or 'chart'} chart.")
        return None

    counts = (
        df.groupby(["type", column], dropna=False)
        .size()
        .reset_index(name="count")
    )
    if counts.empty:
        warnings.append(f"No data for {title or 'chart'} chart.")
        return None

    pivot = counts.pivot_table(index="type", columns=column, values="count", fill_value=0)
    pivot = pivot.reindex(sorted(pivot.index), axis=0)
    categories = list(pivot.columns)

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_MEDIUM)
    bottom = None
    colors = COLORS_4
    for i, cat in enumerate(categories):
        vals = pivot[cat].values
        if bottom is None:
            ax.bar(pivot.index, vals, color=colors[i % len(colors)], label=str(cat))
            bottom = vals
        else:
            ax.bar(pivot.index, vals, bottom=bottom, color=colors[i % len(colors)], label=str(cat))
            bottom = bottom + vals

    # ax.set_title(title or "Distribution by Type")
    ax.set_ylabel("Count")
    ax.set_xlabel("Type")
    ax.legend()
    save_figure(fig, out_path, also_vector)
    return out_path


def plot_scatter(agg, out_path, also_vector, warnings, title=None):
    if agg.empty:
        warnings.append("No aggregated data for scatter plot.")
        return None

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_PLOT)
    types = sorted(agg["type"].dropna().unique())
    datasets = sorted(agg["dataset"].dropna().unique())
    colors = COLORS_4
    markers = ["o", "s", "D", "^"]

    for ti, t in enumerate(types):
        for di, d in enumerate(datasets):
            subset = agg[(agg["type"] == t) & (agg["dataset"] == d)]
            if subset.empty:
                continue
            ax.scatter(
                subset["TotalImpact"],
                subset["TotalAutomation"],
                color=colors[ti % len(colors)],
                marker=markers[di % len(markers)],
                label=f"{t} / {d}",
                alpha=SCATTER_ALPHA,
                edgecolors=SCATTER_EDGE_COLOR,
                linewidths=SCATTER_EDGE_WIDTH,
            )

    # ax.set_title(title or TITLE_IMPACT_VS_AUTOMATION)
    ax.set_xlabel("Total Change Impact")
    ax.set_ylabel("Total Automation Difficulty")
    ax.legend(ncol=LEGEND_COLUMNS_SCATTER, fontsize=LEGEND_TICKER_SIZE)
    
    # Calculate medians for quadrant division
    median_impact = agg["TotalImpact"].median()
    median_automation = agg["TotalAutomation"].median()
    
    # Draw quadrant lines
    ax.axvline(median_impact, color="gray", linestyle="--", linewidth=1, alpha=0.5)
    ax.axhline(median_automation, color="gray", linestyle="--", linewidth=1, alpha=0.5)
    
    # Get axis limits for label positioning
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    
    # Calculate label positions at center of each quadrant
    x_low = (x_min + median_impact) / 2
    x_high = (median_impact + x_max) / 2
    y_low = (y_min + median_automation) / 2
    y_high = (median_automation + y_max) / 2
    
    quadrant_labels = [
        (x_low, y_low, "Easy"),
        (x_high, y_low, "Engineering-difficult"),
        (x_low, y_high, "Automation-difficult"),
        (x_high, y_high, "Hard"),
    ]
    
    for x, y, label in quadrant_labels:
        ax.text(x, y, label, fontsize=9, alpha=0.6, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.3, edgecolor="none"))
    
    save_figure(fig, out_path, also_vector)
    return out_path


def plot_boxplots(agg, out_dir, also_vector, warnings, title_impact=None, title_automation=None):
    if agg.empty or "type" not in agg.columns:
        warnings.append("No data for boxplots.")
        return []

    paths = []
    for metric, default_label, fname in [
        ("TotalImpact", TITLE_BOXPLOT_IMPACT, BOXPLOT_IMPACT_FIGURE),
        ("TotalAutomation", TITLE_BOXPLOT_AUTOMATION, BOXPLOT_AUTOMATION_FIGURE),
    ]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_BOX)
        data = []
        labels = []
        for t in sorted(agg["type"].dropna().unique()):
            vals = agg[agg["type"] == t][metric].dropna().values
            if len(vals) == 0:
                continue
            data.append(vals)
            labels.append(t)
        if not data:
            warnings.append(f"No data for {metric} boxplot.")
            continue
        
        # Use custom title if provided
        if metric == "TotalImpact" and title_impact:
            plot_title = title_impact
        elif metric == "TotalAutomation" and title_automation:
            plot_title = title_automation
        else:
            plot_title = default_label
        
        ax.boxplot(data, labels=labels, showfliers=BOXPLOT_SHOW_FLIERS)
        # ax.set_title(plot_title)
        ax.set_ylabel(metric)
        path = out_dir / fname
        save_figure(fig, path, also_vector)
        paths.append(path)
    return paths


def plot_error_category_by_stage(df, out_dir, also_vector, warnings, title=None):
    """Figure 7: Error category frequency by stage (Build, Run, Exploit) - 3 separate figures with taxonomy codes."""
    if "stage" not in df.columns or "categoryname" not in df.columns:
        if warnings:
            warnings.append("Missing stage or categoryname column; skipping error category chart.")
        return None
    
    # Define error taxonomy mapping (matching actual data format in Excel files)
    taxonomy_mapping = {
        # Build errors (using "/" as in the data)
        "Invalid/obsolete base image": "B1",
        "Missing/obsolete package version": "B2",
        "Missing build dependencies / toolchain": "B3",
        "External resource not found (URL, mirror)": "B4",
        "Build-from-source / compilation failure": "B5",
        "Repository configuration failure": "B6",
        "Compress files without validity checks.": "B7",  # Note: has period at end
        # Run errors
        "Service not started / container exits": "R1",
        "Runtime misconfiguration (config files, env vars)": "R2",
        "Runtime misconfiguration": "R2",  # Alternative format without parentheses
        "Missing runtime dependencies": "R3",
        "Missing multi-service orchestration": "R4",  # Changed from R5 to R4 to match taxonomy
        # Exploitability errors
        "Not actually vulnerable / patched version": "E1",
        "Configuration prerequisites not met": "E2",
        "Exploit requires missing external service or application": "E3",
        "Endpoint unavailable / connection refused": "E4",
        "Exploit script mismatch or assumption violation": "E5",
        "Contextual prerequisites not met": "E6",
    }
    
    # Normalize stage values
    df = df.copy()
    df["stage"] = df["stage"].astype(str).str.strip().str.lower()
    df["categoryname"] = df["categoryname"].astype(str).str.strip()
    
    # Map category names to taxonomy codes FIRST
    df["category_code"] = df["categoryname"].map(taxonomy_mapping)
    
    # Filter rows with valid category codes
    df = df[df["category_code"].notna()]
    
    if df.empty:
        if warnings:
            warnings.append("No valid categories found in taxonomy mapping.")
        return None
    
    # Create reverse mapping (code -> canonical name) to normalize category names
    code_to_canonical_name = {
        "B1": "Invalid/obsolete base image",
        "B2": "Missing/obsolete package version",
        "B3": "Missing build dependencies / toolchain",
        "B4": "External resource not found (URL, mirror)",
        "B5": "Build-from-source / compilation failure",
        "B6": "Repository configuration failure",
        "B7": "Compress files without validity checks",
        "R1": "Service not started / container exits",
        "R2": "Runtime misconfiguration (config files, env vars)",
        "R3": "Missing runtime dependencies",
        "R4": "Missing multi-service orchestration",
        "E1": "Not actually vulnerable / patched version",
        "E2": "Configuration prerequisites not met",
        "E3": "Exploit requires missing external service or application",
        "E4": "Endpoint unavailable / connection refused",
        "E5": "Exploit script mismatch or assumption violation",
        "E6": "Contextual prerequisites not met",
    }
    
    # Normalize category names based on their code
    df["categoryname_normalized"] = df["category_code"].map(code_to_canonical_name)
    
    # Determine the correct stage based on category code prefix
    def get_stage_from_code(code):
        if code.startswith('B'):
            return 'Build'
        elif code.startswith('R'):
            return 'Run'
        elif code.startswith('E'):
            return 'Exploit'
        return None
    
    df["stage_norm"] = df["category_code"].apply(get_stage_from_code)
    df = df[df["stage_norm"].notna()]
    
    if df.empty:
        if warnings:
            warnings.append("No valid stage values found.")
        return None
    
    # Count error categories per stage using normalized names
    counts = df.groupby(["stage_norm", "category_code", "categoryname_normalized"]).size().reset_index(name="count")
    
    # Create 3 separate figures (one for each stage)
    stage_order = ["Build", "Run", "Exploit"]
    stage_files = {"Build": ERROR_CATEGORY_BUILD_FIGURE, "Run": ERROR_CATEGORY_RUN_FIGURE, "Exploit": ERROR_CATEGORY_EXPLOIT_FIGURE}
    
    # Color palette for consistency
    # import matplotlib.cm as cm
    # colors = cm.Set3(range(12))  # Using Set3 for softer colors
    
    chart_paths = []
    
    for stage in stage_order:
        stage_data = counts[counts["stage_norm"] == stage].copy()
        
        if stage_data.empty:
            continue
        
        # Sort by count descending
        stage_data = stage_data.sort_values("count", ascending=True)  # ascending for horizontal bars
        
        # Create labels combining code and description using normalized names
        stage_data["label"] = stage_data.apply(
            lambda row: f"{row['category_code']}: {row['categoryname_normalized']}", axis=1
        )
        
        # Create individual figure
        fig, ax = plt.subplots(figsize=(12, max(6, len(stage_data) * 0.5)))
        
        # Create horizontal bar chart
        selected_color = GREEN_COLOR if stage == "Build" else ORANGE_COLOR if stage == "Run" else RED_COLOR
                  
        bars = ax.barh(
            stage_data["label"],
            stage_data["count"],
            color=[selected_color for i in range(len(stage_data))],
            edgecolor="black",
            linewidth=0.5,
        )
        ax.set_yticklabels(stage_data["label"], fontweight='bold', fontsize=11)
        
        # ax.set_title(f"", fontsize=12, fontweight="bold")
        ax.set_xlabel("Number of Errors", fontsize=14, fontweight="bold")
        # ax.set_ylabel("Build Error Category" if stage == "Build" else ("Run Error Category" if stage == "Run" else "Exploit Error Category"))
        ax.set_ylabel("")
        ax.grid(axis="x", alpha=0.3, linestyle="--")
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                   f"{int(width)}",
                   ha="left", va="center", fontsize=12, fontweight="bold")
        
        plt.tight_layout()
        
        chart_path = out_dir / stage_files[stage]
        save_figure(fig, chart_path, also_vector)
        chart_paths.append(chart_path)
        plt.close(fig)
    
    return chart_paths



def plot_paired_delta_hist(agg, out_path, also_vector, warnings, title=None):
    if agg.empty:
        warnings.append("No aggregated data for paired comparison.")
        return None

    def build_pairs(dataset_label, type_a, type_b):
        subset = agg[(agg["dataset"] == dataset_label) & (agg["type"].isin([type_a, type_b]))]
        if subset.empty:
            return None
        pivot = (
            subset.groupby(["cve_id", "type"], dropna=False)[["TotalImpact", "TotalAutomation"]]
            .sum()
            .reset_index()
            .pivot(index="cve_id", columns="type", values=["TotalImpact", "TotalAutomation"])
        )
        if pivot.empty:
            return None
        types = list(pivot.columns.levels[1])
        if type_a not in types or type_b not in types:
            return None
        impact = pivot["TotalImpact"][[type_a, type_b]].dropna()
        automation = pivot["TotalAutomation"][[type_a, type_b]].dropna()
        return {"impact": impact, "automation": automation}

    # Services: Package vs Source
    services_pair = build_pairs("Services", "Package", "Source")

    # Web: Compose vs Source (fallback to Compose vs Bundle if Source missing)
    web_pair = build_pairs("Web", "Compose", "Source")
    web_label = "Web: Compose vs Source"
    if web_pair is None:
        web_pair = build_pairs("Web", "Compose", "Bundle")
        web_label = "Web: Compose vs Bundle"
        if web_pair is not None:
            warnings.append("Web Source not found; using Compose vs Bundle for paired comparison.")

    if services_pair is None and web_pair is None:
        warnings.append("No paired CVEs for paired comparison.")
        return None

    def plot_dumbbell(ax, df_metric, type_a, type_b, metric_label, panel_title):
        if df_metric is None or df_metric.empty:
            # ax.set_title(panel_title)
            ax.text(0.5, 0.5, "No paired CVEs", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
            return
        df_metric = df_metric.copy()
        df_metric["delta"] = df_metric[type_b] - df_metric[type_a]
        df_metric = df_metric.sort_values("delta")
        df_plot = df_metric.reset_index()
        y_positions = range(len(df_plot))
        ax.hlines(y_positions, df_plot[type_a], df_plot[type_b], color="gray", alpha=0.5, linewidth=1)

        # Split points where values overlap to avoid occlusion
        equal_mask = df_plot[type_a] == df_plot[type_b]
        not_equal_mask = ~equal_mask

        if not_equal_mask.any():
            ax.scatter(
                df_plot.loc[not_equal_mask, type_a],
                df_plot.index[not_equal_mask],
                color=COLORS_4[0],
                label=type_a,
                zorder=3,
            )
            ax.scatter(
                df_plot.loc[not_equal_mask, type_b],
                df_plot.index[not_equal_mask],
                color=COLORS_4[1],
                label=type_b,
                zorder=3,
            )

        if equal_mask.any():
            for idx, row in df_plot.loc[equal_mask].iterrows():
                x_val = row[type_a]
                y_val = idx
                # Draw a half-and-half marker (left/right) when points overlap
                ax.plot(
                    x_val,
                    y_val,
                    marker="o",
                    markersize=7,
                    markerfacecolor=COLORS_4[0],
                    markerfacecoloralt=COLORS_4[1],
                    fillstyle="left",
                    markeredgecolor="black",
                    linestyle="None",
                    zorder=4,
                )
        ax.set_yticks(list(y_positions))
        ax.set_yticklabels(df_plot["cve_id"])
        ax.set_xlabel(metric_label)
        # ax.set_title(panel_title)
        ax.legend(loc="best", fontsize=9)
        ax.grid(axis="x", alpha=0.3, linestyle="--")
        ax.tick_params(axis="y", labelsize=8)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))


    # Determine figure size based on max CVE count
    max_len = 0
    for pair in [services_pair, web_pair]:
        if pair is None:
            continue
        max_len = max(max_len, len(pair["impact"]), len(pair["automation"]))
    fig_height = max(5, 0.25 * max_len + 2)

    fig, axes = plt.subplots(2, 2, figsize=(12, fig_height), sharex=False)

    # Services panels
    if services_pair is not None:
        plot_dumbbell(
            axes[0, 0],
            services_pair["impact"],
            "Package",
            "Source",
            "Total Change Impact",
            "Services: Package vs Source (Impact)",
        )
        plot_dumbbell(
            axes[1, 0],
            services_pair["automation"],
            "Package",
            "Source",
            "Total Automation Difficulty",
            "Services: Package vs Source (Automation)",
        )
    else:
        axes[0, 0].axis("off")
        axes[1, 0].axis("off")

    # Web panels
    if web_pair is not None:
        type_a, type_b = ("Compose", "Source") if "Source" in web_label else ("Compose", "Bundle")
        plot_dumbbell(
            axes[0, 1],
            web_pair["impact"],
            type_a,
            type_b,
            "Total Change Impact",
            f"{web_label} (Impact)",
        )
        plot_dumbbell(
            axes[1, 1],
            web_pair["automation"],
            type_a,
            type_b,
            "Total Automation Difficulty",
            f"{web_label} (Automation)",
        )
    else:
        axes[0, 1].axis("off")
        axes[1, 1].axis("off")

    # fig.suptitle(title or TITLE_PAIRED_DELTA, y=0.98)
    fig.tight_layout()
    save_figure(fig, out_path, also_vector)
    return out_path

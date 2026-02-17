"""
Phase 1 Analysis - Weighted Error Score (WES) Calculation

This script calculates the Weighted Error Score (WES) for Docker image builds.

WES Formula:
- ExecPenalty = 0 if build=1 & run=1 (success)
- ExecPenalty = 1 if build=1 & run=0 (runtime failure)
- ExecPenalty = 2 if build=0 (build failure)
- Score = α * ExecPenalty + fix_level
- where α = 3 (default multiplier to ensure hierarchy)

Score Interpretation:
- 0: Perfect execution (build=1, run=1, fix=0)
- 1-2: Success with minor/major fixes
- 4-5: Runtime failure with fixes
- 7-8: Build failure with fixes
"""

import pandas as pd
import numpy as np
from pathlib import Path


def calculate_wes(build, run, fix_level, alpha=3):
    """
    Calculate Weighted Error Score (WES).
    
    Parameters:
    -----------
    build : int
        Build status (1 = success, 0 = failure)
    run : int
        Run status (1 = success, 0 = failure)
    fix_level : int
        Fix effort level (0 = no fix, 1 = minor fix, 2 = major fix)
    alpha : int
        Multiplier for execution penalty (default=3)
    
    Returns:
    --------
    int : Weighted Error Score
    """
    # Calculate execution penalty
    if build == 1 and run == 1:
        exec_penalty = 0
    elif build == 1 and run == 0:
        exec_penalty = 1
    else:  # build == 0
        exec_penalty = 2
    
    # Calculate WES
    wes = alpha * exec_penalty + fix_level
    
    return wes


def analyze_phase1_results(filepath, alpha=3):
    """
    Analyze Phase 1 results and calculate WES for each entry.
    
    Parameters:
    -----------
    filepath : str or Path
        Path to Phase1_Results.xlsx file
    alpha : int
        Multiplier for execution penalty (default=3)
    
    Returns:
    --------
    pd.DataFrame : Original data with added WES column and analysis
    """
    # Read the Excel file
    df = pd.read_excel(filepath)
    
    # Display first few rows to understand structure
    print("First few rows of Phase1_Results.xlsx:")
    print(df.head())
    print(f"\nColumn names: {df.columns.tolist()}")
    print(f"\nData shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
    
    # Try to identify the correct column names (case-insensitive matching)
    col_mapping = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'build' in col_lower:
            col_mapping['build'] = col
        elif 'run' in col_lower:
            col_mapping['run'] = col
        elif 'fix' in col_lower or 'error' in col_lower or 'level' in col_lower:
            col_mapping['fix_level'] = col
        elif 'cve' in col_lower:
            col_mapping['cve'] = col
        elif 'model' in col_lower:
            col_mapping['model'] = col
    
    print(f"\nIdentified columns: {col_mapping}")
    
    # Calculate WES for each row
    df['WES'] = df.apply(
        lambda row: calculate_wes(
            row[col_mapping['build']], 
            row[col_mapping['run']], 
            row[col_mapping['fix_level']], 
            alpha
        ),
        axis=1
    )
    
    # Add categorical labels for better understanding
    def categorize_wes(wes):
        if wes == 0:
            return "Perfect"
        elif wes <= 2:
            return "Success with fixes"
        elif wes <= 5:
            return "Runtime failure"
        else:
            return "Build failure"
    
    df['WES_Category'] = df['WES'].apply(categorize_wes)
    
    return df, col_mapping


def generate_summary_statistics(df, col_mapping):
    """
    Generate summary statistics for WES analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with calculated WES
    col_mapping : dict
        Mapping of logical column names to actual column names
    
    Returns:
    --------
    dict : Summary statistics
    """
    summary = {}
    
    # Overall statistics
    summary['total_entries'] = len(df)
    summary['mean_wes'] = df['WES'].mean()
    summary['median_wes'] = df['WES'].median()
    summary['std_wes'] = df['WES'].std()
    
    # Distribution by WES value
    summary['wes_distribution'] = df['WES'].value_counts().sort_index().to_dict()
    
    # Distribution by category
    summary['category_distribution'] = df['WES_Category'].value_counts().to_dict()
    
    # Statistics by model (if available)
    if 'model' in col_mapping:
        summary['wes_by_model'] = df.groupby(col_mapping['model'])['WES'].agg(['mean', 'median', 'count']).to_dict()
    
    # Build/Run success rates
    summary['build_success_rate'] = (df[col_mapping['build']] == 1).mean()
    summary['run_success_rate'] = (df[col_mapping['run']] == 1).mean()
    
    # Perfect execution rate (WES = 0)
    summary['perfect_rate'] = (df['WES'] == 0).mean()
    
    return summary


def generate_model_comparison_table(df, col_mapping, output_dir=None):
    """
    Generate LaTeX table comparing legacy (2024) vs modern (2026) models.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with Phase 1 results and WES scores
    col_mapping : dict
        Mapping of logical column names to actual column names
    output_dir : Path or None
        Directory to save the table (if None, only prints)
    
    Returns:
    --------
    str : LaTeX table code
    """
    # Define model groups
    legacy_models = ['Bing', 'Gemini', 'Gpt3.5']
    modern_models = ['Gemini3-Pro', 'Gpt5.2-Thinking', 'Gpt5.2-Thinking-Web']
    
    # Filter data by model groups
    model_col = col_mapping.get('model', 'Model')
    legacy_data = df[df[model_col].isin(legacy_models)]
    modern_data = df[df[model_col].isin(modern_models)]
    
    # Calculate metrics for each group
    def calculate_metrics(data, col_mapping):
        build_col = col_mapping.get('build', 'Build')
        run_col = col_mapping.get('run', 'Run')
        
        total = len(data)
        
        # Build failure rate
        build_failures = (data[build_col] == 0).sum()
        build_failure_rate = (build_failures / total) * 100 if total > 0 else 0
        
        # Runtime failure rate (build succeeded but run failed)
        runtime_data = data[data[build_col] == 1]
        total_builds_succeeded = len(runtime_data)
        runtime_failures = (runtime_data[run_col] == 0).sum() if total_builds_succeeded > 0 else 0
        runtime_failure_rate = (runtime_failures / total_builds_succeeded) * 100 if total_builds_succeeded > 0 else 0
        
        # Perfect execution rate (WES = 0)
        perfect_count = (data['WES'] == 0).sum()
        perfect_rate = (perfect_count / total) * 100 if total > 0 else 0
        
        # Mean WES
        mean_wes = data['WES'].mean()
        
        return {
            'build_failures': build_failures,
            'total': total,
            'build_failure_rate': build_failure_rate,
            'runtime_failures': runtime_failures,
            'total_builds_succeeded': total_builds_succeeded,
            'runtime_failure_rate': runtime_failure_rate,
            'perfect_count': perfect_count,
            'perfect_rate': perfect_rate,
            'mean_wes': mean_wes
        }
    
    legacy_metrics = calculate_metrics(legacy_data, col_mapping)
    modern_metrics = calculate_metrics(modern_data, col_mapping)
    
    # Generate LaTeX table
    latex_lines = []
    latex_lines.append(r"\begin{table}[t]")
    latex_lines.append(r"\centering")
    latex_lines.append(r"\caption{Comparison of execution outcomes between legacy (2024) and modern (2026) models in Phase 1.}")
    latex_lines.append(r"\label{tab:phase1_generation_comparison}")
    latex_lines.append(r"\begin{tabular*}{\tblwidth}{@{} LLL@{} }")
    latex_lines.append(r"\toprule")
    latex_lines.append(r"Outcome & Legacy (2024) & Modern (2026) \\")
    latex_lines.append(r"\midrule")
    
    # Build failure rate with counts
    legacy_bf = f"{legacy_metrics['build_failures']}/{legacy_metrics['total']} ({legacy_metrics['build_failure_rate']:.1f}\\%)"
    modern_bf = f"{modern_metrics['build_failures']}/{modern_metrics['total']} ({modern_metrics['build_failure_rate']:.1f}\\%)"
    latex_lines.append(f"Build failure rate & {legacy_bf} & {modern_bf} \\\\")
    
    # Runtime failure rate with counts
    legacy_rf = f"{legacy_metrics['runtime_failures']}/{legacy_metrics['total_builds_succeeded']} ({legacy_metrics['runtime_failure_rate']:.1f}\\%)"
    modern_rf = f"{modern_metrics['runtime_failures']}/{modern_metrics['total_builds_succeeded']} ({modern_metrics['runtime_failure_rate']:.1f}\\%)"
    latex_lines.append(f"Runtime failure rate & {legacy_rf} & {modern_rf} \\\\")
    
    # Perfect execution rate with counts
    legacy_pe = f"{legacy_metrics['perfect_count']}/{legacy_metrics['total']} ({legacy_metrics['perfect_rate']:.1f}\\%)"
    modern_pe = f"{modern_metrics['perfect_count']}/{modern_metrics['total']} ({modern_metrics['perfect_rate']:.1f}\\%)"
    latex_lines.append(f"Perfect execution rate & {legacy_pe} & {modern_pe} \\\\")
    
    # Mean WES
    latex_lines.append(f"Mean WES & {legacy_metrics['mean_wes']:.2f} & {modern_metrics['mean_wes']:.2f} \\\\")
    
    latex_lines.append(r"\bottomrule")
    latex_lines.append(r"\end{tabular*}")
    latex_lines.append(r"\end{table}")
    
    latex_table = "\n".join(latex_lines)
    
    # Print to console
    print("\n" + "="*60)
    print("PHASE 1 MODEL COMPARISON TABLE (LaTeX)")
    print("="*60)
    print(latex_table)
    
    # Save to file if output_dir is specified
    if output_dir is not None:
        output_path = Path(output_dir) / "tab_phase1_model_comparison.tex"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(latex_table)
        print(f"\nTable saved to: {output_path}")
    
    # Also print summary statistics
    print("\n" + "="*60)
    print("DETAILED METRICS")
    print("="*60)
    print(f"\nLegacy Models (2024): {', '.join(legacy_models)}")
    print(f"  Samples: {len(legacy_data)}")
    print(f"  Build failure rate: {legacy_metrics['build_failures']}/{legacy_metrics['total']} ({legacy_metrics['build_failure_rate']:.1f}%)")
    print(f"  Runtime failure rate: {legacy_metrics['runtime_failures']}/{legacy_metrics['total_builds_succeeded']} ({legacy_metrics['runtime_failure_rate']:.1f}%)")
    print(f"  Perfect execution rate: {legacy_metrics['perfect_count']}/{legacy_metrics['total']} ({legacy_metrics['perfect_rate']:.1f}%)")
    print(f"  Mean WES: {legacy_metrics['mean_wes']:.2f}")
    
    print(f"\nModern Models (2026): {', '.join(modern_models)}")
    print(f"  Samples: {len(modern_data)}")
    print(f"  Build failure rate: {modern_metrics['build_failures']}/{modern_metrics['total']} ({modern_metrics['build_failure_rate']:.1f}%)")
    print(f"  Runtime failure rate: {modern_metrics['runtime_failures']}/{modern_metrics['total_builds_succeeded']} ({modern_metrics['runtime_failure_rate']:.1f}%)")
    print(f"  Perfect execution rate: {modern_metrics['perfect_count']}/{modern_metrics['total']} ({modern_metrics['perfect_rate']:.1f}%)")
    print(f"  Mean WES: {modern_metrics['mean_wes']:.2f}")
    
    return latex_table


def generate_error_taxonomy_table(output_dir=None):
    """
    Generate LaTeX table for error taxonomy (Build, Run, Exploitability).
    
    Parameters:
    -----------
    output_dir : Path or None
        Directory to save the table (if None, only prints)
    
    Returns:
    --------
    str : LaTeX table code
    """
    # Define error taxonomy
    taxonomy = {
        "Build errors": [
            ("B1", "Invalid or obsolete base image"),
            ("B2", "Missing or obsolete package version"),
            ("B3", "Missing build dependencies or toolchain"),
            ("B4", "External resource not found (URL, mirror)"),
            ("B5", "Build-from-source or compilation failure"),
            ("B6", "Repository configuration failure"),
            ("B7", "Compress files without validity checks"),
        ],
        "Run errors": [
            ("R1", "Service not started or container exits"),
            ("R2", "Runtime misconfiguration (config files, env vars)"),
            ("R3", "Missing runtime dependencies"),
            ("R4", "Missing multi-service orchestration"),
        ],
        "Exploitability errors": [
            ("E1", "Not actually vulnerable or patched version"),
            ("E2", "Configuration prerequisites not met"),
            ("E3", "Missing external service or application"),
            ("E4", "Endpoint unavailable or connection refused"),
            ("E5", "Exploit script mismatch or assumption violation"),
            ("E6", "Contextual prerequisites not met"),
        ]
    }
    
    # Generate LaTeX table
    latex_lines = []
    latex_lines.append(r"\begin{table}[t]")
    latex_lines.append(r"\centering")
    latex_lines.append(r"\caption{Build, run, and exploitability error taxonomy (a posteriori).}")
    latex_lines.append(r"\label{tab:taxonomy_errors}")
    latex_lines.append(r"\begin{tabular*}{\tblwidth}{@{}LL@{}}")
    latex_lines.append(r"\toprule")
    latex_lines.append(r"Category & Description \\")
    latex_lines.append(r"\midrule")
    
    for category_idx, (category, items) in enumerate(taxonomy.items()):
        # Add category header
        latex_lines.append(rf"\multicolumn{{2}}{{c}}{{\textbf{{{category}}}}} \\")
        
        # Add items for this category
        for code, description in items:
            latex_lines.append(f"{code} & {description} \\\\")
        
        # Add midrule between categories (except after the last one)
        if category_idx < len(taxonomy) - 1:
            latex_lines.append(r"\midrule")
    
    latex_lines.append(r"\bottomrule")
    latex_lines.append(r"\end{tabular*}")
    latex_lines.append(r"\end{table}")
    
    latex_table = "\n".join(latex_lines)
    
    # Print to console
    print("\n" + "="*60)
    print("ERROR TAXONOMY TABLE (LaTeX)")
    print("="*60)
    print(latex_table)
    
    # Save to file if output_dir is specified
    if output_dir is not None:
        output_path = Path(output_dir) / "tab_taxonomy_errors.tex"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(latex_table)
        print(f"\nTable saved to: {output_path}")
    
    return latex_table


def print_summary(summary):
    """Print formatted summary statistics."""
    print("\n" + "="*60)
    print("WEIGHTED ERROR SCORE (WES) ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\nTotal entries: {summary['total_entries']}")
    print(f"Mean WES: {summary['mean_wes']:.2f}")
    print(f"Median WES: {summary['median_wes']:.2f}")
    print(f"Std Dev WES: {summary['std_wes']:.2f}")
    
    print(f"\nBuild success rate: {summary['build_success_rate']*100:.1f}%")
    print(f"Run success rate: {summary['run_success_rate']*100:.1f}%")
    print(f"Perfect execution rate (WES=0): {summary['perfect_rate']*100:.1f}%")
    
    print("\nWES Distribution:")
    for wes_score, count in sorted(summary['wes_distribution'].items()):
        percentage = (count / summary['total_entries']) * 100
        print(f"  WES {wes_score}: {count} ({percentage:.1f}%)")
    
    print("\nCategory Distribution:")
    for category, count in summary['category_distribution'].items():
        percentage = (count / summary['total_entries']) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")
    
    if 'wes_by_model' in summary and summary['wes_by_model']:
        print("\nWES by Model:")
        for stat_type, model_stats in summary['wes_by_model'].items():
            if stat_type == 'mean':
                print(f"\n  Mean WES:")
                for model, value in model_stats.items():
                    print(f"    {model}: {value:.2f}")


def main():
    """Main execution function."""
    # Set up paths
    script_dir = Path(__file__).parent
    results_file = script_dir / "Phase1_Results_with_WES.csv"
    
    # Check if file exists
    if not results_file.exists():
        # Try Excel file
        results_file = script_dir / "Phase1_Results.xlsx"
        if not results_file.exists():
            print(f"Error: Could not find Phase1_Results files")
            return
        # Analyze results with default alpha=3
        df, col_mapping = analyze_phase1_results(results_file, alpha=3)
    else:
        # Read CSV directly
        df = pd.read_csv(results_file)
        # Identify column mapping
        col_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'build' in col_lower:
                col_mapping['build'] = col
            elif 'run' in col_lower:
                col_mapping['run'] = col
            elif 'model' in col_lower:
                col_mapping['model'] = col
    
    print(f"Reading Phase 1 results from: {results_file}")
    
    # Generate summary statistics
    summary = generate_summary_statistics(df, col_mapping)
    
    # Print summary
    print_summary(summary)
    
    # Generate model comparison table
    latex_output_dir = script_dir / "latex_tables"
    generate_model_comparison_table(df, col_mapping, output_dir=latex_output_dir)
    
    # Generate error taxonomy table
    generate_error_taxonomy_table(output_dir=latex_output_dir)
    
    # Save results with WES (if not already CSV)
    if results_file.suffix == '.xlsx':
        output_file = script_dir / "Phase1_Results_with_WES.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n{'='*60}")
        print(f"Results saved to: {output_file}")
        
        # Also save as CSV for easier inspection
        csv_output = script_dir / "Phase1_Results_with_WES.csv"
        df.to_csv(csv_output, index=False)
        print(f"CSV version saved to: {csv_output}")
    
    return df, summary


if __name__ == "__main__":
    df, summary = main()

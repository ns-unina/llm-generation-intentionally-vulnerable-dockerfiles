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
    results_file = script_dir / "Phase1_Results.xlsx"
    
    # Check if file exists
    if not results_file.exists():
        print(f"Error: Could not find {results_file}")
        return
    
    print(f"Reading Phase 1 results from: {results_file}")
    
    # Analyze results with default alpha=3
    df, col_mapping = analyze_phase1_results(results_file, alpha=3)
    
    # Generate summary statistics
    summary = generate_summary_statistics(df, col_mapping)
    
    # Print summary
    print_summary(summary)
    
    # Save results with WES
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

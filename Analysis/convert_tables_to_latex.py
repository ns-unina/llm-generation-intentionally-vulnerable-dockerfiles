#!/usr/bin/env python3
"""
Convert CSV tables to LaTeX format.
"""
import argparse
import pandas as pd
from pathlib import Path


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in text."""
    if not isinstance(text, str):
        text = str(text)
    
    # Order matters! Backslash must be first
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    
    return text


def csv_to_latex(csv_path: Path, output_dir: Path):
    """Convert a single CSV file to LaTeX table format."""
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Generate label from filename (remove .csv extension and prefix)
    label = csv_path.stem  # e.g., "tab_results_functional_outcomes"
    
    # Generate caption from filename (convert underscores to spaces, title case)
    caption_text = csv_path.stem.replace("tab_results_", "").replace("_", " ").title()
    
    # Determine number of columns
    num_cols = len(df.columns)
    col_spec = "L" * num_cols  # All left-aligned
    
    # Start building LaTeX
    latex_lines = []
    # latex_lines.append(f"\\begin{{table}}[width=.9\\linewidth,cols={num_cols},pos=h]")
    # latex_lines.append(f"\\caption{{{caption_text}}}\\label{{{label}}}")
    latex_lines.append(f"\\begin{{tabular*}}{{\\tblwidth}}{{@{{}} {col_spec}@{{}} }}")
    latex_lines.append("\\toprule")
    
    # Add header row
    header = " & ".join(escape_latex(col) for col in df.columns) + "\\\\"
    latex_lines.append(header)
    latex_lines.append("\\midrule")
    
    # Add data rows
    for _, row in df.iterrows():
        row_str = " & ".join(escape_latex(str(val)) for val in row.values) + " \\\\"
        latex_lines.append(row_str)
    
    latex_lines.append("\\bottomrule")
    latex_lines.append("\\end{tabular*}")
    # latex_lines.append("\\end{table}")
    
    # Write to file
    output_path = output_dir / f"{csv_path.stem}.tex"
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_lines))
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Convert CSV tables to LaTeX format.")
    parser.add_argument(
        "--input-dir",
        default="tables_paper",
        help="Directory containing CSV tables",
    )
    parser.add_argument(
        "--output-dir",
        default="latex_tables",
        help="Output directory for LaTeX tables",
    )
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return 1
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all CSV files
    csv_files = list(input_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in '{input_dir}'.")
        return 1
    
    print(f"Converting {len(csv_files)} CSV files to LaTeX...")
    
    converted = []
    for csv_file in sorted(csv_files):
        try:
            output_path = csv_to_latex(csv_file, output_dir)
            converted.append(output_path)
            print(f"  ✓ {csv_file.name} → {output_path.name}")
        except Exception as e:
            print(f"  ✗ {csv_file.name}: {e}")
    
    print(f"\nConverted {len(converted)} tables to LaTeX format in '{output_dir}/'")
    
    return 0


if __name__ == "__main__":
    exit(main())

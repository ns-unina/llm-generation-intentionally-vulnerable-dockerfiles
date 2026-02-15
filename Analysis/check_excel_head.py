#!/usr/bin/env python3
"""
Script to display the head of both sheets in Phase2RawAnalysis_Services_Classified.xlsx
"""

import pandas as pd
from pathlib import Path

def main():
    # Path to the Excel file
    excel_path = Path(__file__).parent / "Phase2RawAnalysis_Services_Classified.xlsx"
    
    if not excel_path.exists():
        print(f"Error: File not found at {excel_path}")
        return
    
    # Read all sheets
    excel_file = pd.ExcelFile(excel_path)
    
    print(f"File: {excel_path.name}")
    print(f"Number of sheets: {len(excel_file.sheet_names)}")
    print(f"Sheet names: {excel_file.sheet_names}")
    print("=" * 80)
    
    # Display head of each sheet
    for sheet_name in excel_file.sheet_names:
        print(f"\n{'=' * 80}")
        print(f"SHEET: {sheet_name}")
        print(f"{'=' * 80}\n")
        
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        print(f"Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 5 rows:\n")
        print(df.head())
        print("\n")

if __name__ == "__main__":
    main()

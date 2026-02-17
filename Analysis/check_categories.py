#!/usr/bin/env python3
import pandas as pd
import sys

def check_categories(filename):
    try:
        xls = pd.read_excel(filename, sheet_name=None, engine='openpyxl')
        categories = set()
        for sheet_name, df in xls.items():
            df.columns = [c.strip().lower() for c in df.columns]
            if 'categoryname' in df.columns:
                cats = df['categoryname'].dropna().unique()
                categories.update(cats)
        print(f'\nCategories in {filename}:')
        for cat in sorted(categories):
            print(f'  "{cat}"')
        return categories
    except Exception as e:
        print(f'Error reading {filename}: {e}')
        return set()

if __name__ == '__main__':
    all_cats = set()
    all_cats.update(check_categories('Phase2RawAnalysis_Services_Classified.xlsx'))
    all_cats.update(check_categories('Phase2RawAnalysis_Web_Classified.xlsx'))
    
    print('\n\nAll unique categories:')
    for cat in sorted(all_cats):
        print(f'  "{cat}"')

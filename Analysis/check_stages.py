#!/usr/bin/env python3
import pandas as pd

def check_stages(filename):
    try:
        xls = pd.read_excel(filename, sheet_name=None, engine='openpyxl')
        stage_categories = {}
        for sheet_name, df in xls.items():
            df.columns = [c.strip().lower() for c in df.columns]
            if 'stage' in df.columns and 'categoryname' in df.columns:
                for _, row in df.iterrows():
                    stage = str(row['stage']).strip().lower()
                    cat = str(row['categoryname']).strip()
                    if stage not in stage_categories:
                        stage_categories[stage] = set()
                    stage_categories[stage].add(cat)
        
        print(f'\nStages and categories in {filename}:')
        for stage in sorted(stage_categories.keys()):
            print(f'\n  Stage: {stage}')
            for cat in sorted(stage_categories[stage]):
                print(f'    - {cat}')
        return stage_categories
    except Exception as e:
        print(f'Error reading {filename}: {e}')
        return {}

if __name__ == '__main__':
    all_stages = {}
    s1 = check_stages('Phase2RawAnalysis_Services_Classified.xlsx')
    s2 = check_stages('Phase2RawAnalysis_Web_Classified.xlsx')
    
    # Merge
    for stage, cats in s1.items():
        if stage not in all_stages:
            all_stages[stage] = set()
        all_stages[stage].update(cats)
    for stage, cats in s2.items():
        if stage not in all_stages:
            all_stages[stage] = set()
        all_stages[stage].update(cats)
    
    print('\n\nAll stages and categories combined:')
    for stage in sorted(all_stages.keys()):
        print(f'\n  Stage: {stage}')
        for cat in sorted(all_stages[stage]):
            print(f'    - {cat}')

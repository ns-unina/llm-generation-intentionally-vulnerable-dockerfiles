#!/usr/bin/env python3
import pandas as pd

# Same taxonomy mapping as in plots.py
taxonomy_mapping = {
    # Build errors
    "Invalid/obsolete base image": "B1",
    "Missing/obsolete package version": "B2",
    "Missing build dependencies / toolchain": "B3",
    "External resource not found (URL, mirror)": "B4",
    "Build-from-source / compilation failure": "B5",
    "Repository configuration failure": "B6",
    "Compress files without validity checks.": "B7",
    # Run errors
    "Service not started / container exits": "R1",
    "Runtime misconfiguration (config files, env vars)": "R2",
    "Runtime misconfiguration": "R2",
    "Missing runtime dependencies": "R3",
    "Missing multi-service orchestration": "R5",
    # Exploitability errors
    "Not actually vulnerable / patched version": "E1",
    "Configuration prerequisites not met": "E2",
    "Exploit requires missing external service or application": "E3",
    "Endpoint unavailable / connection refused": "E4",
    "Exploit script mismatch or assumption violation": "E5",
    "Contextual prerequisites not met": "E6",
}

def check_run_categories(filename):
    try:
        xls = pd.read_excel(filename, sheet_name=None, engine='openpyxl')
        run_categories = {}
        for sheet_name, df in xls.items():
            df.columns = [c.strip().lower() for c in df.columns]
            if 'categoryname' in df.columns:
                for _, row in df.iterrows():
                    cat = str(row['categoryname']).strip()
                    if cat in taxonomy_mapping:
                        code = taxonomy_mapping[cat]
                        if code.startswith('R'):
                            if code not in run_categories:
                                run_categories[code] = {'category': cat, 'count': 0}
                            run_categories[code]['count'] += 1
        
        print(f'\nRun categories in {filename}:')
        for code in sorted(run_categories.keys()):
            print(f'  {code}: {run_categories[code]["category"]} (count: {run_categories[code]["count"]})')
        return run_categories
    except Exception as e:
        print(f'Error reading {filename}: {e}')
        return {}

if __name__ == '__main__':
    all_run_cats = {}
    r1 = check_run_categories('Phase2RawAnalysis_Services_Classified.xlsx')
    r2 = check_run_categories('Phase2RawAnalysis_Web_Classified.xlsx')
    
    # Merge counts
    for code, data in r1.items():
        if code not in all_run_cats:
            all_run_cats[code] = {'category': data['category'], 'count': 0}
        all_run_cats[code]['count'] += data['count']
    for code, data in r2.items():
        if code not in all_run_cats:
            all_run_cats[code] = {'category': data['category'], 'count': 0}
        all_run_cats[code]['count'] += data['count']
    
    print('\n\nAll Run categories combined:')
    for code in sorted(all_run_cats.keys()):
        print(f'  {code}: {all_run_cats[code]["category"]} (total count: {all_run_cats[code]["count"]})')

#!/usr/bin/env python3
"""
Verifica completa di tutti i file Excel usati negli script.
"""
import pandas as pd

print("="*80)
print("VERIFICA COMPLETA DATI PHASE 2")
print("="*80)

# 1. Verifica Summary Files (dovrebbero avere TUTTI gli scenari)
print("\n" + "="*80)
print("1. PHASE 2 SUMMARY FILES (tutti gli scenari, successi ed errori)")
print("="*80)

# Services Summary
print("\n--- SERVICES SUMMARY ---")
df_services_summary = pd.read_excel('Phase2TableSummaryServices.xlsx', sheet_name=0, engine='openpyxl')
print(f"Totale righe: {len(df_services_summary)}")
print(f"Colonne: {list(df_services_summary.columns)}")

# Check for CVE-ID and Type columns
cve_col = None
type_col = None
for col in df_services_summary.columns:
    if 'cve' in col.lower():
        cve_col = col
    if 'type' in col.lower():
        type_col = col

if cve_col and type_col:
    print(f"CVE unici: {df_services_summary[cve_col].nunique()}")
    print(f"Scenari (CVE+Type): {df_services_summary.groupby([cve_col, type_col]).ngroups}")
    
    print(f"\nPer Type:")
    for t in df_services_summary[type_col].unique():
        subset = df_services_summary[df_services_summary[type_col] == t]
        print(f"  {t}: {len(subset)} scenari")
    
    # Check expected scenarios
    expected = 24  # 12 CVE × 2
    actual = len(df_services_summary)
    if actual == expected:
        print(f"✓ Services Summary: {actual}/{expected} scenari OK")
    else:
        print(f"⚠️  Services Summary: {actual}/{expected} scenari (differenza: {actual - expected})")
else:
    print("⚠️  Non trovo colonne CVE-ID e Type")

# Web Summary
print("\n--- WEB SUMMARY ---")
df_web_summary = pd.read_excel('Phase2TableSummaryWeb.xlsx', sheet_name=0, engine='openpyxl')
print(f"Totale righe: {len(df_web_summary)}")
print(f"Colonne: {list(df_web_summary.columns)}")

cve_col = None
type_col = None
for col in df_web_summary.columns:
    if 'cve' in col.lower():
        cve_col = col
    if 'type' in col.lower():
        type_col = col

if cve_col and type_col:
    print(f"CVE unici: {df_web_summary[cve_col].nunique()}")
    print(f"Scenari (CVE+Type): {df_web_summary.groupby([cve_col, type_col]).ngroups}")
    
    print(f"\nPer Type:")
    for t in df_web_summary[type_col].unique():
        subset = df_web_summary[df_web_summary[type_col] == t]
        print(f"  {t}: {len(subset)} scenari")
    
    # Check expected scenarios
    expected = 16  # 10 CVE × 2 - 4 falliti
    actual = len(df_web_summary)
    if actual == expected:
        print(f"✓ Web Summary: {actual}/{expected} scenari OK")
    else:
        print(f"⚠️  Web Summary: {actual}/{expected} scenari (differenza: {actual - expected})")
else:
    print("⚠️  Non trovo colonne CVE-ID e Type")

# 2. Verifica Classified Files (solo errori)
print("\n" + "="*80)
print("2. PHASE 2 CLASSIFIED FILES (solo scenari con errori)")
print("="*80)

# Services Classified
print("\n--- SERVICES CLASSIFIED ---")
df_services_class = pd.read_excel('Phase2RawAnalysis_Services_Classified.xlsx', 
                                  sheet_name="Phase2RawAnalysis_Services_Clas", 
                                  engine='openpyxl')
print(f"Totale righe (errori): {len(df_services_class)}")
print(f"CVE unici con errori: {df_services_class['CVE-ID'].nunique()}")
print(f"Scenari con errori: {df_services_class.groupby(['CVE-ID', 'Type']).ngroups}")

# Web Classified
print("\n--- WEB CLASSIFIED ---")
df_web_class = pd.read_excel('Phase2RawAnalysis_Web_Classified.xlsx', 
                             sheet_name="Phase2RawAnalysis_Web_Classifie", 
                             engine='openpyxl')
print(f"Totale righe (errori): {len(df_web_class)}")
print(f"CVE unici con errori: {df_web_class['CVE-ID'].nunique()}")
print(f"Scenari con errori: {df_web_class.groupby(['CVE-ID', 'Type']).ngroups}")

# 3. Riepilogo totale
print("\n" + "="*80)
print("3. RIEPILOGO FINALE")
print("="*80)

if cve_col and type_col:
    total_services = len(df_services_summary)
    total_web = len(df_web_summary)
    total = total_services + total_web
    
    expected_total = 40  # 24 services + 16 web
    
    print(f"\nServices scenari: {total_services} (attesi: 24)")
    print(f"Web scenari: {total_web} (attesi: 16)")
    print(f"TOTALE: {total} (attesi: {expected_total})")
    
    if total == expected_total:
        print(f"\n✓✓✓ TUTTO OK: {total} scenari totali ✓✓✓")
    else:
        print(f"\n⚠️⚠️⚠️ PROBLEMA: {total} scenari trovati vs {expected_total} attesi (diff: {total - expected_total})")
    
    # Check composition
    print(f"\n--- DETTAGLIO ---")
    print(f"Services: {df_services_summary[cve_col].nunique()} CVE unici")
    print(f"Web: {df_web_summary[cve_col].nunique()} CVE unici")
    print(f"Totale CVE: {df_services_summary[cve_col].nunique() + df_web_summary[cve_col].nunique()}")
    
    print(f"\n--- SCENARI CON ERRORI (nei Classified) ---")
    print(f"Services con errori: {df_services_class.groupby(['CVE-ID', 'Type']).ngroups}/{total_services}")
    print(f"Web con errori: {df_web_class.groupby(['CVE-ID', 'Type']).ngroups}/{total_web}")
    print(f"Services senza errori: {total_services - df_services_class.groupby(['CVE-ID', 'Type']).ngroups}")
    print(f"Web senza errori: {total_web - df_web_class.groupby(['CVE-ID', 'Type']).ngroups}")

print("\n" + "="*80)
print("VERIFICA COMPLETATA")
print("="*80)

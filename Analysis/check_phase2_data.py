#!/usr/bin/env python3
import pandas as pd

print("=== ANALISI PHASE 2 CLASSIFIED FILES ===\n")

# Services - solo prima scheda
df_services = pd.read_excel('Phase2RawAnalysis_Services_Classified.xlsx', 
                            sheet_name="Phase2RawAnalysis_Services_Clas", 
                            engine='openpyxl')
print("=== SERVICES (Classified) ===")
print(f"Totale righe Services: {len(df_services)}")
print(f"CVE unici: {df_services['CVE-ID'].nunique()}")
print(f"Scenari (CVE+Type): {df_services.groupby(['CVE-ID', 'Type']).ngroups}")

# Count by Type
print(f"\nPer Type:")
type_counts = df_services.groupby('Type')['CVE-ID'].nunique()
for t, count in type_counts.items():
    print(f"  {t}: {count} CVE unici")

print(f"\nScenari per Type (CVE+Type combinations):")
for t in df_services['Type'].unique():
    subset = df_services[df_services['Type'] == t]
    print(f"  {t}: {subset.groupby(['CVE-ID', 'Type']).ngroups} scenari")

# List all Services CVEs per type
print(f"\n{'='*60}")
print("DETTAGLIO CVE SERVICES PER TYPE:")
package_cves = set(df_services[df_services['Type'] == 'Package']['CVE-ID'].unique())
source_cves = set(df_services[df_services['Type'] == 'Source']['CVE-ID'].unique())

print(f"\nPackage CVEs ({len(package_cves)}):")
for cve in sorted(package_cves):
    print(f"  {cve}")

print(f"\nSource CVEs ({len(source_cves)}):")
for cve in sorted(source_cves):
    print(f"  {cve}")

# Find missing CVEs
missing_source = package_cves - source_cves
missing_package = source_cves - package_cves

if missing_source:
    print(f"\n⚠️  CVE con Package ma SENZA Source ({len(missing_source)}):")
    for cve in sorted(missing_source):
        print(f"    {cve}")
        
if missing_package:
    print(f"\n⚠️  CVE con Source ma SENZA Package ({len(missing_package)}):")
    for cve in sorted(missing_package):
        print(f"    {cve}")

if not missing_source and not missing_package:
    print(f"\n✓ Tutti i CVE hanno entrambe le strategie")

print("\n" + "="*60 + "\n")

# Web - solo prima scheda
df_web = pd.read_excel('Phase2RawAnalysis_Web_Classified.xlsx', 
                       sheet_name="Phase2RawAnalysis_Web_Classifie", 
                       engine='openpyxl')
print("=== WEB (Classified) ===")
print(f"Totale righe Web: {len(df_web)}")
print(f"CVE unici: {df_web['CVE-ID'].nunique()}")
print(f"Scenari (CVE+Type): {df_web.groupby(['CVE-ID', 'Type']).ngroups}")

# Count by Type
print(f"\nPer Type:")
type_counts = df_web.groupby('Type')['CVE-ID'].nunique()
for t, count in type_counts.items():
    print(f"  {t}: {count} CVE unici")

print(f"\nScenari per Type (CVE+Type combinations):")
for t in df_web['Type'].unique():
    subset = df_web[df_web['Type'] == t]
    print(f"  {t}: {subset.groupby(['CVE-ID', 'Type']).ngroups} scenari")

# List Web CVEs
print(f"\n{'='*60}")
print("DETTAGLIO CVE WEB PER TYPE:")
compose_cves = set(df_web[df_web['Type'] == 'Compose']['CVE-ID'].unique())
bundle_cves = set(df_web[df_web['Type'] == 'Bundle']['CVE-ID'].unique())

print(f"\nCompose CVEs ({len(compose_cves)}):")
for cve in sorted(compose_cves):
    print(f"  {cve}")

print(f"\nBundle CVEs ({len(bundle_cves)}):")
for cve in sorted(bundle_cves):
    print(f"  {cve}")

# Find missing CVEs
missing_bundle = compose_cves - bundle_cves
missing_compose = bundle_cves - compose_cves

if missing_bundle:
    print(f"\n⚠️  CVE con Compose ma SENZA Bundle ({len(missing_bundle)}):")
    for cve in sorted(missing_bundle):
        print(f"    {cve}")
        
if missing_compose:
    print(f"\n⚠️  CVE con Bundle ma SENZA Compose ({len(missing_compose)}):")
    for cve in sorted(missing_compose):
        print(f"    {cve}")

if not missing_bundle and not missing_compose:
    print(f"\n✓ Tutti i CVE hanno entrambe le strategie")

print(f"\n{'='*60}")
print("RIEPILOGO CVE PER STRATEGIA:")
web_cves = sorted(df_web['CVE-ID'].unique())
print(f"\nCVE Web con dettaglio strategie:")
for cve in web_cves:
    cve_data = df_web[df_web['CVE-ID'] == cve]
    types = sorted([str(t) for t in cve_data['Type'].unique() if pd.notna(t)])
    status = "✓ Completo" if len(types) == 2 else "⚠️  Incompleto"
    print(f"  {cve}: {', '.join(types)} {status}")

# Check failed scenarios
print(f"\n{'='*60}")
print("VERIFICA SCENARI FALLITI (devono essere assenti):")
failed = [
    ("CVE-2017-12617", "Bundle"),
    ("CVE-2017-5638", "Bundle"),
    ("CVE-2017-5638", "Compose"),
    ("CVE-2018-3811", "Bundle"),
]

for cve, typ in failed:
    found = ((df_web['CVE-ID'] == cve) & (df_web['Type'] == typ)).any()
    if found:
        print(f"  ⚠️  {cve} {typ} TROVATO (dovrebbe essere escluso!)")
    else:
        print(f"  ✓  {cve} {typ} correttamente escluso")

print("\n" + "="*60)
print("=== RIEPILOGO TOTALE ===")
services_scenarios = df_services.groupby(['CVE-ID', 'Type']).ngroups
web_scenarios = df_web.groupby(['CVE-ID', 'Type']).ngroups
print(f"Services scenari totali: {services_scenarios}")
print(f"Web scenari totali: {web_scenarios}")
print(f"TOTALE SCENARI: {services_scenarios + web_scenarios}")

services_cve = df_services['CVE-ID'].nunique()
web_cve = df_web['CVE-ID'].nunique()
print(f"\nServices CVE unici: {services_cve}")
print(f"Web CVE unici: {web_cve}")
print(f"TOTALE CVE: {services_cve + web_cve}")

print("\n" + "="*60)
print("=== VERIFICA CON IL TESTO ===")
print(f"Testo dice: 12 CVE services × 2 = 24 scenari")
print(f"Realtà: {services_cve} CVE services, {services_scenarios} scenari")
if services_scenarios == 24:
    print("✓ Services OK")
else:
    print(f"✗ Differenza services: {services_scenarios - 24}")

print(f"\nTesto dice: 10 CVE web iniziali - 1 CVE completamente fallito (CVE-2017-5638)")
print(f"          + 3 scenari Bundle falliti = 9 CVE × 2 - 3 = 15 scenari")
print(f"Realtà: {web_cve} CVE web, {web_scenarios} scenari")
if web_scenarios == 16:
    print("✓ Web ha 16 scenari (9 Compose + 7 Bundle)")
else:
    print(f"✗ Differenza web: {web_scenarios - 16}")

print(f"\n{'='*60}")
print("CORREZIONE TESTO:")
print(f"Il testo va aggiornato:")
print(f"- Da '12 services' a '{services_cve} services'")
print(f"- Da '24 scenari' a '{services_scenarios} scenari services'")
print(f"- Totale: {services_scenarios + web_scenarios} scenari, {services_cve + web_cve} CVE")

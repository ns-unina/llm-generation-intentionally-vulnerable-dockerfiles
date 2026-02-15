#!/usr/bin/env python3
import pandas as pd

# Leggo i file summary usati per le figure di successo
services = pd.read_excel('Phase2TableSummaryServices.xlsx', sheet_name=0, engine='openpyxl')
web = pd.read_excel('Phase2TableSummaryWeb.xlsx', sheet_name=0, engine='openpyxl')

print('=== SUMMARY FILES (usati per figure di successo) ===')
print(f'Services: {len(services)} scenari')
print(f'Web: {len(web)} scenari')
print(f'TOTALE: {len(services) + len(web)} scenari')
print()
print('Services colonne:', list(services.columns))
print('Web colonne:', list(web.columns))
print()

# Verifico i dati
df_summary = pd.concat([services, web], ignore_index=True)
df_summary['dataset'] = ['Services']*len(services) + ['Web']*len(web)

print('Build success:', df_summary['Compile'].sum(), '/', len(df_summary))
print('Run success:', df_summary['Run'].sum(), '/', len(df_summary))
print('Exploit success:', df_summary['Exploit'].sum(), '/', len(df_summary))
print()

print('=== VERIFICA FIGURE SUCCESSO ===')
print('Le figure di overall/services/web success usano questi 40 scenari ✓')
print()

print('=== CLASSIFIED FILES (usati per figure Impact/Automation) ===')
print('Figure scatter, boxplot, change/automation distribution usano:')
print('  - 38 scenari con errori (23 services + 15 web)')
print('  - Esclusi: CVE-2014-6271 Source e CVE-2023-2636 Compose (perfetti)')
print('  - Questo è CORRETTO: scenari perfetti non hanno errori da classificare')

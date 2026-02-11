import pandas as pd

# Check the raw data files
print("=== Phase2RawAnalysis_Services_Classified.xlsx ===")
df_services = pd.read_excel('Phase2RawAnalysis_Services_Classified.xlsx', sheet_name=0)
print(f"Columns: {df_services.columns.tolist()}")
if 'changeclass' in df_services.columns:
    print(f"changeclass values: {df_services['changeclass'].unique()[:5]}")
if 'automationchallenge' in df_services.columns:
    print(f"automationchallenge values: {df_services['automationchallenge'].unique()[:5]}")
print(f"Shape: {df_services.shape}")

print("\n\nFirst few rows:")
print(df_services.head())

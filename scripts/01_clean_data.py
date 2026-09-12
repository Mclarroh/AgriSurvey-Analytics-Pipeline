import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------
# 1. Set up the file paths
# ------------------------------------------
BASE_DIR = Path(__file__).parent.parent          # goes up to agri_survey_system folder
RAW_FILE = BASE_DIR / "data" / "agriculture_survey_raw_surveycto.csv"
CLEAN_FILE = BASE_DIR / "cleaned" / "agriculture_clean.csv"

print("Reading raw data...")
df = pd.read_csv(RAW_FILE)

print(f"Original shape: {df.shape[0]} rows, {df.shape[1]} columns")

# ------------------------------------------
# 2. Clean gender
# ------------------------------------------
df["gender"] = df["gender"].astype(str).str.strip().str.lower()
df["gender"] = df["gender"].replace({
    "male": "Male",
    "m": "Male",
    "female": "Female",
    "f": "Female",
    "nan": np.nan,
    "": np.nan
})

# ------------------------------------------
# 3. Clean education
# ------------------------------------------
df["education_level"] = df["education_level"].astype(str).str.strip().str.title()
df["education_level"] = df["education_level"].replace({
    "Dont Know": "Unknown",
    "Nan": np.nan,
    "": np.nan
})

# ------------------------------------------
# 4. Clean main_crop and other text categories
# ------------------------------------------
for col in ["main_crop", "secondary_crop", "soil_type", "uses_fertilizer", "uses_irrigation", "belongs_to_coop"]:
    df[col] = df[col].astype(str).str.strip().str.title()
    df[col] = df[col].replace({"Nan": np.nan, "": np.nan, "None": "None"})

# ------------------------------------------
# 5. Fix impossible numeric values
# ------------------------------------------
# Age: keep only realistic ages
df.loc[(df["age"] < 15) | (df["age"] > 100), "age"] = np.nan

# Farm size: remove crazy values
df.loc[(df["farm_size_ha"] < 0) | (df["farm_size_ha"] > 100), "farm_size_ha"] = np.nan

# Yield: remove extreme outliers
df.loc[df["yield_kg_last_season"] > 20000, "yield_kg_last_season"] = np.nan

# Income: remove negative values
df.loc[df["estimated_income_kes"] < 0, "estimated_income_kes"] = np.nan

# ------------------------------------------
# 6. Fix bad GPS coordinates
# ------------------------------------------
# Kenya roughly lies between latitude -5 to 5 and longitude 33 to 42
df.loc[(df["gps_latitude"] < -5) | (df["gps_latitude"] > 5), "gps_latitude"] = np.nan
df.loc[(df["gps_longitude"] < 33) | (df["gps_longitude"] > 42), "gps_longitude"] = np.nan

# ------------------------------------------
# 7. Create a simple data quality flag
# ------------------------------------------
df["has_valid_gps"] = df["gps_latitude"].notna() & df["gps_longitude"].notna()
df["data_quality_score"] = (
    df[["age", "farm_size_ha", "yield_kg_last_season", "gender", "main_crop"]].notna().sum(axis=1)
)

# ------------------------------------------
# 8. Save the cleaned data
# ------------------------------------------
df.to_csv(CLEAN_FILE, index=False)

print(f"\nCleaned data saved to: {CLEAN_FILE}")
print(f"New shape: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nMissing values after cleaning:")
print(df[["age", "gender", "farm_size_ha", "yield_kg_last_season", "gps_latitude", "gps_longitude"]].isna().sum())
print("\nDone! Cleaning finished successfully.")
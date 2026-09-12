import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ------------------------------------------
# Paths
# ------------------------------------------
BASE_DIR = Path(__file__).parent.parent
CLEAN_FILE = BASE_DIR / "cleaned" / "agriculture_clean.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading cleaned data...")
df = pd.read_csv(CLEAN_FILE)
print(f"Loaded {len(df)} rows\n")

# ------------------------------------------
# 1. Basic summary statistics
# ------------------------------------------
print("=" * 50)
print("BASIC SUMMARY STATISTICS")
print("=" * 50)

numeric_cols = ["age", "household_size", "farm_size_ha", "yield_kg_last_season", 
                "estimated_income_kes", "years_farming"]

print(df[numeric_cols].describe().round(1))

# ------------------------------------------
# 2. Categorical summaries
# ------------------------------------------
print("\n" + "=" * 50)
print("CATEGORICAL SUMMARIES")
print("=" * 50)

print("\nGender distribution:")
print(df["gender"].value_counts(dropna=False))

print("\nMain crop distribution:")
print(df["main_crop"].value_counts(dropna=False))

print("\nUses fertilizer:")
print(df["uses_fertilizer"].value_counts(dropna=False))

print("\nUses irrigation:")
print(df["uses_irrigation"].value_counts(dropna=False))

# ------------------------------------------
# 3. Create charts
# ------------------------------------------
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Chart 1: Age distribution
plt.figure()
sns.histplot(df["age"].dropna(), bins=15, kde=True, color="steelblue")
plt.title("Age Distribution of Farmers")
plt.xlabel("Age")
plt.ylabel("Number of Farmers")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_age_distribution.png", dpi=150)
plt.close()
print("Saved: 01_age_distribution.png")

# Chart 2: Farm size distribution
plt.figure()
sns.histplot(df["farm_size_ha"].dropna(), bins=20, kde=True, color="green")
plt.title("Farm Size Distribution (hectares)")
plt.xlabel("Farm Size (ha)")
plt.ylabel("Number of Farmers")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_farm_size_distribution.png", dpi=150)
plt.close()
print("Saved: 02_farm_size_distribution.png")

# Chart 3: Main crop bar chart (corrected)
plt.figure()
crop_counts = df["main_crop"].value_counts().head(8)
sns.barplot(
    x=crop_counts.values, 
    y=crop_counts.index, 
    hue=crop_counts.index, 
    palette="viridis", 
    legend=False
)
plt.title("Most Common Main Crops")
plt.xlabel("Number of Farmers")
plt.ylabel("Crop")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_main_crops.png", dpi=150)
plt.close()
print("Saved: 03_main_crops.png")

# Chart 4: Yield by fertilizer use (corrected)
plt.figure()
sns.boxplot(
    data=df, 
    x="uses_fertilizer", 
    y="yield_kg_last_season", 
    hue="uses_fertilizer", 
    palette="Set2", 
    legend=False
)
plt.title("Yield by Fertilizer Use")
plt.xlabel("Uses Fertilizer")
plt.ylabel("Yield (kg)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_yield_by_fertilizer.png", dpi=150)
plt.close()
print("Saved: 04_yield_by_fertilizer.png")

# Chart 5: Income vs Farm Size scatter
plt.figure()
sns.scatterplot(
    data=df, 
    x="farm_size_ha", 
    y="estimated_income_kes", 
    hue="uses_irrigation", 
    alpha=0.7
)
plt.title("Farm Size vs Estimated Income")
plt.xlabel("Farm Size (ha)")
plt.ylabel("Estimated Income (KES)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_size_vs_income.png", dpi=150)
plt.close()
print("Saved: 05_size_vs_income.png")

# ------------------------------------------
# 4. Simple correlation
# ------------------------------------------
print("\n" + "=" * 50)
print("CORRELATIONS (numeric variables)")
print("=" * 50)
corr = df[numeric_cols].corr().round(2)
print(corr)

# Save correlation as CSV too
corr.to_csv(OUTPUT_DIR / "correlations.csv")
print("\nSaved: correlations.csv")

print("\n" + "=" * 50)
print("Quantitative analysis finished successfully!")
print(f"All charts and tables saved in: {OUTPUT_DIR}")
print("=" * 50)
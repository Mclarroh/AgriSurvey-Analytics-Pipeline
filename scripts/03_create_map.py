import pandas as pd
import folium
from folium.plugins import MarkerCluster
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

# Keep only rows that have valid GPS coordinates
df_map = df.dropna(subset=["gps_latitude", "gps_longitude"]).copy()
print(f"Farmers with valid GPS: {len(df_map)}")

# ------------------------------------------
# Create the map
# ------------------------------------------
# Center the map on the average location of the farmers
map_center = [df_map["gps_latitude"].mean(), df_map["gps_longitude"].mean()]

# Use Esri tiles (no API key needed)
m = folium.Map(
    location=map_center,
    zoom_start=8,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri"
)

# Add a marker cluster (groups points when you zoom out)
marker_cluster = MarkerCluster().add_to(m)

# Add one marker for each farmer
for idx, row in df_map.iterrows():
    # Popup text that appears when you click a point
    popup_text = f"""
    <b>Respondent:</b> {row['respondent_id']}<br>
    <b>Crop:</b> {row['main_crop']}<br>
    <b>Farm size:</b> {row['farm_size_ha']} ha<br>
    <b>Yield:</b> {row['yield_kg_last_season']} kg<br>
    <b>Irrigation:</b> {row['uses_irrigation']}
    """
    
    folium.Marker(
        location=[row["gps_latitude"], row["gps_longitude"]],
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=f"{row['main_crop']} - {row['respondent_id']}"
    ).add_to(marker_cluster)

# ------------------------------------------
# Save the map
# ------------------------------------------
map_file = OUTPUT_DIR / "farmers_map.html"
m.save(str(map_file))

print(f"\nInteractive map saved to: {map_file}")
print("Double-click the HTML file to open it in your browser.")
print("Done!")
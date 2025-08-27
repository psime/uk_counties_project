import geopandas as gpd
import matplotlib.pyplot as plt
import os
import re
import zipfile
import requests

# --- 1. Download ---
url = "https://osdatahub.os.uk/downloads/open/BoundaryLine/GB/CountyUnitary.gpkg.zip"
r = requests.get(url)
with open("CountyUnitary.zip", "wb") as f:
    f.write(r.content)

# --- 2. Extract ---
with zipfile.ZipFile("CountyUnitary.zip", "r") as zip_ref:
    zip_ref.extractall("data")

# --- 3. Load ---
gdf = gpd.read_file("data/CountyUnitary.gpkg")

# --- 4. Create output folder ---
os.makedirs("output_counties", exist_ok=True)

# --- 5. Loop and save maps ---
for _, row in gdf.iterrows():
    name = row["CTYUA21NM"]  # adjust if column name differs
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", name)
    
    county = gpd.GeoDataFrame([row], crs=gdf.crs)
    
    fig, ax = plt.subplots(figsize=(6,6))
    county.plot(ax=ax, color="skyblue", edgecolor="black")
    ax.axis("off")
    
    plt.savefig(f"output_counties/{safe_name}.png", bbox_inches="tight", pad_inches=0, dpi=300)
    plt.close()

print("All county PNGs saved in output_counties/")

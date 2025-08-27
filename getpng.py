import geopandas as gpd
import matplotlib.pyplot as plt
import os
import re
import zipfile
import requests
from tqdm import tqdm  # for progress bar

# --- 1. Download Boundary-Line dataset ---
url = "https://osdatahub.os.uk/downloads/open/BoundaryLine/GB/CountyUnitary.gpkg.zip"
zip_path = "CountyUnitary.zip"

if not os.path.exists(zip_path):
    print("Downloading Boundary-Line dataset...")
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    with open(zip_path, "wb") as f, tqdm(
        total=total_size, unit='B', unit_scale=True, desc="Downloading"
    ) as bar:
        for chunk in r.iter_content(1024):
            f.write(chunk)
            bar.update(len(chunk))
else:
    print("Boundary-Line ZIP already exists, skipping download.")

# --- 2. Extract ZIP ---
extract_dir = "data"
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_dir)
print(f"Extracted to {extract_dir}/")

# --- 3. Load GeoPackage ---
gpkg_path = os.path.join(extract_dir, "CountyUnitary.gpkg")
gdf = gpd.read_file(gpkg_path)

# --- 4. Prepare output folder ---
output_dir = "output_counties"
os.makedirs(output_dir, exist_ok=True)

# --- 5. Loop through counties and save PNGs ---
print("Generating PNGs for each county/unitary authority...")
for idx, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Counties"):
    name = row["CTYUA21NM"]  # adjust if column name differs
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", name)
    
    county = gpd.GeoDataFrame([row], crs=gdf.crs)
    
    fig, ax = plt.subplots(figsize=(6,6))
    county.plot(ax=ax, color="skyblue", edgecolor="black")
    ax.axis("off")
    
    plt.savefig(f"{output_dir}/{safe_name}.png", bbox_inches="tight", pad_inches=0, dpi=300)
    plt.close()

print(f"All county PNGs saved in {output_dir}/")

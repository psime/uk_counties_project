import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Load shapefile/GeoPackage
gdf = gpd.read_file("data/Counties.gpkg")

# Ensure an output folder exists
os.makedirs("output_counties", exist_ok=True)

# Loop through counties
for _, row in gdf.iterrows():
    name = row["CTYUA21NM"]  # Column with county name (may vary, check gdf.columns)
    county = gdf[gdf["CTYUA21NM"] == name]
    
    fig, ax = plt.subplots(figsize=(6,6))
    county.plot(ax=ax, color="skyblue", edgecolor="black")
    ax.axis("off")
    
    plt.savefig(f"output_counties/{name}.png", bbox_inches="tight", pad_inches=0, dpi=300)
    plt.close()

print("All county PNGs saved in output_counties/")

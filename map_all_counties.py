import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Load the realistic test data that was created
print("Loading the 5 test counties...")
gdf = gpd.read_file("data/UK_Test_Realistic.gpkg")

print(f"Found {len(gdf)} counties:")
for i, name in enumerate(gdf['name']):
    print(f"  {i+1}. {name}")

# Create individual maps for each county
print("\nCreating individual county maps...")

colors = ['lightcoral', 'lightgreen', 'gold', 'lightblue', 'plum']
edge_colors = ['darkred', 'darkgreen', 'orange', 'navy', 'purple']

os.makedirs("output_counties", exist_ok=True)

for i, (idx, row) in enumerate(gdf.iterrows()):
    name = row['name']
    color = colors[i % len(colors)]
    edge_color = edge_colors[i % len(edge_colors)]
    
    print(f"Creating map for: {name}")
    
    # Create single county GeoDataFrame
    county = gpd.GeoDataFrame([row], crs=gdf.crs)
    
    # Create the map
    fig, ax = plt.subplots(figsize=(10, 8))
    county.plot(ax=ax, color=color, edgecolor=edge_color, linewidth=3)
    
    ax.set_title(f"{name}", fontsize=18, pad=20, weight='bold')
    ax.axis("off")
    ax.set_facecolor('lightsteelblue')  # Water/background
    
    # Add some styling touches
    ax.grid(True, alpha=0.2)
    
    # Save individual map
    safe_name = name.replace(" ", "_")
    output_path = f"output_counties/{safe_name}_Individual.png"
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0.2, 
               dpi=300, facecolor='white')
    
    print(f"  ✅ Saved: {output_path}")
    plt.show()
    plt.close()

# Create a combined map showing all counties together
print("\nCreating combined map of all counties...")

fig, ax = plt.subplots(figsize=(15, 12))

for i, (idx, row) in enumerate(gdf.iterrows()):
    county = gpd.GeoDataFrame([row], crs=gdf.crs)
    county.plot(ax=ax, color=colors[i], edgecolor=edge_colors[i], 
               linewidth=2, alpha=0.8)
    
    # Add county name labels
    centroid = county.geometry.centroid.iloc[0]
    ax.annotate(row['name'], xy=(centroid.x, centroid.y), 
               fontsize=12, ha='center', va='center', weight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

ax.set_title("All Test UK Counties", fontsize=20, pad=30, weight='bold')
ax.axis("off")
ax.set_facecolor('lightsteelblue')
ax.grid(True, alpha=0.2)

# Save combined map
combined_path = "output_counties/All_Counties_Combined.png"
plt.savefig(combined_path, bbox_inches="tight", pad_inches=0.3, 
           dpi=300, facecolor='white')

print(f"✅ Combined map saved: {combined_path}")
plt.show()
plt.close()

print(f"\n🎉 Complete! Generated maps for all {len(gdf)} counties")
print(f"📁 Files in output folder: {sorted(os.listdir('output_counties'))}")

# Show summary of what was created
print(f"\n📊 Summary:")
print(f"Individual county maps: {len(gdf)}")
print(f"Combined overview map: 1")
print(f"Total images created: {len(gdf) + 1}")

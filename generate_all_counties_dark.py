import geopandas as gpd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm  # For progress bar

print("🗺️ Generating all 218 UK counties as dark maps...")

# Load the real UK county data
gpkg_path = "data/Counties_and_Unitary_Authorities_May_2023_UK_BGC.gpkg"
uk_gdf = gpd.read_file(gpkg_path)

print(f"📊 Loaded {len(uk_gdf)} real UK administrative areas")

# Find the name column
name_columns = ['CTYUA23NM', 'CTYUA21NM', 'NAME', 'name']
name_col = None

for col in name_columns:
    if col in uk_gdf.columns:
        name_col = col
        break

print(f"📝 Using '{name_col}' for county names")

# Create output directory
os.makedirs("output_counties/all_dark_counties", exist_ok=True)

# Dark color schemes to choose from
color_schemes = {
    'black': {'fill': 'black', 'edge': 'white', 'bg': 'white'},
    'charcoal': {'fill': '#2F2F2F', 'edge': 'white', 'bg': 'white'},
    'navy': {'fill': '#1a1a2e', 'edge': '#16213e', 'bg': 'white'},
    'dark_green': {'fill': '#1b4332', 'edge': '#2d6a4f', 'bg': 'white'},
    'dark_purple': {'fill': '#301934', 'edge': '#512b58', 'bg': 'white'}
}

# Choose your preferred color scheme
scheme = color_schemes['black']  # Change to 'charcoal', 'navy', etc. if preferred

print(f"🎨 Using color scheme: {list(color_schemes.keys())[0]} (black shapes)")
print(f"📁 Output folder: output_counties/all_dark_counties/")

# Generate individual maps for all 218 counties
print(f"\n⚡ Generating {len(uk_gdf)} individual county maps...")

# Create progress bar
failed_counties = []
success_count = 0

for idx, (_, county_row) in enumerate(tqdm(uk_gdf.iterrows(), total=len(uk_gdf), desc="Creating maps")):
    try:
        county_name = county_row[name_col]
        
        # Create single county GeoDataFrame
        county_gdf = gpd.GeoDataFrame([county_row], crs=uk_gdf.crs)
        
        # Create the map
        fig, ax = plt.subplots(figsize=(10, 8))
        county_gdf.plot(ax=ax, 
                       color=scheme['fill'], 
                       edgecolor=scheme['edge'], 
                       linewidth=2)
        
        # Clean styling
        ax.set_title(f"{county_name}", fontsize=16, weight='bold', pad=15, color='black')
        ax.axis('off')
        ax.set_facecolor(scheme['bg'])
        
        # Create clean filename
        safe_name = (county_name.replace('/', '_')
                               .replace(' ', '_')
                               .replace("'", "")
                               .replace(',', '')
                               .replace('&', 'and'))
        
        # Save with consistent naming
        output_path = f"output_counties/all_dark_counties/{idx+1:03d}_{safe_name}.png"
        plt.savefig(output_path, 
                   bbox_inches='tight', 
                   pad_inches=0.1, 
                   dpi=300, 
                   facecolor='white',
                   edgecolor='none')
        
        plt.close()  # Important: close to free memory
        success_count += 1
        
    except Exception as e:
        failed_counties.append(f"{county_name}: {str(e)}")
        plt.close()  # Clean up even on error
        continue

print(f"\n🎊 BATCH PROCESSING COMPLETE!")
print(f"✅ Successfully created: {success_count} county maps")
print(f"❌ Failed: {len(failed_counties)} counties")

if failed_counties:
    print("\n⚠️ Failed counties:")
    for failure in failed_counties[:5]:  # Show first 5 failures
        print(f"  • {failure}")
    if len(failed_counties) > 5:
        print(f"  ... and {len(failed_counties) - 5} more")

# Create a summary overview with all counties in dark style
print(f"\n🌍 Creating dark overview map of all {len(uk_gdf)} counties...")

fig, ax = plt.subplots(figsize=(24, 20))
uk_gdf.plot(ax=ax, 
           color=scheme['fill'], 
           edgecolor=scheme['edge'], 
           linewidth=0.3,
           alpha=0.9)

ax.set_title(f"All UK Counties & Unitary Authorities - Dark Style\n{len(uk_gdf)} Administrative Areas (ONS May 2023)", 
            fontsize=24, weight='bold', pad=40, color='black')
ax.axis('off')
ax.set_facecolor(scheme['bg'])

# Save dark overview
overview_path = "output_counties/all_dark_counties/000_UK_ALL_DARK_OVERVIEW.png"
plt.savefig(overview_path, 
           bbox_inches='tight', 
           pad_inches=0.4, 
           dpi=300, 
           facecolor='white')

plt.close()

# Create file listing
print(f"\n📋 Creating file index...")
files = sorted([f for f in os.listdir("output_counties/all_dark_counties/") if f.endswith('.png')])

with open("output_counties/all_dark_counties/FILE_INDEX.txt", 'w') as f:
    f.write(f"UK Counties Dark Maps - Generated Files\n")
    f.write(f"=====================================\n\n")
    f.write(f"Total files: {len(files)}\n")
    f.write(f"Color scheme: Black shapes with white borders\n")
    f.write(f"Resolution: 300 DPI\n")
    f.write(f"Data source: ONS May 2023\n\n")
    f.write("Files:\n")
    for i, filename in enumerate(files, 1):
        f.write(f"{i:3d}. {filename}\n")

print(f"📄 File index saved: output_counties/all_dark_counties/FILE_INDEX.txt")

print(f"\n🎯 FINAL SUMMARY:")
print(f"📂 Location: output_counties/all_dark_counties/")
print(f"📊 Individual maps: {success_count}")
print(f"🌍 Overview map: 1")
print(f"📄 File index: 1")
print(f"🎨 Style: Dark/black county shapes")
print(f"📐 Resolution: 300 DPI")
print(f"💾 Total files: {len(os.listdir('output_counties/all_dark_counties/'))}")

print(f"\n✨ All 218 UK counties now available as dark individual maps!")

import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import zipfile
import os
from io import BytesIO

print("📥 Downloading REAL UK County Boundaries from Official ONS Sources...")

# Create data directory
os.makedirs("data", exist_ok=True)
os.makedirs("output_counties", exist_ok=True)

# Official ONS (Office for National Statistics) data sources
official_sources = [
    {
        "name": "ONS Counties & Unitary Authorities 2023 (Generalised)",
        "zip_url": "https://www.arcgis.com/sharing/rest/content/items/b789ba7030074d2bb26e7e60e7bb21e2/data",
        "description": "Official UK government county boundaries - simplified for mapping"
    },
    {
        "name": "ONS Counties & Unitary Authorities 2023 (Full Resolution)", 
        "zip_url": "https://www.arcgis.com/sharing/rest/content/items/1d26fb65fb454ba1a5b01fb1e3c8a57b/data",
        "description": "Official UK government county boundaries - full detail"
    },
    {
        "name": "Alternative ONS Source",
        "zip_url": "https://opendata.arcgis.com/api/v3/datasets/6638c31a8e9842f98a037748f72258ed_0/downloads/data?format=shp&spatialRefId=4326",
        "description": "ONS Open Data Portal"
    }
]

success = False
uk_gdf = None

for source in official_sources:
    print(f"\n🔄 Trying: {source['name']}")
    print(f"   {source['description']}")
    
    try:
        print("   📡 Downloading ZIP file...")
        response = requests.get(source['zip_url'], timeout=30)
        
        if response.status_code == 200:
            print("   📦 Extracting shapefile...")
            
            # Extract ZIP file
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                # Extract to temporary directory
                extract_path = "data/temp_boundaries"
                os.makedirs(extract_path, exist_ok=True)
                zip_file.extractall(extract_path)
                
                # Find the shapefile
                shp_files = [f for f in os.listdir(extract_path) if f.endswith('.shp')]
                
                if shp_files:
                    shp_path = os.path.join(extract_path, shp_files[0])
                    print(f"   📂 Found shapefile: {shp_files[0]}")
                    
                    # Load the data
                    uk_gdf = gpd.read_file(shp_path)
                    
                    print(f"   ✅ SUCCESS! Loaded {len(uk_gdf)} administrative areas")
                    print(f"   📊 Columns: {list(uk_gdf.columns)}")
                    
                    # Save as GeoPackage for easy reuse
                    uk_gdf.to_file("data/UK_Real_Counties_Official.gpkg", driver="GPKG")
                    print("   💾 Saved as: data/UK_Real_Counties_Official.gpkg")
                    
                    success = True
                    break
                else:
                    print("   ❌ No shapefile found in ZIP")
                    
        else:
            print(f"   ❌ Download failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        continue

if success and uk_gdf is not None:
    print(f"\n🎉 Successfully downloaded REAL UK boundaries!")
    
    # Find the best column for names
    name_columns = ['CTYUA23NM', 'NAME', 'name', 'CTYUA21NM', 'county_name', 'COUNTY']
    name_col = None
    
    for col in name_columns:
        if col in uk_gdf.columns:
            name_col = col
            print(f"📝 Using '{col}' for area names")
            break
    
    if name_col is None:
        name_col = uk_gdf.columns[0]
        print(f"📝 Using first column '{name_col}' for names")
    
    # Show sample of what we got
    print(f"\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 Sample UK Counties/Areas:")
    for i in range(min(10, len(uk_gdf))):
        area_name = uk_gdf.iloc[i][name_col]
        print(f"  {i+1:2d}. {area_name}")
    
    if len(uk_gdf) > 10:
        print(f"     ... and {len(uk_gdf) - 10} more areas")
    
    # Create a map of the first real county
    print(f"\n🗺️ Creating map of first area...")
    first_row = uk_gdf.iloc[0]
    first_name = str(first_row[name_col])
    
    # Single county map
    county_gdf = gpd.GeoDataFrame([first_row], crs=uk_gdf.crs)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    county_gdf.plot(ax=ax, color='lightcoral', edgecolor='darkred', linewidth=2)
    
    ax.set_title(f"REAL UK Boundary: {first_name}", fontsize=18, weight='bold', pad=20)
    ax.axis('off')
    ax.set_facecolor('lightsteelblue')
    
    # Save individual map
    safe_name = first_name.replace('/', '_').replace(' ', '_').replace("'", "")
    individual_path = f"output_counties/{safe_name}_REAL_OFFICIAL.png"
    plt.savefig(individual_path, bbox_inches='tight', pad_inches=0.2, dpi=300, facecolor='white')
    
    print(f"💾 Individual map saved: {individual_path}")
    plt.show()
    plt.close()
    
    # Create overview map of ALL real UK areas
    print(f"\n🌍 Creating overview map of all {len(uk_gdf)} real UK areas...")
    
    fig, ax = plt.subplots(figsize=(20, 16))
    
    # Plot all areas with different colors
    uk_gdf.plot(ax=ax, color='lightgreen', edgecolor='white', linewidth=0.8, alpha=0.8)
    
    ax.set_title(f"Official UK Counties & Unitary Authorities ({len(uk_gdf)} areas)", 
                fontsize=24, weight='bold', pad=30)
    ax.axis('off')
    ax.set_facecolor('lightsteelblue')
    
    # Save overview
    overview_path = "output_counties/UK_All_Real_Counties_Official.png"
    plt.savefig(overview_path, bbox_inches='tight', pad_inches=0.3, dpi=300, facecolor='white')
    
    print(f"💾 Overview map saved: {overview_path}")
    plt.show()
    plt.close()
    
    print(f"\n🎯 SUCCESS SUMMARY:")
    print(f"✅ Downloaded official UK government boundary data")
    print(f"✅ {len(uk_gdf)} real administrative areas loaded")
    print(f"✅ Data saved as: data/UK_Real_Counties_Official.gpkg")
    print(f"✅ Individual map: {individual_path}")
    print(f"✅ Overview map: {overview_path}")
    print(f"\n📁 These are REAL boundaries from the UK Office for National Statistics!")
    
else:
    print("\n❌ All official sources failed.")
    print("📝 Manual download instructions:")
    print("1. Go to: https://geoportal.statistics.gov.uk/")
    print("2. Search for 'Counties and Unitary Authorities'")
    print("3. Download the shapefile")
    print("4. Extract to your 'data' folder")
    print("5. Run a simple loading script")

print(f"\n📂 Current files in data folder: {os.listdir('data')}")
print(f"📂 Current files in output folder: {os.listdir('output_counties')}")

import geopandas as gpd
import matplotlib.pyplot as plt
import os

print("Downloading real UK boundary data...")

# Create data directory
os.makedirs("data", exist_ok=True)

# Try multiple reliable sources
sources = [
    {
        "name": "UK Government Boundaries (Simplified)",
        "url": "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/united-kingdom/uk-counties.json",
        "format": "topojson"
    },
    {
        "name": "World Bank UK Data", 
        "url": "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/UK_map_data.geojson",
        "format": "geojson"
    },
    {
        "name": "OpenDataSoft UK",
        "url": "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-kingdom-county/exports/geojson",
        "format": "geojson"
    }
]

success = False

for source in sources:
    print(f"\nTrying: {source['name']}")
    try:
        # Read directly from URL
        uk_gdf = gpd.read_file(source['url'])
        
        print(f"✅ Success! Downloaded {len(uk_gdf)} areas")
        print(f"Columns available: {list(uk_gdf.columns)}")
        
        # Save to local file
        uk_gdf.to_file("data/UK_Real_Boundaries.gpkg", driver="GPKG")
        
        # Find the best name column
        name_cols = ['name', 'NAME', 'Name', 'county', 'COUNTY', 'region', 'REGION']
        name_col = None
        
        for col in name_cols:
            if col in uk_gdf.columns:
                name_col = col
                break
        
        if not name_col:
            name_col = uk_gdf.columns[0]  # Use first column as fallback
            
        print(f"Using '{name_col}' for area names")
        
        # Show first few area names
        print("Sample areas:")
        for i in range(min(5, len(uk_gdf))):
            area_name = uk_gdf.iloc[i][name_col]
            print(f"  {i+1}. {area_name}")
        
        # Create visualization of first area
        row = uk_gdf.iloc[0]
        name = str(row[name_col])
        print(f"\n🗺️ Creating map for: {name}")
        
        # Create single area GeoDataFrame
        area = gpd.GeoDataFrame([row], crs=uk_gdf.crs)
        
        # Create the map
        fig, ax = plt.subplots(figsize=(12, 10))
        area.plot(ax=ax, color="lightcoral", edgecolor="darkred", linewidth=2)
        
        ax.set_title(f"Real UK Boundary: {name}", fontsize=18, pad=20, weight='bold')
        ax.axis("off")
        ax.set_facecolor('lightblue')  # Water/background color
        
        # Add grid for context
        ax.grid(True, alpha=0.3)
        
        # Save the map
        os.makedirs("output_counties", exist_ok=True)
        safe_name = name.replace("/", "_").replace(" ", "_").replace("'", "")
        
        output_path = f"output_counties/{safe_name}_REAL.png"
        plt.savefig(output_path, bbox_inches="tight", pad_inches=0.2, 
                   dpi=300, facecolor='white', edgecolor='none')
        
        print(f"💾 Map saved: {output_path}")
        plt.show()
        plt.close()
        
        # Create a overview map of all areas
        print("\n🌍 Creating overview map of all UK areas...")
        fig, ax = plt.subplots(figsize=(15, 12))
        uk_gdf.plot(ax=ax, color="lightgreen", edgecolor="white", linewidth=0.5)
        
        ax.set_title("All UK Administrative Areas", fontsize=20, pad=30, weight='bold')
        ax.axis("off")
        ax.set_facecolor('lightblue')
        
        overview_path = "output_counties/UK_All_Areas_Overview.png"
        plt.savefig(overview_path, bbox_inches="tight", pad_inches=0.2, 
                   dpi=300, facecolor='white')
        
        print(f"💾 Overview map saved: {overview_path}")
        plt.show()
        plt.close()
        
        success = True
        break
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        continue

if not success:
    print("\n⚠️ All sources failed. Creating enhanced test data...")
    
    # Create more realistic test shapes if all else fails
    from shapely.geometry import Polygon
    import numpy as np
    
    # Create some realistic-looking county shapes
    def create_irregular_shape(center_x, center_y, size=0.5, points=20):
        angles = np.linspace(0, 2*np.pi, points)
        # Add some randomness to make it look more realistic
        radii = size * (0.7 + 0.3 * np.random.random(points))
        x = center_x + radii * np.cos(angles)
        y = center_y + radii * np.sin(angles)
        return Polygon(zip(x, y))
    
    # Create several test counties
    counties_data = []
    county_names = ["Yorkshire", "Lancashire", "Cornwall", "Devon", "Kent"]
    centers = [(-1.0, 54.0), (-2.5, 53.5), (-4.5, 50.2), (-3.8, 50.7), (1.0, 51.3)]
    
    for name, (cx, cy) in zip(county_names, centers):
        shape = create_irregular_shape(cx, cy, 0.4, 25)
        counties_data.append({
            'name': name,
            'geometry': shape
        })
    
    test_gdf = gpd.GeoDataFrame(counties_data, crs='EPSG:4326')
    test_gdf.to_file("data/UK_Test_Realistic.gpkg", driver="GPKG")
    
    # Visualize first test county
    row = test_gdf.iloc[0]
    name = row['name']
    area = gpd.GeoDataFrame([row], crs=test_gdf.crs)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    area.plot(ax=ax, color="gold", edgecolor="darkorange", linewidth=2)
    ax.set_title(f"Realistic Test Shape: {name}", fontsize=16, weight='bold')
    ax.axis("off")
    
    plt.savefig(f"output_counties/{name}_RealisticTest.png", 
               bbox_inches="tight", pad_inches=0.1, dpi=300)
    plt.show()
    plt.close()
    
    print(f"✅ Created realistic test data with {len(test_gdf)} areas")

print(f"\n📁 Final files:")
print(f"Data folder: {os.listdir('data')}")
if os.path.exists('output_counties'):
    print(f"Output folder: {os.listdir('output_counties')}")
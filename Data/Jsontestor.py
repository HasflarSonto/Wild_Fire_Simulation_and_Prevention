import geopandas as gpd

# Load GeoJSON file
geojson_path = "/Users/antonioli/Desktop/Wild_Fire_Simulation_and_Prevention/Data/LC20_Asp_220.GeoJSON"
gdf = gpd.read_file(geojson_path)

# Print available columns
print("Available columns in GeoJSON:", gdf.columns)

import rasterio
import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# File paths
terrain_tif_path = "LC20_Asp_220.tif"
fuel_geojson_path = "LC20_Asp_220.GeoJSON"

gdf = gpd.read_file(fuel_geojson_path)

# Print available columns
print("Available columns in GeoJSON:", gdf.columns)

# --- Process Terrain Data (GeoTIFF) ---
with rasterio.open(terrain_tif_path) as dataset:
    terrain_data = dataset.read(1)  # Read elevation/aspect data
    transform = dataset.transform  # Get transformation metadata

# Convert raster data into a point cloud format
rows, cols = terrain_data.shape
x_coords = np.array([transform * (c, r) for r in range(rows) for c in range(cols)])
z_values = terrain_data.flatten()

# Create point cloud data
terrain_points = np.column_stack((x_coords[:, 0], x_coords[:, 1], z_values))
terrain_df = pd.DataFrame(terrain_points, columns=['X', 'Y', 'Z'])

# --- Process Fuel Data (GeoJSON) ---
gdf = gpd.read_file(fuel_geojson_path)  # Load GeoJSON
fuel_data = gdf[['geometry', 'fuel_model']]  # Extract fuel model info

# Normalize fuel values using Fire Behavior Fuel Models (FBFM13)
fbfm_burn_prob = {
    1: 0.7, 2: 0.6, 3: 0.8, 4: 0.9, 5: 0.5, 6: 0.6, 7: 0.7,
    8: 0.3, 9: 0.4, 10: 0.5, 11: 0.7, 12: 0.8, 13: 0.9
}
fuel_data['burn_probability'] = fuel_data['fuel_model'].map(fbfm_burn_prob)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(terrain_data, cmap="terrain", extent=(x_coords[:, 0].min(), x_coords[:, 0].max(), 
                                                 x_coords[:, 1].min(), x_coords[:, 1].max()))
ax.set_title("Terrain Data from LANDFIRE (Aspect or Elevation)")
plt.show()

fuel_data.plot(column='burn_probability', cmap='OrRd', legend=True, figsize=(8, 6))
plt.title("Fuel Availability Based on LANDFIRE Data")
plt.show()

# Save processed data
terrain_df.to_csv("processed_terrain.csv", index=False)
fuel_data.to_file("processed_fuel.geojson", driver="GeoJSON")

print("Processing Complete: Terrain and Fuel Data Saved")

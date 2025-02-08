import rasterio
print("Rasterio is installed and working!")
import numpy as np
import csv

def process_raster_to_csv(tif_path, csv_path, is_fuel_model=False):
    """
    Reads a GeoTIFF file and extracts X, Y coordinates along with elevation or fuel model values.
    
    Parameters:
    - tif_path (str): Path to the .tif file.
    - csv_path (str): Path to save the .csv output.
    - is_fuel_model (bool): If True, processes as a fuel model and adds burn probability.
    """

    # Burn probability lookup for FBFM13 model
    burn_probabilities = {
        1: 0.7,  2: 0.6,  3: 0.8,  4: 0.9,  5: 0.5,  6: 0.6,  7: 0.7,
        8: 0.3,  9: 0.4, 10: 0.5, 11: 0.7, 12: 0.8, 13: 0.9
    }

    # Open the raster file
    with rasterio.open(tif_path) as dataset:
        band1 = dataset.read(1)  # Read first band (elevation or fuel model)
        transform = dataset.transform  # Get spatial transform

        # Open CSV file for writing
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write header
            if is_fuel_model:
                writer.writerow(["X", "Y", "Fuel_Model", "Burn_Probability"])
            else:
                writer.writerow(["X", "Y", "Elevation"])

            # Process each pixel
            rows, cols = band1.shape
            for row in range(rows):
                for col in range(cols):
                    x, y = transform * (col, row)  # Convert pixel to coordinates
                    value = band1[row, col]  # Elevation or fuel model value

                    if is_fuel_model:
                        burn_prob = burn_probabilities.get(int(value), 0.2)  # Default burn prob if unknown
                        writer.writerow([x, y, value, burn_prob])
                    else:
                        writer.writerow([x, y, value])

    print(f"Processed: {csv_path}")

# Example Usage
process_raster_to_csv("/Users/antonioli/Desktop/Wild_Fire_Simulation_and_Prevention/Data/LC20_Elev_220_Big.tif",
                      "processed_topo_data_Big.csv", is_fuel_model=False)
process_raster_to_csv("/Users/antonioli/Desktop/Wild_Fire_Simulation_and_Prevention/Data/LC23_F13_240_Big.tif",
                      "processed_fuel_data_Big.csv", is_fuel_model=True)

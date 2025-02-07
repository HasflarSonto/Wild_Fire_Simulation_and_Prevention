import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import clr
clr.AddReference("Grasshopper")
clr.AddReference("RhinoCommon")
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
from Rhino.Geometry import Point3d
import csv

def scale_to_fit(points, max_size=100):
    """Scales all points proportionally while keeping them aligned."""
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    range_x = max_x - min_x
    range_y = max_y - min_y
    scale_factor = max_size / max(range_x, range_y)

    scaled_points = [
        ((p[0] - min_x) * scale_factor, (p[1] - min_y) * scale_factor, p[2])
        for p in points
    ]
    return scaled_points

# File paths (update for actual location)
topo_csv_path = "processed_topo_data.csv"
fuel_csv_path = "processed_fuel_model_data.csv"

# Read CSVs
topo_points, fuel_points, burn_probs = [], [], []
with open(topo_csv_path, 'r') as topo_file, open(fuel_csv_path, 'r') as fuel_file:
    topo_reader, fuel_reader = csv.reader(topo_file), csv.reader(fuel_file)
    next(topo_reader), next(fuel_reader)  # Skip headers

    for topo_row, fuel_row in zip(topo_reader, fuel_reader):
        x_t, y_t, elevation = map(float, topo_row)
        x_f, y_f, fuel_model, burn_prob = map(float, fuel_row)

        # Ensure they match
        if (x_t, y_t) == (x_f, y_f):
            topo_points.append((x_t, y_t, elevation))
            fuel_points.append((x_f, y_f, fuel_model))
            burn_probs.append(burn_prob)

# Scale all points together
scaled_topo = scale_to_fit(topo_points, max_size=100)
scaled_fuel = scale_to_fit(fuel_points, max_size=100)

# Create Rhino points
rhino_points = [Point3d(x, y, z) for (x, y, z) in scaled_topo]

# Assign outputs for Grasshopper
a = rhino_points  # Aligned list of scaled points
b = burn_probs    # Burn probability values

print("Elevation and Fuel Model Data Processed & Scaled Successfully!")

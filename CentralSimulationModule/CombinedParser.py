import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import clr
clr.AddReference("Grasshopper")
clr.AddReference("RhinoCommon")
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
from Rhino.Geometry import Point3d

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

# Example lists of strings for topography and fuel model data
topo_data = [
    "X,Y,Elevation",
    "-2010645.0,2765325.0,547.0",
    "-2010615.0,2765325.0,560.0",
    "-2010585.0,2765325.0,32767.0"  # No-data elevation
]

fuel_data = [
    "X,Y,Fuel_Model,Burn_Probability",
    "-2010645.0,2765325.0,10.0,0.5",
    "-2010615.0,2765325.0,9.0,0.4",
    "-2010585.0,2765325.0,8.0,0.3"
]

# Extract valid points
topo_data.pop(0)  # Remove header
fuel_data.pop(0)

topo_points, fuel_points, burn_probs = [], [], []
for topo_line, fuel_line in zip(topo_data, fuel_data):
    x_t, y_t, elevation = map(float, topo_line.split(","))
    x_f, y_f, fuel_model, burn_prob = map(float, fuel_line.split(","))
    
    # Exclude no-data elevation values
    if elevation == 32767.0:
        continue
    
    # Ensure coordinates match
    if (x_t, y_t) == (x_f, y_f):
        topo_points.append((x_t, y_t, elevation))
        fuel_points.append((x_f, y_f, fuel_model))
        burn_probs.append(burn_prob)

if not topo_points:
    a = "No valid points found."
else:
    # Scale all points together
    scaled_topo = scale_to_fit(topo_points, max_size=100)

    # Create Rhino points
    rhino_points = [Point3d(x, y, z) for (x, y, z) in scaled_topo]

    # Assign outputs for Grasshopper
    a = rhino_points  # Aligned list of scaled points
    b = burn_probs    # Burn probability values

print("Elevation and Fuel Model Data Processed, No-Data Values Removed, and Scaled Successfully!")

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
    """Scales all points proportionally to fit within a max_size x max_size bounding box while preserving relative proportions."""
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    range_x = max_x - min_x
    range_y = max_y - min_y
    scale_factor = max_size / max(range_x, range_y)
    
    scaled_points = [
        ((p[0] - min_x) * scale_factor, (p[1] - min_y) * scale_factor, 0)
        for p in points
    ]
    return scaled_points

# Raw input data as a list of strings
fuel_data = [
    "X,Y,Fuel_Model,Burn_Probability",
    "-2010645.0,2765325.0,10.0,0.5",
    "-2010615.0,2765325.0,9.0,0.4"
]

# Extract valid fuel model points
fuel_data.pop(0)  # Remove header
valid_points = []
burn_probs = []
for line in fuel_data:
    x, y, fuel_model, burn_prob = map(float, line.split(","))
    valid_points.append((x, y, fuel_model))
    burn_probs.append(burn_prob)

if not valid_points:
    a = "No valid points found."
else:
    # Scale all points proportionally to fit within 100x100
    scaled_points = scale_to_fit(valid_points, max_size=100)

    # Create Rhino points for Grasshopper
    rhino_points = [Point3d(x, y, 0) for x, y, _ in scaled_points]
    
    a = rhino_points  # List of points
    b = burn_probs  # Corresponding burn probabilities

print("Fuel Model Data Processed and Scaled Successfully!")

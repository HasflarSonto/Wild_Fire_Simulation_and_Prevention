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
        ((p[0] - min_x) * scale_factor, (p[1] - min_y) * scale_factor, (p[2] - min(points, key=lambda p: p[2])[2]) * scale_factor)
        for p in points
    ]
    return scaled_points

# Raw input data as a list of strings
topology_data = [
    "X,Y,Z",  # Example header, will be skipped
    "-2012355.0,2765325.0,32767.0",
    "-2012325.0,2765325.0,32767.0",
    "-2012295.0,2765325.0,32767.0",
    "-2012265.0,2765325.0,32767.0",
    "-2010645.0,2765325.0,547.0",
    "-2010615.0,2765325.0,560.0",
    "-2010585.0,2765325.0,572.0"
]

# Extract valid points and compute bounds
topology_data.pop(0)  # Remove header
valid_points = []
for line in topology_data:
    x, y, z = map(float, line.split(","))
    if z != 32767.0:  # Filter out invalid values
        valid_points.append((x, y, z))

if not valid_points:
    a = "No valid points found."
else:
    # Scale all points proportionally to fit within 100x100
    scaled_points = scale_to_fit(valid_points, max_size=100)

    # Create Rhino points and store them in a list
    rhino_points = [Point3d(x, y, z) for x, y, z in scaled_points]
    a = rhino_points  # Output only the list of points

print("Topology Data Processed, Scaled Proportionally to Fit 100x100, and Points Output Successfully!")

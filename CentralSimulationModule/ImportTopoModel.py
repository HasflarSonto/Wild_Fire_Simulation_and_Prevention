import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import clr
clr.AddReference("Grasshopper")
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

def remap(value, old_min, old_max, new_min, new_max):
    """Remaps a value from one range to another, handling zero-division errors."""
    if old_max == old_min:
        return (new_min + new_max) / 2
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

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
valid_points = []
for line in topology_data:
    if not line[0].isdigit():  # Skip header row
        continue
    x, y, z = map(float, line.split(","))
    if z != 32767.0:  # Filter out invalid values
        valid_points.append((x, y, z))

if not valid_points:
    a, b = "No valid points found.", None
else:
    # Determine global min/max for remapping
    min_x = min(p[0] for p in valid_points)
    max_x = max(p[0] for p in valid_points)
    min_y = min(p[1] for p in valid_points)
    max_y = max(p[1] for p in valid_points)

    # Remap coordinates to fit within 100x100
    remapped_points = [(remap(p[0], min_x, max_x, 0, 100), remap(p[1], min_y, max_y, 0, 100), p[2]) for p in valid_points]

    # Create Rhino points and store them in a DataTree
    point_tree = DataTree[object]()
    for index, (x, y, z) in enumerate(remapped_points):
        pt = rs.AddPoint(x, y, z)
        path = GH_Path(index)
        point_tree.Add(pt, path)

    # Create a Delaunay mesh from points if enough exist
    mesh = None
    if len(remapped_points) > 2:
        mesh = rs.AddMesh([rs.coerce3dpoint(pt) for pt in point_tree.AllData()])
        rs.ObjectColor(mesh, (200, 200, 200))  # Set mesh color to gray

    # Assign outputs
    a = point_tree  # DataTree of points
    b = mesh  # Mesh object

print("Topology Data Processed, Scaled to 100x100, and Outputs Assigned Successfully!")

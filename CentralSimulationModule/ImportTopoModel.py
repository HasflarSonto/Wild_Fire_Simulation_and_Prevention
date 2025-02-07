import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

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

# Scaling factor to fit within a 100x100 Rhino viewport
min_x, min_y = float('inf'), float('inf')
max_x, max_y = float('-inf'), float('-inf')

# Process input data
topology_points = []
for line in topology_data:
    if not line[0].isdigit():  # Skip header row or any non-numeric lines
        continue
    x, y, z = map(float, line.split(","))
    if z != 32767.0:  # Filter out invalid values
        topology_points.append((x, y, z))
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

# Compute scaling factor to fit within 100x100 space
range_x = max_x - min_x
range_y = max_y - min_y
scale_x = 100 / range_x if range_x != 0 else 1
scale_y = 100 / range_y if range_y != 0 else 1
scale_factor = min(scale_x, scale_y)

# Apply scaling and translation
scaled_points = [((x - min_x) * scale_factor, (y - min_y) * scale_factor, z) for x, y, z in topology_points]

# Create points in Rhino based on topology locations
topology_rhino_points = []
for x, y, z in scaled_points:
    pt = rs.AddPoint(x, y, z)
    topology_rhino_points.append(pt)

# Create a Delaunay mesh from points
mesh = None
if len(topology_rhino_points) > 2:  # Ensure there are enough points for a mesh
    mesh = rs.AddMesh(topology_rhino_points)
    rs.ObjectColor(mesh, (200, 200, 200))  # Gray color for terrain

# Assign outputs for Grasshopper
sc.doc = Rhino.RhinoDoc.ActiveDoc  # Ensure Rhino context is active
a = topology_rhino_points if topology_rhino_points else None
b = mesh if mesh else None
sc.doc = ghdoc  # Reset to Grasshopper document

print("Topology Data Processed, Scaled to 100x100, and Mesh Created Successfully!")

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

# Raw input data as a list of strings
topology_data = [
    "-2012355.0,2765325.0,32767.0",
    "-2012325.0,2765325.0,32767.0",
    "-2012295.0,2765325.0,32767.0",
    "-2012265.0,2765325.0,32767.0",
    "-2010645.0,2765325.0,547.0",
    "-2010615.0,2765325.0,560.0",
    "-2010585.0,2765325.0,572.0"
]

# Scaling factor to remap coordinates to a manageable Rhino scale
scale_factor = 0.001  # Adjust as needed

# Process input data
topology_points = []
for line in topology_data:
    x, y, z = map(float, line.split(","))
    if z != 32767.0:  # Filter out invalid values
        x, y = x * scale_factor, y * scale_factor  # Apply scaling
        topology_points.append((x, y, z))

# Create points in Rhino based on topology locations
topology_rhino_points = []
for x, y, z in topology_points:
    pt = rs.AddPoint(x, y, z)
    topology_rhino_points.append(pt)

# Create a Delaunay mesh from points
if topology_rhino_points:
    mesh = rs.AddMesh(topology_rhino_points)
    rs.ObjectColor(mesh, (200, 200, 200))  # Gray color for terrain

print("Topology Data Processed, Scaled, and Mesh Created Successfully!")

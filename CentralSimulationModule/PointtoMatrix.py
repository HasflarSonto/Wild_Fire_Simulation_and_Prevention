import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import clr
clr.AddReference("Grasshopper")
clr.AddReference("RhinoCommon")
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
from Rhino.Geometry import Point3d

def create_burn_probability_matrix(coords_list, burn_prob_list):
    """
    Converts a list of coordinates and burn probabilities into a structured 2D matrix.
    
    Parameters:
    - coords_list (list): List of coordinate strings in format "{X, Y, Z}".
    - burn_prob_list (list): List of burn probabilities (same length as coords_list).
    
    Returns:
    - list: A structured 2D matrix of burn probabilities.
    """

    # Parse coordinates into numerical format
    parsed_coords = [tuple(map(float, coord.strip("{} ").split(","))) for coord in coords_list]
    burn_probs = [float(prob) for prob in burn_prob_list]

    # Extract unique sorted X and Y values to form the grid
    unique_x = sorted(set(p[0] for p in parsed_coords))
    unique_y = sorted(set(p[1] for p in parsed_coords), reverse=True)  # Reverse for top-down ordering

    # Create index mappings for X and Y
    x_index_map = {x: i for i, x in enumerate(unique_x)}
    y_index_map = {y: j for j, y in enumerate(unique_y)}

    # Initialize matrix
    burn_matrix = [[None for _ in range(len(unique_x))] for _ in range(len(unique_y))]

    # Fill the matrix with burn probabilities
    for (x, y, _), burn_prob in zip(parsed_coords, burn_probs):
        row = y_index_map[y]  # Y corresponds to row index
        col = x_index_map[x]  # X corresponds to column index
        burn_matrix[row][col] = burn_prob  # Assign burn probability

    return burn_matrix

# Example Usage
coords_list = ["{20.238095, 57.142857, 7.02381}", "{21.428571, 57.142857, 7.460317}", "{22.619048, 57.142857, 8.333333}", "{23.809524, 57.142857, 8.849206}", "{25, 57.142857, 9.166667}"]
burn_prob_list = ["0.4", "0.3", "0.3", "0.3", "0.4"]

burn_matrix = create_burn_probability_matrix(coords_list, burn_prob_list)

# Assign matrix to Grasshopper output
a = burn_matrix
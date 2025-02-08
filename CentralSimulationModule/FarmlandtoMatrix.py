def create_boolean_matrix(coords_list, bool_list):
    """
    Converts a list of coordinates and booleans into a structured 2D matrix.

    Parameters:
    - coords_list (list): List of coordinate strings in format "{X, Y, Z}".
    - bool_list (list): List of "True" or "False" values (same length as coords_list).

    Returns:
    - list: A structured 2D matrix of 0s (False) and 1s (True).
    """
    
    # Parse coordinates into numerical format
    parsed_coords = [tuple(map(float, coord.strip("{}").split(", "))) for coord in coords_list]
    bool_values = [1 if val == "True" else 0 for val in bool_list]  # Convert to 1/0

    # Extract unique sorted X and Y values to form the grid
    unique_x = sorted(set(p[0] for p in parsed_coords))
    unique_y = sorted(set(p[1] for p in parsed_coords), reverse=True)  # Reverse Y for top-down ordering

    # Create index mappings for X and Y
    x_index_map = {x: i for i, x in enumerate(unique_x)}
    y_index_map = {y: j for j, y in enumerate(unique_y)}

    # Initialize matrix
    bool_matrix = [[0 for _ in range(len(unique_x))] for _ in range(len(unique_y))]

    # Fill the matrix with boolean values
    for (x, y, _), value in zip(parsed_coords, bool_values):
        row = y_index_map[y]  # Y corresponds to row index
        col = x_index_map[x]  # X corresponds to column index
        bool_matrix[row][col] = value  # Assign 1 (True) or 0 (False)

    return bool_matrix

# Example Usage
coords_list = ["{33.333333, 69.047619, 10.674603}", "{34.52381, 69.047619, 10.753968}", "{35.714286, 69.047619, 10.793651}"]
bool_list = ["False", "True", "False"]

bool_matrix = create_boolean_matrix(coords_list, bool_list)

# Assign matrix to Grasshopper output
a = bool_matrix

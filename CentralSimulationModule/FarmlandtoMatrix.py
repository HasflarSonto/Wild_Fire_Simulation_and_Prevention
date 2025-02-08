def create_boolean_matrix(coords_list, boolean_list):
    """
    Converts a list of coordinates and booleans into a structured 2D matrix grid.
    
    Parameters:
    - coords_list (list): List of coordinate strings in format "{X, Y, Z}".
    - boolean_list (list): List of "True" or "False" values (same length as coords_list).
    
    Returns:
    - list: A structured 2D matrix with 0 (False) and 1 (True) values.
    """
    
    # Parse coordinates into numerical format
    parsed_coords = [tuple(map(float, coord.strip("{} ").split(","))) for coord in coords_list]
    boolean_values = [1 if value == "True" else 0 for value in boolean_list]
    
    # Extract unique sorted X and Y values to form the grid
    unique_x = sorted(set(p[0] for p in parsed_coords))
    unique_y = sorted(set(p[1] for p in parsed_coords), reverse=True)  # Reverse for top-down ordering
    
    # Create index mappings for X and Y
    x_index_map = {x: i for i, x in enumerate(unique_x)}
    y_index_map = {y: j for j, y in enumerate(unique_y)}
    
    # Initialize matrix
    boolean_matrix = [[None for _ in range(len(unique_x))] for _ in range(len(unique_y))]
    
    # Fill the matrix with boolean values
    for (x, y, _), value in zip(parsed_coords, boolean_values):
        row = y_index_map[y]  # Y corresponds to row index
        col = x_index_map[x]  # X corresponds to column index
        boolean_matrix[row][col] = value  # Assign boolean value
    
    return boolean_matrix

def matrix_to_boolean_list(matrix):
    """
    Converts a 2D boolean matrix back into a structured single list of strings.
    
    Returns:
    - list: A single list of "True" or "False" values matching the original order.
    """
    ordered_list = []
    for row in reversed(matrix):  # Reverse rows to match Grasshopper's top-down Y ordering
        for cell in row:
            ordered_list.append("True" if cell == 1 else "False")
    return ordered_list

# Example Usage
coords_list = ["{33.333333, 69.047619, 10.674603}", "{34.52381, 69.047619, 10.753968}", "{35.714286, 69.047619, 10.793651}", "{36.904762, 69.047619, 10.873016}", "{38.095238, 69.047619, 10.873016}"]
boolean_list = ["False", "True", "False", "False", "True"]

boolean_matrix = create_boolean_matrix(coords_list, boolean_list)
boolean_list_converted = matrix_to_boolean_list(boolean_matrix)

# Assign outputs
a = boolean_matrix  # 2D matrix representation
b = boolean_list_converted  # Converted back to a single list

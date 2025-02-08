import random
import math

def compute_wind_severity(direction_vector, wind_vector):
    """Calculates wind severity in a given direction."""
    magnitude = (direction_vector[0]**2 + direction_vector[1]**2) ** 0.5
    if magnitude == 0:
        return 0
    unit_vector = (direction_vector[0] / magnitude, direction_vector[1] / magnitude)
    wind_magnitude = (wind_vector[0]**2 + wind_vector[1]**2) ** 0.5
    wind_unit_vector = (wind_vector[0] / wind_magnitude, wind_vector[1] / wind_magnitude)
    return unit_vector[0] * wind_unit_vector[0] + unit_vector[1] * wind_unit_vector[1]

def find_fire_start(grid, wind_vector):
    """Finds fire starting location based on wind direction."""
    row = 0 if wind_vector[1] < 0 else len(grid) - 1
    col = len(grid[0]) - 1 if wind_vector[0] < 0 else 0
    return row, col

def calculate_fire_probability(material, direction_vector, wind_vector):
    """Determines probability of fire spread based on material and wind."""
    prob = material
    severity = compute_wind_severity(direction_vector, wind_vector)
    return 0 if severity < 0 else prob * severity

def spread_fire(grid, wind_vector, steps=10):
    """Simulates fire spread over a given number of steps."""
    fire_grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])
    timer = {}
    material_timer = {0.5: 10, 0.4: 10, 0.3: 10, 0.2: 10}
    
    row, col = find_fire_start(grid, wind_vector)
    timer[(row, col)] = material_timer[grid[row][col]]
    fire_grid[row][col] = 1  # Fire starts
    
    for _ in range(steps):
        new_fire_grid = fire_grid.copy()
        for i in range(rows):
            for j in range(cols):
                if fire_grid[i][j] == 1:  # Tile is on fire
                    timer[(i, j)] -= 1
                    if timer[(i, j)] <= 0:
                        new_fire_grid[i][j] = -1  # Burnt out
                        continue
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and new_fire_grid[ni][nj] > 0 and new_fire_grid[ni][nj] < 1:
                            material = grid[ni][nj]
                            #di changes the y
                            #dj chnages the x
                            new_prob = calculate_fire_probability(material, (dj, -di), wind_vector)
                            if random.random() < new_prob:
                                new_fire_grid[ni][nj] = 1
                                timer[(ni, nj)] = material_timer[material]
        fire_grid = new_fire_grid
    return fire_grid

def matrix_to_list(matrix):
    """Converts a 2D matrix back into a structured single list of strings in row-major order."""
    ordered_list = []
    for row in matrix:
        for cell in row:
            ordered_list.append(str(cell))  # Convert each value back to a string
    return ordered_list

# Example Usage
grid = [[0.3, 0.4, 0.4], [0.3, 0.3, 0.4], [0.3, 0.3, 0.5]]
wind_vector = (-4,3)
def simulate_fire(grid, wind_vector):
    final_fire_grid = spread_fire(grid, wind_vector)
    a = final_fire_grid
    # b = matrix_to_list(final_fire_grid)
    # print(a)
    # print(b)
    return a
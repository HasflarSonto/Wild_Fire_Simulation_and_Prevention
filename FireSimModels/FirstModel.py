import random

# Wind vector: (x, y) direction
WIND_VECTOR = (2, 3)

def compute_wind_severity(direction_vector):
    """Calculates wind severity in a given direction."""
    magnitude = (direction_vector[0]**2 + direction_vector[1]**2) ** 0.5
    if magnitude == 0:
        return 0  # No wind influence
    unit_vector = (direction_vector[0] / magnitude, direction_vector[1] / magnitude)
    wind_magnitude = (WIND_VECTOR[0]**2 + WIND_VECTOR[1]**2) ** 0.5
    wind_unit_vector = (WIND_VECTOR[0] / wind_magnitude, WIND_VECTOR[1] / wind_magnitude)
    
    return unit_vector[0] * wind_unit_vector[0] + unit_vector[1] * wind_unit_vector[1]

# Material burn probabilities
MATERIALS = {
    -1: 0.0,  # Burnt
    0: 0.5,   # Brush
    1: 0.4,   # Long Needle Litter
    2: 0.3,   # Short Needle Litter
    3: 0.2    # Short Grass
}

# Time before a tile is considered burnt out
material_timer = {0.5: 10, 0.4: 10, 0.3: 10, 0.2: 10}

# Example Grid (Manually Defined)
grid = [
    [0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4],
    [0.3, 0.3, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.4],
    [0.3, 0.3, 0.5, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4],
    [0.3, 0.4, 0.5, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3]
]

# Find fire starting point
def find_fire_start(wind):
    """Finds fire starting location based on wind direction."""
    row = 0 if wind[1] < 0 else len(grid) - 1
    col = len(grid[0]) - 1 if wind[0] < 0 else 0
    return row, col

# Initialize fire
row, col = find_fire_start(WIND_VECTOR)
timer = {}
timer[(row, col)] = material_timer[grid[row][col]]
grid[row][col] = 1  # Fire starts

# Fire spread calculation
def calculate_fire_probability(material, direction_vector):
    """Determines probability of fire spread based on material and wind."""
    prob = material
    severity = compute_wind_severity(direction_vector)
    if severity < 0:
        return 0
    return prob * severity

# Spread fire function
def spread_fire(fire_grid):
    """Spreads fire in the grid based on rules."""
    new_fire_grid = [row[:] for row in fire_grid]  # Copy grid
    rows, cols = len(grid), len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if new_fire_grid[i][j] == 1:  # Tile is on fire
                timer[(i, j)] -= 1
                if timer[(i, j)] <= 0:
                    new_fire_grid[i][j] = -1  # Burnt out
                    continue

                # Spread fire to neighbors
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and new_fire_grid[ni][nj] > 0 and new_fire_grid[ni][nj] < 1:
                        material = grid[ni][nj]
                        new_prob = calculate_fire_probability(material, (-di, dj))
                        if random.random() < new_prob:
                            new_fire_grid[ni][nj] = 1  # Tile catches fire
                            timer[(ni, nj)] = material_timer[material]
    
    return new_fire_grid

# Run simulation for 10 steps
fire_grid = grid
for step in range(10):
    print(f"Step {step+1}:")
    fire_grid = spread_fire(fire_grid)
    for row in fire_grid:
        print(row)
    print()

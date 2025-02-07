import numpy as np
import random
import math

#inputs are:
# 1) 2d matrix w/ (x, y, type of material, current burn probability)
# 2) wind tuple

# Wind direction influence as a tuple (x, y) and severity
WIND_VECTOR = np.array([2, 3])
WIND_UNIT = WIND_VECTOR / np.linalg.norm(WIND_VECTOR)
#severity will just be calculated on the norm of (x,y)

def compute_wind_severity(direction_vector):
    direction_magnitude = np.linalg.norm(direction_vector)
    
    if direction_magnitude == 0:
        return 0  # No wind influence if the direction vector is zero
    
    direction_unit = direction_vector / direction_magnitude
    
    severity = np.dot(WIND_UNIT, direction_unit)
    return severity


MATERIALS = {
    -1: 0.0, #Burnt
    0: 0.6,  # Grass
    1: 0.8,  # Wood
    2: 0.0,  # Water (cannot catch fire)
    3: 0.3   # Dirt
}


material_timer = {
    0: 2,  # Grass
    1: 5,  # Wood
    3: 1   # Dirt

}


# Initialize a grid with materials
grid = np.array([
    [0, 0, 1, 2, 3],
    [0, 1, 1, 2, 3],
    [0, 0, 0, 2, 3],
    [3, 0, 1, 1, 0],
    [3, 3, 0, 0, 0]
])


# Fire grid (0 = not on fire, 1 = on fire)
# the higher the value is, the higher probability it ends on fire
fire_grid = np.zeros(grid.shape, dtype=float)
for r in range(len(grid)):
    for c in range(len(grid[0])):
        fire_grid[r][c] = MATERIALS[grid[r][c]]

#should have values in a double format



# Start fire at a random location
fire_grid[1, 2] = 1

#timer is going to be a dictionary with key (i,j) and value of the time set
timer = dict()
timer[(1,2)] = material_timer[grid[1][2]]

#right now only calculates this value based on wind and material
def calculate_fire_probability(material, direction_vector):
    prob = MATERIALS[material]
    severity = compute_wind_severity(direction_vector)
    if severity < 0:
        return 0
    res = prob * severity
    return prob * severity

#should I take in the previous probability? 
#probably nice 



def spread_fire(grid, fire_grid):
    new_fire_grid = fire_grid.copy()
    rows, cols = grid.shape
    
    for i in range(rows):
        for j in range(cols):
            if fire_grid[i, j] == 1:  # If the tile is on fire
                timer[(i,j)] -= 1
                if timer[(i,j)] <= 0:
                    new_fire_grid[i][j] = -1
                    timer.pop((i,j))
                    continue
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Check all neighbors
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and new_fire_grid[ni, nj] > 0 and new_fire_grid[ni,nj] < 1:
                        material = grid[ni, nj]
                        newProb = calculate_fire_probability(material, (di,dj))
                        if random.random() < newProb:
                            new_fire_grid[ni, nj] = 1  # Tile catches fire
                            timer[(ni,nj)] = material_timer[material]
    return new_fire_grid

# Run simulation for a few steps

for step in range(10):
    print(f"Step {step+1}:")
    fire_grid = spread_fire(grid, fire_grid)
    print(fire_grid)
    print()


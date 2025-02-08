import random
import math

wind_vector = (-1,3)
windVectors = []
windVectors.append(wind_vector)
for i in range(9,5,-1):
        newMagnitude = i * 0.10
        newX = newMagnitude * wind_vector[0] * math.cos(1 - newMagnitude)
        newY = newMagnitude * wind_vector[1] * math.sin(1 - newMagnitude)
        windVectors.append([newX,newY])
def compute_wind_severity(direction_vector, windVectors):
    """Calculates wind severity in a given direction."""
    magnitude = (direction_vector[0]**2 + direction_vector[1]**2) ** 0.5
    if magnitude == 0:
        return 0
    
    unit_vector = (direction_vector[0] / magnitude, direction_vector[1] / magnitude)

    maxSeverity = 0
    for wind_vector in windVectors:
        wind_magnitude = (wind_vector[0]**2 + wind_vector[1]**2) ** 0.5
        wind_unit_vector = (wind_vector[0] / wind_magnitude, wind_vector[1] / wind_magnitude)
        maxSeverity = max(maxSeverity, unit_vector[0] * wind_unit_vector[0] + unit_vector[1] * wind_unit_vector[1])
    return maxSeverity

def find_fire_start(grid, wind_vector):
    """Finds fire starting location based on wind direction."""
    row = 0 if wind_vector[1] < 0 else len(grid) - 1
    col = len(grid[0]) - 1 if wind_vector[0] < 0 else 0
    return row, col

def calculate_fire_probability(material, direction_vector, wind_vector):
    """Determines probability of fire spread based on material and wind."""
    prob = material
    severity = compute_wind_severity(direction_vector, wind_vector)
    #divide by the distance
    direction_magnitude = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
    return 0 if severity < 0 else prob * severity / (direction_magnitude)

def spread_fire(grid, wind_vector, steps=10):
    """Simulates fire spread over a given number of steps."""
    rows, cols = len(grid), len(grid[0])
    timer = {}
    material_timer = {0.5: 5, 0.4: 5, 0.3: 5, 0.2: 5}
    
    row, col = find_fire_start(grid, wind_vector)
    timer[(row, col)] = material_timer[grid[row][col]]
    new_fire_grid = [row[:] for row in grid]
    new_fire_grid[row][col] = 1  # Fire starts
    probabilityMatrix = [[0]*len(grid[0]) for row in grid]
    probabilityMatrix[row][col] = 1
    coordinates = [(x, y) for x in range(-2, 3) for y in range(-2, 3) if not (x == 0 and y == 0)]
    for _ in range(steps):
        #probabilityMatrix = [[0]*len(grid[0]) for row in grid]
        for i in range(rows):
            for j in range(cols):
                if (i,j) in timer: # Tile is on fire
                    timer[(i, j)] -= 1
                    if timer[(i, j)] <= 0:
                        new_fire_grid[i][j] = -1  # Burnt out
                        timer.pop(i,j)
                        continue
                    for di, dj in coordinates:
                        ni, nj = i + di, j + dj

                        if 0 <= ni < rows and 0 <= nj < cols and (ni,nj) not in timer:
                            material = grid[ni][nj]
                            # #di changes the y
                            # #dj chnages the x
                            new_prob = calculate_fire_probability(material, (dj, -di), windVectors)
                            probabilityMatrix[ni][nj] = max(probabilityMatrix[ni][nj],new_prob)
                            if random.random() < probabilityMatrix[ni][nj]:
                                new_fire_grid[ni][nj] = 1
                                timer[(ni,nj)] = material_timer[material]

    return new_fire_grid

def matrix_to_list(matrix):
    """Converts a 2D matrix back into a structured single list of strings in row-major order."""
    ordered_list = []
    for row in matrix:
        for cell in row:
            ordered_list.append(str(cell))  # Convert each value back to a string
    return ordered_list

# Example Usage
grid = [[0.4, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3], [0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.4, 0.5, 0.3, 0.4, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.5, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.4, 0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.4, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.4, 0.4, 0.3, 0.3, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.3, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.3], [0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.5, 0.2, 0.2, 0.2, 0.3, 0.4, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3], [0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.4, 0.4, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.2, 0.2, 0.4, 0.2, 0.2, 0.5, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.2, 0.2, 0.5, 0.2, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2], [0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.4, 0.5, 0.2, 0.2, 0.2, 0.2], [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.5, 0.5, 0.4, 0.4, 0.2, 0.2, 0.4], [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.4, 0.4, 0.2, 0.2], [0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.4, 0.3, 0.4], [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.5, 0.4, 0.4, 0.4, 0.4], [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.5], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.3, 0.3, 0.3, 0.5, 0.4, 0.5, 0.5], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.4, 0.4, 0.5, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4], [0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4], [0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.3, 0.5, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3]]

def simulate_fire(grid, wind_vector):
    final_fire_grid = spread_fire(grid, wind_vector)
    a = final_fire_grid
    # b = matrix_to_list(final_fire_grid)
    # print(a)
    # print(b)
    return a

simulate_fire(grid,wind_vector)


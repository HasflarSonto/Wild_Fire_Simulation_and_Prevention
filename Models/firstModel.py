import random
import math
import heapq

wind_vector = (0,2)
windVectors = []
windVectors.append(wind_vector)


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
    x = wind_vector[0]
    y = wind_vector[1]
    
    #the c's correspond to the interval of x's
    xInterval = None
    yInterval = None
    if x > 0:
        xInterval = [0,x]
    elif x < 0:
        xInterval = [ x + len(grid[0]) -1  ,len(grid[0])-1]
    
    #this is the c
    if y > 0:
        yInterval = [len(grid) - 1 - y ,len(grid) -1]
    elif y < 0:
        yInterval = [0, abs(y)]
    #this is the r
    hp = []
    heapq.heapify(hp)

    if x < 0 and yInterval:
        for r in yInterval:
            heapq.heappush(hp, [grid[r][len(grid[0])-1],(r, len(grid[0])-1)])
    elif x > 0 and yInterval:
        for r in yInterval:
            heapq.heappush(hp, [grid[r][0],(r, 0)])
    elif yInterval:
        
        for r in yInterval:
            heapq.heappush(hp, [grid[r][len(grid[0])//2], (r, int(len(grid[0])//2) )])
    if y < 0 and xInterval:
        for c in xInterval:
            heapq.heappush(hp, [grid[0][c], (0, c)])
    elif y > 0 and xInterval:
        for c in xInterval:
            heapq.heappush(hp, [grid[len(grid)-1][c], (len(grid)-1 , c)])
    elif xInterval:
        heapq.heappush(hp, [grid[int(len(grid)//2)][c], (int(len(grid)//2), c)])
    res = hp[0][1]
    while len(hp) > 10:
        heapq.heappop(hp)
    
    for i in range(random.randint(1, len(hp))):
        res = heapq.heappop(hp)
    row = res[1][0]
    col = res[1][1]
    return row, col

def calculate_fire_probability(material, direction_vector, wind_vector):
    """Determines probability of fire spread based on material and wind."""
    prob = material
    severity = compute_wind_severity(direction_vector, wind_vector)
    return 0 if severity < 0 else prob * severity

def matrix_to_list(matrix):
    """Converts a 2D matrix back into a structured single list of strings in row-major order."""
    ordered_list = []
    for row in (matrix):
        for cell in row:
            ordered_list.append(str(cell))  # Convert each value back to a string
    return ordered_list

def spread_fire(grid, wind_vector, steps=10):
    """Simulates fire spread over a given number of steps."""
    fire_grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])
    timer = {}
    
    
    row, col = find_fire_start(grid, wind_vector)
    timer[(row, col)] = 10
    fire_grid[row][col] = 1  # Fire starts
    
    for _ in range(steps):
        new_fire_grid = [row[:] for row in fire_grid]
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
                            new_prob = calculate_fire_probability(material, (dj, -di), wind_vector)
                            if random.random() < new_prob:
                                new_fire_grid[ni][nj] = 1
                                timer[(ni, nj)] = 10
        fire_grid = new_fire_grid
    return fire_grid



# Example Usage
grid = [[0.4, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3], [0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.4, 0.5, 0.3, 0.4, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.5, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.4, 0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.4, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.4, 0.4, 0.3, 0.3, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.3, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.3], [0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.5, 0.2, 0.2, 0.2, 0.3, 0.4, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3], [0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.4, 0.4, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.2, 0.2, 0.4, 0.2, 0.2, 0.5, 0.4], [0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.3, 0.4, 0.4, 0.4, 0.2, 0.2, 0.5, 0.2, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2], [0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.4, 0.5, 0.2, 0.2, 0.2, 0.2], [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.5, 0.5, 0.4, 0.4, 0.2, 0.2, 0.4], [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.4, 0.4, 0.2, 0.2], [0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.4, 0.3, 0.4], [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.5, 0.4, 0.4, 0.4, 0.4], [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.5], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.3, 0.3, 0.3, 0.5, 0.4, 0.5, 0.5], [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.3, 0.3, 0.4, 0.4, 0.5, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4], [0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4], [0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.3, 0.5, 0.3, 0.3, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3]]

#wind_vector = (float(wind_input_x),float(wind_input_y))
print(wind_vector)



allGrids = []
for _ in range(100):
    final_grid = spread_fire(grid, wind_vector)
    allGrids.append(final_grid)


#print(allGrids)

res = allGrids[0].copy()
#divide by the number of steps
for r in range(len(res)):
    for c in range(len(res[0])):
        currVal = 0
        for arr in allGrids:
            currVal += abs(arr[r][c])
        
        res[r][c] = currVal/100


a = res
for i in res:
    print(i)

b = matrix_to_list(res)
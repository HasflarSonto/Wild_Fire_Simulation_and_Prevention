import collections
import heapq
import math

wind_vector = (3,7)

def create_firebreak_land(mat, walls, strips):
    rows, cols = len(mat), len(mat[0])

    print(walls)

    for m in range(rows):
        for n in range(cols):
            if (m,n) in walls:
                mat[m][n] = True
            else:
                mat[m][n] = False

    return mat

def find_matrix_bounds(mat):
    high_x, high_y = float('-inf'), float('-inf')
    low_x, low_y = float('inf'), float('inf')

    rows, cols = len(mat), len(mat[0])

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 1:  # Only consider farmed land
                high_x = max(r, high_x)
                low_x = min(r, low_x)
                high_y = max(c, high_y)
                low_y = min(c, low_y)

    # If no farmland was found, return None
    if high_x == float('-inf'):
        return None  

    return high_x, low_x, high_y, low_y

def find_cluster_bounds(cluster):
    high_x, high_y = float('-inf'), float('-inf')
    low_x, low_y = float('inf'), float('inf')

    for c in cluster:
        high_x = max(c[0], high_x)
        low_x = min(c[0], low_x)
        high_y = max(c[1], high_y)
        low_y = min(c[1], low_y)
    
    return high_x, low_x, high_y, low_y

def create_bound(high_cluster_x, low_cluster_x, high_cluster_y, low_cluster_y):
    boundary = set()

    for x in range(low_cluster_x, high_cluster_x + 1):
        boundary.add((x, low_cluster_y))
        boundary.add((x, high_cluster_y)) 

    for y in range(low_cluster_y, high_cluster_y + 1):
        boundary.add((low_cluster_x, y))
        boundary.add((high_cluster_x, y))

    return boundary

        
def generate_structures(farm_mat, landX, landY, burn_cluster, wall_threshold):
    heuristic_cluster = assign_heuristic(burn_cluster, *find_matrix_bounds(farm), landX, landY, 10)

    wall_generation = set()
    strip_generation = []

    for info, coords in heuristic_cluster.items():
        if len(coords) < wall_threshold:
            wall_generation.update(create_bound(*find_cluster_bounds(coords)))
            continue

    return wall_generation

def assign_heuristic(burn_cluster, high_farm_x, low_farm_x, high_farm_y, low_farm_y, land_len_x, land_len_y, chop, wind_vector):
    heuristic_values =  []

    farm_center = (((high_farm_x + low_farm_x)/2), ((high_farm_y + low_farm_y)/2))

    for info, coords in burn_cluster.items():
        for c in coords:
            # COM_x = info[0]
            # COM_y = info[1] 
            # MOI = info[2]

            x = c[0]
            y = c[1]

            if not (x in range(low_farm_x, high_farm_x) and y in range(low_farm_y, high_farm_y)):
                distance_from_farm = min(
                    math.sqrt((x - low_farm_x) ** 2 + (y - low_farm_y) ** 2),
                    math.sqrt((x - low_farm_x) ** 2 + (y - high_farm_y) ** 2),
                    math.sqrt((x - high_farm_x) ** 2 + (y - low_farm_y) ** 2),
                    math.sqrt((x - high_farm_x) ** 2 + (y - high_farm_y) ** 2)
                )
            else:
                #automatically set the hueristic to 1 (HIGH PRIORITY)
                # # new_info = (x, y, info[2], 1, 1, 1)
                # heapq.heappush(heuristic_values, (-1.0, (x,y)))
                continue

            decay_constant = 0.3
            alignment_constant = 0.1

            wind_x, wind_y = wind_vector[0], wind_vector[1]
            point_to_farm_x, point_to_farm_y = farm_center[0] - x, farm_center[1] - y

            alignment = (wind_x * point_to_farm_x) + (wind_y * point_to_farm_y)


            distance_heuristic = math.exp(-decay_constant * distance_from_farm)            
            wind_heuristic = 1 / (1 + math.exp(-alignment_constant * alignment))
            # spread_heuristic = MOI/chop
            # size_heuristic = len(coords) / (land_len_x * land_len_y)

            # new_info = (COM_x, COM_y, info[2], distance_heuristic, spread_heuristic, size_heuristic)

            w1, w2, w3 = 0.5, 0.4, 0.1

            total_heuristic = (w1 * distance_heuristic) + (w2 * wind_heuristic)
            
            heapq.heappush(heuristic_values, (-total_heuristic, (x,y)))

    return heuristic_values
    
            
def find_burn_probability_clusters(mat, threshold, cluster_size):
    burn_clusters = {}

    visited_land = set()  

    rows, cols = len(mat), len(mat[0])

    def bfs_helper(r, c):
        q = collections.deque()
        visited_land.add((r,c))
        q.append((r,c))

        current_cluster = [(r,c)]
        sum_x, sum_y, count = r, c, 1

        while q:
            row, col = q.popleft()
            dirs = [[1,0], [-1,0], [0,1], [0,-1]]

            for dr, dc in dirs:
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < rows and 0 <= new_col < cols:

                    if mat[new_row][new_col] >= threshold and (new_row, new_col) not in visited_land:
                        visited_land.add((new_row, new_col))
                        q.append((new_row, new_col))
                        current_cluster.append((new_row, new_col))
                        sum_x += new_row
                        sum_y += new_col
                        count += 1
        
        if len(current_cluster) >= cluster_size:
            moment_of_inertia = 0
            COM_x, COM_y = sum_x / count, sum_y / count

            moment_of_inertia = sum(
                ( (c[0] - COM_x) ** 2 + (c[1] - COM_y) ** 2 ) for c in current_cluster
            )

            moment_of_inertia /= len(current_cluster)
            
            burn_clusters[(COM_x, COM_y, moment_of_inertia)] = current_cluster


    for r in range(rows):
        for c in range(cols):
            if mat[r][c] >= threshold and (r,c) not in visited_land:
                bfs_helper(r, c)
    
    return burn_clusters


# walls = generate_structures(farm, len(farmland_matrix), len(farmland_matrix[0]), clusters, 10)
# new_matrix = create_firebreak_land(farmland_matrix, walls, [])

farmland_matrix = []
farm = []

def find_n_priority_points(n, heuristics):
    priority = []

    for _ in range(n):
        priority.append(heapq.heappop(heuristics)[1])

    return priority

clusters = find_burn_probability_clusters(farmland_matrix, 0.8, 0)

# assign_heuristic(burn_cluster, *find_matrix_bounds(farm), landX, landY, 10)

heuristics = assign_heuristic(clusters, *find_matrix_bounds(farm), len(farmland_matrix), len(farmland_matrix[0]), 10, (2,2))

priority_points = find_n_priority_points(20, heuristics)

rows = len(farmland_matrix)
cols = len(farmland_matrix[0])

new_mat = [[False for _ in range(cols)] for _ in range(rows)]

for p in priority_points:
    new_mat[p[0]][p[1]] = True
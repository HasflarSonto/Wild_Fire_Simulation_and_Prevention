import collections
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
        high_x = max(r, high_x)
        low_x = min(r, low_x)
        for c in range(cols):
            high_y = max(c, high_y)
            low_y = min(c, low_y)
    
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
    heuristic_cluster = assign_heuristic(burn_cluster, *find_matrix_bounds(farm), landX, landY, 0.3, 10)

    wall_generation = set()
    strip_generation = []

    for info, coords in heuristic_cluster.items():
        if len(coords) < wall_threshold:
            wall_generation.update(create_bound(*find_cluster_bounds(coords)))
            continue

    return wall_generation

def assign_heuristic(burn_cluster, high_farm_x, low_farm_x, high_farm_y, low_farm_y, land_len_x, land_len_y, decay_constant, chop):
    heuristic_cluster = {}

    farm_center = (((high_farm_x + low_farm_x)/2), ((high_farm_y + low_farm_y)/2))

    for info, coords in burn_cluster.items():
        COM_x = info[0]
        COM_y = info[1] 
        MOI = info[2]

        if COM_x not in range(low_farm_x, high_farm_x) and COM_y not in range(low_farm_y, high_farm_y):
            distance_from_farm = ((farm_center[0] - COM_x)**2 + (farm_center[1] - COM_y)**2)**0.5
        else:
            #automatically set the hueristic to 1 (HIGH PRIORITY)
            new_info = (COM_x, COM_y, info[2], 1, 1, 1)
            heuristic_cluster[new_info] = coords
            continue

        distance_heuristic = math.exp(-decay_constant * distance_from_farm)
        spread_heuristic = MOI/chop
        size_heuristic = len(coords) / (land_len_x * land_len_y)

        new_info = (COM_x, COM_y, info[2], distance_heuristic, spread_heuristic, size_heuristic)
        
        heuristic_cluster[new_info] = coords 

    return heuristic_cluster
    
            
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

clusters = find_burn_probability_clusters(farmland_matrix, 0.9, 4)
walls = generate_structures(farm, len(farmland_matrix), len(farmland_matrix[0]), clusters, 10)
new_matrix = create_firebreak_land(farmland_matrix, walls, [])

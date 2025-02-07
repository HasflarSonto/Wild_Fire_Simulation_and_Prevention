import collections

farmland_matrix = [
    [(0, 0, 0.1), (0, 1, 0.1), (0, 2, 0.1), (0, 3, 0.2), (0, 4, 0.2), (0, 5, 0.2), (0, 6, 0.1), (0, 7, 0.1), (0, 8, 0.1), (0, 9, 0.1)],
    [(1, 0, 0.1), (1, 1, 0.1), (1, 2, 0.2), (1, 3, 0.3), (1, 4, 0.3), (1, 5, 0.3), (1, 6, 0.2), (1, 7, 0.1), (1, 8, 0.1), (1, 9, 0.1)],
    [(2, 0, 0.1), (2, 1, 0.2), (2, 2, 0.3), (2, 3, 0.4), (2, 4, 0.4), (2, 5, 0.4), (2, 6, 0.3), (2, 7, 0.2), (2, 8, 0.1), (2, 9, 0.1)],
    [(3, 0, 0.2), (3, 1, 0.3), (3, 2, 0.4), (3, 3, 0.5), (3, 4, 0.6), (3, 5, 0.5), (3, 6, 0.4), (3, 7, 0.3), (3, 8, 0.2), (3, 9, 0.1)],
    [(4, 0, 0.2), (4, 1, 0.3), (4, 2, 0.4), (4, 3, 0.6), (4, 4, 0.7), (4, 5, 0.6), (4, 6, 0.4), (4, 7, 0.3), (4, 8, 0.2), (4, 9, 0.1)],
    [(5, 0, 0.2), (5, 1, 0.3), (5, 2, 0.4), (5, 3, 0.5), (5, 4, 0.6), (5, 5, 0.5), (5, 6, 0.4), (5, 7, 0.3), (5, 8, 0.2), (5, 9, 0.1)],
    [(6, 0, 0.1), (6, 1, 0.2), (6, 2, 0.3), (6, 3, 0.4), (6, 4, 0.4), (6, 5, 0.4), (6, 6, 0.3), (6, 7, 0.2), (6, 8, 0.1), (6, 9, 0.1)],
    [(7, 0, 0.1), (7, 1, 0.1), (7, 2, 0.2), (7, 3, 0.3), (7, 4, 0.3), (7, 5, 0.3), (7, 6, 0.2), (7, 7, 0.1), (7, 8, 0.1), (7, 9, 0.1)],
    [(8, 0, 0.1), (8, 1, 0.1), (8, 2, 0.1), (8, 3, 0.2), (8, 4, 0.2), (8, 5, 0.2), (8, 6, 0.1), (8, 7, 0.1), (8, 8, 0.1), (8, 9, 0.1)],
    [(9, 0, 0.1), (9, 1, 0.1), (9, 2, 0.1), (9, 3, 0.1), (9, 4, 0.1), (9, 5, 0.1), (9, 6, 0.1), (9, 7, 0.1), (9, 8, 0.1), (9, 9, 0.1)]
]

def create_firebreak(mat, fire_break_position):
    for x,y in fire_break_position:
        mat[x][y] = 0

def find_burn_clusters(mat, threshold):
    burn_clusters = {}
    cluster_num = 0

    visited_land = set()  

    rows, cols = len(mat), len(mat[0])

    def bfs_helper(r, c, cluster_id):
        q = collections.deque()
        visited_land.add((r,c))
        q.append((r,c))

        burn_clusters[cluster_id] = [mat[r][c]]

        while q:
            row, col = q.popleft()
            dirs = [[1,0], [-1,0], [0,1], [0,-1]]

            for dr, dc in dirs:
                new_row, new_col = row + dr, col + dc

                if 0 <= new_row < rows and 0 <= new_col < cols:

                    if mat[new_row][new_col][2] >= threshold and (new_row, new_col) not in visited_land:
                        visited_land.add((new_row, new_col))
                        q.append((new_row, new_col))
                        burn_clusters[cluster_id].append(mat[r][c])


    for r in range(rows):
        for c in range(cols):
            if mat[r][c][2] >= threshold and (r,c) not in visited_land:
                bfs_helper(r, c, cluster_num)
                cluster_num += 1
    
    return burn_clusters
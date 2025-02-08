import FirstModel
import random

grid = [[0.3, 0.4, 0.4], [0.3, 0.3, 0.4], [0.3, 0.3, 0.5]]
wind_vector = (-1,3)
allGrids = []
for _ in range(100):
    
    final_grid = FirstModel.simulate_fire(grid, wind_vector)
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

print(res)
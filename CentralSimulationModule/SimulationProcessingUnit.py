import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import random

# Inputs from Grasshopper
terrain_points = IN[0]  # 2D grid of points (x, y, z)
wind_vector = IN[1]  # Wind influence (x, y)
fuel_map = IN[2]  # Fuel values per point (0 to 1)
sim_steps = IN[3]  # Number of simulation steps
fire_start = IN[4]  # Initial fire points (list of indices)

# Grid dimensions
grid_width = len(set([p.X for p in terrain_points]))
grid_height = len(set([p.Y for p in terrain_points]))

# Initialize fire grid: 0 = unburned, 1 = burning, 2 = burned
fire_grid = [0] * len(terrain_points)
for idx in fire_start:
    fire_grid[idx] = 1  # Start fire at given indices

# Fire spread function
def spread_fire():
    global fire_grid
    new_grid = fire_grid[:]
    for i, state in enumerate(fire_grid):
        if state == 1:  # Burning
            x, y, z = terrain_points[i].X, terrain_points[i].Y, terrain_points[i].Z
            
            # Check neighboring points (N, S, E, W)
            neighbors = [i - 1, i + 1, i - grid_width, i + grid_width]
            for ni in neighbors:
                if 0 <= ni < len(fire_grid) and fire_grid[ni] == 0:  # Unburned
                    # Compute probability of burning
                    fuel = fuel_map[ni]
                    wind_effect = (terrain_points[ni].X - x) * wind_vector[0] + (terrain_points[ni].Y - y) * wind_vector[1]
                    burn_prob = min(1.0, fuel + wind_effect * 0.1)
                    
                    if random.random() < burn_prob:
                        new_grid[ni] = 1  # Set to burning
            
            new_grid[i] = 2  # Mark as burned
    
    fire_grid = new_grid[:]

# Run simulation
frames = []
for _ in range(sim_steps):
    spread_fire()
    frames.append(fire_grid[:])

# Output fire states as color-mapped points
output_colors = []
for step in frames:
    colors = [
        Rhino.Display.ColorRGBA(0, 255, 0, 255) if s == 0 else  # Green (unburned)
        Rhino.Display.ColorRGBA(255, 0, 0, 255) if s == 1 else  # Red (burning)
        Rhino.Display.ColorRGBA(0, 0, 0, 255)  # Black (burned)
        for s in step
    ]
    output_colors.append(colors)

OUT = output_colors

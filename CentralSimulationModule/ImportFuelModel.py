import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import csv

# Input: Path to the processed fuel model CSV file
csv_path = "processed_fuel_model_data.csv"  # Update with actual path

# Read CSV file and extract X, Y, Fuel_Model, Burn_Probability
fuel_points = []
with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        x, y, fuel_model, burn_prob = map(float, row)
        fuel_points.append((x, y, fuel_model, burn_prob))

# Create points in Rhino based on fuel model locations
for x, y, fuel_model, burn_prob in fuel_points:
    pt = rs.AddPoint(x, y, 0)  # Set elevation to 0 for 2D visualization
    color = (int(255 * burn_prob), 0, 255 - int(255 * burn_prob))  # Color based on burn probability
    rs.ObjectColor(pt, color)

print("Fuel Model Data Imported Successfully!")

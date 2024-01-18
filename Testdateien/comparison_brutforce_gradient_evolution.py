import numpy as np
from scipy.optimize import minimize, shgo
from shapely.geometry import Polygon, Point
from shapely.affinity import translate, rotate
import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
from optimal_pattern_calculation import opt_pattern_calc
from scipy.optimize import differential_evolution

# Funktion zur Berechnung der unbedeckten Fläche
def opt_points_calc_gradient_descent( params, polygon, distance):
    angle_degrees, pattern_move_x, pattern_move_y = params
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

    return -sum([point.x + point.y for point in points])

# Definition des Vierecks
polygon = Polygon([(-1, 2), (0, 4), (3, 5), (1, -2)])
distance = 0.5
opt_calc_iter = 10

# Gradientenabstieg
initial_params = np.array([0, -100, -100])  # Startposition und Rotation des Musters

# Funktion für minimieren aufrufen und dabei das Dreieck übergeben
result = minimize(opt_points_calc_gradient_descent, initial_params, args=(polygon, distance), method='L-BFGS-B')

# Extrahiere die optimierten Parameter
optimized_params = result.x
angle_degrees, pattern_move_x, pattern_move_y = optimized_params

# Evolution
result2 = differential_evolution(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 1), (-1, 1)], args=(polygon, distance))

# Extrahiere die optimierten Parameter
optimized_params2 = result2.x
angle_degrees2, pattern_move_x2, pattern_move_y2 = optimized_params2

result4 = shgo(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 1), (-1, 1)], args=(polygon, distance))

# Extrahiere die optimierten Parameter
optimized_params4 = result4.x
angle_degrees4, pattern_move_x4, pattern_move_y4 = optimized_params4

points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
points2 = opt_pattern_calc(polygon, distance, opt_calc_iter)
points3 = generate_triangular_points_rotated(polygon, distance, angle_degrees2, pattern_move_x2, pattern_move_y2)
points4 = generate_triangular_points_rotated(polygon, distance, angle_degrees4, pattern_move_x4, pattern_move_y4)

# Zeichne das Polygon und die Punkte
fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(10, 4))
x, y = polygon.exterior.xy
ax[0].fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
ax[0].plot(*polygon.exterior.xy, color='black')

for point in points:
    ax[0].plot(point.x, point.y, 'bo')

ax[0].set_aspect('equal', 'box')

ax[1].fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
ax[1].plot(*polygon.exterior.xy, color='black')

for point in points2:
    ax[1].plot(point.x, point.y, 'bo')

ax[1].set_aspect('equal', 'box')

ax[2].fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
ax[2].plot(*polygon.exterior.xy, color='black')

for point in points3:
    ax[2].plot(point.x, point.y, 'bo')

ax[2].set_aspect('equal', 'box')

ax[3].fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
ax[3].plot(*polygon.exterior.xy, color='black')

for point in points4:
    ax[3].plot(point.x, point.y, 'bo')

ax[3].set_aspect('equal', 'box')

print(len(points))
print(len(points2))
print(len(points3))
print(len(points4))

plt.xlabel('X-Koordinate')
plt.ylabel('Y-Koordinate')
plt.title('Polygon und dreiecksförmige Saatverteilung')
plt.show()


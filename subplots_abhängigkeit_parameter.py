import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from rotate_pattern import generate_triangular_points_rotated

polygon = Polygon([(-1, 2), (0, 4), (3, 5), (4.5, 4), (5, 3), (3, -1), (2, 1), (1, -2)])
distance = 0.17

def opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y):
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
    return len(points)

# Parameterbereiche für die Plots
angle_degrees_range = np.linspace(0, 60, 10)
pattern_move_x_range = np.linspace(0, 100, 10)
pattern_move_y_range = np.linspace(0, 100, 10)

# Plots erstellen
plt.figure(figsize=(10, 5))

# Plot 1: Variation des ersten Parameters (angle_degrees)
plt.subplot(3, 1, 1)
plt.title('Summe der Saatpunkte in Abhängigkeit des Winkels sowie der Verschiebung in X- und Y-Richtung')
for pattern_move_x in [0]:
    for pattern_move_y in [0]:
        output_values = [opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y) for angle_degrees in angle_degrees_range]
        plt.plot(angle_degrees_range, output_values)
plt.xlabel('Winkel [°]')
plt.ylabel('Saatpunkte')
plt.legend()

# Plot 2: Variation des zweiten Parameters (pattern_move_x)
plt.subplot(3, 1, 2)
for angle_degrees in [0]:
    for pattern_move_y in [0]:
        output_values = [opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y) for pattern_move_x in pattern_move_x_range]
        plt.plot(pattern_move_x_range, output_values)
plt.xlabel('Verschiebung in X-Richtung [%]')
plt.ylabel('Saatpunkte')
plt.legend()

# Plot 3: Variation des dritten Parameters (pattern_move_y)
plt.subplot(3, 1, 3)
for angle_degrees in [0]:
    for pattern_move_x in [0]:
        output_values = [opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y) for pattern_move_y in pattern_move_y_range]
        plt.plot(pattern_move_y_range, output_values)
plt.xlabel('Verschiebung in Y-Richtung [%]')
plt.ylabel('Saatpunkte')
plt.legend()

plt.tight_layout()
plt.show()


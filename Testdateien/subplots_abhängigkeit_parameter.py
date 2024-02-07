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
angle_degrees_range = np.linspace(0, 100, 300)
pattern_move_x_range = np.linspace(0, 100, 300)
pattern_move_y_range = np.linspace(0, 100, 300)

# Plots erstellen
plt.figure(figsize=(10, 5))

data = open("angle.dat", "w")
data.write("x y\n")
# Plot 1: Variation des ersten Parameters (angle_degrees)
plt.subplot(3, 1, 1)
plt.title('Summe der Saatpunkte in Abhängigkeit des Winkels sowie der Verschiebung in X- und Y-Richtung')
for pattern_move_x in [0]:
    for pattern_move_y in [0]:
        output_values = [opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y) for angle_degrees in angle_degrees_range]
        plt.plot(angle_degrees_range, output_values)
        # Schreiben der Daten in die Datei
        for angle_degrees, output_value in zip(angle_degrees_range, output_values):
            data.write(f"{angle_degrees} {output_value}\n")
plt.xlabel('Winkel [°]')
plt.ylabel('Saatpunkte')
plt.legend()

data = open("pattern_move_x.dat", "w")
data.write("x y\n")
# Plot 2: Variation des zweiten Parameters (pattern_move_x)
plt.subplot(3, 1, 2)
for angle_degrees in [0]:
    for pattern_move_y in [0]:
        output_values = [opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y) for pattern_move_x in pattern_move_x_range]
        plt.plot(pattern_move_x_range, output_values)
        # Schreiben der Daten in die Datei
        for pattern_move_x, output_value in zip(pattern_move_x_range, output_values):
            data.write(f"{pattern_move_x} {output_value}\n")
plt.xlabel('Verschiebung in X-Richtung [%]')
plt.ylabel('Saatpunkte')
plt.legend()

data = open("pattern_move_y.dat", "w")
data.write("x y\n")
# Plot 3: Variation des dritten Parameters (pattern_move_y)
plt.subplot(3, 1, 3)
for angle_degrees in [0]:
    for pattern_move_x in [0]:
        output_values = [opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y) for pattern_move_y in pattern_move_y_range]
        plt.plot(pattern_move_y_range, output_values)
        # Schreiben der Daten in die Datei
        for pattern_move_y, output_value in zip(pattern_move_y_range, output_values):
            data.write(f"{pattern_move_y} {output_value}\n")
plt.xlabel('Verschiebung in Y-Richtung [%]')
plt.ylabel('Saatpunkte')
plt.legend()

data = open("Punkte.dat", "w")
data.write("In diesem Dokument befinden sich berechneten geographischen Koordinaten für die Saatpunkte.")
data.write("\n")
data.write("\n")

data.close()

plt.tight_layout()
plt.show()


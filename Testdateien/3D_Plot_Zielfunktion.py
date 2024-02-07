import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Polygon
from rotate_pattern import generate_triangular_points_rotated


# Setzen Sie das Matplotlib-Backend auf 'TkAgg'
matplotlib.use('TkAgg')

# Ihre Zielfunktion (Beispiel: f(x, y, z) = x^2 + y^2 + z^2)
polygon = Polygon([(-1, 2), (0, 4), (3, 5), (4.5, 4), (5, 3), (3, -1), (2, 1), (1, -2)])
distance = 0.3

def opt_points_calc_gradient_descent(angle_degrees, pattern_move_x, pattern_move_y):
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

    # Hier sollte Ihre eigentliche Zielfunktion stehen
    # Im Beispiel wird nur die Anzahl der Punkte als Funktionswert zurückgegeben
    return len(points)


# Erstellen Sie Werte für die Parameter angle_degrees, pattern_move_x, pattern_move_y
angle_degrees = np.arange(0, 60, 3)
pattern_move_x = np.arange(0, 100, 5)
pattern_move_y = np.arange(0, 100, 5)

# Erstellen Sie Gitter aus den Parametern
angle_degrees_mesh, pattern_move_x_mesh, pattern_move_y_mesh = np.meshgrid(angle_degrees, pattern_move_x,
                                                                           pattern_move_y)

# Berechnen Sie die Funktionswerte für jedes Gitterpunkt
function_values = np.vectorize(opt_points_calc_gradient_descent)(angle_degrees_mesh, pattern_move_x_mesh,
                                                                 pattern_move_y_mesh)

# Plot in 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Erstellen Sie den 3D-Plot
scatter = ax.scatter(angle_degrees_mesh, pattern_move_x_mesh, pattern_move_y_mesh, c=function_values, cmap='gnuplot2')

# Legende und Farbskala
cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Funktionswerte')

# Achsenbeschriftungen
ax.set_xlabel('Angle Degrees')
ax.set_ylabel('Pattern Move X')
ax.set_zlabel('Pattern Move Y')
ax.set_title('3D-Plot der Zielfunktion')
plt.show(block=False)
plt.show()

from rotate_pattern import generate_triangular_points_rotated
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

polygon = Polygon([(-1, 2), (0, 4), (3, 5), (1, -2)])
distance = 2

# Parameterbereiche
angle_degrees_range = np.linspace(0, 720, 720)
pattern_move_x_range = np.linspace(0, 2, 200)
pattern_move_y_range = np.linspace(0, 2, 200)

points_count1 = np.zeros(720)
points_count2 = np.zeros(200)
points_count3 = np.zeros(200)

pattern_move_x = 0
pattern_move_y = 0

for i in range(len(angle_degrees_range)):
    angle_degrees = angle_degrees_range[i]
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
    points_count1[i] = len(points)

angle_degrees = 0
pattern_move_y = 0
for j in range(len(pattern_move_x_range)):
    pattern_move_x = pattern_move_x_range[j]
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
    points_count2[j] = len(points)

pattern_move_x = 0
angle_degrees = 0
for k in range(len(pattern_move_y_range)):
    pattern_move_y = pattern_move_y_range[k]
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
    points_count3[k] = len(points)



# Zeichne das Polygon und die Punkte
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))

ax.plot(angle_degrees_range, points_count1, color='red')
plt.xlabel('Winkel (Grad)')
plt.ylabel('Anzahl Punkte')
plt.title('Anzahl Punkte in Abhängigkeit des Winkels')
plt.show()
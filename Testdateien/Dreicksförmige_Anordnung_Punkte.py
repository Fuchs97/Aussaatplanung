import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import numpy as np

def fill_polygon_with_triangular_points(polygon, distance):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    
    # Erstelle ein Raster von Punkten mit dem gegebenen Abstand
    x_points = np.arange(min_x, max_x, distance)
    y_points = np.arange(min_y, max_y, distance)
    
    # Erzeuge die Punkte in einer Dreiecksform
    for i, y in enumerate(y_points):
        x_offset = i % 2 * 0.5 * distance  # Versatz für Dreiecksform
        for x in x_points:
            point = Point(x + x_offset, y)
            if polygon.contains(point):
                points.append(point)
    
    return points

# Erstelle ein Polygon
polygon_coords = [(0, 0), (0, 5), (5, 5), (5, 0)]
polygon = Polygon(polygon_coords)

# Definiere den Abstand zwischen den Punkten
distance = 0.9

# Befülle das Polygon mit Dreieckspunkten
points = fill_polygon_with_triangular_points(polygon, distance)

# Extrahiere die x- und y-Koordinaten der Punkte
x_points = [point.x for point in points]
y_points = [point.y for point in points]

# Plotte das Polygon und die Punkte
x_coords, y_coords = polygon.exterior.xy

plt.figure(figsize=(8, 6))
plt.plot(x_coords, y_coords, 'b-', label='Polygon')
plt.fill(x_coords, y_coords, facecolor='lightblue', alpha=0.5)
plt.scatter(x_points, y_points, c='r', marker='o', s=10, label='Dreieckspunkte')
plt.xlabel('X-Koordinaten')
plt.ylabel('Y-Koordinaten')
plt.title('Polygon mit Dreieckspunkten')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()

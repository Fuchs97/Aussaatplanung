import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union

# Erstelle das Polygon mit schrägen Linien (Beispiel)
polygon_coords = [(1, 1), (2, 4), (5, 5), (6, 3), (4, 1)]
polygon = Polygon(polygon_coords)

# Definiere den gewünschten Mindestabstand zwischen den Punkten
min_distance = 0.5  # Beispielabstand von 0.5 Einheiten

# Extrahiere die Linien des Polygons
lines = [LineString([polygon.exterior.coords[i], polygon.exterior.coords[i + 1]]) for i in range(len(polygon.exterior.coords) - 1)]

# Vereinige die Linien zu einem einzigen LineString
boundary = unary_union(lines)

# Erstelle eine leere Liste für die Punkte
points = []

# Bestimme die Breite und Höhe des umgebenden Rechtecks für das Polygon
x_min, y_min, x_max, y_max = polygon.bounds
width = x_max - x_min
height = y_max - y_min

# Berechne die Anzahl der Punkte in jeder Richtung
num_x_points = int(width / min_distance)
num_y_points = int(height / min_distance)

# Verteile die Punkte entlang des Polygon-Rands
for i in range(num_x_points + 1):
    x = x_min + i * (width / num_x_points)
    for j in range(num_y_points + 1):
        y = y_min + j * (height / num_y_points)
        point = Point(x, y)
        if polygon.contains(point):
            valid = True
            for existing_point in points:
                if point.distance(existing_point) < min_distance:
                    valid = False
                    break
            if valid:
                points.append(point)

# Visualisiere das Polygon, fülle es mit einer Farbe und zeige die generierten Punkte
fig, ax = plt.subplots()
x_poly, y_poly = polygon.exterior.xy
ax.fill(x_poly, y_poly, facecolor='lightblue', edgecolor='blue')
x_points = [point.x for point in points]
y_points = [point.y for point in points]
ax.scatter(x_points, y_points, c='r', marker='o', s=5)
ax.set_xlabel('X-Koordinaten')
ax.set_ylabel('Y-Koordinaten')
ax.set_title('Polygon mit Punkten (Mindestabstand)')
plt.grid()
plt.show()






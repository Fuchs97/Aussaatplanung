import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from triangular_pattern import generate_triangular_points

def rotate_point(point, angle_degrees, origin=(0, 0)):
    angle_radians = np.radians(angle_degrees)
    ox, oy = origin
    qx = ox + np.cos(angle_radians) * (point.x - ox) - np.sin(angle_radians) * (point.y - oy)
    qy = oy + np.sin(angle_radians) * (point.x - ox) + np.cos(angle_radians) * (point.y - oy)
    return Point(qx, qy)

def rotate_polygon(polygon, angle_degrees, origin=(0, 0)):
    rotated_exterior = [rotate_point(Point(coord), angle_degrees, origin) for coord in polygon.exterior.coords]
    rotated_interiors = [[rotate_point(Point(coord), angle_degrees, origin) for coord in interior.coords] for interior in polygon.interiors]
    return Polygon(rotated_exterior, rotated_interiors)

def generate_triangular_points(polygon, distance):
    min_x, min_y, max_x, max_y = polygon.bounds
    triangle_height = distance * (np.sqrt(3) / 2)

    points = []
    y = max_y
    even_row = True
    while y >= min_y:
        if even_row:
            x = min_x
        else:
            x = min_x + (distance/2)
        while x <= max_x:
            point = Point(x, y)
            if polygon.contains(point) or polygon.touches(point) or polygon.distance(point) < 1e-10:
                points.append(point)
            x += distance
        even_row = not even_row
        y -= triangle_height

    return points

def generate_triangular_points_rotated(polygon, distance, angle_degrees):
    rotated_polygon = rotate_polygon(polygon, angle_degrees)
    x, y = rotated_polygon.exterior.xy
    plt.plot(x, y, label='Rotated Polygon', color='blue')
    rotated_points = generate_triangular_points(rotated_polygon, distance)
    original_points = [rotate_point(point, -angle_degrees) for point in rotated_points]
    return original_points

def plot_polygon_and_points(polygon, points):
    x, y = polygon.exterior.xy
    plt.plot(x, y, label='Original Polygon', color='blue')

    x, y = zip(*[(point.x, point.y) for point in points])
    plt.scatter(x, y, label='Generated Points', color='red')

    plt.axis('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon and Generated Points')
    plt.legend()
    plt.show()

# Beispiel:
polygon = Polygon([(0, 0), (1, 0), (1, 1), (0.5, 1.5), (0, 1)])
distance = 0.1
angle_degrees = 0                 #Ab 60 Grad wiederholt sich das Muster, d.h. bis 60 Grad ergibt eine Drehung Sinn.

original_points = generate_triangular_points_rotated(polygon, distance, angle_degrees)

plot_polygon_and_points(polygon, original_points)

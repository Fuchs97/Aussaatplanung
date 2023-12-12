"""
Datum: 27.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
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

def generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y):
    rotated_polygon = rotate_polygon(polygon, angle_degrees)
    rotated_points = generate_triangular_points(rotated_polygon, distance, pattern_move_x, pattern_move_y)
    original_points = [rotate_point(point, -angle_degrees) for point in rotated_points]
    return original_points
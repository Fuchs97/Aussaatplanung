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


def rotate_point(point, angle_degrees, centroid):
    angle_radians = np.radians(angle_degrees)
    ox, oy = centroid.coords[0]
    qx = (ox + np.cos(angle_radians) * (point.x - ox) -
          np.sin(angle_radians) * (point.y - oy))
    qy = (oy + np.sin(angle_radians) * (point.x - ox) +
          np.cos(angle_radians) * (point.y - oy))
    return Point(qx, qy)

def rotate_polygon(polygon, angle_degrees, centroid):
    rotated_exterior = [rotate_point(Point(coord),
                                     angle_degrees,
                                     centroid)
                        for coord in polygon.exterior.coords]

    rotated_interiors = [[rotate_point(Point(coord),
                                       angle_degrees,
                                       centroid)
                          for coord in interior.coords]
                         for interior in polygon.interiors]

    return Polygon(rotated_exterior, rotated_interiors)


def generate_triangular_points_rotated(polygon, distance,
                                       angle_degrees,
                                       pattern_move_x,
                                       pattern_move_y):
    centroid = Point(polygon.centroid.x, polygon.centroid.y)
    rotated_polygon = rotate_polygon(polygon, angle_degrees, centroid)
    rotated_points = generate_triangular_points(rotated_polygon,
                                                distance,
                                                pattern_move_x,
                                                pattern_move_y)
    original_points = [rotate_point(point, -angle_degrees, centroid)
                       for point in rotated_points]
    return original_points

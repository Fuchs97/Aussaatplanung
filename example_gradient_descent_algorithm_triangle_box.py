import numpy as np
from scipy.optimize import minimize
import geopandas as gpd
from shapely.geometry import Polygon, Point
from shapely.affinity import translate, rotate
import matplotlib.pyplot as plt

# Definition des Vierecks
rectangle = Polygon([(0, 0), (0, 4), (3, 4), (3, 0)])

# Funktion zur Berechnung der unbedeckten Fläche
def calculate_uncovered_area(params, triangle):
    tx, ty, angle = params

    # Rotieren und Verschieben des Dreiecks
    rotated_triangle = rotate(translate(triangle, tx, ty), angle, origin=Point(0, 0))

    intersection = rectangle.intersection(rotated_triangle)
    return (rectangle.area - intersection.area)

# Gradientenabstieg
initial_params = np.array([0, 0, 0])  # Startposition und Rotation des Dreiecks

# Dreieck mit Seitenlängen 2 und 3
initial_triangle = Polygon([(-1, -2), (3, 1), (2, 7)])

# Funktion für minimieren aufrufen und dabei das Dreieck übergeben
result = minimize(calculate_uncovered_area, initial_params, args=(initial_triangle,), method='L-BFGS-B')

# Extrahiere die optimierten Parameter
optimized_params = result.x
tx_opt, ty_opt, angle_opt = optimized_params

# Erstelle das optimierte Dreieck
rotated_triangle = rotate(translate(initial_triangle, tx_opt, ty_opt), angle_opt, origin=Point(0, 0))

# Visualisierung
fig, ax = plt.subplots()
gdf = gpd.GeoDataFrame(geometry=[rectangle, rotated_triangle], crs="EPSG:4326")
gdf.plot(ax=ax, edgecolor='black', facecolor='none')

plt.axis('equal')
plt.show()



import numpy as np
from scipy.optimize import minimize, shgo, basinhopping, dual_annealing, brute
from shapely.geometry import Polygon, Point
from shapely.affinity import translate, rotate
import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
from optimal_pattern_calculation import opt_pattern_calc
from scipy.optimize import differential_evolution
import time
from coords_kml import extract_coordinates_kml
from coords_transformation import robinson_to_geo_points, robinson_to_geo_polygon, geo_to_robinson, get_utm_zone

# Funktion zur Berechnung der unbedeckten Fläche
def opt_points_calc_gradient_descent( params, polygon, distance):
    angle_degrees, pattern_move_x, pattern_move_y = params
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

    return -sum([point.x + point.y for point in points])

# Definition des Vierecks
#polygon = Polygon([(-1, 2), (0, 4), (3, 5), (1, -2)])
# KML-Datei aufrufen, die die geographischen Koordinaten besitzt
kml_file_path = r"C:\Users\49152\Desktop\Maschkopf\Studienarbeit\Python Programm\test.kml"
# Polygonkoordinaten aus der KML-Datei extrahieren
#coords = [(1, 1), (4, 1), (6, 4), (3, 7), (1, 6), (0, 3)]
coords_geo = extract_coordinates_kml(kml_file_path)
# Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
utm_zone = get_utm_zone(coords_geo)
# Koordinaten in das Robinson KGS projizieren, um in Metern weiterzurechnen
coords = geo_to_robinson(coords_geo, utm_zone)
# Polygon-Objekt erstellen
polygon = Polygon(coords)
distance = 20
opt_calc_iter = 6

# Gradientenabstieg
initial_params = np.array([0, 0, 0])  # Startposition und Rotation des Musters

start_time = time.time()


#result = basinhopping(opt_points_calc_gradient_descent, x0=initial_params, niter=10, minimizer_kwargs={'args': (polygon, distance)})
result = differential_evolution(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 100), (0, 100)], strategy='best1bin', maxiter=150, args=(polygon, distance))
#result = dual_annealing(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 100), (0, 100)], maxiter=50,  args=(polygon, distance))
#result = shgo(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 100), (0, 100)], iters=5, args=(polygon, distance))
#result = brute(opt_points_calc_gradient_descent, ranges=[slice(0, 60, 4), slice(0, 100, 8), slice(0, 100, 8)], Ns=20, args=(polygon, distance))

end_time = time.time()
elapsed_time = end_time - start_time

# Extrahiere die optimierten Parameter
optimized_params = result.x
#optimized_params = result
angle_degrees, pattern_move_x, pattern_move_y = optimized_params

points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

# Ursprüngliche Optimierungsfkt.
#start_time = time.time()
#points = opt_pattern_calc(polygon, distance, opt_calc_iter)
#end_time = time.time()
#elapsed_time = end_time - start_time

# Zeichne das Polygon und die Punkte
fig, ax = plt.subplots(nrows=1, ncols=1)
x, y = polygon.exterior.xy
ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
ax.plot(*polygon.exterior.xy, color='black')

for point in points:
    ax.plot(point.x, point.y, 'bo')

ax.set_aspect('equal', 'box')


#print(f"{len(points)} Punkte.")
#print(f"{elapsed_time:.4f} Sekunden Rechnenzeit")

plt.xlabel('X-Koordinate')
plt.ylabel('Y-Koordinate')
plt.title(f"Brute Force: {len(points)} Punkte, {elapsed_time:.4f} Sek.")
plt.show()

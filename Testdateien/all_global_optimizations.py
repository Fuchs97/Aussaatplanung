import numpy as np
from scipy.optimize import minimize, shgo, basinhopping, dual_annealing, brute, direct
from shapely.geometry import Polygon, Point
from shapely.affinity import translate, rotate
import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
from optimal_pattern_calculation import opt_pattern_calc
from scipy.optimize import differential_evolution
import time
from pyswarm import pso


## Funktion zur Berechnung der unbedeckten Fläche
#def opt_points_calc_gradient_descent(params, polygon, distance):
#    angle_degrees, pattern_move_x, pattern_move_y = params
#    # Berechnung der Saatpunkte
#    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
#
#    return -sum([point.x + point.y for point in points])

def opt_points_calc_gradient_descent(params):
    angle_degrees, pattern_move_x, pattern_move_y = params
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

    return -sum([point.x + point.y for point in points])

# Definition des Vierecks
polygon = Polygon([(-1, 2), (0, 4), (3, 5), (4.5, 4), (5, 3), (3, -1), (2, 1), (1, -2)])
distance = 1 #0.17
opt_calc_iter = 1
opt_calc_iter_angle = 120
# Gradientenabstieg
initial_params = np.array([30, 50, 50])  # Startposition und Rotation des Musters

start_time = time.time()

#result = basinhopping(opt_points_calc_gradient_descent, x0=initial_params, niter=2)
#strategy='best1bin'
#result = differential_evolution(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 100), (0, 100)], maxiter=140)
#result = dual_annealing(opt_points_calc_gradient_descent, bounds=[(0, 60), (0, 100), (0, 100)], maxiter=50,  args=(polygon, distance))
#result = brute(opt_points_calc_gradient_descent, ranges=[slice(0, 60, 60), slice(0, 100, 100), slice(0, 100, 100)])
#result = cma.fmin(opt_points_calc_gradient_descent, initial_params, sigma0=25, options={'bounds': [[0, 0, 0], [60, 100, 100]],'maxiter':40})
# boyesian opt.:
# result = gp_minimize(opt_points_calc_gradient_descent,                  # the function to minimize
#                 [(0, 60), (0, 100), (0, 100)],      # the bounds on each dimension of x
#                 n_calls=80,         # the number of evaluations of f
#                 n_random_starts=35,
#                 acq_func="EI")   # the random seed
 #pyswarm:
lb = [0,0,0]
ub = [60,100,100]
result = pso(opt_points_calc_gradient_descent, lb, ub, swarmsize= 50, maxiter= 5)

end_time = time.time()
elapsed_time = end_time - start_time

#plot_convergence(result)      #für boyesian
# Extrahiere die optimierten Parameter
#otimized_params = result.x
optimized_params = result[0]
#optimized_params = result #Für brute force

angle_degrees, pattern_move_x, pattern_move_y = optimized_params

points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

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

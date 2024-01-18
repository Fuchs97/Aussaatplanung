import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
from PSO_modified import pso

def opt_func_generate_points(params):
    angle_degrees, pattern_move_x, pattern_move_y = params
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
    return -sum([point.x + point.y for point in points])

def pyswarm_global_optimization(polygon, distance, maxiter, swarmsize):
    # pyswarm:
    lb = [0,0,0]
    ub = [60,100,100]
    result = pso(opt_func_generate_points, lb, ub, swarmsize= swarmsize, maxiter= maxiter)
    # Extrahiere die optimierten Parameter
    optimized_params = result[0]
    angle_degrees, pattern_move_x, pattern_move_y = optimized_params
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)
    return points



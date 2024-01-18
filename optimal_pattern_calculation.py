"""
Datum: 28.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
from rotate_pattern import generate_triangular_points_rotated
import numpy as np

def opt_pattern_calc(polygon, distance, opt_calc_iter, opt_calc_iter_angle):
    # Erstelle eine leere Liste als Platzhalter für die optimalen Koordinaten der Punkte
    opt_points = []

    # Schrittweite der Verschiebungsinkremente
    angle_steps = 60 / opt_calc_iter_angle
    move_y_steps = move_x_steps = 100 / opt_calc_iter    # move_y und  move_x sind in % angegeben

    for steps1 in range(opt_calc_iter_angle):
        angle_degrees = angle_steps*steps1    # Winkel des jeweiligen Inkrementes wird berechnet
        print(angle_degrees)
        for steps2 in range(opt_calc_iter):
            pattern_move_x = move_x_steps*steps2     # Verschiebung des jeweiligen Inkrementes wird berechnet
            for steps3 in range(opt_calc_iter):
                pattern_move_y = move_y_steps*steps3     # Verschiebung des jeweiligen Inkrementes wird berechnet

                # Berechnung der Saatpunkte
                points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

                # Muster mit der höchsten Anzahl an Saatpunkten wird gespeichert
                if len(points) > len(opt_points):
                    opt_points = points

    return opt_points

import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

def generate_triangular_points(polygon, distance, pattern_move_x, pattern_move_y):
    min_x, min_y, max_x, max_y = polygon.bounds         #Funktion bounds angewandt
    triangle_height = distance * (np.sqrt(3) / 2)           #Berechnung Dreickshöhe mithilfe des Sinus

    # Erweiterung der Berechnung, da durch Verschiebungen Lücken entstehen können
    # Verschiebungen werden durch pattern_move_x und pattern_move_y berücksichtigt
    min_x -= (pattern_move_x/100)*distance
    max_x += distance
    min_y -= 2*triangle_height
    max_y += (pattern_move_y/100)*(2*triangle_height)

    points = []
    y = max_y                                           #Startwert bei maximalem Y-Wert
    even_row = True
    while y >= min_y:
        if even_row:                                    #Jede zweite Reihe wird um die halbe Seitenlänge verschoben
            x = min_x
        else:
            x = min_x + (distance/2)
        while x <= max_x:
            point = Point(x, y)
            if polygon.contains(point) or polygon.touches(point) or polygon.distance(point) < 1e-10:   #Punkt wird gespeichert, falls sicher dieser innerhalb des Polygons befindet
                points.append(point)
            x += distance
        even_row = not even_row
        y -= triangle_height

    return points

if __name__ == "__main__":
    #---------------- Parameter ------------------------------
    # Polygonkoordinaten
    polygon = Polygon([(1, 1), (4, 1), (6, 4), (1, 6)])
    # Pflanzenabstand
    distance = 0.5
    # Verschiebung des Musters in X-Richtung in % (max. so groß wie distance_plant)
    pattern_move_x = 0
    # Verschiebung des Musters in Y-Richtung in % (max. so groß wie das Doppelte der Dreieckshöhe)
    pattern_move_y = 0

    #----------------------------------------------------------
    # Generiere die dreiecksförmigen Punkte innerhalb des Polygons
    points = generate_triangular_points(polygon, distance, pattern_move_x, pattern_move_y)

    # Zeichne das Polygon und die Punkte
    fig, ax = plt.subplots()
    x, y = polygon.exterior.xy
    ax.fill(x, y, alpha=0.5, edgecolor='black', facecolor='gray')
    ax.plot(*polygon.exterior.xy, color='black')

    for point in points:
        ax.plot(point.x, point.y, 'ro')

    ax.set_aspect('equal', 'box')
    plt.xlabel('X-Koordinate')
    plt.ylabel('Y-Koordinate')
    plt.title('Polygon und dreiecksförmige Punkteverteilung')
    plt.show()
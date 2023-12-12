"""
Datum: 27.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
import matplotlib.pyplot as plt
from rotate_pattern import rotate_polygon

def plot_field_and_points(polygon, reduced_polygon, points, angle_degrees):
    # Zeichne das Polygon und die Punkte
    fig, ax = plt.subplots()
    x, y = polygon.exterior.xy
    x_red, y_red = reduced_polygon.exterior.xy
    ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
    plt.plot(x_red, y_red, 'g--', label='Reduziertes Polygon')
    ax.plot(*polygon.exterior.xy, color='black')

    #Gedrehtes Polygon ebenfalls anzeigen lassen zum Prüfen
        #rotated_polygon = rotate_polygon(polygon, angle_degrees)
        #rot_x, rot_y = rotated_polygon.exterior.xy
        #plt.plot(rot_x, rot_y, 'g--', label='Rotated Polygon')

    for point in points:
        ax.plot(point.x, point.y, 'bo')

    ax.set_aspect('equal', 'box')
    plt.xlabel('X-Koordinate')
    plt.ylabel('Y-Koordinate')
    plt.title('Polygon und dreiecksförmige Saatverteilung')
    plt.show()




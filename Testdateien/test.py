import matplotlib.pyplot as plt
from rotate_pattern import rotate_polygon
from coords_transformation import utm_to_geo_points, utm_to_geo_polygon, geo_to_utm, get_utm_zone
from shapely.geometry import Polygon
from rotate_pattern import generate_triangular_points_rotated
import matplotlib.ticker as ticker
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import StrMethodFormatter
from shapely.geometry import Polygon
from matplotlib.ticker import FuncFormatter

def plot(coords, coords_headland):
    def format_ticks(x, pos):
        return f'{x:.2e}'[:4]

    polygon = Polygon(coords)
    # Zeichne das Polygon und die Punkte
    points = generate_triangular_points_rotated(polygon,
                                                distance=0.5,
                                                angle_degrees=0,
                                                pattern_move_x=0,
                                                pattern_move_y=0)
    fig, ax = plt.subplots()
    x, y = polygon.exterior.xy
    ax.fill(x, y, alpha=1, edgecolor='brown', facecolor='lightgreen')
    for point in points:
        # Größe der Saatpunkte in Abhängigkeit der Gesamtpunktzahl
        ax.plot(point.x, point.y, 'bo', markersize=3)

    # Aktualisieren des Plots
    ax.plot(*polygon.exterior.xy, color='black')
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('Östliche Koordinate [m]')
    ax.set_ylabel('Nördliche Koordinate [m]')

    ax.set_title('Koordinatenpunkte der Aussaat mit gleichseitigem \n Dreiecksmuster im UTM-System', y=1.03)

    # Vorgewende berücksichtigen!
    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
    polygon_headland1 = Polygon(coords_headland)
    x, y = polygon_headland1.exterior.xy
    ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='green', hatch='//', linewidth=2)
    ax.plot(*polygon_headland1.exterior.xy, color='black')

    # Achsenbeschriftungen formatieren
    plt.gca().xaxis.get_major_formatter().set_scientific(True)
    plt.gca().yaxis.get_major_formatter().set_scientific(True)
    plt.gca().xaxis.offsetText.set_visible(False)
    plt.gca().yaxis.offsetText.set_visible(False)

    # Maximale und minimale Werte der Achsen abrufen
    x_min, x_max = plt.gca().get_xlim()
    y_min, y_max = plt.gca().get_ylim()

    plt.text(0.0, 1.07, f'$\\times 10^{{{int(np.log10(x_max))}}}$', transform=plt.gca().transAxes, va='top')
    plt.text(1.02, 0.0, f'$\\times 10^{{{int(np.log10(y_max))}}}$', transform=plt.gca().transAxes, va='bottom')

    # Achsenbeschriftungen für ganze Zahlen formatieren und auf maximal drei Ziffern begrenzen
    plt.gca().xaxis.set_major_formatter(FuncFormatter(format_ticks))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_ticks))

    # Anzahl der Ticks auf der x-Achse festlegen
    num_ticks = 5
    x_ticks = np.linspace(x_min, x_max, num_ticks)
    plt.gca().set_xticks(x_ticks)
    y_ticks = np.linspace(y_min, y_max, num_ticks)
    plt.gca().set_yticks(y_ticks)

    plt.show()

if __name__ == "__main__":
    # Ursprüngliches Polygon mit 4 Eckpunkten und schrägen Linien
    coords = [(67531, 67531), (67532, 67534), (67534, 67533), (67534, 67531)]
    coords_headland = [(67531, 67531), (67531, 67531), (67531, 67532), (67532, 67532)]
    plot(coords, coords_headland)


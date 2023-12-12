import matplotlib.pyplot as plt
from shapely.geometry import Polygon
def reduced_polygon(coords, distance_field_edge):
    original_coords = Polygon(coords)
    # Verkleinere das Polygon durch Anwenden der buffer-function
    reduced_polygon = original_coords.buffer(-distance_field_edge, join_style=2)
    return reduced_polygon

if __name__ == "__main__":
    # Ursprüngliches Polygon mit 4 Eckpunkten und schrägen Linien
    original_coords = [(1, 1), (2, 4), (4, 3), (4, 1)]

    original_polygon = Polygon(original_coords)

    # Abstand um den die Wandstärke erhöht werden soll
    erweiterung_abstand = 0.5  # Beispielabstand von 0.5 Einheiten

    # Vergrößere das Polygon durch Anwenden der Pufferoperation (Buffer)
    erweitertes_polygon = reduced_polygon(original_coords, erweiterung_abstand)

    # Plotten der beiden Polygone in einem Plot
    x_original, y_original = original_polygon.exterior.xy
    x_erweitert, y_erweitert = erweitertes_polygon.exterior.xy

    plt.figure()
    plt.plot(x_original, y_original, 'b-', label='Ursprüngliches Polygon')
    plt.fill(x_original, y_original, facecolor='lightblue')
    plt.plot(x_erweitert, y_erweitert, 'g-', label='Erweitertes Polygon')
    plt.fill(x_erweitert, y_erweitert, facecolor='lightgreen')
    plt.xlabel('X-Koordinaten')
    plt.ylabel('Y-Koordinaten')
    plt.axis('equal')
    plt.title('Vergleich: Ursprüngliches vs. Erweitertes Polygon')
    plt.legend()
    plt.grid()
    plt.show()
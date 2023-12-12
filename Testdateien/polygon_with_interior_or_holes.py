"""
Datum: 27.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Äußere Kontur
outer_ring_coords = [(0, 0), (0, 4), (4, 4), (4, 0)]

# Innere Ringe (Löcher)
hole1_coords = [(1, 1), (1, 2), (2, 2), (2, 0), (1.5,0)]
hole2_coords = [(2.5, 2.5), (2.5, 3), (3, 3), (3, 2.5)]

# Erstelle Polygon mit Löchern
polygon_with_holes = Polygon(outer_ring_coords, [hole1_coords, hole2_coords])

# Plotte das Polygon mit Löchern
x, y = polygon_with_holes.exterior.xy
plt.fill(x, y, alpha=0.5, fc='blue', label='Polygon mit Löchern (äußere Kontur)')

for hole in polygon_with_holes.interiors:
    x, y = hole.xy
    plt.fill(x, y, alpha=0.5, fc='white', hatch='/', label='Loch')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Polygon mit Löchern')
plt.legend()
plt.show()

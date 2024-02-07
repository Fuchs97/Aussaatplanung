"""
Datum: 16.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from triangular_pattern import generate_triangular_points
from polygon_with_field_edge import reduced_polygon
from rotate_pattern import generate_triangular_points_rotated
from plot_field_and_points import plot_field_and_points
from save_data import save_data_seed_coords
from optimal_pattern_calculation import opt_pattern_calc
from coords_kml import extract_coordinates_kml
from coords_transformation import utm_to_geo_points, utm_to_geo_polygon, geo_to_utm, get_utm_zone


#---------------- Parameter ------------------------------
# KML-Datei aufrufen, die die geographischen Koordinaten besitzt
kml_file_path = r"C:\Users\49152\Desktop\Maschkopf\Studienarbeit\Python Programm\test.kml"
# Polygonkoordinaten aus der KML-Datei extrahieren
#coords = [(1, 1), (4, 1), (6, 4), (3, 7), (1, 6), (0, 3)]
coords_geo = extract_coordinates_kml(kml_file_path)
# Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
utm_zone = get_utm_zone(coords_geo)
# Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
coords = geo_to_utm(coords_geo, utm_zone)
# Polygon-Objekt erstellen
polygon = Polygon(coords)
# Feldrandabstand in m
distance_field_edge = 10
# Pflanzenabstand in m
distance_plant = 25
# Drehung des Musters (bis max. 60 Grad)
angle_degrees = 0
# Verschiebung des Musters in X-Richtung in % (max. so groß wie distance_plant)
pattern_move_x = 0
# Verschiebung des Musters in Y-Richtung in % (max. so groß wie das Doppelte der Dreieckshöhe)
pattern_move_y = 0
# Optimale Berechnung der Position des Musters
# (alle rotatorischen und translatorischen Freiheitsgrade werden genutzt, um die Anzahl an Saatpunkten zu maximieren)
opt_calc = False
# Anzahl Iterationen für die opt. Berechnung (mind. 1 und Wert muss ^3 genommen werden)
opt_calc_iter = 1
#----------------------------------------------------------
# Verkleinertes Polygon mit Berücksichtigung des Feldrandes
reduced_polygon = reduced_polygon(coords, distance_field_edge)

if opt_calc:
    # Berechnung des opt. Musters unter Brücksichtigung des Genauigkeitsgrades
    points = opt_pattern_calc(reduced_polygon, distance_plant, opt_calc_iter)
else:
    # Generiere die dreiecksförmigen Punkte innerhalb des Polygons
    points = generate_triangular_points_rotated(reduced_polygon,
                                                distance_plant,
                                                angle_degrees,
                                                pattern_move_x,
                                                pattern_move_y)

# Saatpunkte in geographische Koordinaten transformieren
points_geo = utm_to_geo_points(points, utm_zone)

# Speichere Koordinaten der Saat in einer Textdatei
save_data_seed_coords(points_geo)

# Feldpolygon und Polygon mit Feldabstand in geographische Koordinaten transformieren
#reduced_polygon_geo = utm_to_geo_polygon(str(reduced_polygon), utm_zone)
#polygon_geo = utm_to_geo_polygon(str(polygon), utm_zone)

# Plotte das Feld und die Saatpunkte
plot_field_and_points(polygon, reduced_polygon, points, angle_degrees)
"""
Datum: 27.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
import simplekml

def save_data_seed_coords (file_name, points, fieldnumber, headland_option, points_headland1, points_headland2, points_headland_circ, seed):
    try:
        if fieldnumber == 1:
            with open(file_name, "w") as data:
                data.write("Dieses Dokument enthält die berechneten geographischen Koordinaten für die Saatpunkte.\n"
                           "Die Breitengrade sind auf der linken Seite und die Längengrade auf der rechten Seite aufgeführt.\n"
                           f"Die geographischen Koordinaten mit dem Saatgut '{seed}' des {fieldnumber}. Feldes:\n\n")
                for point in points:
                    # lat lon
                    data.write(f"{point.y} {point.x}\n")
            if headland_option == "Individueller Bereich":
                if points_headland1 != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des 1. Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland1:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
                if points_headland2 != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des 2. Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland2:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
            else:
                if points_headland_circ != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des umläufigen Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland_circ:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
        elif fieldnumber == 2:
            with open(file_name, "a") as data:
                data.write(f"\nDie geographischen Koordinaten mit dem Saatgut '{seed}' des {fieldnumber}. Feldes:\n\n")
                for point in points:
                    # lat lon
                    data.write(f"{point.y} {point.x}\n")
            if headland_option == "Individueller Bereich":
                if points_headland1 != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des 1. Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland1:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
                if points_headland2 != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des 2. Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland2:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
            else:
                if points_headland_circ != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des umläufigen Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland_circ:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
        elif fieldnumber == 3:
            with open(file_name, "a") as data:
                data.write(f"\nDie geographischen Koordinaten mit dem Saatgut '{seed}' des {fieldnumber}. Feldes:\n\n")
                for point in points:
                    # lat lon
                    data.write(f"{point.y} {point.x}\n")
            if headland_option == "Individueller Bereich":
                if points_headland1 != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des 1. Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland1:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
                if points_headland2 != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des 2. Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland2:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
            else:
                if points_headland_circ != "":
                    with open(file_name, "a") as data:
                        data.write(f"\nDie geographischen Koordinaten des umläufigen Vorgewende vom {fieldnumber}. Feld:\n\n")
                        for point in points_headland_circ:
                            # lat lon
                            data.write(f"{point.y} {point.x}\n")
    except Exception as e:
        print(f'Fehler beim Schreiben der Daten in die Datei: {e}')

def save_data_seed_coords_kml (file_name, points):
    try:
        # KML-Objekt erstellen
        kml = simplekml.Kml()
        # Marker für jede Koordinate hinzufügen
        for point in points:
            # lon lat
            kml.newpoint(name='', coords=[(point.x, point.y)])
        # KML-Datei speichern
        kml.save(file_name)
    except Exception as e:
        print(f'Fehler beim Schreiben der Daten in die Datei: {e}')
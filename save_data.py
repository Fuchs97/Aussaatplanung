"""
Datum: 27.11.2023
Autor: Justin Fuchs
Matrikelnummer: 4912635
TU-Braunschweig
"""
def save_data_seed_coords (points):
    data = open("Koordinaten_Saatpunkte.txt", "w")
    data.write("In diesem Dokument befinden sich berechneten geographischen Koordinaten für die Saatpunkte.")
    data.write("\n")
    data.write("\n")

    for point in points:
        data.write(str(point.x))
        data.write(" ")
        data.write(str(point.y))
        data.write("\n")

    data.close()
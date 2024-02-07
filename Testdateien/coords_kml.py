import xml.etree.ElementTree as ET

def extract_coordinates_kml(kml_file_path):
    tree = ET.parse(kml_file_path)
    root = tree.getroot()

    coordinates = []

    # Finde alle Koordinaten in den KML-Elementen
    for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        # Beachte, dass das Namensraum-Präfix möglicherweise abweichen kann.
        # In diesem Beispiel wurde der häufig verwendete Standardpräfix "kml" verwendet.
        coordinates_element = placemark.find(".//{http://www.opengis.net/kml/2.2}coordinates")

        if coordinates_element is not None:
            # Extrahiere Koordinaten und füge sie der Liste hinzu
            coordinates.extend(coordinates_element.text.strip().split())

    # 3. Koordinate "0" entfernen, da nicht relevant
    coordinates = [row[:-2] for row in coordinates]

    # Umwandlung der Zeichenketten in numerische Werte (floats)
    coordinates_num = [tuple(map(float, coord.split(','))) for coord in coordinates]

    return coordinates_num

if __name__ == "__main__":
    # Beispielaufruf
    kml_file_path = r"C:\Users\Justi\Desktop\Studienarbeit\Python Programm\test.kml"
    coords = extract_coordinates_kml(kml_file_path)
    print(coords)
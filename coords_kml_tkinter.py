import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog

def select_kml_file():
    root = Tk()
    root.withdraw()  # Verstecke das Hauptfenster

    # Öffne einen Dateiauswahldialog für KML-Dateien
    file_path = filedialog.askopenfilename(filetypes=[("KML files", "*.kml")])

    return file_path

def extract_coordinates(kml_file_path):
    tree = ET.parse(kml_file_path)
    root = tree.getroot()

    coordinates = []

    # Finde alle Koordinaten in den KML-Elementen
    for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        coordinates_element = placemark.find(".//{http://www.opengis.net/kml/2.2}coordinates")

        if coordinates_element is not None:
            coordinates.extend(coordinates_element.text.strip().split())

    # 3. Koordinate "0" entfernen, da nicht relevant
    coordinates = [row[:-2] for row in coordinates]

    # Umwandlung der Zeichenketten in numerische Werte (floats)
    coordinates_num = [tuple(map(float, coord.split(','))) for coord in coordinates]

    return coordinates_num

if __name__ == "__main__":
# Benutzer wählt die KML-Datei aus
    selected_file = select_kml_file()

    # Überprüfe, ob eine Datei ausgewählt wurde
    if selected_file:
        # Extrahiere Koordinaten und gebe sie aus
        koordinaten = extract_coordinates(selected_file)
        print(koordinaten)
    else:
        print("Keine Datei ausgewählt.")

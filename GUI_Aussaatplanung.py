from tkinter import messagebox
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
from shapely.geometry import Polygon
from triangular_pattern import generate_triangular_points
from polygon_with_field_edge import reduced_polygon
from coords_kml_tkinter import select_kml_file, extract_coordinates
from coords_transformation import get_utm_zone, geo_to_utm

class PlotApp(customtkinter.CTk):
    def __init__(self):
        # customtkinter.CTk-Methoden erben
        super().__init__()

        # Titel und Fenstergröße
        self.title("Aussaatplanung")
        self.geometry("700x700")

        # Infotext Koordinaten
        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Eingabefelder
        self.coords_label = customtkinter.CTkLabel(self, text="Koordinaten:")
        self.coords_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.coords_entry = customtkinter.CTkTextbox(self, width=100)
        self.coords_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.coords_entry.bind("<FocusIn>", self.add_info_text_coords)
        self.coords_entry.bind("<FocusOut>", self.remove_info_text)

        self.field_edge_label = customtkinter.CTkLabel(self, text="Feldrandbreite:")
        self.field_edge_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.field_edge_entry = customtkinter.CTkEntry(self)
        self.field_edge_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.param2_label = customtkinter.CTkLabel(self, text="Pflanzenabstand:")
        self.param2_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.param2_entry = customtkinter.CTkEntry(self)
        self.param2_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Optionsliste
        self.option_plants_label = customtkinter.CTkLabel(self, text="Saatgut:")
        self.option_plants_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.option_plants_entry = customtkinter.CTkOptionMenu(self, values=["", "Zuckerrübe", "Mais", "Getreide"], state="readonly")
        self.option_plants_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Button um Koordinaten der KML-File zu extrahieren
        self.coords_kml = customtkinter.CTkButton(self, text="KML-Datei hochladen",
                                                  command=self.extract_coordinates_kml)
        self.coords_kml.grid(row=1, column=2, pady=10)

        # Button zum Berechnen und Anzeigen des Plots
        self.calculate_button = customtkinter.CTkButton(self, text="Berechnen", command= self.calculate_and_show_plot)
        self.calculate_button.grid(row=6, column=0, columnspan= 2, pady=10)

        # Tabs hinzufügen
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=5, column=1, padx=20, pady=20)
        self.tab1 = self.tabview.add("Tab 1")
        self.tab2 = self.tabview.add("Tab 2")

        # Widgets zu Tab 1 hinzufügen
        self.label_tab1 = customtkinter.CTkLabel(master=self.tab1, text="Inhalt von Tab 1")
        self.label_tab1.grid(row=5, column=1, padx=20, pady=10)

        # Widgets zu Tab 2 hinzufügen
        self.label_tab2 = customtkinter.CTkLabel(master=self.tab2, text="Inhalt von Tab 2")
        self.label_tab2.grid(row=5, column=1, padx=20, pady=10)

        # Matplotlib-Figure für den Plot
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Platzhalter für den Plot
        self.plot_placeholder()

        # Zeilen- und Spaltenanpassung bei Lücken im Fenster
        #self.grid_rowconfigure(1, weight=1)
        #self.grid_rowconfigure(5, weight=0)  # weniger Gewicht für die Tabview-Zeile
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(2, weight=3)

    def calculate_and_show_plot(self):
        try:
            # Holen der eingegebenen Parameter
            field_edge = float(self.field_edge_entry.get())
            param2 = float(self.param2_entry.get())

            self.ax.clear()

            # Polygonkoordinaten
            coords = [(1, 1), (4, 1), (6, 4), (3, 7), (1, 6), (0, 3)]
            polygon = Polygon(coords)
            # Drehung des Musters (bis max. 60 Grad)
            angle_degrees = 0
            # Verschiebung des Musters in X-Richtung in % (max. so groß wie distance_plant)
            pattern_move_x = 0
            # Verschiebung des Musters in Y-Richtung in % (max. so groß wie das Doppelte der Dreieckshöhe)
            pattern_move_y = 0
            # Verkleinertes Polygon mit Berücksichtigung des Feldrandes
            field_edge_polygon = reduced_polygon(coords, field_edge)
            # Generiere die dreiecksförmigen Punkte innerhalb des Polygons
            points = generate_triangular_points_rotated(field_edge_polygon, param2, angle_degrees,
                                                pattern_move_x,
                                                pattern_move_y)

            # Zeichne das Polygon und die Punkte
            self.x, self.y = polygon.exterior.xy
            x_red, y_red = field_edge_polygon.exterior.xy
            self.ax.fill(self.x, self.y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
            self.ax.plot(x_red, y_red, 'g--', label='Reduziertes Polygon')

            for point in points:
                self.ax.plot(point.x, point.y, 'bo')

            # Aktualisieren des Plots
            self.ax.plot(*polygon.exterior.xy, color='black')
            self.ax.set_aspect('equal', 'box')
            self.ax.set_xlabel('X-Achse')
            self.ax.set_ylabel('Y-Achse')
            self.ax.set_title('Feld mit Saatverteilung')

            # Neuzeichnen der Matplotlib-Figur
            self.canvas.draw()

        # Fehlermeldung für ungültige Eingaben
        except ValueError as error:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(error)}")

    def extract_coordinates_kml(self):
        self.ax.clear()
        selected_file = select_kml_file()
        koordinaten = extract_coordinates(selected_file)
        self.coords_entry.insert("1.0", text=koordinaten)
        # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
        utm_zone = get_utm_zone(koordinaten)
        # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
        coords = geo_to_utm(koordinaten, utm_zone)
        polygon = Polygon(coords)
        x, y = polygon.exterior.xy
        self.ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
        self.ax.plot(*polygon.exterior.xy, color='black')
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlabel('Breitengrad')
        self.ax.set_ylabel('Längengrad')
        self.ax.set_title('Darstellung des Feldes')
        # Neuzeichnen der Matplotlib-Figur
        self.canvas.draw()

    def add_info_text_coords(self, event):
        self.info_label.configure(text="Info: Schreibe die Koordinaten der Feldpunkte in folgender Form auf: {Längengrad Breitengrad}{L2 B2}{L3 B3}...", text_color="gray")

    def remove_info_text(self, event):
        self.info_label.configure(text="")

    def plot_placeholder(self):
        # Platzhalter-Plot anzeigen
        self.ax.set_xlabel('X-Achse')
        self.ax.set_ylabel('Y-Achse')
        self.ax.set_title('Feld mit Saatverteilung')
        self.canvas.draw()

if __name__ == "__main__":
    app = PlotApp()
    app.mainloop()


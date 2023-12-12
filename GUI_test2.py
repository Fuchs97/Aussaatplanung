from tkinter import messagebox
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from triangular_pattern import generate_triangular_points
from polygon_with_field_edge import reduced_polygon
class PlotApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aussaatplanung")
        self.geometry("600x600")

        # Parameter-Eingabefelder
        self.param1_label = customtkinter.CTkLabel(self, text="Feldrandbreite:")
        self.param1_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.param1_entry = customtkinter.CTkEntry(self)
        self.param1_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.param2_label = customtkinter.CTkLabel(self, text="Pflanzenabstand:")
        self.param2_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.param2_entry = customtkinter.CTkEntry(self)
        self.param2_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

#        self.param3_label = customtkinter.CTkLabel(self, text="Parameter 3:")
#        self.param3_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
#        self.param3_entry = customtkinter.CTkEntry(self)
#        self.param3_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Button zum Berechnen und Anzeigen des Plots
        self.calculate_button = customtkinter.CTkButton(self, text="Berechnen", command=self.calculate_and_show_plot)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Matplotlib-Figure für den Plot
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Platzhalter für den Plot
        self.plot_placeholder()

        # Vergrößerbare Zeilen und Spalten
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.reduced_polygon = None
        self.points = None
        self.x_red = None
        self.y_red = None
        self.x = None
        self.y = None
    def calculate_and_show_plot(self):
        try:
            # Holen der eingegebenen Parameter
            param1 = float(self.param1_entry.get())
            param2 = float(self.param2_entry.get())

            self.ax.clear()

            # Polygonkoordinaten
            coords = [(1, 1), (4, 1), (6, 4), (3, 7), (1, 6), (0, 3)]
            polygon = Polygon(coords)
            # Verkleinertes Polygon mit Berücksichtigung des Feldrandes
            self.reduced_polygon = reduced_polygon(coords, param1)
            # Generiere die dreiecksförmigen Punkte innerhalb des Polygons
            self.points = generate_triangular_points(self.reduced_polygon, param2)

            # Zeichne das Polygon und die Punkte
            self.x, self.y = polygon.exterior.xy
            self.x_red, self.y_red = self.reduced_polygon.exterior.xy
            self.ax.fill(self.x, self.y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
            self.ax.plot(self.x_red, self.y_red, 'g--', label='Reduziertes Polygon')

            for point in self.points:
                self.ax.plot(point.x, point.y, 'bo')

            # Aktualisieren des Plots
            self.ax.plot(*polygon.exterior.xy, color='black')
            self.ax.set_aspect('equal', 'box')
            self.ax.set_xlabel('X-Achse')
            self.ax.set_ylabel('Y-Achse')
            self.ax.set_title('Feld mit Saatverteilung')

            # Neuzeichnen der Matplotlib-Figur
            self.canvas.draw()

        except ValueError:
            # Fehlerbehandlung für ungültige Eingaben
            messagebox.showerror("Fehler", "Ungültige Eingabe. Bitte geben Sie gültige Zahlen ein.")

    def plot_placeholder(self):
        # Platzhalter-Plot anzeigen
        self.ax.set_xlabel('X-Achse')
        self.ax.set_ylabel('Y-Achse')
        self.ax.set_title('Feld mit Saatverteilung')
        self.canvas.draw()

if __name__ == "__main__":
    app = PlotApp()
    app.mainloop()


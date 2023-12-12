from tkinter import Tk, Label, Entry, Button, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely.geometry import Polygon
from triangular_pattern import generate_triangular_points
from polygon_with_field_edge import reduced_polygon
import customtkinter as ctk

# Definiere param1_entry und param2_entry als globale Variablen
param1_entry = None
param2_entry = None
def calculate_and_show_plot(ax, param1_entry, param2_entry):
    try:
        # Holen der eingegebenen Parameter
        param1 = float(param1_entry.get())
        param2 = float(param2_entry.get())

        ax.clear()

        # Polygonkoordinaten
        coords = [(1, 1), (4, 1), (6, 4), (3, 7), (1, 6), (0, 3)]
        polygon = Polygon(coords)
        # Verkleinertes Polygon mit Berücksichtigung des Feldrandes
        reduced_polygon_coords = reduced_polygon(coords, param1)
        reduced_polygon_shape = Polygon(reduced_polygon_coords)
        # Generiere die dreiecksförmigen Punkte innerhalb des Polygons
        points = generate_triangular_points(reduced_polygon_shape, param2)

        # Zeichne das Polygon und die Punkte
        x, y = polygon.exterior.xy
        x_red, y_red = reduced_polygon_shape.exterior.xy
        ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
        ax.plot(x_red, y_red, 'g--', label='Reduziertes Polygon')

        for point in points:
            ax.plot(point.x, point.y, 'bo')

        # Aktualisieren des Plots
        ax.plot(*polygon.exterior.xy, color='black')
        ax.set_aspect('equal', 'box')
        ax.set_xlabel('X-Achse')
        ax.set_ylabel('Y-Achse')
        ax.set_title('Feld mit Saatverteilung')

        # Neuzeichnen der Matplotlib-Figur
        canvas.draw()

    except ValueError:
        # Fehlerbehandlung für ungültige Eingaben
        messagebox.showerror("Fehler", "Ungültige Eingabe. Bitte geben Sie gültige Zahlen ein.")

def plot_placeholder(ax):
    # Platzhalter-Plot anzeigen
    ax.set_xlabel('X-Achse')
    ax.set_ylabel('Y-Achse')
    ax.set_title('Feld mit Saatverteilung')
    canvas.draw()

def adding_objects_to_GUI(root):
    root.title("Aussaatplanung")
    root.geometry("600x600")

    # Parameter-Eingabefelder
    param1_label = ctk.CTkLabel(root, text="Feldrandbreite:")
    param1_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    param1_entry = ctk.CTkEntry(root)
    param1_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    param2_label = ctk.CTkLabel(root, text="Pflanzenabstand:")
    param2_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    param2_entry = ctk.CTkEntry(root)
    param2_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Matplotlib-Figure für den Plot
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Button zum Berechnen und Anzeigen des Plots
    calculate_button = ctk.CTkButton(root, text="Berechnen", command=lambda: calculate_and_show_plot(ax, param1_entry, param2_entry))
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Platzhalter für den Plot
    plot_placeholder(ax)

    # Vergrößerbare Zeilen und Spalten
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(1, weight=1)


# Erstelle Hauptfenster der App
app = ctk.CTk()

adding_objects_to_GUI(app)

# Starte Tkinter Hauptloop
app.mainloop()




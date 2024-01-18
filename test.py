from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
import time
from pyswarm import pso
import tkinter as tk
from threading import Thread

class MyApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimierung mit PSO")

        self.precision_var = tk.DoubleVar(value=0.1)

        self.precision_label = tk.Label(root, text="Präzision:")
        self.precision_label.pack()

        self.precision_slider = tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, orient="horizontal", variable=self.precision_var)
        self.precision_slider.pack()

        self.start_button = tk.Button(root, text="Optimierung starten", command=self.start_optimization)
        self.start_button.pack()

        self.abort_button = tk.Button(root, text="Optimierung abbrechen", command=self.abort_optimization, state="disabled")
        self.abort_button.pack()

        self.optimization_thread = None
        self.abort_flag = False

    def start_optimization(self):
        self.start_button["state"] = "disabled"
        self.abort_button["state"] = "normal"
        self.abort_flag = False

        # Parameter für die Optimierung
        lb = [0, 0, 0]
        ub = [60, 100, 100]
        swarmsize = 1

        # Thread für die Optimierung starten
        self.optimization_thread = Thread(target=self.run_optimization, args=(lb, ub, swarmsize))
        self.optimization_thread.start()

    def abort_optimization(self):
        # Benutzer hat den Abbruch angefordert
        self.abort_flag = True
        self.start_button["state"] = "normal"
        self.abort_button["state"] = "disabled"

    def run_optimization(self, lb, ub, swarmsize):
        # Algorithmus starten
        max_iterations = 1000  # Maximal erlaubte Iterationen

        for iteration in range(max_iterations):
            # Berechnungen für diese Iteration durchführen
            result = self.run_single_iteration(lb, ub, swarmsize)

            # Ergebnisse aktualisieren oder visualisieren (je nach Bedarf)

            # Prüfen, ob der Benutzer den Algorithmus abbrechen möchte
            if self.abort_flag:
                break

            # Pause zwischen den Iterationen für die Visualisierung oder Aktualisierung
            time.sleep(1)

        # Aufräumarbeiten nach Abschluss der Optimierung
        self.cleanup_after_optimization()

    def run_single_iteration(self, lb, ub, swarmsize):
        # Hier deine Berechnungen für eine Iteration einfügen
        # Beispiel: Ergebnisse der PSO-Optimierung zurückgeben
        result = pso(opt_points_calc_gradient_descent, lb, ub, swarmsize=swarmsize, maxiter=1)
        return result

    def cleanup_after_optimization(self):
        # Hier aufräumen oder Abschlussarbeiten durchführen
        self.start_button["state"] = "normal"
        self.abort_button["state"] = "disabled"

def opt_points_calc_gradient_descent(params):
    angle_degrees, pattern_move_x, pattern_move_y = params
    # Berechnung der Saatpunkte
    points = generate_triangular_points_rotated(polygon, distance, angle_degrees, pattern_move_x, pattern_move_y)

    return -sum([point.x + point.y for point in points])

# Definition des Vierecks
polygon = Polygon([(-1, 2), (0, 4), (3, 5), (4.5, 4), (5, 3), (3, -1), (2, 1), (1, -2)])
distance = 1

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    root.mainloop()

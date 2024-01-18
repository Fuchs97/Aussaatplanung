import numpy as np
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt

# Zielfunktion (kann an deine spezifische Funktion angepasst werden)
def objective_function(x):
    return np.sum(x**2)

# Callback-Funktion für das Plotten der Konvergenz
def callback_function(xk, convergence):
    convergence_curve.append(objective_function(xk))

# Definition des Optimierungsproblems
bounds = [(-5, 5), (-5, 5), (-5, 5)]  # Beispiel: 3 Parameter im Bereich von -5 bis 5
convergence_curve = []  # Hier werden die Zielfunktionswerte im Laufe der Iterationen gespeichert

# Aufruf des Differential Evolution Algorithmus mit Callback
result = differential_evolution(objective_function, bounds, callback=callback_function)

# Plot des Konvergenzverhaltens
plt.plot(convergence_curve, label='Differential Evolution')
plt.xlabel('Iterationen')
plt.ylabel('Zielfunktionswert')
plt.title('Konvergenzverhalten des Differential Evolution Algorithmus')
plt.legend()
plt.show()

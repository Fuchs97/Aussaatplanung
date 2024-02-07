import matplotlib.pyplot as plt
import numpy as np

# Daten erzeugen
x = np.linspace(0, 100, 122)
y = np.sin(x)

# Plot erstellen
plt.plot(x, y)
plt.xlabel('X-Achse')
plt.ylabel('Y-Achse')

# Achsenbeschriftungen formatieren
plt.gca().xaxis.get_major_formatter().set_scientific(True)
plt.gca().yaxis.get_major_formatter().set_scientific(True)
plt.gca().xaxis.offsetText.set_visible(False)
plt.gca().yaxis.offsetText.set_visible(False)

# Maximale und minimale Werte der Achsen abrufen
x_min, x_max = plt.gca().get_xlim()
y_min, y_max = plt.gca().get_ylim()

# Notation am oberen linken Ende der Achsen einfügen
plt.text(0.0, 1.07, f'$\\times 10^{{{np.log10(x_max):.0f}}}$', transform=plt.gca().transAxes, va='top')
plt.text(1.02, 0.0, f'$\\times 10^{{{np.log10(y_max):.0f}}}$', transform=plt.gca().transAxes, va='top')

# Plot anzeigen
plt.show()



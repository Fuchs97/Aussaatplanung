import matplotlib.pyplot as plt
import random

# Größe des Ackerfelds
feld_breite = 100
feld_höhe = 100

# Anzahl der Saatpunkte
anzahl_saatpunkte = 20

# Funktion zur Generierung zufälliger Saatpunkte
def generiere_saatpunkte(anzahl, breite, höhe):
    saatpunkte = []
    for _ in range(anzahl):
        x = random.randint(0, breite)
        y = random.randint(0, höhe)
        saatpunkte.append((x, y))
    return saatpunkte

# Saatpunkte generieren
saatpunkte = generiere_saatpunkte(anzahl_saatpunkte, feld_breite, feld_höhe)

# Ackerfeld erstellen
plt.figure(figsize=(8, 8))
plt.scatter(*zip(*saatpunkte), marker='o', color='green', label='Saatpunkte')
plt.xlim(0, feld_breite)
plt.ylim(0, feld_höhe)
plt.xlabel('X-Koordinate')
plt.ylabel('Y-Koordinate')
plt.title('Ackerfeld mit Saatpunkten')
plt.legend()
plt.grid(True)

# Diagramm anzeigen
plt.show()
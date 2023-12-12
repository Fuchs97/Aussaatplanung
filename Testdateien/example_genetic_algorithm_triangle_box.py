import random
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box


# Funktion zur Berechnung der unbedeckten Fläche
def calculate_uncovered_area(rectangle, triangle):
    intersection = rectangle.intersection(triangle)
    return rectangle.area - intersection.area

# Funktion zur Generierung eines zufälligen Individuums

# Funktion zur Kreuzung zweier Elternindividuen
def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1))
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def generate_individual():
    # Zufällige Position des Dreiecks im Bereich des Vierecks
    tx = random.uniform(0, 10)
    ty = random.uniform(0, 10)

    # Zufällige Rotation des Dreiecks
    angle = random.uniform(0, 360)

    return tx, ty, angle

# Funktion zur Mutation eines Individuums
def mutate(individual):
    # Zufällige Mutation der Position und Rotation
    mutation_factor = 0.2
    mutated_tx = individual[0] + random.uniform(-mutation_factor, mutation_factor)
    mutated_ty = individual[1] + random.uniform(-mutation_factor, mutation_factor)
    mutated_angle = individual[2] + random.uniform(-mutation_factor * 50, mutation_factor * 50)

    # Begrenze die Werte auf den Bereich des Vierecks bzw. 360 Grad
    mutated_tx = np.clip(mutated_tx, 0, 10)
    mutated_ty = np.clip(mutated_ty, 0, 10)
    mutated_angle = np.clip(mutated_angle, 0, 360)

    return mutated_tx, mutated_ty, mutated_angle

# Funktion zur Durchführung des genetischen Algorithmus
def genetic_algorithm(rectangle, generations, population_size):
    population = [generate_individual() for _ in range(population_size)]

    for generation in range(generations):
        # Bewertung der Individuen anhand der unbedeckten Fläche
        scores = [calculate_uncovered_area(rectangle, generate_rotated_triangle(individual)) for individual in population]

        # Auswahl der besten Individuen
        best_indices = sorted(range(len(scores)), key=lambda i: scores[i])
        best_individuals = [population[i] for i in best_indices[:population_size // 2]]

        # Crossover und Mutation
        new_generation = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.choices(best_individuals, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_generation.append(child)

        population = best_individuals + new_generation

    # Wähle das beste Individuum als Ergebnis aus
    best_individual = min(population, key=lambda ind: calculate_uncovered_area(rectangle, generate_rotated_triangle(ind)))

    return best_individual

def generate_rotated_triangle(individual):
    # Annahme: Das Dreieck hat die Seitenlängen 4, 3, 5
    tx, ty, angle = individual

    # Definition der Eckpunkte des Dreiecks
    triangle_points = [(tx + 5, ty), (tx + 14, ty), (tx, ty + 10)]

    # Homogene Koordinaten hinzufügen
    homogeneous_triangle_points = [point + (1,) for point in triangle_points]

    # Rotation der homogenen Koordinaten um den Ursprung
    rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0],
                                [0, 0, 1]])

    # Anwenden der Rotation
    rotated_homogeneous_triangle_points = [tuple(rotation_matrix @ np.array(point)) for point in homogeneous_triangle_points]

    # Homogene Koordinaten entfernen
    rotated_triangle_points = [(x, y) for x, y, _ in rotated_homogeneous_triangle_points]

    return Polygon(rotated_triangle_points)

# Beispielaufruf
rectangle = box(0, 0, 10, 10)
triangle = generate_rotated_triangle(generate_individual())

# Zeichne das Dreieck
#x, y = triangle.exterior.xy
#plt.plot(x, y, color='r')

# Zeichne das Viereck
x, y = rectangle.exterior.xy
plt.plot(x, y, color='b')

# Zeichne das beste Dreieck
best_solution = genetic_algorithm(rectangle, generations=50, population_size=50)
best_triangle = generate_rotated_triangle(best_solution)
x, y = best_triangle.exterior.xy
plt.plot(x, y, color='g')

plt.axis('equal')
plt.show()

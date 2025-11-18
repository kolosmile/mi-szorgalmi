# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# A pontgenerátor importálása a másik fájlból
from point_generator import generate_point_cloud, visualize_point_cloud

class CircleGA:
    """
    Genetikus algoritmus a legkisebb befoglaló kör megkeresésére.
    """
    def __init__(self, points, population_size=100, mutation_rate=0.1, crossover_rate=0.8, generations=200):
        self.points = points
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        
        # A populáció inicializálása a ponthalmaz határain belül
        min_coords = points.min(axis=0)
        max_coords = points.max(axis=0)
        self.x_range = (min_coords[0], max_coords[0])
        self.y_range = (min_coords[1], max_coords[1])
        
        # A sugár lehetséges tartományának becslése
        max_dim = max(self.x_range[1] - self.x_range[0], self.y_range[1] - self.y_range[0])
        self.r_range = (max_dim / 10, max_dim)

        self.population = self._initialize_population()

    def _initialize_population(self):
        """Létrehozza a kezdeti populációt véletlenszerű körökből."""
        population = np.zeros((self.population_size, 3))
        population[:, 0] = np.random.uniform(self.x_range[0], self.x_range[1], self.population_size) # cx
        population[:, 1] = np.random.uniform(self.y_range[0], self.y_range[1], self.population_size) # cy
        population[:, 2] = np.random.uniform(self.r_range[0], self.r_range[1], self.population_size) # r
        return population

    def _calculate_fitness(self):
        """
        Kiértékeli minden egyed (kör) fitneszét a populációban.
        A fitnesz a sugártól és a büntetéstől függ.
        """
        fitness_scores = np.zeros(self.population_size)
        for i, individual in enumerate(self.population):
            cx, cy, r = individual
            
            # Távolságok a kör középpontjától
            distances = np.sqrt((self.points[:, 0] - cx)**2 + (self.points[:, 1] - cy)**2)
            
            # Büntetés a körön kívül eső pontokért
            outside_points = distances[distances > r]
            penalty = np.sum(outside_points - r) * 10 # A büntetés súlyozása
            
            # A fitnesz a sugár és a büntetés összege. A cél a minimalizálás.
            # Kisebb érték = jobb fitnesz.
            fitness_scores[i] = r + penalty
            
        return fitness_scores

    def _select(self, fitness_scores):
        """
        Szelektálja a szülőket a következő generációhoz.
        A jobb fitneszű (kisebb értékű) egyedek nagyobb eséllyel lesznek kiválasztva.
        """
        # A fitnesz értékeket invertáljuk, mert a kisebb a jobb, de a szelekcióhoz a nagyobbnak kell jobbnak lennie
        inverted_fitness = 1 / (fitness_scores + 1e-6) # + 1e-6 a nullával való osztás elkerülésére
        probabilities = inverted_fitness / np.sum(inverted_fitness)
        
        selected_indices = np.random.choice(
            self.population_size, size=self.population_size, p=probabilities
        )
        return self.population[selected_indices]

    def _crossover(self, parents):
        """Keresztezi a szülőket, hogy utódokat hozzon létre."""
        offspring = np.zeros_like(parents)
        for i in range(0, self.population_size, 2):
            parent1, parent2 = parents[i], parents[i+1]
            if np.random.rand() < self.crossover_rate:
                # Egypontos keresztezés
                crossover_point = np.random.randint(1, 3)
                offspring[i, :crossover_point] = parent1[:crossover_point]
                offspring[i, crossover_point:] = parent2[crossover_point:]
                offspring[i+1, :crossover_point] = parent2[:crossover_point]
                offspring[i+1, crossover_point:] = parent1[crossover_point:]
            else:
                offspring[i], offspring[i+1] = parent1, parent2
        return offspring

    def _mutate(self, offspring):
        """Végrehajtja a mutációt az utódokon."""
        for i in range(len(offspring)):
            if np.random.rand() < self.mutation_rate:
                # Véletlenszerűen kiválaszt egy gént (cx, cy, vagy r) és módosítja
                gene_to_mutate = np.random.randint(0, 3)
                if gene_to_mutate == 0: # cx
                    mutation_value = np.random.normal(0, (self.x_range[1] - self.x_range[0]) * 0.05)
                    offspring[i, 0] += mutation_value
                elif gene_to_mutate == 1: # cy
                    mutation_value = np.random.normal(0, (self.y_range[1] - self.y_range[0]) * 0.05)
                    offspring[i, 1] += mutation_value
                else: # r
                    mutation_value = np.random.normal(0, (self.r_range[1] - self.r_range[0]) * 0.05)
                    offspring[i, 2] += mutation_value
        
        # Biztosítjuk, hogy az értékek a tartományon belül maradjanak
        np.clip(offspring[:, 0], self.x_range[0], self.x_range[1], out=offspring[:, 0])
        np.clip(offspring[:, 1], self.y_range[0], self.y_range[1], out=offspring[:, 1])
        np.clip(offspring[:, 2], self.r_range[0], self.r_range[1], out=offspring[:, 2])
        
        return offspring

    def run(self):
        """Futtatja a genetikus algoritmust a megadott generációszámig."""
        best_fitness_overall = np.inf
        best_individual_overall = None

        for generation in range(self.generations):
            # 1. Fitnesz számítás
            fitness_scores = self._calculate_fitness()
            
            # 2. A legjobb egyed elmentése
            best_idx = np.argmin(fitness_scores)
            if fitness_scores[best_idx] < best_fitness_overall:
                best_fitness_overall = fitness_scores[best_idx]
                best_individual_overall = self.population[best_idx]

            if (generation + 1) % 20 == 0:
                print(f"Generáció: {generation + 1}/{self.generations}, Legjobb fitnesz: {best_fitness_overall:.2f}")

            # 3. Szelekció
            parents = self._select(fitness_scores)
            
            # 4. Keresztezés
            offspring = self._crossover(parents)
            
            # 5. Mutáció
            mutated_offspring = self._mutate(offspring)
            
            # Az új populáció a mutált utódokból áll
            self.population = mutated_offspring
            
        return best_individual_overall

def visualize_solution(points, circle_params, title="Megoldás"):
    """Megjeleníti a ponthalmazt és a megtalált kört."""
    cx, cy, r = circle_params
    
    fig, ax = plt.subplots(figsize=(8, 8))
    # Pontok kirajzolása
    ax.scatter(points[:, 0], points[:, 1], alpha=0.7, edgecolors='k', label="Adatpontok")
    
    # A megtalált kör kirajzolása
    solution_circle = Circle((cx, cy), r, color='r', fill=False, linewidth=2, label="Illesztett kör")
    ax.add_patch(solution_circle)
    
    ax.set_title(title)
    ax.set_xlabel("X koordináta")
    ax.set_ylabel("Y koordináta")
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.legend()
    plt.show()


if __name__ == '__main__':
    # 1. Ponthalmaz generálása
    points = generate_point_cloud(
        center=(50, 50),
        radius=100,
        num_points=150,
        shape_error=0.1,
        random_noise=5.0,
        num_outliers=8
    )
    
    # 2. Genetikus algoritmus inicializálása és futtatása
    ga = CircleGA(points, population_size=200, generations=300, mutation_rate=0.2)
    best_circle = ga.run()
    
    print("\n--- Eredmény ---")
    print(f"A legjobb megtalált kör paraméterei:")
    print(f"  Középpont: ({best_circle[0]:.2f}, {best_circle[1]:.2f})")
    print(f"  Sugár: {best_circle[2]:.2f}")
    
    # 3. Eredmény megjelenítése
    visualize_solution(points, best_circle, "Genetikus Algoritmus Eredménye")

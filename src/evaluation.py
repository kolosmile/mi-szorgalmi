# -*- coding: utf-8 -*-
import time
import numpy as np
import matplotlib.pyplot as plt
import argparse

from point_generator import generate_point_cloud
from genetic_algorithm import CircleGA

def evaluate_runtime_vs_points(point_counts, ga_params):
    """
    Kiértékeli a futási időt a pontok számának függvényében.

    Args:
        point_counts (list): A tesztelni kívánt pontszámok listája.
        ga_params (dict): A genetikus algoritmus fix paraméterei.
    """
    print("\n--- Futási idő kiértékelése a pontok száma alapján ---")
    execution_times = []

    for n_points in point_counts:
        print(f"Futtatás {n_points} ponttal...")
        # Mindig ugyanazt a ponthalmazt generáljuk az összehasonlíthatóságért
        np.random.seed(42) 
        points = generate_point_cloud(num_points=n_points)
        
        ga = CircleGA(points, **ga_params)
        
        start_time = time.time()
        ga.run()
        end_time = time.time()
        
        execution_times.append(end_time - start_time)

    # Eredmények ábrázolása
    plt.figure(figsize=(10, 6))
    plt.plot(point_counts, execution_times, marker='o', linestyle='-')
    plt.title("Futási idő a pontok számának függvényében")
    plt.xlabel("Pontok száma")
    plt.ylabel("Futási idő (másodperc)")
    plt.grid(True)
    plt.show()

def evaluate_mutation_rate_vs_fitness(mutation_rates, ga_params):
    """
    Kiértékeli a mutációs ráta hatását a végső fitneszre.

    Args:
        mutation_rates (list): A tesztelni kívánt mutációs ráták listája.
        ga_params (dict): A genetikus algoritmus fix paraméterei.
    """
    print("\n--- Mutációs ráta hatásának kiértékelése ---")
    final_radii = []
    
    # Fix ponthalmaz a tesztekhez
    np.random.seed(42)
    points = generate_point_cloud()

    for rate in mutation_rates:
        print(f"Futtatás {rate} mutációs rátával...")
        current_params = ga_params.copy()
        current_params['mutation_rate'] = rate
        
        ga = CircleGA(points, **current_params)
        best_circle, _ = ga.run()
        final_radii.append(best_circle[2]) # A sugár a fitnesz jó mérőszáma

    # Eredmények ábrázolása
    plt.figure(figsize=(10, 6))
    plt.bar([str(r) for r in mutation_rates], final_radii, color='skyblue')
    plt.title("A mutációs ráta hatása a végső sugárra")
    plt.xlabel("Mutációs ráta")
    plt.ylabel("Eredmény kör sugara (minél kisebb, annál jobb)")
    plt.grid(axis='y')
    plt.show()

def plot_convergence_from_history(history):
    """
    Ábrázolja a konvergenciát a kapott fitnesz előzmények alapján.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(history)
    plt.title("Fitnesz érték alakulása a generációk során (Konvergencia)")
    plt.xlabel("Generáció")
    plt.ylabel("Legjobb fitnesz (minél kisebb, annál jobb)")
    plt.grid(True)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Kiértékelő szkript a körillesztő genetikus algoritmushoz.")
    parser.add_argument(
        '--test', 
        type=str, 
        choices=['runtime', 'mutation', 'convergence'], 
        required=True,
        help="A futtatni kívánt kiértékelési teszt: 'runtime', 'mutation', vagy 'convergence'."
    )
    args = parser.parse_args()

    # Közös GA paraméterek a tesztekhez
    common_ga_params = {
        "population_size": 100,
        "generations": 150,
        "crossover_rate": 0.8
    }

    if args.test == 'runtime':
        point_numbers = [50, 100, 150, 200, 300, 400, 500]
        evaluate_runtime_vs_points(point_numbers, {**common_ga_params, 'mutation_rate': 0.1})
    
    elif args.test == 'mutation':
        rates = [0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8]
        evaluate_mutation_rate_vs_fitness(rates, common_ga_params)

    elif args.test == 'convergence':
        print("\n--- Konvergencia vizsgálat futtatása ---")
        np.random.seed(42)
        points = generate_point_cloud(num_points=200, num_outliers=10)
        ga = CircleGA(points, **common_ga_params, mutation_rate=0.1)
        _, history = ga.run()
        plot_convergence_from_history(history)


if __name__ == '__main__':
    main()

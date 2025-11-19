# -*- coding: utf-8 -*-
import time
import numpy as np
import matplotlib.pyplot as plt
import argparse
import tracemalloc
import pandas as pd
import os
from point_generator import generate_point_cloud
from genetic_algorithm import CircleGA

# Konfiguráció a mentéshez
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'documentation', 'images')
CSV_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'documentation', 'data')

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

def measure_single_run(points, ga_params):
    """
    Egyetlen futtatás mérése: idő, memória, eredmény.
    """
    tracemalloc.start()
    start_time = time.time()
    
    ga = CircleGA(points, **ga_params)
    best_circle, history = ga.run()
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = end_time - start_time
    peak_memory_mb = peak / (1024 * 1024)
    final_radius = best_circle[2]
    
    return runtime, peak_memory_mb, final_radius, history

def run_scalability_test(repeats=10):
    """
    A. Skálázhatóság vizsgálata (Bemeneti méret hatása)
    """
    print("\n--- A. Skálázhatóság vizsgálata (Futási idő és Memória) ---")
    point_counts = [50, 100, 500, 1000, 2000, 5000]
    results = []

    ga_params = {
        "population_size": 100,
        "generations": 100,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1
    }

    for n in point_counts:
        print(f"  Mérés {n} ponttal ({repeats} ismétlés)...")
        for i in range(repeats):
            points = generate_point_cloud(num_points=n)
            runtime, memory, radius, _ = measure_single_run(points, ga_params)
            results.append({
                "n_points": n,
                "run_id": i,
                "runtime": runtime,
                "memory_mb": memory,
                "radius": radius
            })

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(CSV_DIR, 'scalability_results.csv'), index=False)

    # Ábrázolás - Futási idő
    plt.figure(figsize=(10, 6))
    stats = df.groupby('n_points')['runtime'].agg(['mean', 'std']).reset_index()
    plt.errorbar(stats['n_points'], stats['mean'], yerr=stats['std'], fmt='-o', capsize=5, label='Átlagos futási idő')
    plt.title("Futási idő a pontok számának függvényében")
    plt.xlabel("Pontok száma")
    plt.ylabel("Futási idő (s)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(RESULTS_DIR, 'scalability_runtime.png'))
    plt.close()

    # Ábrázolás - Memória
    plt.figure(figsize=(10, 6))
    stats_mem = df.groupby('n_points')['memory_mb'].agg(['mean', 'std']).reset_index()
    plt.errorbar(stats_mem['n_points'], stats_mem['mean'], yerr=stats_mem['std'], fmt='-s', color='orange', capsize=5, label='Átlagos memóriahasználat')
    plt.title("Memóriahasználat a pontok számának függvényében")
    plt.xlabel("Pontok száma")
    plt.ylabel("Memória (MB)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(RESULTS_DIR, 'scalability_memory.png'))
    plt.close()
    print("  Kész. Eredmények mentve.")

def run_mutation_test(repeats=10):
    """
    B1. Mutációs ráta hatása
    """
    print("\n--- B. Mutációs ráta érzékenységvizsgálata ---")
    mutation_rates = [0.01, 0.05, 0.1, 0.2, 0.4, 0.6]
    results = []
    
    base_params = {
        "population_size": 100,
        "generations": 100,
        "crossover_rate": 0.8
    }

    for i in range(repeats):
        print(f"  Ismétlés {i+1}/{repeats}...")
        points = generate_point_cloud(num_points=200) # Közepes méret
        
        for rate in mutation_rates:
            params = base_params.copy()
            params['mutation_rate'] = rate
            runtime, memory, radius, _ = measure_single_run(points, params)
            results.append({
                "mutation_rate": rate,
                "run_id": i,
                "radius": radius
            })

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(CSV_DIR, 'mutation_results.csv'), index=False)

    # Ábrázolás
    plt.figure(figsize=(10, 6))
    stats = df.groupby('mutation_rate')['radius'].agg(['mean', 'std']).reset_index()
    plt.errorbar(stats['mutation_rate'].astype(str), stats['mean'], yerr=stats['std'], fmt='o', capsize=5, color='green')
    plt.title("Mutációs ráta hatása a megtalált kör sugarára")
    plt.xlabel("Mutációs ráta")
    plt.ylabel("Kör sugara (kisebb = jobb)")
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(RESULTS_DIR, 'sensitivity_mutation.png'))
    plt.close()
    print("  Kész. Eredmények mentve.")

def run_robustness_test(repeats=10):
    """
    C. Robusztusság vizsgálata (Outlierek)
    """
    print("\n--- C. Robusztusság vizsgálata (Outlierek hatása) ---")
    outlier_counts = [0, 5, 10, 20, 50] # 200 pont mellett ez 0%, 2.5%, 5%, 10%, 25%
    results = []
    
    base_params = {
        "population_size": 100,
        "generations": 150,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1
    }
    
    n_points = 200

    for n_out in outlier_counts:
        print(f"  Mérés {n_out} outlierrel ({repeats} ismétlés)...")
        for i in range(repeats):
            # Fontos: az outlierek a generálásnál kerülnek bele
            points = generate_point_cloud(num_points=n_points, num_outliers=n_out)
            runtime, memory, radius, _ = measure_single_run(points, base_params)
            results.append({
                "n_outliers": n_out,
                "run_id": i,
                "radius": radius
            })

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(CSV_DIR, 'robustness_results.csv'), index=False)

    # Ábrázolás
    plt.figure(figsize=(10, 6))
    df.boxplot(column='radius', by='n_outliers', grid=True)
    plt.title("Outlierek hatása a kör sugarára")
    plt.suptitle("") # A pandas automatikus címét töröljük
    plt.xlabel("Outlierek száma")
    plt.ylabel("Kör sugara")
    plt.savefig(os.path.join(RESULTS_DIR, 'robustness_outliers.png'))
    plt.close()
    print("  Kész. Eredmények mentve.")

def run_convergence_test(repeats=30):
    """
    D. Konvergencia vizsgálat
    """
    print("\n--- D. Konvergencia vizsgálat ---")
    histories = []
    
    params = {
        "population_size": 100,
        "generations": 150,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1
    }
    
    points = generate_point_cloud(num_points=200, num_outliers=10) # Egy fix nehéz eset
    
    print(f"  {repeats} futtatás a konvergencia átlagolásához...")
    for i in range(repeats):
        _, _, _, history = measure_single_run(points, params)
        histories.append(history)
    
    # Átlag és szórás számítása generációnként
    min_len = min(len(h) for h in histories)
    histories = [h[:min_len] for h in histories] # Vágás a legrövidebbre
    arr = np.array(histories)
    
    mean_history = np.mean(arr, axis=0)
    std_history = np.std(arr, axis=0)
    generations = np.arange(len(mean_history))

    # Ábrázolás
    plt.figure(figsize=(10, 6))
    plt.plot(generations, mean_history, label='Átlagos legjobb fitnesz', color='blue')
    plt.fill_between(generations, mean_history - std_history, mean_history + std_history, color='blue', alpha=0.2, label='Szórás')
    plt.title("Konvergencia sebesség (30 futtatás átlaga)")
    plt.xlabel("Generáció")
    plt.ylabel("Legjobb fitnesz (Sugár)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(RESULTS_DIR, 'convergence_plot.png'))
    plt.close()
    print("  Kész. Eredmények mentve.")

def main():
    parser = argparse.ArgumentParser(description="Részletes kiértékelő szkript.")
    parser.add_argument('--all', action='store_true', help="Minden teszt futtatása")
    parser.add_argument('--scalability', action='store_true', help="Skálázhatósági teszt")
    parser.add_argument('--mutation', action='store_true', help="Mutációs ráta teszt")
    parser.add_argument('--robustness', action='store_true', help="Robusztusság teszt")
    parser.add_argument('--convergence', action='store_true', help="Konvergencia teszt")
    
    args = parser.parse_args()

    if not any(vars(args).values()):
        print("Kérlek válassz legalább egy tesztet (pl. --all vagy --scalability)")
        return

    if args.all or args.scalability:
        run_scalability_test()
    
    if args.all or args.mutation:
        run_mutation_test()
        
    if args.all or args.robustness:
        run_robustness_test()
        
    if args.all or args.convergence:
        run_convergence_test()

if __name__ == '__main__':
    main()

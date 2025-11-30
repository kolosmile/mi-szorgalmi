# -*- coding: utf-8 -*-
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import argparse
import tracemalloc
import pandas as pd
import os
from point_generator import generate_point_cloud
from genetic_algorithm import CircleGA, visualize_solution

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


# =============================================================================
# ÚJ TESZTEK - Konzulensi visszajelzés alapján
# =============================================================================

def generate_regular_polygon(n_vertices, radius, center=(0, 0)):
    """
    Szabályos sokszög csúcsait generálja.
    Az optimális befoglaló kör sugara megegyezik a megadott sugárral.
    
    Args:
        n_vertices: Csúcsok száma (3=háromszög, 4=négyzet, 6=hatszög, stb.)
        radius: A körülírt kör sugara (ez az optimális megoldás)
        center: Középpont
    
    Returns:
        points: A csúcspontok koordinátái
        optimal_radius: Az elméleti optimális sugár
    """
    cx, cy = center
    angles = np.linspace(0, 2 * np.pi, n_vertices, endpoint=False)
    x = cx + radius * np.cos(angles)
    y = cy + radius * np.sin(angles)
    points = np.vstack((x, y)).T
    return points, radius


def generate_square_vertices(side_length, center=(0, 0)):
    """
    Négyzet 4 csúcsát generálja.
    Az optimális befoglaló kör sugara = átló / 2 = side_length * sqrt(2) / 2
    """
    cx, cy = center
    half = side_length / 2
    points = np.array([
        [cx - half, cy - half],
        [cx + half, cy - half],
        [cx + half, cy + half],
        [cx - half, cy + half]
    ])
    optimal_radius = side_length * np.sqrt(2) / 2
    return points, optimal_radius


def generate_ellipse_points(a, b, num_points=100, center=(0, 0)):
    """
    Ellipszis pontjait generálja.
    Az optimális befoglaló kör sugara = max(a, b) (a nagy féltengely)
    
    Args:
        a: Féltengely az x irányban
        b: Féltengely az y irányban
        num_points: Pontok száma
        center: Középpont
    """
    cx, cy = center
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = cx + a * np.cos(angles)
    y = cy + b * np.sin(angles)
    points = np.vstack((x, y)).T
    optimal_radius = max(a, b)
    return points, optimal_radius


def run_known_optimum_test(repeats=10):
    """
    E. Ismert optimumú tesztesetek validálása
    Szabályos alakzatokon teszteli az algoritmust, ahol az optimális megoldás ismert.
    """
    print("\n--- E. Ismert optimumú tesztesetek ---")
    
    test_cases = []
    results = []
    
    # 1. Szabályos háromszög
    points_tri, opt_tri = generate_regular_polygon(3, 100)
    test_cases.append(("Szabályos háromszög (3 csúcs)", points_tri, opt_tri))
    
    # 2. Négyzet
    points_sq, opt_sq = generate_square_vertices(100)
    test_cases.append(("Négyzet (4 csúcs)", points_sq, opt_sq))
    
    # 3. Szabályos hatszög
    points_hex, opt_hex = generate_regular_polygon(6, 100)
    test_cases.append(("Szabályos hatszög (6 csúcs)", points_hex, opt_hex))
    
    # 4. Szabályos tízszög
    points_dec, opt_dec = generate_regular_polygon(10, 100)
    test_cases.append(("Szabályos tízszög (10 csúcs)", points_dec, opt_dec))
    
    # 5. Ellipszis (a=100, b=60)
    points_ell, opt_ell = generate_ellipse_points(100, 60, num_points=50)
    test_cases.append(("Ellipszis (a=100, b=60)", points_ell, opt_ell))
    
    # 6. Ellipszis (a=80, b=120)
    points_ell2, opt_ell2 = generate_ellipse_points(80, 120, num_points=50)
    test_cases.append(("Ellipszis (a=80, b=120)", points_ell2, opt_ell2))
    
    ga_params = {
        "population_size": 150,
        "generations": 200,
        "crossover_rate": 0.8,
        "mutation_rate": 0.15
    }
    
    # Futtatás minden tesztesetre
    for name, points, optimal in test_cases:
        print(f"  Teszt: {name}")
        found_radii = []
        
        for i in range(repeats):
            _, _, radius, _ = measure_single_run(points, ga_params)
            found_radii.append(radius)
        
        mean_radius = np.mean(found_radii)
        std_radius = np.std(found_radii)
        error_pct = ((mean_radius - optimal) / optimal) * 100
        
        results.append({
            "test_case": name,
            "optimal_radius": optimal,
            "mean_found_radius": mean_radius,
            "std_found_radius": std_radius,
            "error_percent": error_pct
        })
        
        print(f"    Optimális: {optimal:.2f}, Talált: {mean_radius:.2f} ± {std_radius:.2f}, Hiba: {error_pct:.2f}%")
    
    # Eredmények mentése
    df = pd.DataFrame(results)
    df.to_csv(os.path.join(CSV_DIR, 'known_optimum_results.csv'), index=False)
    
    # Vizualizáció: minden teszteset ábrázolása
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, points, optimal) in enumerate(test_cases):
        ax = axes[idx]
        
        # Pontok
        ax.scatter(points[:, 0], points[:, 1], alpha=0.8, edgecolors='k', s=50, label='Pontok')
        
        # Optimális kör
        opt_circle = Circle((0, 0), optimal, color='green', fill=False, linewidth=2, linestyle='--', label=f'Optimális (r={optimal:.1f})')
        ax.add_patch(opt_circle)
        
        # Futtatás és megtalált kör
        ga = CircleGA(points, **ga_params)
        best_circle, _ = ga.run()
        found_circle = Circle((best_circle[0], best_circle[1]), best_circle[2], 
                              color='red', fill=False, linewidth=2, label=f'Talált (r={best_circle[2]:.1f})')
        ax.add_patch(found_circle)
        
        ax.set_title(name)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=8)
        
        # Tengelyek beállítása
        all_coords = np.concatenate([points, [[0, 0]]])
        margin = optimal * 0.3
        ax.set_xlim(all_coords[:, 0].min() - margin, all_coords[:, 0].max() + margin)
        ax.set_ylim(all_coords[:, 1].min() - margin, all_coords[:, 1].max() + margin)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'known_optimum_validation.png'), dpi=150)
    plt.close()
    
    # Összefoglaló táblázat grafikon
    plt.figure(figsize=(10, 6))
    x_labels = [r['test_case'].split('(')[0].strip() for r in results]
    errors = [r['error_percent'] for r in results]
    colors = ['green' if abs(e) < 1 else 'orange' if abs(e) < 5 else 'red' for e in errors]
    
    bars = plt.bar(x_labels, errors, color=colors, edgecolor='black')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.axhline(y=1, color='green', linestyle='--', linewidth=1, alpha=0.5, label='1% hiba')
    plt.axhline(y=-1, color='green', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.title("Algoritmus pontossága ismert optimumú teszteseteken")
    plt.xlabel("Teszteset")
    plt.ylabel("Hiba az optimálishoz képest (%)")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'known_optimum_errors.png'), dpi=150)
    plt.close()
    
    print("  Kész. Eredmények mentve.")


def run_iteration_runtime_test(repeats=5):
    """
    F. Futási idő és iterációszám (generációszám) kapcsolata
    """
    print("\n--- F. Futási idő vs. Iterációszám (generációszám) ---")
    
    generation_counts = [25, 50, 100, 150, 200, 300, 500, 750, 1000]
    results = []
    
    base_params = {
        "population_size": 100,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1
    }
    
    # Fix ponthalmaz a konzisztens méréshez
    points = generate_point_cloud(num_points=200, num_outliers=5)
    
    for n_gen in generation_counts:
        print(f"  Mérés {n_gen} generációval ({repeats} ismétlés)...")
        for i in range(repeats):
            params = base_params.copy()
            params['generations'] = n_gen
            
            runtime, _, radius, _ = measure_single_run(points, params)
            
            results.append({
                "generations": n_gen,
                "run_id": i,
                "runtime": runtime,
                "radius": radius,
                "time_per_iteration": runtime / n_gen
            })
    
    df = pd.DataFrame(results)
    df.to_csv(os.path.join(CSV_DIR, 'iteration_runtime_results.csv'), index=False)
    
    # Ábrázolás - Futási idő vs. generációszám
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Futási idő
    ax1 = axes[0]
    stats = df.groupby('generations')['runtime'].agg(['mean', 'std']).reset_index()
    ax1.errorbar(stats['generations'], stats['mean'], yerr=stats['std'], 
                 fmt='-o', capsize=5, color='blue', label='Átlagos futási idő')
    
    # Lineáris illesztés
    coeffs = np.polyfit(stats['generations'], stats['mean'], 1)
    fit_line = np.polyval(coeffs, stats['generations'])
    ax1.plot(stats['generations'], fit_line, '--', color='red', 
             label=f'Lineáris illesztés (meredekség: {coeffs[0]*1000:.3f} ms/gen)')
    
    ax1.set_title("Futási idő a generációszám függvényében")
    ax1.set_xlabel("Generációk száma")
    ax1.set_ylabel("Futási idő (s)")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Iterációnkénti idő (ellenőrzés, hogy konstans-e)
    ax2 = axes[1]
    stats_per_iter = df.groupby('generations')['time_per_iteration'].agg(['mean', 'std']).reset_index()
    ax2.errorbar(stats_per_iter['generations'], stats_per_iter['mean'] * 1000, 
                 yerr=stats_per_iter['std'] * 1000, fmt='-s', capsize=5, color='green')
    ax2.axhline(y=stats_per_iter['mean'].mean() * 1000, color='red', linestyle='--', 
                label=f'Átlag: {stats_per_iter["mean"].mean()*1000:.2f} ms/generáció')
    
    ax2.set_title("Átlagos idő generációnként")
    ax2.set_xlabel("Generációk száma")
    ax2.set_ylabel("Idő/generáció (ms)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'iteration_runtime_analysis.png'), dpi=150)
    plt.close()
    
    # Összefoglaló statisztikák kiírása
    avg_time_per_iter = df['time_per_iteration'].mean() * 1000
    print(f"\n  Átlagos idő generációnként: {avg_time_per_iter:.2f} ms")
    print(f"  Lineáris kapcsolat meredeksége: {coeffs[0]*1000:.3f} ms/generáció")
    print("  Kész. Eredmények mentve.")


def run_parameter_variation_test():
    """
    G. Konkrét példák különböző paraméter-beállításokkal
    Bemutatja az alakhiba, zaj és kiugró pontok hatását vizuálisan.
    """
    print("\n--- G. Paraméter variációk vizuális bemutatása ---")
    
    ga_params = {
        "population_size": 150,
        "generations": 200,
        "crossover_rate": 0.8,
        "mutation_rate": 0.15
    }
    
    # Tesztesetek definiálása
    test_configs = [
        # (név, pontgenerátor paraméterek)
        ("Ideális eset\n(zaj=2, alakhiba=0, outlier=0)", 
         {"num_points": 100, "radius": 100, "random_noise": 2.0, "shape_error": 0.0, "num_outliers": 0}),
        
        ("Közepes zaj\n(zaj=5, alakhiba=0.1, outlier=5)", 
         {"num_points": 100, "radius": 100, "random_noise": 5.0, "shape_error": 0.1, "num_outliers": 5}),
        
        ("Nagy zaj\n(zaj=15, alakhiba=0.1, outlier=5)", 
         {"num_points": 100, "radius": 100, "random_noise": 15.0, "shape_error": 0.1, "num_outliers": 5}),
        
        ("Nagy alakhiba\n(zaj=5, alakhiba=0.3, outlier=5)", 
         {"num_points": 100, "radius": 100, "random_noise": 5.0, "shape_error": 0.3, "num_outliers": 5}),
        
        ("Sok outlier\n(zaj=5, alakhiba=0.1, outlier=20)", 
         {"num_points": 100, "radius": 100, "random_noise": 5.0, "shape_error": 0.1, "num_outliers": 20}),
        
        ("Extrém eset\n(zaj=10, alakhiba=0.2, outlier=15)", 
         {"num_points": 100, "radius": 100, "random_noise": 10.0, "shape_error": 0.2, "num_outliers": 15}),
    ]
    
    results = []
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, pg_params) in enumerate(test_configs):
        print(f"  Teszt: {name.replace(chr(10), ' ')}")
        
        # Ponthalmaz generálása
        points = generate_point_cloud(**pg_params)
        
        # Algoritmus futtatása
        start_time = time.time()
        ga = CircleGA(points, **ga_params)
        best_circle, history = ga.run()
        runtime = time.time() - start_time
        
        # Eredmény mentése
        results.append({
            "config": name.replace('\n', ' '),
            "noise": pg_params['random_noise'],
            "shape_error": pg_params['shape_error'],
            "outliers": pg_params['num_outliers'],
            "found_radius": best_circle[2],
            "runtime": runtime
        })
        
        # Vizualizáció
        ax = axes[idx]
        ax.scatter(points[:, 0], points[:, 1], alpha=0.6, edgecolors='k', s=30)
        
        circle = Circle((best_circle[0], best_circle[1]), best_circle[2], 
                        color='red', fill=False, linewidth=2)
        ax.add_patch(circle)
        
        ax.set_title(f"{name}\nr = {best_circle[2]:.1f}, t = {runtime:.2f}s", fontsize=10)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, alpha=0.3)
        
        # Tengelyek beállítása
        margin = 30
        ax.set_xlim(points[:, 0].min() - margin, points[:, 0].max() + margin)
        ax.set_ylim(points[:, 1].min() - margin, points[:, 1].max() + margin)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'parameter_variations.png'), dpi=150)
    plt.close()
    
    # Eredmények táblázat mentése
    df = pd.DataFrame(results)
    df.to_csv(os.path.join(CSV_DIR, 'parameter_variation_results.csv'), index=False)
    
    print("  Kész. Eredmények mentve.")


def main():
    parser = argparse.ArgumentParser(description="Részletes kiértékelő szkript.")
    parser.add_argument('--all', action='store_true', help="Minden teszt futtatása")
    parser.add_argument('--scalability', action='store_true', help="Skálázhatósági teszt")
    parser.add_argument('--mutation', action='store_true', help="Mutációs ráta teszt")
    parser.add_argument('--robustness', action='store_true', help="Robusztusság teszt")
    parser.add_argument('--convergence', action='store_true', help="Konvergencia teszt")
    parser.add_argument('--known-optimum', action='store_true', help="Ismert optimumú tesztesetek")
    parser.add_argument('--iteration-runtime', action='store_true', help="Futási idő vs. iterációszám")
    parser.add_argument('--parameter-variation', action='store_true', help="Paraméter variációk bemutatása")
    
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
    
    if args.all or args.known_optimum:
        run_known_optimum_test()
    
    if args.all or args.iteration_runtime:
        run_iteration_runtime_test()
    
    if args.all or args.parameter_variation:
        run_parameter_variation_test()
    
    print("\n" + "="*50)
    print("Minden kiválasztott teszt sikeresen lefutott!")
    print("="*50)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import argparse
import time
import numpy as np

from point_generator import generate_point_cloud
from genetic_algorithm import CircleGA, visualize_solution

def main():
    """
    A program fő belépési pontja.
    Feldolgozza a parancssori argumentumokat, futtatja a szimulációt és megjeleníti az eredményt.
    """
    parser = argparse.ArgumentParser(description="Genetikus algoritmus futtatása legkisebb befoglaló kör keresésére.")

    # --- Argumentumok a pontgeneráláshoz ---
    pg_group = parser.add_argument_group("Ponthalmaz Generátor Paraméterek")
    pg_group.add_argument('--points', type=int, default=150, help="A generált pontok száma.")
    pg_group.add_argument('--radius', type=float, default=100.0, help="Az alap kör sugara.")
    pg_group.add_argument('--noise', type=float, default=5.0, help="A véletlen zaj mértéke (szórás).")
    pg_group.add_argument('--outliers', type=int, default=8, help="A kiugró pontok száma.")
    pg_group.add_argument('--shape_error', type=float, default=0.1, help="Alakhiba mértéke.")

    # --- Argumentumok a genetikus algoritmushoz ---
    ga_group = parser.add_argument_group("Genetikus Algoritmus Paraméterek")
    ga_group.add_argument('--pop_size', type=int, default=200, help="Populáció mérete.")
    ga_group.add_argument('--generations', type=int, default=300, help="Generációk száma.")
    ga_group.add_argument('--mutation_rate', type=float, default=0.2, help="Mutációs ráta.")
    ga_group.add_argument('--crossover_rate', type=float, default=0.8, help="Keresztezési ráta.")
    
    # --- Egyéb argumentumok ---
    other_group = parser.add_argument_group("Egyéb")
    other_group.add_argument('--no_visualization', action='store_true', help="Ne jelenjen meg a vizualizációs ablak.")
    other_group.add_argument('--save_points_to', type=str, default=None, help="Fájl útvonal, ahova a generált pontok mentésre kerülnek (CSV).")


    args = parser.parse_args()

    print("--- Paraméterek ---")
    print(f"Pontgenerálás: Pontok={args.points}, Sugár={args.radius}, Zaj={args.noise}, Kiugró pontok={args.outliers}")
    print(f"Genetikus Algoritmus: Populáció={args.pop_size}, Generációk={args.generations}, Mutáció={args.mutation_rate}")
    print("-" * 20)

    # 1. Ponthalmaz generálása
    print("1. Ponthalmaz generálása...")
    points = generate_point_cloud(
        num_points=args.points,
        radius=args.radius,
        random_noise=args.noise,
        num_outliers=args.outliers,
        shape_error=args.shape_error
    )
    
    if args.save_points_to:
        np.savetxt(args.save_points_to, points, delimiter=",")
        print(f"Pontok elmentve ide: {args.save_points_to}")

    # 2. Genetikus algoritmus futtatása
    print("2. Genetikus algoritmus futtatása...")
    start_time = time.time()
    
    ga = CircleGA(
        points,
        population_size=args.pop_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate
    )
    best_circle, fitness_history = ga.run()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Az algoritmus futási ideje: {execution_time:.2f} másodperc.")

    # 3. Eredmények kiírása
    print("\n--- Eredmény ---")
    print(f"A legjobb megtalált kör paraméterei:")
    print(f"  Középpont: ({best_circle[0]:.2f}, {best_circle[1]:.2f})")
    print(f"  Sugár: {best_circle[2]:.2f}")

    # 4. Vizualizáció
    if not args.no_visualization:
        print("\n3. Eredmény megjelenítése...")
        visualize_solution(
            points, 
            best_circle, 
            title=f"GA Eredménye ({args.generations} generáció)"
        )

if __name__ == '__main__':
    main()

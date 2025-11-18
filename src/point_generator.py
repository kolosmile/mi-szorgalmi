import numpy as np
import matplotlib.pyplot as plt

def generate_point_cloud(
    center=(0, 0),
    radius=100,
    num_points=100,
    shape_error=0.1,
    random_noise=5.0,
    num_outliers=5,
    outlier_range_factor=1.5
):
    """
    Hibákkal terhelt 2D ponthalmazt generál egy kör alapján.

    Args:
        center (tuple): Az alap kör (x, y) középpontja.
        radius (float): Az alap kör sugara.
        num_points (int): A fő ponthalmazban lévő pontok száma.
        shape_error (float): Alakhiba tényező. 0 esetén tökéletes kör,
                             nagyobb értékek ellipszis-szerűbb alakot eredményeznek.
        random_noise (float): A pontokhoz adott Gauss-zaj szórása.
        num_outliers (int): A generálandó kiugró pontok száma.
        outlier_range_factor (float): Meghatározza, milyen messze lehetnek a kiugró pontok.
                                      A tartomány `radius`-tól `radius * outlier_range_factor`-ig terjed.

    Returns:
        np.ndarray: Egy (num_points + num_outliers, 2) alakú numpy tömb, ami a pontokat tartalmazza.
    """
    cx, cy = center
    
    # 1. Alap pontok generálása egy körön
    angles = np.linspace(0, 2 * np.pi, num_points)
    x_base = cx + radius * np.cos(angles)
    y_base = cy + radius * np.sin(angles)

    # 2. Alakhiba hozzáadása (enyhén ellipszis-szerűvé téve)
    x_distorted = x_base * (1 + np.random.uniform(-shape_error, shape_error))
    y_distorted = y_base * (1 + np.random.uniform(-shape_error, shape_error))

    # 3. Véletlen zaj hozzáadása
    noise_x = np.random.normal(0, random_noise, num_points)
    noise_y = np.random.normal(0, random_noise, num_points)
    x_noisy = x_distorted + noise_x
    y_noisy = y_distorted + noise_y
    
    main_points = np.vstack((x_noisy, y_noisy)).T

    # 4. Kiugró pontok generálása
    outlier_points = np.array([])
    if num_outliers > 0:
        outlier_angles = np.random.uniform(0, 2 * np.pi, num_outliers)
        outlier_radii = np.random.uniform(radius, radius * outlier_range_factor, num_outliers)
        
        outlier_x = cx + outlier_radii * np.cos(outlier_angles)
        outlier_y = cy + outlier_radii * np.sin(outlier_angles)
        outlier_points = np.vstack((outlier_x, outlier_y)).T

    # 5. Fő pontok és kiugró pontok egyesítése
    if outlier_points.any():
        points = np.concatenate([main_points, outlier_points])
    else:
        points = main_points
        
    np.random.shuffle(points) # Pontok megkeverése
    
    return points

def visualize_point_cloud(points, title="Generált ponthalmaz", save_path=None):
    """
    Megjeleníti a ponthalmazt egy pontdiagram segítségével.

    Args:
        points (np.ndarray): A megjelenítendő pontokat tartalmazó tömb.
        title (str): A diagram címe.
        save_path (str, optional): Ha meg van adva, a diagramot elmenti a megadott útvonalra.
    """
    plt.figure(figsize=(8, 8))
    plt.scatter(points[:, 0], points[:, 1], alpha=0.7, edgecolors='k')
    plt.title(title)
    plt.xlabel("X koordináta")
    plt.ylabel("Y koordináta")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path)
        print(f"A diagram elmentve: {save_path}")
        
    plt.show()

if __name__ == '__main__':
    # --- Paraméterek a pontgeneráláshoz ---
    params = {
        "center": (50, 50),
        "radius": 100,
        "num_points": 150,
        "shape_error": 0.15,
        "random_noise": 4.0,
        "num_outliers": 10,
        "outlier_range_factor": 1.8
    }

    # Pontok generálása
    generated_points = generate_point_cloud(**params)
    
    print(f"Legenerált pontok száma: {len(generated_points)}.")
    print("Első 5 pont:\n", generated_points[:5])

    # Pontok megjelenítése
    visualize_point_cloud(
        generated_points,
        title=f"Ponthalmaz (Zaj: {params['random_noise']}, Kiugró pontok: {params['num_outliers']})"
    )

    # Opcionálisan a pontok mentése fájlba későbbi felhasználásra
    # np.savetxt("data/generated_points.csv", generated_points, delimiter=",")
    # print("Pontok elmentve: data/generated_points.csv")

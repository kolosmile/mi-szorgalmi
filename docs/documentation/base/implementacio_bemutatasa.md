# 5. Az implementáció bemutatása

A szoftver Python 3 nyelven készült, moduláris felépítéssel, hogy a különböző funkciók (pontgenerálás, algoritmus, kiértékelés) logikailag elkülönüljenek.

## A projekt struktúrája

A projekt fő mappái és fájljai a következők:

```
.
|-- docs/                 # Dokumentáció és feladatkiírás
|-- src/                  # A Python forráskódok
|   |-- point_generator.py
|   |-- genetic_algorithm.py
|   |-- evaluation.py
|   |-- main.py
|-- venv/                 # Virtuális környezet
|-- .gitignore
|-- requirements.txt      # Projekt függőségek
|-- README.md
```

## `point_generator.py`: A ponthalmaz generátor

Ez a modul felel a tesztadatok, azaz a hibákkal terhelt ponthalmazok létrehozásáért.
*   **`generate_point_cloud(...)`**: A központi függvény, amely a megadott paraméterek (középpont, sugár, pontszám, hibák mértéke) alapján legenerálja és visszaadja a pontokat egy `NumPy` tömbben.
*   **`visualize_point_cloud(...)`**: Egy segédfüggvény, amely a `Matplotlib` segítségével kirajzolja a generált pontokat.

## `genetic_algorithm.py`: A körillesztő algoritmus

Ez a fájl tartalmazza a genetikus algoritmus logikáját egy `CircleGA` nevű osztályba zárva.

*   **`CircleGA.__init__(...)`**: A konstruktor inicializálja az algoritmust a megadott paraméterekkel (populációméret, mutációs ráta stb.), és létrehozza a kezdeti, véletlenszerű körökből álló populációt.
*   **`CircleGA._calculate_fitness()`**: Az algoritmus legfontosabb metódusa. Kiszámítja minden egyes körhöz a fitnesz értéket. A fitnesz a kör sugarából és egy büntetőtagból áll.
    ```python
    # Részlet a fitnesz számításból
    distances = np.sqrt((self.points[:, 0] - cx)**2 + (self.points[:, 1] - cy)**2)
    
    # Büntetés a körön kívül eső pontokért
    outside_points = distances[distances > r]
    penalty = np.sum(outside_points - r) * 10 # A büntetés súlyozása
    
    # A fitnesz a sugár és a büntetés összege
    fitness_scores[i] = r + penalty
    ```
*   **`CircleGA._select()`**, **`_crossover()`**, **`_mutate()`**: Ezek a metódusok valósítják meg a klasszikus evolúciós lépéseket.
*   **`CircleGA.run()`**: A fő ciklus, amely a generációkon keresztül futtatja az evolúciót, és a végén visszaadja a legjobb megtalált kört és a konvergencia-történetet.

## `main.py`: A központi vezérlő szkript

Ez a szkript a program belépési pontja. Összefogja a többi modul működését, és lehetővé teszi a program parancssori futtatását és paraméterezését.
*   **Argumentumok feldolgozása:** Az `argparse` könyvtár segítségével kezeli a parancssori argumentumokat, így a pontgenerálás és a genetikus algoritmus minden fontos paramétere könnyen módosítható futás közben.
*   **Vezérlés:** Meghívja a pontgenerátort, majd az eredményül kapott pontokra ráfuttatja a genetikus algoritmust.
*   **Eredményközlés:** Kiírja a konzolra a futási időt és a megtalált kör paramétereit, majd vizuálisan is megjeleníti az eredményt.

## `evaluation.py`: A kiértékelő modul

Ez a modul az algoritmus teljesítményének részletes, statisztikai alapú elemzésére szolgál. A modul képes automatikusan lefuttatni a különböző teszteket, az eredményeket CSV fájlba menteni, és professzionális grafikonokat generálni a dokumentációhoz.

A modul parancssori argumentumokkal vezérelhető:
*   `--all`: Az összes teszt futtatása.
*   `--scalability`: Skálázhatósági teszt (futási idő és memória a pontszám függvényében).
*   `--mutation`: Mutációs ráta érzékenységvizsgálata.
*   `--robustness`: Robusztusság vizsgálata (outlierek hatása).
*   `--convergence`: Konvergencia vizsgálat.

A modul a `tracemalloc` könyvtárat használja a memóriahasználat mérésére, és a `pandas` segítségével kezeli a mérési adatokat. Az eredmények a `docs/documentation/data` (CSV) és `docs/documentation/images` (PNG) mappákba kerülnek.

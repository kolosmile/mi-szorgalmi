# Kör illesztése adott ponthalmazra - Mesterséges Intelligencia Szorgalmi Feladat

Ez a projekt a Budapesti Műszaki és Gazdaságtudományi Egyetem Gépészmérnöki Karán, a Mesterséges Intelligencia tárgy keretein belül készült szorgalmi feladat megoldását tartalmazza.

**Téma:** Kör illesztése adott ponthalmazra mesterséges intelligencia segítségével.

## A projekt célja

A feladat célja egy olyan algoritmus kifejlesztése, amely egy hibákkal (alakhiba, zaj, kiugró pontok) terhelt ponthalmazra képes a legkisebb befoglaló kört illeszteni. A megoldás egy genetikus algoritmust alkalmaz a probléma optimalizálására.

## Technológiai Stack

*   **Nyelv:** Python 3
*   **Könyvtárak:**
    *   `numpy`: Numerikus műveletekhez és adatszerkezetek kezeléséhez.
    *   `matplotlib`: Az eredmények (ponthalmaz, illesztett kör) vizualizációjához.

## Projekt Struktúra

```
.
├── docs/
│   ├── documentation/      # A szorgalmi feladat dokumentációja
│   └── objective/          # A feladatkiírás eredeti dokumentumai
├── src/
│   ├── point_generator.py  # Modul a hibákkal terhelt ponthalmaz generálásához
│   ├── genetic_algorithm.py # A körillesztő genetikus algoritmus implementációja
│   ├── evaluation.py       # Az algoritmus kiértékeléséért felelős modul
│   └── main.py             # A fő alkalmazás, amely összefogja a folyamatot
├── .gitignore
└── README.md
```

## Használat

### Telepítés

1.  **Klónozza a repository-t:**
    ```bash
    git clone https://github.com/kolosmile/mi-szorgalmi.git
    cd mi-szorgalmi
    ```

2.  **Hozzon létre és aktiváljon egy virtuális környezetet:**
    ```powershell
    # Windows (PowerShell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Telepítse a szükséges csomagokat:**
    ```bash
    pip install -r requirements.txt
    ```

### Fő program futtatása

A `main.py` szkript futtatja a körillesztést egyetlen, véletlenszerűen generált ponthalmazon. A paraméterek a parancssorból módosíthatók.

**Példa futtatásra:**
```bash
# Futtatás alapértelmezett beállításokkal
python src/main.py

# Futtatás egyedi paraméterekkel (több pont, nagyobb zaj)
python src/main.py --points 300 --noise 10 --generations 500
```
A lehetséges argumentumok listájáért futtassa a `python src/main.py --help` parancsot.

### Kiértékelés futtatása

Az `evaluation.py` szkript különböző teszteket futtat az algoritmus teljesítményének elemzésére.

**Példa futtatások:**

1.  **Futási idő vizsgálata a pontok számának függvényében:**
    ```bash
    python src/evaluation.py --test runtime
    ```

2.  **Mutációs ráta hatásának vizsgálata a végeredményre:**
    ```bash
    python src/evaluation.py --test mutation
    ```

3.  **Konvergencia-görbe megjelenítése:**
    ```bash
    python src/evaluation.py --test convergence
    ```

---
*Készítette: Mile Kolos (OXEZ80)*
*Konzulens: Dr. Póka György*
*2025*

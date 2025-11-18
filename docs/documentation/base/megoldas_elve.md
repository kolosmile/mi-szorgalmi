# 4. A megoldás elve, módszere

A probléma megoldására egy Python-alapú szoftveres megoldás készült, amely egy genetikus algoritmust alkalmaz a legkisebb befoglaló kör megkeresésére.

## Technológiai háttér

A projekt az alábbi technológiákra épül:
*   **Nyelv:** Python 3
*   **Könyvtárak:**
    *   `NumPy`: A numerikus számítások (távolságmérés, koordináta-manipuláció) hatékony elvégzéséért felel. Nélkülözhetetlen a nagy mennyiségű pontadat gyors feldolgozásához.
    *   `Matplotlib`: Az adatok és eredmények vizualizációjáért felel. Segítségével ábrázoljuk a generált ponthalmazokat, az illesztett köröket és a kiértékelés során kapott grafikonokat.

## Ponthalmaz generálása hibákkal

A kiindulási adathalmazt egy dedikált modul (`point_generator.py`) hozza létre, amely egy ideális körből indul ki, és szisztematikusan hibákat ad hozzá:
1.  **Alap kör definiálása:** Egy `(x, y)` középpontú, `r` sugarú körön egyenletesen elhelyezünk `N` számú pontot.
2.  **Alakhiba hozzáadása:** A pontok koordinátáit enyhén torzítjuk, ami egy ellipszis-szerű alakot eredményez.
3.  **Véletlen zaj hozzáadása:** Minden pont `x` és `y` koordinátájához egy normális eloszlású véletlen értéket adunk, ami a mérési pontatlanságot szimulálja.
4.  **Kiugró pontok generálása:** A fő ponthalmazon kívül, nagyobb távolságra elhelyezünk néhány pontot, amelyek a durva mérési hibákat reprezentálják.

## A genetikus algoritmus mint megoldási módszer

A legkisebb befoglaló kör egy optimalizálási problémaként fogható fel, amelynek megoldására a genetikus algoritmus (GA) kiválóan alkalmas. A GA az evolúció elveit (szelekció, keresztezés, mutáció) utánozva keresi a legjobb megoldást.

*   **Egyed (Individuum):** Egy lehetséges megoldás, esetünkben egy kör. Minden egyedet három gén ír le: a kör középpontjának `cx` és `cy` koordinátája, valamint `r` sugara. A kromoszóma tehát egy `[cx, cy, r]` számtömb.

*   **Populáció:** Egyedek (körök) egy csoportja, amelyekkel az algoritmus egy adott generációban dolgozik.

*   **Fitneszfüggvény:** Az algoritmus legkritikusabb része. Megmondja, hogy egy adott kör (egyed) mennyire "jó" megoldás. A cél a sugár minimalizálása, miközben az összes pont a körön belül helyezkedik el. A fitnesz értékét a következőképpen számoljuk:
    > `fitnesz = sugár + büntetés`
    *   A **büntetés** értéke nulla, ha az összes pont a körön belül van.
    *   Ha egy vagy több pont a körön kívülre esik, a büntetés arányos a körvonalon kívül eső pontok távolságainak összegével. Ez a büntetőtag "kényszeríti" az algoritmust, hogy olyan köröket részesítsen előnyben, amelyek minden pontot lefednek.

*   **Evolúciós folyamat:**
    1.  **Inicializálás:** Véletlenszerű körökből álló kezdő populáció létrehozása.
    2.  **Szelekció:** A populációból a legjobb fitneszértékkel (legkisebb értékkel) rendelkező egyedek kiválasztása. A jobb egyedek nagyobb eséllyel vesznek részt a szaporodásban.
    3.  **Keresztezés (Crossover):** Két kiválasztott szülőegyed génjeinek (koordináták, sugár) kombinálásával új utódok jönnek létre.
    4.  **Mutáció:** Az utódok génjeit kis, véletlenszerű mértékben módosítjuk. Ez biztosítja a változatosságot és segít elkerülni a lokális optimumokba való beragadást.
    5.  **Ismétlés:** A folyamat a szelekciótól a mutációig ismétlődik egy előre meghatározott generációszámon keresztül.

*   **Leállási feltétel:** Az algoritmus a megadott számú generáció lefutása után leáll, és a legjobb addig talált egyedet (kört) adja vissza megoldásként.

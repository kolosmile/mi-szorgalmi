# Kiértékelési Terv - Kör illesztése genetikus algoritmussal

A feladatkiírás és a követelmények alapján a kiértékelés célja a kifejlesztett genetikus algoritmus teljesítményének, pontosságának és robusztusságának objektív vizsgálata. A korábbi `evaluation.py` szkript hiányosságait pótolva, egy statisztikailag megalapozottabb, több szempontú vizsgálatot tervezünk.

## 1. A kiértékelés módszertana

Mivel a genetikus algoritmusok sztochasztikus (véletlen alapú) működésűek, egyetlen futtatás eredménye nem mérvadó. Minden mérést **többször megismétlünk** (pl. N=10 vagy N=30 alkalommal), és az eredmények **átlagát**, valamint **szórását** vizsgáljuk.

### Mért metrikák
1.  **Futási idő (Runtime):** Az algoritmus indulásától a leállási feltétel teljesüléséig eltelt idő (másodpercben).
2.  **Memóriahasználat (Memory Usage):** A program által lefoglalt maximális memória (Peak Memory) a futás során (MB-ban), `tracemalloc` modul segítségével mérve.
3.  **Megoldás jósága (Fitness/Radius):** A megtalált legkisebb befoglaló kör sugara. (Mivel a feladat a *legkisebb* kör keresése, a kisebb sugár jobb eredményt jelent, feltéve, hogy érvényes a megoldás).
4.  **Reprodukálhatóság (Stability):** A többszöri futtatás eredményeinek szórása. Kicsi szórás esetén az algoritmus stabil.
5.  **Konvergencia sebesség:** Hány generáció szükséges a szuboptimális vagy optimális megoldás eléréséhez.

## 2. Tervezett vizsgálati esetek (Esettanulmányok)

A dokumentáció "tapasztalatok ismertetése" fejezetéhez az alábbi négy fő vizsgálatot végezzük el:

### A. Skálázhatóság vizsgálata (Bemeneti méret hatása)
Azt vizsgáljuk, hogyan növekszik a futási idő és a memóriaigény a pontok számának növelésével.
*   **Változó:** Pontok száma ($N_{points}$).
*   **Értékek:** 50, 100, 500, 1000, 2000, 5000.
*   **Rögzített paraméterek:** Populáció=100, Generációk=100, Mutáció=0.1.
*   **Várt eredmény:** Lineáris vagy polinomiális növekedés.

### B. Algoritmus paramétereinek érzékenységvizsgálata
A genetikus algoritmus belső paramétereinek hatása a megoldás minőségére és a konvergenciára.

#### B1. Mutációs ráta hatása
*   **Változó:** Mutációs ráta ($p_m$).
*   **Értékek:** 0.01, 0.05, 0.1, 0.2, 0.4, 0.6.
*   **Mért érték:** Végső kör sugara (átlag).
*   **Cél:** Megtalálni az "arany középutat" a korai konvergencia (túl kicsi mutáció) és a véletlenszerű keresés (túl nagy mutáció) között.

#### B2. Populációméret hatása
*   **Változó:** Populáció mérete ($P_{size}$).
*   **Értékek:** 20, 50, 100, 200.
*   **Mért érték:** Futási idő vs. elért pontosság.
*   **Kérdés:** Megéri-e növelni a populációt a jobb eredményért, vagy túl nagy a számítási költség?

### C. Robusztusság vizsgálata (Zaj és Outlierek)
Hogyan viselkedik az algoritmus, ha a bemeneti adatok minősége romlik?
*   **Változó:** Outlierek (kiugró pontok) aránya.
*   **Értékek:** 0%, 5%, 10%, 20%.
*   **Megfigyelés:** Mivel a matematikai definíció szerint a befoglaló körnek *minden* pontot tartalmaznia kell, az outlierek drasztikusan növelhetik a sugarat. Azt vizsgáljuk, hogy az algoritmus megtalálja-e ezt a (kényszerűen) nagy kört, vagy "beragad" a sűrű ponthalmaz köré (ami lokális optimum, de nem érvényes megoldás).

### D. Konvergencia és Reprodukálhatóság
*   **Vizsgálat:** Egy adott konfigurációt 30-szor lefuttatunk.
*   **Ábrázolás:**
    *   Konvergencia görbék (legjobb fitnesz a generációk függvényében) egy ábrán (pl. átlagos görbe + szórás sáv).
    *   Boxplot (dobozdiagram) a végső sugarak eloszlásáról.

## 3. Implementációs terv (`evaluation_v2.py`)

Létrehozunk egy új, `evaluation_v2.py` szkriptet, amely:
1.  **Adatgyűjtés:** CSV fájlba menti a nyers mérési adatokat (run_id, n_points, mutation_rate, time, memory, final_radius).
2.  **Memóriamérés:** A `tracemalloc` Python könyvtárat használja.
3.  **Vizualizáció:** Professzionálisabb `matplotlib` diagramokat készít (error bar-ok, boxplotok), és ezeket automatikusan a `docs/documentation/images/` mappába menti, hogy könnyen beilleszthetők legyenek a LaTeX dokumentációba.

## 4. Dokumentációba illesztés
A kapott eredményeket és grafikonokat a "6. Tapasztalatok és kiértékelés" fejezetben fogjuk tárgyalni, külön kitérve a memóriahasználatra, ami a követelményekben kifejezetten szerepelt.

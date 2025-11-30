# Javítási Terv - Konzulensi Visszajelzés Alapján

**Dátum:** 2025. november 30.
**Konzulens:** Dr. Póka György

---

## Visszajelzés Összefoglalása

A konzulens pozitívan értékelte a megoldást ("Nagyon igényes"), de a magasabb pontszám érdekében az alábbi kiegészítéseket javasolta:

---

## Szükséges Javítások

### 1. Konkrét Példák Bemutatása (Dokumentáció Bővítése)

**Feladat:** A dokumentáció végére új szekció hozzáadása konkrét futtatási példákkal.

**Tartalom:**
- [ ] Különböző **alakhiba** értékek hatásának bemutatása (pl. 0.0, 0.1, 0.3)
- [ ] Különböző **zaj** mértékek összehasonlítása (pl. 2.0, 5.0, 15.0)
- [ ] Különböző **kiugró pont** számok vizsgálata (pl. 0, 5, 20)
- [ ] Minden beállításhoz: ábra + számszerű eredmények (megtalált sugár, futási idő)

**Fájlok:**
- `src/evaluation.py` - új tesztfüggvény hozzáadása
- `docs/documentation/dokumentacio.tex` - új szekció: "Példafuttatások"

---

### 2. Ismert Optimumú Teszteset

**Feladat:** Az algoritmus validálása olyan ponthalmazon, ahol az optimális megoldás előre ismert.

**Javaslatok:**
- [ ] **Szabályos sokszög:** pl. szabályos hatszög csúcsai → optimális kör a körülírt kör
- [ ] **Ellipszis:** pontok ellipszisen → optimális kör a nagy féltengellyel megegyező sugarú
- [ ] **Négyzet csúcsai:** 4 pont → optimális kör átmérője = átló

**Megvalósítás:**
- [ ] Új függvény: `generate_regular_polygon(n_vertices, radius)` a `point_generator.py`-ban
- [ ] Összehasonlítás: elméleti vs. megtalált sugár (hibaszázalék)
- [ ] Dokumentálás ábrával és táblázattal

---

### 3. Futási Idő és Iterációszám Kapcsolata

**Feladat:** A futási idő és a generációk/iterációk számának kapcsolatát vizsgálni és dokumentálni.

**Vizsgálandó:**
- [ ] Futási idő a generációszám függvényében (fix pontszám mellett)
- [ ] Lineáris kapcsolat várható → grafikon készítése
- [ ] Iterációnkénti átlagos idő kiszámítása

**Új teszt:**
```python
generations = [50, 100, 200, 300, 500, 1000]
# Mérés minden értékre, grafikon készítése
```

**Dokumentáció:**
- [ ] Új alszekció: "Futási idő és iterációszám kapcsolata"
- [ ] Grafikon + elemzés

---

## Ütemterv

| Prioritás | Feladat | Becsült Idő |
|-----------|---------|-------------|
| 1 | Ismert optimumú teszteset | 1-2 óra |
| 2 | Futási idő vs. iterációszám vizsgálat | 1 óra |
| 3 | Konkrét példák különböző beállításokkal | 2 óra |
| 4 | Dokumentáció frissítése és fordítása | 1 óra |

**Összesen:** ~5-6 óra

---

## Megjegyzések

- A konzulens jelezte, hogy a feladat jelenlegi formájában is "bevehető"
- A javítások a magasabb pontszám érdekében javasoltak
- Érdemes a legfontosabb (ismert optimum) teszttel kezdeni, mert ez validálja az algoritmus helyességét

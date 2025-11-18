# 3. A feladat leírása

## A probléma bemutatása

A feladat egy klasszikus geometriai-optimalizálási probléma modern, mesterséges intelligencia alapú megközelítése. A cél egy adott 2D ponthalmazra a **legkisebb befoglaló kör** (minimum enclosing circle) meghatározása. A kihívást az jelenti, hogy a ponthalmaz nem ideális, hanem valós mérési vagy digitalizálási folyamatokból származó hibákat szimulál, úgymint:

*   **Alakhiba:** A pontok nem egy tökéletes köríven helyezkednek el.
*   **Véletlen zaj:** Minden pont pozíciója egy kis mértékű, véletlenszerű eltolással terhelt.
*   **Kiugró pontok (outlierek):** A ponthalmaz tartalmaz néhány, a fő csoporttól távol eső, hibás mérési eredményt szimuláló pontot.

Az algoritmusnak robusztusnak kell lennie, hogy ezekkel a hibákkal megbirkózzon, és a definíció szerint megtalálja azt a legkisebb sugarú kört, amely a ponthalmaz *összes* elemét tartalmazza.

## Célkitűzések

A projekt során a következő fő célokat kellett elérni:

1.  **Ponthalmaz generálása:** Egy olyan programmodul létrehozása, amely képes paraméterezhető módon, a fent említett hibákkal terhelt ponthalmazokat generálni.
2.  **Algoritmus fejlesztése:** Egy mesterséges intelligencia alapú algoritmus (esetünkben genetikus algoritmus) implementálása, amely a generált ponthalmazra illeszti a legkisebb befoglaló kört.
3.  **Kiértékelés:** A kifejlesztett módszer teljesítményének objektív elemzése. Vizsgálni kell a futási időt a bemeneti adatok méretének függvényében, elemezni kell az algoritmus paramétereinek (pl. mutációs ráta) hatását az eredményre, és vizsgálni kell a megoldás konvergenciáját.
4.  **Dokumentálás:** A teljes folyamat, a módszer és az elért eredmények részletes dokumentálása a követelményeknek megfelelően.

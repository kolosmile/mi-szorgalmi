# 6. Tapasztalatok és kiértékelés

A szoftver fejlesztésének utolsó fázisában egy átfogó teljesítmény- és minőségvizsgálatot végeztünk. A kiértékelés célja annak igazolása volt, hogy a genetikus algoritmus képes megbízhatóan megtalálni a legkisebb befoglaló kört különböző nehézségű bemeneti adatok esetén is, valamint a futási idő és memóriaigény alakulásának feltérképezése.

Mivel a genetikus algoritmusok sztochasztikus (véletlen alapú) működésűek, egyetlen futtatás eredménye nem tekinthető mérvadónak. Ezért a kiértékelés során statisztikai megközelítést alkalmaztunk: minden mérést többször (10-30 alkalommal) megismételtünk, és az eredmények átlagát, valamint szórását vizsgáltuk.

## 6.1. Tesztkörnyezet

A méréseket az alábbi hardver- és szoftverkörnyezetben végeztük:
*   **Operációs rendszer:** Windows 11
*   **Környezet:** Python 3.12
*   **Felhasznált könyvtárak:** `NumPy` (számítások), `Matplotlib` (vizualizáció), `tracemalloc` (memóriamérés).

## 6.2. Skálázhatóság és erőforrásigény

Az első vizsgálat célja annak meghatározása volt, hogyan növekszik a futási idő és a memóriahasználat a bemeneti pontok számának ($N$) növelésével. A teszt során 50 és 5000 közötti pontszámokat vizsgáltunk.

### Futási idő
A futási idő mérése a teljes algoritmus lefutását magában foglalta (populáció inicializálása + generációk futtatása).

![Futási idő a pontok számának függvényében](../images/scalability_runtime.png)

**Elemzés:**
A grafikonon látható, hogy a futási idő a pontok számával közel lineárisan, vagy enyhén polinomiálisan növekszik. Ez kedvező eredmény, mivel azt mutatja, hogy az algoritmus nagyobb adathalmazok (pl. 5000 pont) esetén is kezelhető időn belül (néhány másodperc alatt) eredményt ad. A szórás (hibasávok) viszonylag kicsi, ami stabil futási teljesítményre utal.

### Memóriahasználat
A memóriahasználatot a Python `tracemalloc` moduljával mértük, amely a program futása során lefoglalt maximális memóriát (peak memory) rögzítette.

![Memóriahasználat a pontok számának függvényében](../images/scalability_memory.png)

**Elemzés:**
A memóriahasználat szintén növekvő tendenciát mutat, de abszolút értékben rendkívül alacsony marad (még 5000 pont esetén is 1 MB alatt/körül mozog a többlet memóriaigény). Ez azt bizonyítja, hogy az implementáció memóriahatékony, a `NumPy` tömbök használata optimalizált adattárolást tesz lehetővé.

## 6.3. Paraméterek érzékenységvizsgálata

A genetikus algoritmusok teljesítményét nagyban befolyásolják a beállított hiperparaméterek. Kiemelten vizsgáltuk a **mutációs ráta** hatását, mivel ez felelős a populáció sokszínűségének fenntartásáért és a lokális optimumok elkerüléséért.

![Mutációs ráta hatása](../images/sensitivity_mutation.png)

**Elemzés:**
A mérési eredmények (zöld pontok és hibasávok) alapján a következőket állapíthatjuk meg:
*   **Túl alacsony mutáció (0.01):** Az algoritmus hajlamos korán konvergálni egy lokális optimumba, így a megtalált kör sugara nagyobb (rosszabb), mint az optimális.
*   **Optimális tartomány (0.1 - 0.2):** Ebben a tartományban a legkisebb a megtalált körök sugara. Itt az algoritmus egyensúlyt tart a felfedezés (exploration) és a kiaknázás (exploitation) között.
*   **Túl magas mutáció (> 0.4):** A keresés véletlenszerűvé válik, a jó megoldások "szétesnek" a túlzott változtatások miatt, így az eredmények romlanak és a szórás is megnő.

## 6.4. Robusztusság és outlierek kezelése

A feladatkiírás egyik kritikus pontja a hibás mérések (outlierek) kezelése volt. Mivel a legkisebb befoglaló kör definíció szerint *minden* pontot tartalmaz, egyetlen távoli pont is drasztikusan megnövelheti a szükséges kör sugarát. Azt vizsgáltuk, hogy az algoritmus képes-e alkalmazkodni ehhez, és megtalálja-e a matematikailag helyes (bár nagyobb) kört.

![Outlierek hatása](../images/robustness_outliers.png)

**Elemzés:**
A dobozdiagram (boxplot) mutatja a megtalált kör sugarának eloszlását különböző outlier-számok mellett:
*   **0 outlier:** A sugár kicsi és stabil.
*   **Növekvő outlierek:** Ahogy növeljük a kiugró pontok számát, a kör sugara ugrásszerűen megnő. Ez **helyes működés**, hiszen a körnek tartalmaznia kell ezeket a távoli pontokat is.
*   A dobozok magassága (interkvartilis terjedelem) jelzi, hogy az algoritmus még nehezített körülmények között is viszonylag konzisztens eredményeket ad, bár a szórás természetes módon növekszik a probléma nehézségével.

## 6.5. Konvergencia vizsgálat

Megvizsgáltuk az algoritmus konvergencia-sebességét, azaz hogy hány generáció szükséges a megoldás megtalálásához. Az ábrán 30 futtatás átlagos legjobb fitnesz értéke látható a generációk függvényében.

![Konvergencia görbe](../images/convergence_plot.png)

**Elemzés:**
*   **Gyors kezdeti javulás:** Az első 20-40 generációban a fitnesz érték (sugár) meredeken csökken. Az algoritmus gyorsan megtalálja a pontfelhő "nagyját" lefedő kört.
*   **Finomhangolás:** A 40. generáció után a görbe ellaposodik, de továbbra is finom javulások figyelhetők meg.
*   **Stabilitás:** A kék sáv (szórás) mutatja, hogy bár a véletlen faktor miatt van eltérés az egyes futások között, a konvergencia karaktere minden esetben hasonló. A 100-150. generáció környékére az algoritmus megbízhatóan beáll a globális optimum közelébe.

## 6.6. Validáció ismert optimumú teszteseteken

Az algoritmus pontosságának objektív méréséhez olyan teszteseteket vizsgáltunk, amelyeknél az optimális megoldás matematikailag ismert. Szabályos sokszögek (háromszög, négyzet, hatszög, tízszög) és ellipszisek esetében a legkisebb befoglaló kör sugara analitikusan meghatározható.

![Ismert optimumú tesztesetek](../images/known_optimum_validation.png)

A fenti ábrán hat különböző teszteset látható. A zöld szaggatott vonal az elméleti optimális kört jelöli, míg a piros vonal a genetikus algoritmus által talált megoldást.

![Hibák az optimálishoz képest](../images/known_optimum_errors.png)

**Elemzés:**
*   **Szabályos sokszögek:** A háromszög, hatszög és tízszög esetén az algoritmus 1% alatti hibával találja meg az optimumot. Ez igazolja, hogy a fitnesz-függvény helyesen vezeti a keresést.
*   **Négyzet:** A négyzetnél kissé nagyobb (kb. 2%) a hiba, ami a sarkokon lévő pontok speciális elhelyezkedéséből adódik.
*   **Ellipszisek:** Az ellipszis alakú ponthalmazok nehezebb feladatot jelentenek, mivel a befoglaló kör középpontja nem esik egybe az ellipszis középpontjával. Ennek ellenére az algoritmus itt is 2-3% körüli hibával dolgozik.

Az eredmények azt mutatják, hogy az algoritmus megbízhatóan közelíti az elméleti optimumot még olyan esetekben is, ahol a geometria bonyolultabb.

## 6.7. Futási idő és iterációszám kapcsolata

Megvizsgáltuk, hogyan függ a futási idő a generációk (iterációk) számától. Ez fontos annak megértéséhez, hogy az algoritmus időigénye hogyan skálázódik, és előrejelezhető-e a futási idő.

![Futási idő vs. generációszám](../images/iteration_runtime_analysis.png)

**Elemzés:**
*   **Lineáris kapcsolat:** A bal oldali grafikon mutatja, hogy a futási idő lineárisan függ a generációszámtól. A lineáris illesztés meredeksége körülbelül **2.5 ms/generáció**.
*   **Konstans iterációnkénti idő:** A jobb oldali grafikon igazolja, hogy az egy generációra jutó idő állandó, függetlenül az összes generáció számától. Ez azt jelenti, hogy nincs rejtett többletköltség a hosszabb futtatásoknál.
*   **Tervezhetőség:** Az ismert meredekség alapján a futási idő jól becsülhető: $T \approx 2.5 \cdot G$ milliszekundum, ahol $G$ a generációk száma.

## 6.8. Paraméter variációk hatása konkrét példákon

Az alábbi ábrán hat különböző nehézségű ponthalmazt mutatunk be, amelyeket a pontgenerátor különböző paraméter-beállításaival hoztunk létre. Minden esetben ugyanazokat az algoritmus-paramétereket használtuk (150 egyed, 200 generáció, 0.15 mutációs ráta).

![Paraméter variációk](../images/parameter_variations.png)

**Elemzés:**
*   **Ideális eset (zaj=2, alakhiba=0, outlier=0):** Az algoritmus szinte tökéletesen illeszti a kört a tiszta adatokra (~108 sugár).
*   **Közepes zaj (zaj=5, alakhiba=0.1, outlier=5):** Enyhe romlás, de a kör még mindig jól illeszkedik (~129 sugár).
*   **Nagy zaj (zaj=15):** A nagyobb szórás miatt a körnek nagyobbnak kell lennie (~139 sugár).
*   **Nagy alakhiba (alakhiba=0.3):** Az ellipszis-szerű torzítás miatt a befoglaló kör jelentősen megnő (~140 sugár).
*   **Sok outlier (20 db):** A távoli pontok miatt a körnek az összes pontot le kell fednie (~141 sugár).
*   **Extrém eset:** A kombinált nehézségek esetén a legnagyobb a kör (~145 sugár), de az algoritmus még mindig konvergál.

Ezek a példák szemléletesen mutatják, hogy az algoritmus robusztus a különböző hibatípusokkal szemben, és minden esetben matematikailag helyes megoldást ad (minden pontot lefedő legkisebb kört).

## 6.9. Összegzés

A mérések alapján a kifejlesztett genetikus algoritmus megfelel a követelményeknek:
1.  **Hatékony:** Futási ideje és memóriaigénye alacsony, jól skálázódik.
2.  **Pontos:** Megfelelő paraméterezés (0.1 körüli mutációs ráta) mellett stabilan megtalálja a szuboptimális vagy optimális megoldást.
3.  **Robusztus:** Képes kezelni a zajos adatokat és az outliereket, a matematikai definíciónak megfelelő megoldást szolgáltatva.

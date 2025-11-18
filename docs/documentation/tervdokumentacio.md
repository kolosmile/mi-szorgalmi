# Tervdokumentáció - Kör illesztése adott ponthalmazra

## 1. Címlap

**Mesterséges Intelligencia szorgalmi feladat**
**Kör illesztése adott ponthalmazra 2.**

**Készítette:**
Mile Kolos
Neptun: OXEZ80
E-mail: kolosk5@gmail.com

**Konzulens:**
Dr. Póka György

Budapesti Műszaki és Gazdaságtudományi Egyetem
Gépészmérnöki Kar
Gyártástudomány és technológia Tanszék

**Budapest, 2025. november 18.**

---

## 2. Tartalomjegyzék

1. Címlap
2. Tartalomjegyzék
3. A feladat leírása
4. A megoldás elve, módszere
    4.1. Ponthalmaz generálása
    4.2. Körillesztő algoritmus: Genetikus Algoritmus
    4.3. Értékelési metrika
5. Az implementáció bemutatása
6. Futtatási tapasztalatok és esettanulmányok

---

## 3. A feladat leírása

A projekt célja egy mesterséges intelligencia alapú algoritmus kifejlesztése, amely képes egy adott, hibákkal terhelt ponthalmazra a legkisebb befoglaló kört illeszteni.

A feladat három fő részből áll:
1.  **Ponthalmaz generálása:** Egy ideális körből kiindulva olyan ponthalmazt kell létrehozni, amely valós mérési helyzeteket szimulálva különböző hibákat tartalmaz (alakhibák, véletlen zaj, kiugró pontok).
2.  **Algoritmus fejlesztése:** Egy mesterséges intelligencia módszer (pl. genetikus algoritmus) implementálása, amely a generált ponthalmaz alapján megkeresi a legkisebb sugarú kört, ami az összes pontot tartalmazza.
3.  **Értékelés:** A kifejlesztett algoritmus működésének elemzése és értékelése pontossági, hatékonysági (futási idő, memóriahasználat) és egyéb releváns szempontok szerint.

---

## 4. A megoldás elve, módszere

A probléma megoldását egy Python-alapú szoftvereszközzel tervezzük megvalósítani, amely két fő modulból áll: egy ponthalmaz-generátorból és egy genetikus algoritmust alkalmazó körillesztőből.

### 4.1. Ponthalmaz generálása

A ponthalmazt egy szkript fogja generálni, amely a következő lépéseket hajtja végre:
1.  **Alap kör definiálása:** Megadunk egy bázis kört (középpont `(x, y)` és sugár `r`).
2.  **Pontok generálása:** A körön egyenletesen vagy véletlenszerűen pontokat helyezünk el.
3.  **Hibák hozzáadása:**
    *   **Alakhiba:** A pontokat enyhén torzítjuk, például egy ellipszis mentén, hogy a ponthalmaz ne tökéletes kör legyen.
    *   **Véletlen hiba (zaj):** Minden pont koordinátájához hozzáadunk egy normális eloszlású véletlen értéket.
    *   **Kiugró pontok (outlierek):** Néhány pontot szándékosan a klaszteren kívülre helyezünk, hogy az algoritmus robusztusságát teszteljük.
4.  **Vizualizáció:** A generált pontokat egy diagramon ábrázoljuk a könnyebb ellenőrizhetőség érdekében.

### 4.2. Körillesztő algoritmus: Genetikus Algoritmus

A legkisebb befoglaló kör megkeresésére egy genetikus algoritmust (GA) fogunk használni. A GA egy populációnyi lehetséges megoldással (körrel) dolgozik, és az evolúció elvei alapján iteratívan javítja azokat.

-   **Egyed (kromoszóma):** Egy lehetséges megoldást egy kör ír le, amelyet a középpontjának `(x, y)` koordinátái és `r` sugara határoz meg. A kromoszóma tehát egy `[x, y, r]` számtömb.
-   **Fitneszfüggvény:** Az algoritmus lelke. Egy adott kört (egyedet) értékel aszerint, hogy mennyire jó megoldás. A cél a sugár minimalizálása, miközben az összes pont a körön belül van.
    -   Ha egy kör nem tartalmazza az összes pontot, büntetést kap, amely arányos a körön kívül eső pontok távolságával.
    -   Ha minden pontot tartalmaz, a fitnesz értéke a sugárral lesz arányos (kisebb sugár jobb fitnesz).
-   **Evolúciós lépések:**
    1.  **Kezdeti populáció:** Véletlenszerű körök (egyedek) generálása.
    2.  **Szelekció:** A legjobb fitneszértékkel rendelkező egyedek kiválasztása (pl. rulettkerék-szelekcióval).
    3.  **Keresztezés:** Két szülőegyedből új utódok létrehozása a tulajdonságaik (x, y, r) kombinálásával.
    4.  **Mutáció:** Az utódok tulajdonságainak véletlenszerű, kis mértékű módosítása a diverzitás fenntartása érdekében.
-   **Leállási feltétel:** Az algoritmus egy előre meghatározott generációszám után, vagy ha a legjobb egyed fitnesze már nem javul szignifikánsan, leáll.

### 4.3. Értékelési metrika

Az algoritmus teljesítményét az alábbiak szerint értékeljük:
-   **Pontosság:** Mennyire közelíti meg az algoritmus által talált kör a valódi, analitikusan is meghatározható legkisebb befoglaló kört.
-   **Hatékonyság:** A futási idő és a memóriahasználat mérése a ponthalmaz méretének és a GA paramétereinek (populációméret, generációszám) függvényében.
-   **Robusztusság:** Az algoritmus viselkedésének vizsgálata zajos adatok és kiugró pontok jelenlétében.

---

## 5. Az implementáció bemutatása

A megoldás Python nyelven készül, a következő főbb könyvtárak felhasználásával:
-   `numpy`: Hatékony numerikus műveletekhez és tömbkezeléshez.
-   `matplotlib`: A ponthalmazok és az illesztett körök vizualizációjához.
-   `scipy` / `scikit-learn` (opcionális): Esetlegesen előfeldolgozási vagy optimalizálási lépésekhez.

A kód struktúrája:
-   `point_generator.py`: A hibákkal terhelt ponthalmazok generálásáért felelős modul.
-   `genetic_algorithm.py`: A körillesztő genetikus algoritmus implementációja.
-   `main.py`: A fő szkript, amely összefogja a folyamatot: generálja a pontokat, futtatja az algoritmust, és kiértékeli/megjeleníti az eredményt.
-   `evaluation.py`: Az értékelési metrikákat és az esettanulmányok futtatását végző modul.

---

## 6. Futtatási tapasztalatok és esettanulmányok

Ebben a fejezetben dokumentáljuk a program futtatásának eredményeit.
-   **Esettanulmányok:** Különböző paraméterezésű ponthalmazokon (eltérő pontszám, zajszint, outlier arány) teszteljük az algoritmust.
-   **Paraméterhangolás:** Megvizsgáljuk, hogyan befolyásolja a genetikus algoritmus paramétereinek (populációméret, mutációs ráta, keresztezési stratégia) változtatása az eredmény pontosságát és a konvergencia sebességét.
-   **Eredmények vizualizációja:** Grafikonokon ábrázoljuk a futási időt, a memóriahasználatot és a pontosságot a különböző bemeneti paraméterek függvényében.
-   **Összegzés:** Kiértékeljük a módszer előnyeit, hátrányait és javaslatokat teszünk a lehetséges továbbfejlesztési irányokra.

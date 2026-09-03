# Find Students with Study Spiral Pattern

## Cel zadania
Identyfikacja studentów, którzy konsekwentnie uczą się wielu przedmiotów w obracającym się cyklu (Study Spiral Pattern). Wzorzec wymaga nauki minimum 3 różnych przedmiotów w powtarzającej się sekwencji przez co najmniej 2 pełne cykle (minimum 6 sesji). Dodatkowo analizowane są przerwy między sesjami, które nie mogą przekraczać 2 dni. Wymagane jest również obliczenie długości cyklu oraz zsumowanie całkowitego czasu nauki.

Rozwiązanie zostało zaimplementowane w dwóch technologiach z silnym naciskiem na wydajność, opierając się na rygorystycznej weryfikacji sekwencji i architekturze odpornej na "edge cases".

## Rozwiązanie w PostgreSQL
* **Wczesne filtrowanie (Early pruning):** Zastosowano wczesną klauzulę `HAVING COUNT(*) >= 6 AND COUNT(DISTINCT subject) >= 3` w pierwszym CTE. Pozwala to na drastyczne zmniejszenie wolumenu danych (odrzucenie studentów bez szans na spełnienie warunków) przed przekazaniem ich do kosztownych obliczeniowo funkcji okna.
* **Dynamiczny offset w funkcjach okna:** Zamiast skomplikowanych złączeń typu Self-Join, do weryfikacji sekwencji użyto natywnej funkcji `LAG(subject, cycle_length::INT)`. Zastosowano rzutowanie typu na `INT`, co zapobiega błędom typowania i pozwala na dynamiczne cofanie się w oknie o obliczoną wcześniej, zmienną długość cyklu każdego studenta.
* **Defensywne agregaty logiczne:** Całkowicie zrezygnowano ze skomplikowanej matematyki zliczającej pasujące wiersze na rzecz funkcji `bool_and()`. Szukanie odstępstw od reguły (`subject = prev_subject OR prev_subject IS NULL`) na etapie ewaluacji grup w `HAVING` jest rozwiązaniem wysoce zoptymalizowanym, odpornym na anomalie i wyjątkowo czytelnym z perspektywy *Clean Code*.

## Rozwiązanie w Pandas
* **Method Chaining (Fluent Pandas):** Kod napisany w czystym, deklaratywnym stylu jako jeden nieprzerwany potok transformacji (pipeline) z wykorzystaniem metody `.pipe()`. Wyeliminowano tworzenie zbędnych zmiennych tymczasowych w pamięci RAM.
* **Wektoryzacja zamiast iteracji (Vectorized Self-Join):** Zamiast powolnego nakładania funkcji w pętlach (`.apply()`), symulację funkcji `LAG` ze zmiennym przesunięciem zrealizowano za pomocą złączenia `.merge()` lewostronnego. Użyto wektoryzowanego "celownika" (`rn_shift`), co gwarantuje błyskawiczne wykonanie kodu na wielomilionowych zbiorach danych.
* **Filter early, compute late:** Zastosowano opóźnione wyliczanie identyfikatorów rzędów (`cumcount()`). Funkcje zliczające okna wykonywane są dopiero po odfiltrowaniu całych grup niespełniających kryterium maksymalnej przerwy między sesjami (`~invalid_gap`), co minimalizuje zużycie procesora.
* **Projekcja kolumn (Projection Pushdown / Zero-copy drop):** Zrezygnowano z używania metody `.drop()` wewnątrz łańcucha, co zapobiega zjawisku fragmentacji pamięci i niepotrzebnemu, wielokrotnemu kopiowaniu DataFrame pod maską. Wyboru docelowych kolumn dokonano na samym końcu transformacji.
* **Precyzyjne zarządzanie nazewnictwem i sufiksami:** Zastosowanie `suffixes=('', '_prev')` na etapie `.merge()` gwarantuje bezkolizyjne łączenie tabel z zachowaniem czytelności, bez konieczności ręcznego wywoływania metody `.rename()`.
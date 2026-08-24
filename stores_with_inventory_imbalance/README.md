# 🏬 Stores with Inventory Imbalance

## Cel zadania
Identyfikacja sklepów, w których występuje nierównowaga zapasów (inventory imbalance). Nierównowaga ma miejsce wtedy, gdy ilość najdroższego produktu na stanie jest mniejsza niż ilość produktu najtańszego. Analizie podlegają wyłącznie sklepy posiadające w asortymencie co najmniej 3 różne produkty.

Rozwiązanie zostało zaimplementowane w dwóch technologiach z silnym naciskiem na wydajność, omijając typowe dla tego problemu pułapki wydajnościowe (tzw. "Greatest-N-per-Group problem").

## 🐘 Rozwiązanie w PostgreSQL
* **Single Scan (Funkcje Okna):** Zamiast klasycznego, wielokrotnego skanowania tabeli i łączenia jej samej ze sobą (Self-Join), zastosowano funkcje okna (`FIRST_VALUE` oraz `LAST_VALUE`), co redukuje operacje I/O do jednego przejścia przez tabelę.
* **Optymalizacja Sortowania:** Wszystkie funkcje okna współdzielą identyczną klauzulę `PARTITION BY store_id ORDER BY price DESC`. Dzięki temu optymalizator bazy danych wykonuje kosztowną operację sortowania tylko jeden raz.
* **Niestandardowe Ramki Okna (Window Frames):** Wykorzystano klauzulę `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` dla funkcji `LAST_VALUE`, co pozwoliło na pobranie najtańszego produktu bez konieczności odwracania kierunku sortowania.
* **Optymalizacja Klucza Grupowania:** W końcowym etapie grupowanie (`GROUP BY`) odbywa się wyłącznie po kolumnie typu całkowitoliczbowego (`store_id`). Wartości tekstowe wyciągane są za pomocą funkcji `MAX()`, co znacznie przyspiesza proces haszowania w pamięci.

## 🐼 Rozwiązanie w Pandas
* **Method Chaining:** Kod napisany w czystym, deklaratywnym stylu jako jeden potok transformacji (pipeline), bez tworzenia zbędnych zmiennych pośrednich i modyfikowania ramek w miejscu.
* **Wczesne Filtrowanie (Early Filtering):** Użycie metody `.transform('size')` pozwoliło na obliczenie wielkości asortymentu w locie i odrzucenie sklepów z mniej niż 3 produktami jeszcze przed wykonaniem ciężkiej operacji sortowania.
* **Ominięcie iteracji (Vectorization):** Problem wyciągania pierwszego i ostatniego elementu grupy rozwiązano natywnymi, zoptymalizowanymi w C metodami `.first()` oraz `.last()` wewnątrz bloku agregacji. Całkowicie wyeliminowano potrzebę stosowania wolnych pętli czy funkcji `apply()`.
* **Rozwiązywanie remisów:** Sortowanie wielokolumnowe (`sort_values(by=['store_id', 'price'])`) gwarantuje deterministyczne wyniki i płynnie rozwiązuje problem produktów o tej samej cenie, omijając konieczność budowania skomplikowanej logiki deduplikacji.
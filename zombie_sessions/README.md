# 🧟 Find Zombie Sessions

## Cel zadania
Identyfikacja tzw. "zombie sessions" – sesji użytkowników wykazujących nienaturalne wzorce zachowań. Aby sesja została uznana za anomalię, musi spełniać rygorystyczne kryteria biznesowe: odpowiedni czas trwania, minimalna liczba scrolli, niski współczynnik kliknięć do scrolli oraz całkowity brak zakupów. 

Rozwiązanie zostało zaimplementowane w dwóch technologiach, z naciskiem na optymalizację pod duże zbiory danych (Big Data) i czystość kodu (**Clean Code**).

## 🐘 Rozwiązanie w PostgreSQL
* **Defensywne programowanie:** Ponieważ SQL nie gwarantuje kolejności wykonywania warunków (brak *short-circuitingu* w klauzuli `WHERE`), użyto `NULLIF(scroll_count, 0)`. Całkowicie chroni to kod przed błędem `Division by zero`.
* **Praca z przedziałami czasowymi:** Bezpieczna konwersja kłopotliwego typu `INTERVAL` na uniwersalne liczby zmiennoprzecinkowe przy użyciu `EXTRACT(EPOCH FROM ...)`.
* **Funkcja FILTER:** Wykorzystanie `COUNT(*) FILTER (WHERE ...)` zamiast przestarzałego `SUM(CASE WHEN...)` dla maksymalnej czytelności.
* **Architektura CTE:** Rozbicie logiki na logiczne potoki (pipelines), ułatwiające debugowanie i testowanie.

## 🐍 Rozwiązanie w Pandas
Zastosowano nowoczesną konwencję **Method Chaining** – funkcyjny styl pisania bez tworzenia zbędnych zmiennych pośrednich.
* **Early Filtering (Anti-Join):** Sesje z zakupami zostały odfiltrowane (`query("session_id not in...")`) jeszcze przed kosztowną operacją `groupby`. W środowisku Big Data drastycznie oszczędza to pamięć RAM.
* **Defensywne dzielenie z automatu:** Filtracja wierszy (`scroll_count >= 5`) następuje krok przed blokiem `.assign()`, który liczy wskaźnik konwersji. Dzięki temu naturalnie zapobiegamy błędom matematycznym bez używania `try-except`.
* **Wydajność:** Zastosowano wektoryzowane operacje na datach (`.dt.total_seconds()`) oraz wyłączono domyślne sortowanie podczas grupowania (`sort=False`), odciążając procesor.

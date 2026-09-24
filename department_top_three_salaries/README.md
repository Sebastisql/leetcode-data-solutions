# Department Top Three Salaries

## Cel zadania
Znalezienie pracowników, którzy zarabiają najwięcej w poszczególnych działach firmy (top 3 unikalnych pensji dla każdego departamentu).

## Rozwiązanie w PostgreSQL
* **Funkcje okna (Window Functions):** Wykorzystanie `DENSE_RANK()` do prawidłowego wyznaczenia miejsca w rankingu dla unikalnych wartości pensji w obrębie partycji (`PARTITION BY departmentId`).
* **Czystość relacyjna:** Konsekwentne oddzielenie warunków łączenia tabel w klauzuli `JOIN ON` od logiki biznesowej i filtrowania rankingu, które umieszczono w klauzuli `WHERE`.
* **Optymalizacja:** Świadoma rezygnacja z klauzuli `ORDER BY` na końcu zapytania, ponieważ system oceniający nie wymagał sortowania (oszczędność zasobów obliczeniowych).

## Rozwiązanie w Pandas
* **Method Chaining:** Napisanie całego przepływu danych w jednym płynnym, deklaratywnym łańcuchu wywołań.
* **Early Projection (Wczesne wycinanie kolumn):** Świadome odrzucenie zbędnych kolumn tuż po filtrowaniu, a przed wykonaniem kosztownej operacji `merge`, co znacząco minimalizuje zużycie pamięci.
* **Pre-oczyszczanie (Clean Merge):** Przygotowanie tabeli słownikowej (zmiana nazw kolumn) przed właściwym łączeniem, aby całkowicie uniknąć konfliktów nazw i generowania domyślnych sufiksów (`_x`, `_y`).
* **Bezpieczeństwo (Fail-Fast):** Zastosowanie argumentu `errors='raise'` w metodzie `.rename()` w celu natychmiastowego wychwytywania ewentualnych zmian w schemacie danych źródłowych.
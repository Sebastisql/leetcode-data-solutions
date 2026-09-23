# 🚕 Trips and Users

## Cel zadania
Wyliczenie dziennego wskaźnika anulowań (Cancellation Rate) dla przejazdów. W analizie należy uwzględnić wyłącznie żądania, w których zarówno uczestniczący klient, jak i kierowca posiadają aktywny status (nie są zbanowani w systemie).

Rozwiązanie zostało zaimplementowane w dwóch technologiach z silnym naciskiem na wydajność i czytelność.

## 🐘 Rozwiązanie w PostgreSQL
* **Relacyjne filtrowanie Semi-Join:** Użyto operatora `EXISTS` do niezależnej weryfikacji statusu klienta oraz kierowcy w tabeli `users`. Zapobiega to kosztownemu łączeniu tabel i gwarantuje brak powielania rekordów (duplikacji) wierszy z tabeli głównej.
* **Agregacja warunkowa (Conditional Aggregation):** Zastosowano natywną dla PostgreSQL klauzulę `FILTER` wewnątrz bloku `SELECT`. Zastępuje to zagnieżdżone, wieloliniowe instrukcje `CASE WHEN`, czyniąc kod bardziej idiomatycznym i znacznie czytelniejszym.

## 🐼 Rozwiązanie w Pandas
* **Method Chaining:** Cała logika została zamknięta w pojedynczym, deklaratywnym potoku transformacji danych (data pipeline), co eliminuje konieczność alokowania pamięci na zmienne tymczasowe.
* **Wektoryzacja (Early Filtering):** Klasyczne złączenia (joins) zastąpiono błyskawicznym filtrowaniem przy użyciu metody `.isin()` sprawdzającej przynależność ID do z góry zdefiniowanego wektora aktywnych użytkowników.
* **Matematyczna optymalizacja wskaźnika:** Zrezygnowano z osobnego zliczania sumy anulowań i wielkości grup. Zastosowano wektorową maskę logiczną (`cancel_mask`) przechowującą wartości `True`/`False`. Wykorzystano fakt, że w Pythonie ewaluują one odpowiednio do `1` i `0` – dzięki temu agregacja `.agg(Cancellation_Rate=('cancel_mask', 'mean'))` bezpośrednio i w jednym kroku oblicza prawidłową proporcję.
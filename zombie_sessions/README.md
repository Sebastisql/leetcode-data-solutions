# 🧟 Find Zombie Sessions

## Cel zadania
Identyfikacja tzw. "zombie sessions" – sesji użytkowników w aplikacji, które wykazują nienaturalne wzorce zachowań. Aby sesja została uznana za anomalię, musi spełniać rygorystyczne kryteria biznesowe (czas trwania, liczba scrolli, współczynnik kliknięć do scrolli oraz brak zakupów).

## Przemyślenia architektoniczne i optymalizacja

To rozwiązanie zostało zaprojektowane z myślą o czystości kodu (**Clean Code**) i przewidywaniu skrajnych przypadków (**Defensive Programming**).

### 1. Defensywne programowanie i podział na CTE
Logika została celowo podzielona na dwa kroki za pomocą CTE (Common Table Expressions):
1. Zebranie surowych statystyk i flag (`bool_or`).
2. Wyliczenie metryk biznesowych.

W SQL silnik bazy danych nie gwarantuje kolejności sprawdzania warunków (brak mechanizmu *short-circuiting* w klauzuli `WHERE`). Dlatego do wyliczenia `click_to_scroll_ratio` zastosowano zabezpieczenie w postaci **`NULLIF(scroll_count, 0)`**. Chroni to całkowicie kod przed błędem `Division by zero` w sytuacji, gdy użytkownik przeklikał sesję bez żadnego scrollowania.

### 2. Praca z przedziałami czasowymi w PostgreSQL
Odejmowanie dat (`TIMESTAMP`) w PostgreSQL zwraca typ `INTERVAL`. Jest on wygodny do czytania, ale problematyczny w dalszej obróbce i rzutowaniu w środowiskach zewnętrznych (np. w warstwie aplikacji lub w formacie JSON). 
W rozwiązaniu wykorzystano funkcję **`EXTRACT(EPOCH FROM ...)`**, która w bezpieczny i optymalny sposób transformuje `INTERVAL` na liczbę sekund (`double precision`), pozwalając na łatwe wyliczenie czasu w minutach matematycznym dzieleniem.

### 3. Zastosowanie funkcji FILTER
Zamiast tradycyjnego, przestarzałego i trudnego w czytaniu zapisu `SUM(CASE WHEN...)`, wykorzystano natywną dla PostgreSQL (od wersji 9.4) klauzulę **`FILTER (WHERE ...)`** wewnątrz funkcji agregujących, co znacznie poprawia czytelność kodu i ułatwia wprowadzanie kolejnych warunków biznesowych.
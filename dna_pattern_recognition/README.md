# DNA Pattern Recognition

## Cel zadania
Identyfikacja specyficznych wzorców w sekwencjach DNA (takich jak kodony start/stop oraz powtarzające się motywy) i zwrócenie wyników w postaci flag logicznych (1/0). Rozwiązanie wymagało sprawnego manipulowania ciągami znaków i ekstrahowania z nich konkretnych cech.

## Rozwiązanie w PostgreSQL
* **Zgodność ze standardem (ANSI SQL):** Zastosowano uniwersalną konstrukcję `CASE WHEN` do rzutowania warunków logicznych na wartości całkowite, co gwarantuje przenośność kodu między różnymi silnikami baz danych.
* **Optymalizacja wyszukiwania:** Zamiast wielokrotnego użycia operatora `OR`, do sprawdzania wielu sufiksów naraz wykorzystano konstrukcję `LIKE ANY (ARRAY[...])`. Do weryfikacji prefiksów użyto natywnej, szybkiej funkcji `starts_with()`.

## Rozwiązanie w Pandas
* **Method Chaining:** Kod napisany w deklaratywnym, czystym stylu z wykorzystaniem metody `.assign()`. Pozwala to na wyliczenie i doklejenie nowych kolumn w jednym przepływie (pipeline), bez modyfikowania oryginalnego DataFrame'a w locie.
* **Wektoryzacja i wydajność:** Wykorzystano akcesor `.str` operujący pod spodem na szybkim silniku C. Do sprawdzania końcówek przekazano krotkę (tuple) w `.str.endswith()`. Dodatkowo, w metodach `.str.contains()` świadomie wyłączono silnik wyrażeń regularnych (`regex=False`), co znacząco przyspiesza wyszukiwanie stałych ciągów znaków.
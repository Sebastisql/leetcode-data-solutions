# 🎯 Users with Persistent Behavior Patterns

## Cel zadania
Identyfikacja użytkowników wykazujących stabilne zachowanie (behaviorally stable). Użytkownik uznawany jest za stabilnego, jeśli przez co najmniej 5 kolejnych dni wykonywał dokładnie jedną, tę samą akcję każdego dnia. W przypadku wielu takich sekwencji u jednego użytkownika, pod uwagę brana jest tylko najdłuższa z nich.

Rozwiązanie zostało zaimplementowane w dwóch technologiach z silnym naciskiem na wydajność, opierając się na zaawansowanym wzorcu analitycznym "Gaps and Islands".

## 🐘 Rozwiązanie w PostgreSQL
* **Wczesne filtrowanie (Pre-aggregation):** Zamiast używać kosztownych funkcji okna do zliczania akcji per dzień, zastosowano klasyczne grupowanie `GROUP BY` z klauzulą `HAVING COUNT(*) = 1`. Pozwala to na szybkie odrzucenie "zaburzonych" dni już na początkowym etapie przetwarzania, zmniejszając obciążenie pamięci RAM przed kolejnymi krokami.
* **Wzorzec Gaps and Islands:** Ciągłość dni wyliczana jest za pomocą techniki odejmowania funkcji okna od daty: `action_date - ROW_NUMBER()::INT`. Wynik tej operacji matematycznej generuje niezmienną datę (identyfikator grupy/wyspy) dla dni występujących bezpośrednio po sobie w spójnym ciągu.
* **Optymalizacja wyboru i determinizm:** Zamiast podwójnego sortowania za pomocą funkcji okna dla wyciągnięcia najdłuższego ciągu, użyto natywnej dla PostgreSQL klauzuli `DISTINCT ON (user_id)`. Dodatkowo wprowadzono tie-breaker (`start_date DESC`), co gwarantuje deterministyczne wyniki w przypadku remisów (wybiera najnowszą wyspę).

## 🐼 Rozwiązanie w Pandas
* **Method Chaining:** Kod napisany w czystym, deklaratywnym stylu jako jeden potok transformacji (pipeline), bez tworzenia zbędnych zmiennych tymczasowych. Zastosowanie w bloku `.assign()` sekwencyjnej ewaluacji argumentów ułatwia czytelność logiki.
* **Wydajne filtrowanie natywne w C:** Całkowicie zrezygnowano ze standardowego zliczania w grupach (np. `.transform('size')`) na rzecz metody `.drop_duplicates(keep=False)`. Wykorzystuje ona niskopoziomowe algorytmy oparte na tablicach haszujących (Cython), błyskawicznie odrzucając dni z wieloma akcjami bez konieczności robienia *broadcasting'u*.
* **Early Filtering & Late Casting:** Ciężka dla procesora operacja parsowania stringów na obiekty typu data (`pd.to_datetime()`) wykonywana jest dopiero *po* początkowym odfiltrowaniu nieprawidłowych dni. Oszczędza to zasoby CPU na konwertowaniu danych, które i tak zostałyby usunięte.
* **Kuloodporny odpowiednik ROW_NUMBER:** Zastosowano metodę `.rank(method='first')` na wartościach daty. Gwarantuje to w 100% poprawne działanie algorytmu Gaps & Islands niezależnie od tego, czy ramka wejściowa była domyślnie posortowana, w przeciwieństwie do naiwnych metod zliczania wierszy.
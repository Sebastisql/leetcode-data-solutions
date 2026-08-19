# 🤝 Find Loyal Customers

## Cel zadania
Identyfikacja lojalnych klientów na podstawie historii ich transakcji. Aby klient został uznany za lojalnego, musi spełnić trzy warunki: dokonać co najmniej 3 zakupów, być aktywnym przez co najmniej 30 dni oraz posiadać wskaźnik zwrotów (refund rate) na poziomie poniżej 20%.

Rozwiązanie zostało zaimplementowane w dwóch technologiach z naciskiem na defensywne programowanie i optymalizację matematyczną zapytań.

## 🐘 Rozwiązanie w PostgreSQL
* **Podejście limitowe (Algebraiczne):** Zamiast klasycznego wyliczania ułamka i dzielenia (`Zwroty / Total < 0.2`), zastosowano przekształcenie równania (`Zwroty < 0.2 * Total`). Całkowicie eliminuje to ryzyko błędu "Division by zero" oraz zdejmuje konieczność rzutowania typów (np. `::NUMERIC`).
* **Funkcja FILTER:** Wykorzystanie nowoczesnej klauzuli `COUNT(*) FILTER (WHERE ...)` zgodnie ze standardem ANSI SQL, zastępując archaiczne konstrukcje `SUM(CASE WHEN...)`.
* **Arytmetyka dat:** Bezpośrednie odejmowanie dat (`MAX - MIN`), co natywnie w PostgreSQL zwraca interwał w postaci liczby całkowitej (dni).

## 🐼 Rozwiązanie w Pandas
* **Method Chaining:** Kod napisany w czystym, funkcyjnym stylu jako jeden ciąg transformacji (pipeline), bez tworzenia zbędnych zmiennych pośrednich.
* **Defensywne wyliczanie Total:** Mianownik (`total_count`) jest precyzyjnie definiowany jako suma zakupów i zwrotów (`purchase_count + refund_count`), a nie przez metodę `.size()`. Chroni to logikę biznesową w przypadku pojawienia się w przyszłości nowych statusów transakcji w bazie.
* **Early Filtering:** Odsianie klientów bez wymaganej liczby zakupów na wczesnym etapie, jeszcze przed obliczaniem rozpiętości dni aktywności (`active_days`), co optymalizuje czas wykonania.
* **Brak zbędnych kolumn:** Przekształcenie matematyczne wskaźnika na proste mnożenie pozwoliło użyć go bezpośrednio w klauzuli `.query()`, oszczędzając pamięć RAM (brak konieczności tworzenia dedykowanej kolumny `refund_rate`).
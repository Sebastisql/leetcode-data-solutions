# Find Overbooked Employees

## Cel zadania
Identyfikacja pracowników, którzy są "meeting-heavy" – czyli takich, którzy spędzają więcej niż 50% swojego standardowego czasu pracy (ponad 20 z 40 godzin tygodniowo) na spotkaniach w ciągu dowolnego tygodnia, przez co najmniej 2 tygodnie. Wynik należy posortować malejąco według liczby "ciężkich" tygodni, a następnie rosnąco po imieniu pracownika.

## Rozwiązanie w PostgreSQL
* **Agregacja Tygodniowa (CTE):** Użyto funkcji `date_trunc('week', meeting_date)` w celu pogrupowania spotkań do tygodni zaczynających się w poniedziałek, a następnie zsumowano czas trwania spotkań za pomocą `SUM()` z filtrem `HAVING > 20`.
* **Wielopoziomowe CTE:** Drugie CTE (`heavy_employees`) grupuje dane po pracowniku i zlicza tygodnie spełniające kryterium, odrzucając osoby z wynikiem mniejszym niż 2 (`HAVING COUNT(*) >= 2`).
* **Późne złączenie (Join Late):** Połączenie z tabelą `employees` następuje dopiero na samym końcu, co optymalizuje wydajność zapytania, operując wcześniej na zredukowanym zbiorze danych.
* **Sortowanie:** Wyniki są sortowane wielokolumnowo (`meeting_heavy_weeks DESC`, `employee_name ASC`).

## Rozwiązanie w Pandas
* **Method Chaining:** Kod napisany w czystym, deklaratywnym stylu jako jeden potok transformacji (pipeline), bez tworzenia zbędnych zmiennych pośrednich.
* **Bezpieczne grupowanie czasowe:** Zastosowano `pd.Grouper` z parametrami `freq='W-MON'`, `closed='left'` oraz `label='left'`, co precyzyjnie odwzorowuje tygodnie pracownicze (poniedziałek–niedziela) i eliminuje tzw. "problem północy".
* **Wczesne filtrowanie (Early Filtering):** Odfiltrowanie tygodni z liczbą godzin `<= 20` oraz pracowników z liczbą "ciężkich" tygodni `< 2` następuje przed operacją `.merge()`, co oszczędza pamięć operacyjną.
* **Optymalne łączenie i sortowanie:** Połączenie z DataFrame `employees` wykonano za pomocą `inner join`, a na końcu zastosowano stabilne sortowanie wielokolumnowe metodą `.sort_values()`.
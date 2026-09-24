# 📊 LeetCode Data Solutions

Zbiór zoptymalizowanych rozwiązań zadań z zakresu inżynierii danych i analizy z platformy LeetCode.
Skupiam się tutaj na pisaniu czystego kodu (Clean Code), optymalizacji zapytań oraz wykorzystaniu zaawansowanych technik architektonicznych (CTE, Method Chaining).

## 🚀 Rozwiązane zadania

| Projekt | Technologie | Krótki opis |
| :--- | :--- | :--- |
| [Course Completion Transitions](./course_transitions) | `PostgreSQL`, `Pandas` | Analiza ścieżek kursów, Early Filtering i optymalizacja Window Functions. |
| [Golden Hour Customers](./golden_hour_customers) | `PostgreSQL`, `Pandas` | Identyfikacja kluczowych klientów z użyciem kaskadowych CTE i agregacji warunkowych. |
| [Find Zombie Sessions](./zombie_sessions) | `PostgreSQL`, `Pandas` | Detekcja anomalii i filtrowanie z użyciem agregacji. Defensywne programowanie (`NULLIF`) oraz manipulacja interwałami czasowymi. |
| [Find Loyal Customers](./loyal_customers) | `PostgreSQL`, `Pandas` | Identyfikacja lojalnych klientów. Zastosowanie podejścia limitowego (zamiast wskaźnikowego) do omijania dzielenia przez zero, klauzula `FILTER` oraz precyzyjne łańcuchowanie (Method Chaining). |
| [Stores with Inventory Imbalance](./stores_with_inventory_imbalance) | `PostgreSQL`, `Pandas` | Rozwiązanie problemu Greatest-N-per-Group. Eliminacja Self-Joinów przez zastosowanie funkcji okna (Single Scan, custom Window Frames). W Pandas użyto wczesnego filtrowania (`transform`) i bezpośredniej agregacji skrajnych wartości. |
| [Users with Persistent Behavior Patterns](./users_with_persistent_behavior_patterns) | `PostgreSQL`, `Pandas` | Zastosowanie zaawansowanego wzorca Gaps and Islands. W SQL użyto natywnego `DISTINCT ON` do optymalizacji sortowania. W Pandas zaimplementowano Early Filtering, `rank()` jako kuloodporny ROW_NUMBER oraz błyskawiczne filtrowanie natywne w C (`drop_duplicates(keep=False)`). |
| [Find Students with Study Spiral Pattern](./students_with_study_spiral_pattern) | `PostgreSQL`, `Pandas` | Identyfikacja sekwencji typu Gaps and Islands ze zmiennym offsetem. W SQL użyto dynamicznego `LAG` z rzutowaniem typów oraz defensywnego agregatu `bool_and()`. W Pandas zastosowano wektoryzowany Self-Join z celownikiem `rn_shift` oraz pełny Method Chaining w jednym potoku `pipe()`. |
| [Find Overbooked Employees](./find_overbooked_employees) | `PostgreSQL`, `Pandas` | Identyfikacja przeciążonych pracowników. Optymalizacja zapytań wzorcem "Aggregate Early, Join Late" (zagnieżdżone CTE). W Pandas zastosowano `pd.Grouper` z precyzyjnym domykaniem przedziałów czasowych (`closed='left'`) do wyeliminowania "problemu północy". |
| [DNA Pattern Recognition](./dna_pattern_recognition) | `PostgreSQL`, `Pandas` | Ekstrakcja cech z ciągów tekstowych. W SQL wykorzystano wzorce `LIKE ANY (ARRAY[...])` i `CASE WHEN`, a w Pandas postawiono na wektoryzację (`.str`) z wyłączonym silnikiem regex dla lepszej wydajności. |
| [Trips and Users](./trips_and_users) | `PostgreSQL`, `Pandas` | Obliczanie wskaźnika anulowań (Cancellation Rate) z filtrowaniem relacyjnym. W SQL użyto `EXISTS` (Semi-Join) do walidacji statusów oraz natywnej klauzuli `FILTER`. W Pandas zastosowano wektoryzowane filtrowanie (`.isin`) w pełnym łańcuchu metod (Method Chaining) oraz zoptymalizowano wyliczenie proporcji wykorzystując funkcję `.mean()` bezpośrednio na masce logicznej. |
| [Department Top Three Salaries](./department_top_three_salaries) | `PostgreSQL`, `Pandas` | Identyfikacja najlepiej zarabiających pracowników. W SQL wykorzystano `DENSE_RANK()`. W Pandas zastosowano pełny Method Chaining z wczesnym odcinaniem kolumn (Early Projection) i rygorystycznym przygotowaniem tabel przed złączeniem. |

---
*Repozytorium jest na bieżąco aktualizowane w miarę rozwiązywania kolejnych problemów.*

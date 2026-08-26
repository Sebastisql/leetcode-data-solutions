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

---
*Repozytorium jest na bieżąco aktualizowane w miarę rozwiązywania kolejnych problemów.*
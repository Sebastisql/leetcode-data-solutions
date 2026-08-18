# 🍔 Golden Hour Customers Analysis

This directory contains optimized solutions for identifying top restaurant customers based on their order frequency, timing (peak hours), and satisfaction ratings. Solutions are implemented in **PostgreSQL** and **Python (Pandas)**.

## 🎯 The Challenge

The task was to find "golden hour customers" who consistently order during peak hours and provide high satisfaction.
* **Criteria:**
  * Made at least 3 orders.
  * At least 60% of their orders are during peak hours (11:00-14:00 or 18:00-21:00).
  * Average rating is at least 4.0.
  * Rated at least 50% of their orders.

## 💡 Solution Highlights & Optimizations

### 🐘 PostgreSQL Implementation (`golden_hour_customers.sql`)
* **CTE Cascading (Clean Code):** Used a multi-layered Common Table Expression (CTE) approach to calculate raw metrics first, then derive percentages, adhering to the DRY (Don't Repeat Yourself) principle.
* **Advanced Aggregations:** Utilized native `COUNT(...) FILTER (WHERE ...)` for optimal conditional counting, alongside type casting logic (`AVG(...::int)`) for calculating boolean distributions.
* **Defensive Programming:** Applied `NULLIF()` to prevent potential division-by-zero errors during percentage calculations.

### 🐼 Python / Pandas Implementation (`golden_hour_customers.py`)
* **End-to-End Method Chaining:** The entire transformation logic is wrapped in a single, robust method chain, eliminating intermediate variables and memory leaks.
* **Time-Series Windowing:** Efficiently isolates peak hours using `pd.to_datetime` combined with vectorized `.dt.time.between()` operations.
* **Modern Named Aggregation:** Leverages Pandas' modern `.groupby().agg(new_name=('col', 'func'))` syntax to compute counts, means, and boolean sums cleanly in a single pass.
* **Targeted Transformations:** Uses a highly readable `.query()` string for complex business logic filtering, followed by a dictionary-based `.round()` method to selectively format specific numeric columns.

## 📁 Files in this Repository
* `golden_hour_customers.sql` - The optimized PostgreSQL query.
* `golden_hour_customers.py` - The production-ready Pandas data pipeline.

# leetcode-data-solutions
Zbiór zoptymalizowanych rozwiązań zadań z zakresu inżynierii danych i analizy z platformy LeetCode, napisanych w PostgreSQL oraz Pandas.
# 📊 Course Completion Transitions Analysis

This repository contains highly optimized solutions to a complex data engineering/analytics problem from LeetCode. The solutions are implemented in both **PostgreSQL** and **Python (Pandas)**, demonstrating cross-technology proficiency.

## 🎯 The Challenge
The task was to analyze skill mastery pathways by tracking the sequence of courses completed by top-performing students. 
* **Criteria for top performers:** Completed at least 5 courses with an average rating of 4.0 or higher.
* **Goal:** Identify and count the frequencies of all consecutive course pairs (Course A → Course B) taken by these top students, ranked by popularity.

## 💡 Solution Highlights & Optimizations

Instead of brute-forcing the problem, these solutions focus on **Early Filtering** and **Performance Optimization**—critical skills for working with Big Data.

### 🐘 PostgreSQL Implementation (`course_transitions.sql`)
* **Early Filtering:** Utilized a Semi-Join/CTE approach to identify top students *before* applying expensive Window Functions.
* **Avoided Global Sorting:** Prevented the database from executing heavy `ORDER BY` and `LEAD()` operations on the entire dataset, restricting these calculations strictly to the pre-filtered subset of top performers.
* **Clean Code:** Structured with clear Common Table Expressions (CTEs) for maintainability and readability.

### 🐼 Python / Pandas Implementation (`course_transitions.py`)
* **Method Chaining:** Code is written as a single, clean pipeline using standard Pandas method chaining (no unnecessary intermediate variables or memory leaks).
* **Defensive Programming:** Implemented `.merge(..., validate='one_to_many')` to prevent accidental Cartesian explosions during data joins.
* **Efficient Memory Usage:** Used `as_index=False` and optimized column selection using `.loc` instead of `.filter()` to ensure strict error handling (fail-fast architecture).
* **Dynamic Sorting:** Applied intelligent lambda functions within the `sort_values` key parameter to handle case-insensitive sorting across mixed data types efficiently.

## 📁 Files in this Repository
* `course_transitions.sql` - The optimized PostgreSQL query.
* `course_transitions.py` - The production-ready Pandas data pipeline.

import pandas as pd

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:

    dept_clean = department.rename(columns={'id': 'departmentId', 'name': 'Department'})

    return (
        employee
        .assign(
            SalaryRanking=lambda x: x.groupby('departmentId')['salary'].rank(method='dense', ascending=False)
        )
        .query("SalaryRanking <=3")
        [['name', 'salary', 'departmentId']]
        .merge(dept_clean, on='departmentId', how='inner')
        .rename(columns={'name': 'Employee', 'salary': 'Salary'}, errors='raise')
        [['Department', 'Employee', 'Salary']]
    )
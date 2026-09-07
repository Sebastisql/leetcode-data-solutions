import pandas as pd

def find_overbooked_employees(employees: pd.DataFrame, meetings: pd.DataFrame) -> pd.DataFrame:
    return (
        meetings
        .assign(
            meeting_date=lambda x: pd.to_datetime(x['meeting_date'], errors='coerce'),
        )
        .groupby(['employee_id', pd.Grouper(key='meeting_date', freq='W-MON', closed='left', label='left')], as_index=False)
        .agg(
            total_hours=('duration_hours', 'sum')
        )
        .query("total_hours > 20")
        .groupby('employee_id', as_index=False)
        .agg(
            meeting_heavy_weeks=('total_hours', 'size')
        )
        .query("meeting_heavy_weeks >= 2")
        .merge(employees, on='employee_id', how='inner')
        [['employee_id', 'employee_name', 'department', 'meeting_heavy_weeks']]
        .sort_values(by=['meeting_heavy_weeks', 'employee_name'], ascending=[False, True])
    )
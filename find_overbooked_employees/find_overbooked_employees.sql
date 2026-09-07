with week_stats as (
    select
        employee_id
    from meetings 
    group by 
        employee_id,
        date_trunc('week', meeting_date)
    having sum(duration_hours) > 20
),
heavy_employees as (
    select 
        employee_id,
        count(*) as meeting_heavy_weeks 
    from week_stats
    group by 
        employee_id
    having count(*) >= 2
)
select 
    he.employee_id,
    e.employee_name,
    e.department,
    he.meeting_heavy_weeks 
from heavy_employees he
join employees e on he.employee_id = e.employee_id
order by 
    he.meeting_heavy_weeks desc,
    e.employee_name asc;
with top_students as(
    select 
        user_id
    from course_completions 
    group by user_id
    having 
        avg(course_rating) >=4 
        and count(*) >=5
),
 student_sequences as (
    select
        c.user_id,
        c.course_name      ,
        lead(c.course_name) over (partition by c.user_id order by c.completion_date asc) as second_course    
    from course_completions c
    join top_students t
    on t.user_id = c.user_id
)

select 
    course_name as first_course,
    second_course,
    count(*) as transition_count 
from student_sequences
where second_course is not null
group by 
    course_name, 
    second_course
order by transition_count desc, lower(course_name) asc, lower(second_course)

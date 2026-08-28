WITH student_metrics AS (
    SELECT
        student_id,
        COUNT(DISTINCT subject) AS cycle_length
    FROM study_sessions 
    GROUP BY student_id
    HAVING COUNT(*) >= 6 AND COUNT(DISTINCT subject) >= 3
),
session_analysis AS (
    SELECT
        s.student_id,
        s.session_date,
        sm.cycle_length,
        s.subject,
        s.session_date - LAG(s.session_date) OVER(PARTITION BY s.student_id ORDER BY s.session_date) AS gap_between_session,
        LAG(s.subject, sm.cycle_length::INT) OVER(PARTITION BY s.student_id ORDER BY s.session_date) AS prev_subject,
        SUM(s.hours_studied) OVER(PARTITION BY s.student_id) AS total_study_hours 
    FROM study_sessions s
    JOIN student_metrics sm ON s.student_id = sm.student_id
),
valid_students AS (
    SELECT 
        student_id,
        MAX(cycle_length) AS cycle_length,
        MAX(total_study_hours) AS total_study_hours
    FROM session_analysis
    GROUP BY student_id
    HAVING MAX(gap_between_session) <= 2
       AND bool_and(subject = prev_subject OR prev_subject IS NULL)
)

SELECT 
    v.student_id,
    st.student_name,
    st.major,
    v.cycle_length,
    v.total_study_hours
FROM valid_students v
JOIN students st ON v.student_id = st.student_id
ORDER BY
    v.cycle_length DESC,
    v.total_study_hours DESC;
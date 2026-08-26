WITH valid_daily_actions AS (
    SELECT 
        user_id,
        action_date,
        MAX(action) AS action
    FROM activity
    GROUP BY 
        user_id,
        action_date
    HAVING 
        COUNT(*) = 1
),
islands AS (
    SELECT 
        user_id,
        action_date,
        action,
        action_date - (ROW_NUMBER() OVER(PARTITION BY user_id, action ORDER BY action_date))::INT AS group_id
    FROM valid_daily_actions
),
longest_streaks AS (
    SELECT DISTINCT ON (user_id)
        user_id,
        action,
        COUNT(*) AS streak_length,
        MIN(action_date) AS start_date,
        MAX(action_date) AS end_date
    FROM islands
    GROUP BY 
        user_id, 
        action, 
        group_id
    HAVING 
        COUNT(*) >= 5
    ORDER BY 
        user_id ASC,
        streak_length DESC,
        start_date DESC 
)
SELECT 
    user_id,
    action,
    streak_length,
    start_date,
    end_date
FROM longest_streaks
ORDER BY 
    streak_length DESC,
    user_id ASC;
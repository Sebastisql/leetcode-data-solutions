WITH valid_trips AS (
    SELECT 
        request_at AS "Day",
        1.0 * COUNT(*) FILTER (WHERE status IN ('cancelled_by_driver', 'cancelled_by_client')) / COUNT(*) AS "Cancellation Rate"
    FROM trips t
    WHERE EXISTS (
        SELECT 1 
        FROM users u 
        WHERE t.client_id = u.users_id AND u.banned = 'No'
    )
    AND EXISTS (
        SELECT 1 
        FROM users u 
        WHERE t.driver_id = u.users_id AND u.banned = 'No'
    )
    AND request_at BETWEEN '2013-10-01' AND '2013-10-03'
    GROUP BY request_at
)
SELECT 
    "Day",
    ROUND("Cancellation Rate", 2) AS "Cancellation Rate"
FROM valid_trips;
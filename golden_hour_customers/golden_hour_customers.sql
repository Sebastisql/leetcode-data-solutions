with user_stats AS (
    SELECT 
        customer_id,
        count(*) AS total_orders,
        count(order_rating) AS orders_rating,
        avg(order_rating) AS average_rating,
        count(*) filter (WHERE (order_timestamp::time BETWEEN '11:00:00' AND '14:00:00') 
            OR (order_timestamp::time BETWEEN '18:00:00' AND '21:00:00')) AS peak_hours
    FROM restaurant_orders
    GROUP BY customer_id
),
calculated_metrics AS (
    SELECT
        customer_id,
        total_orders,
        orders_rating::numeric /  NULLIF(total_orders, 0) AS rated_percentage,
        average_rating,
        peak_hours::numeric / NULLIF(total_orders, 0) * 100 AS peak_hour_percentage
    FROM user_stats

)
SELECT 
    customer_id,
    total_orders,
    ROUND(peak_hour_percentage) AS peak_hour_percentage,
    ROUND(average_rating, 2) AS average_rating
FROM calculated_metrics
WHERE 
    total_orders >= 3
    AND peak_hour_percentage >= 60
    AND average_rating >= 4.0
    AND rated_percentage >= 0.5
ORDER BY average_rating DESC, customer_id DESC


SELECT 
    customer_id
FROM customer_transactions 
GROUP BY customer_id
HAVING 
    (MAX(transaction_date) - MIN(transaction_date) >= 30)
    AND (COUNT(*) FILTER(WHERE transaction_type = 'purchase') >= 3)
    AND COUNT(*) FILTER(WHERE transaction_type = 'refund')  < 0.2 * COUNT(*)
ORDER BY customer_id ASC
    


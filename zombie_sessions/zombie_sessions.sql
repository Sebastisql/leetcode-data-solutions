/*
  Find Zombie Sessions
  Podejście: Clean Code & Defensive Programming
  - Użycie CTE dla zwiększenia czytelności (Pipeline logiki).
  - Wykorzystanie FILTER w funkcjach agregujących.
  - Zabezpieczenie przed dzieleniem przez zero za pomocą NULLIF.
  - Bezpieczna konwersja typu INTERVAL za pomocą EXTRACT(EPOCH...).
*/

WITH group_stats AS (
    -- Krok 1: Podstawowa agregacja danych dla każdej sesji
    SELECT
        user_id,
        session_id,
        COUNT(*) FILTER(WHERE event_type = 'scroll') AS scroll_count,
        COUNT(*) FILTER(WHERE event_type = 'click') AS click_count,
        MAX(event_timestamp) AS max_date_session,
        MIN(event_timestamp) AS min_date_session,
        bool_or(event_type = 'purchase') AS purchase_check
    FROM app_events 
    GROUP BY 
        user_id,
        session_id
),
calc_criteria AS (
    -- Krok 2: Wyliczenie wskaźników biznesowych i bezpieczna matematyka
    SELECT 
        session_id,
        user_id,
        scroll_count,
        click_count,
        purchase_check,
        1.0 * EXTRACT(EPOCH FROM (max_date_session - min_date_session)) / 60 AS session_duration_minutes,
        click_count::numeric / NULLIF(scroll_count, 0) AS click_to_scroll_ratio
    FROM group_stats
)

-- Krok 3: Aplikacja końcowych filtrów biznesowych (łatwe do czytania)
SELECT 
    session_id,
    user_id,
    session_duration_minutes,
    scroll_count
FROM calc_criteria
WHERE
    scroll_count >= 5
    AND session_duration_minutes > 30
    AND click_to_scroll_ratio < 0.2
    AND purchase_check IS FALSE
ORDER BY 
    scroll_count DESC,
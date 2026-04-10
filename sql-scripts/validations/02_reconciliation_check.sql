-- Reconciliation check between Bronze and Silver
-- Run this if the marketing team complains about missing orders

/* 
-- OLD VERSION (Too slow for large volumes)
SELECT COUNT(*) FROM bronze_ecommerce_events
UNION ALL
SELECT COUNT(*) FROM silver_orders
*/

-- NEW VERSION: Grouped by day to spot specific gaps
WITH b AS (
    SELECT CAST(event_timestamp AS DATE) as d, count(*) as cnt 
    FROM bronze_ecommerce_events 
    WHERE event_type = 'ORDER_PLACED'
    GROUP BY 1
),
s AS (
    SELECT CAST(event_time AS DATE) as d, count(*) as cnt 
    FROM silver_orders 
    GROUP BY 1
)
SELECT 
    b.d as event_date,
    b.cnt as bronze_count,
    s.cnt as silver_count,
    (b.cnt - s.cnt) as diff
FROM b
LEFT JOIN s ON b.d = s.d
ORDER BY 1 DESC;

-- TODO: Add checks for Payment events once the Silver payment table is stable
-- FIXME: Diff is always > 0 for the current day because of streaming lag. Ignore today's row.

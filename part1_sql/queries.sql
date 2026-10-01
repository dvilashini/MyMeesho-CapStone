-- 1. Monthly revenue by category
.headers on
.mode csv
.output Part1_SQL/output/monthly_category_revenue.csv
SELECT month,
       category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;

-- 2. Region-wise total revenue and order count
.output Part1_SQL/output/region_revenue.csv
SELECT r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region;

-- 3. Top resellers by total spend (>50000)
.output Part1_SQL/output/top_resellers.csv
SELECT r.reseller_id,
       r.reseller_name,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- 4a. Resellers who never placed an order
.output Part1_SQL/output/zero_order_resellers.csv
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- 4b. Demonstrate COUNT(*) vs COUNT(order_id)
.output Part1_SQL/output/zero_order_count_demo.csv
SELECT r.reseller_id,
       COUNT(*) AS count_star,
       COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;

-- 5. Average Order Value (AOV) for June, Delivered only
.output Part1_SQL/output/june_aov.csv
SELECT ROUND(SUM(quantity * unit_price) * 1.0 / COUNT(*), 2) AS june_aov
FROM orders
WHERE month = 'June' AND status = 'Delivered';

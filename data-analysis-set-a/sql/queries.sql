-- SQL dialect: MySQL 8.0.36
-- Run setup.sql first, then this file.
USE delivery_delay_analysis;

-- S2a — Total delay_days by service type
SELECT
    r.service_type,
    SUM(GREATEST(d.actual_days - d.promised_days, 0)) AS total_delay_days
FROM deliveries d
JOIN routes r ON r.route_id = d.route_id
GROUP BY r.service_type
ORDER BY total_delay_days DESC;

-- S2b — Routes with significant delay (summed delay_days > 8)
SELECT
    r.route_id,
    r.route,
    SUM(GREATEST(d.actual_days - d.promised_days, 0)) AS total_delay_days
FROM deliveries d
JOIN routes r ON r.route_id = d.route_id
GROUP BY r.route_id, r.route
HAVING SUM(GREATEST(d.actual_days - d.promised_days, 0)) > 8
ORDER BY total_delay_days DESC, r.route_id ASC;

-- S2c — Top two hubs by summed delay; alphabetical order breaks ties
SELECT
    d.hub,
    SUM(GREATEST(d.actual_days - d.promised_days, 0)) AS total_delay_days
FROM deliveries d
GROUP BY d.hub
ORDER BY total_delay_days DESC, d.hub ASC
LIMIT 2;

-- S3 — Diagnostic: every fact route_id should match a lookup row.
SELECT
    COUNT(*) AS unmatched_route_rows
FROM deliveries d
LEFT JOIN routes r ON r.route_id = d.route_id
WHERE r.route_id IS NULL;

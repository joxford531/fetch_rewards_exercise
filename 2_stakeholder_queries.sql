-- Top 5 brands by the number of distinct occurrences on all receipts for the current month

SELECT b.id, b."name", COUNT(r.id) as brand_receipt_apperances
	FROM Receipts r
	INNER JOIN Receipt_Items ri ON r.id = ri.receipt_id
	INNER JOIN Items i ON i.id = ri.item_id
	INNER JOIN Brands b on b.id = i.brand_id
WHERE DATETIME(ROUND(r.purchase_date / 1000), 'unixepoch') BETWEEN date('now', '-1 month', 'start of month') AND date('now')
GROUP BY b.id
ORDER BY brand_receipt_apperances DESC
LIMIT 5;


-- Top 5 Brands by the number of distinct occurrences for the current month and the previous month

WITH best_brands_previous_month AS (
	SELECT b.id
		FROM Receipts r
		INNER JOIN Receipt_Items ri ON r.id = ri.receipt_id
		INNER JOIN Items i ON i.id = ri.item_id
		INNER JOIN Brands b on b.id = i.brand_id
	WHERE DATETIME(ROUND(r.purchase_date / 1000), 'unixepoch') BETWEEN date('now', '-1 month', 'start of month') AND date('now')
	GROUP BY b.id
	ORDER BY COUNT(r.id) DESC
	LIMIT 5
)
SELECT b.id, b."name", strftime( "%Y-%m", DATETIME(ROUND(r.purchase_date / 1000), 'unixepoch') ) as receipt_month, 
COUNT(r.id) as brand_receipt_apperances
	FROM Receipts r
	INNER JOIN Receipt_Items ri ON r.id = ri.receipt_id
	INNER JOIN Items i ON i.id = ri.item_id
	INNER JOIN Brands b on b.id = i.brand_id
WHERE DATETIME(ROUND(r.purchase_date / 1000), 'unixepoch') BETWEEN date('now', '-2 month', 'start of month') AND date('now')
AND b.id IN (
	SELECT * FROM best_brands_previous_month		
)
GROUP BY b.id, receipt_month;


-- Average price by status for all items in each Receipt

SELECT AVG(CAST(ri.final_price as DECIMAL)) AS Total_Spent, rs.status FROM Receipts r
	INNER JOIN Receipt_Items ri ON ri.receipt_id = r.id
	INNER JOIN Receipt_Statuses rs ON rs.id = r.rewards_receipt_status_id
GROUP BY rs.status;


-- Total spent on Brand by Users created in the past six months

SELECT b.id, b.name, SUM(CAST(ri.final_price AS DECIMAL)) as total_user_brand_spend
	FROM Receipts r
	INNER JOIN Users u ON u.id = r.user_id
	INNER JOIN Receipt_Items ri ON r.id = ri.receipt_id
	INNER JOIN Items i ON i.id = ri.item_id
	INNER JOIN Brands b on b.id = i.brand_id
WHERE DATETIME(ROUND(u.created_date / 1000), 'unixepoch') BETWEEN date('now', '-6 month', 'start of month') AND date('now')
GROUP BY b.id
ORDER BY total_user_brand_spend DESC;


-- Total transactions for Brand by Users created in the past six months

SELECT b.id, b.name, COUNT(r.id) as total_brand_transactions
	FROM Receipts r
	INNER JOIN Users u ON u.id = r.user_id
	INNER JOIN Receipt_Items ri ON r.id = ri.receipt_id
	INNER JOIN Items i ON i.id = ri.item_id
	INNER JOIN Brands b on b.id = i.brand_id
WHERE DATETIME(ROUND(u.created_date / 1000), 'unixepoch') BETWEEN date('now', '-6 month', 'start of month') AND date('now')
GROUP BY b.id
ORDER BY total_brand_transactions DESC;
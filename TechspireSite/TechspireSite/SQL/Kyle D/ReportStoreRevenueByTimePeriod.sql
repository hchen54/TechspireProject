-- Kyle Dela Pena
--Store Revenue within a given time frame
-- The report is useful when the client wants to know which time period gives her the most revenue. Using that information, she can plan production and pricing accordingly to take advantage of the most profitable time windows. She can also limit production on days where anticipated revenue is low so that products and materials are not wasted. The client can also compare revenue between different periods, then apply her business strategies from profitable periods to mediocre or low business periods.
-- Calculates total revenue and average revenue per order in a given time period for a given store.
-- Time Period, Store Name, Total Orders, Products Sold, Total Revenue, Avg Revenue Per Order
-- null,null,right,right,right,right

DECLARE @store_id VARCHAR(12) = 1
DECLARE @start_date VARCHAR(12) = '2018-08-01'
DECLARE @end_date VARCHAR(12) = '2018-08-31'

SELECT DISTINCT @start_date + ' - '+ @end_date AS 'Time Period',
	(SELECT store_name FROM Store WHERE id = @store_id) AS 'Store Name',
	(SELECT COUNT("Order".id) AS 'Order Count'
	FROM "Order"
	INNER JOIN Store ON Store.id = "Order".store_id
	WHERE Store.id = @store_id
	AND "Order".order_date >= @start_date AND "Order".order_date <= @end_date) AS 'Total Orders',
	(SELECT SUM(OrderLine.quantity) AS 'Product Count'
	FROM OrderLine
	INNER JOIN "Order" ON "Order".id = OrderLine.order_id
	INNER JOIN Store ON Store.id = "Order".store_id
	WHERE Store.id = @store_id
	AND "Order".order_date >= @start_date AND "Order".order_date <= @end_date) AS 'Products Sold',
	(SELECT FORMAT(SUM(OrderLine.total_price),'c') AS 'OL Total Price'
	FROM "Order"
	INNER JOIN Store ON Store.id = "Order".store_id
	INNER JOIN OrderLine ON OrderLine.order_id = "Order".id
	INNER JOIN Product ON OrderLine.product_id = Product.id
	WHERE Store.id = @store_id
	AND "Order".order_date >= @start_date AND "Order".order_date <= @end_date) AS 'Total Revenue',
	(SELECT FORMAT((SUM("Order".final_total) / COUNT("Order".id)),'c') AS 'Avg Revenue Per Order'
	FROM "Order"
	INNER JOIN Store ON Store.id = "Order".store_id
	WHERE Store.id = @store_id
	AND "Order".order_date >= @start_date AND "Order".order_date <= @end_date) AS 'Avg Revenue Per Order'

FROM OrderLine
INNER JOIN "Order" ON "Order".id = OrderLine.order_id
INNER JOIN Store ON Store.id = "Order".store_id
INNER JOIN Product ON OrderLine.product_id = Product.id




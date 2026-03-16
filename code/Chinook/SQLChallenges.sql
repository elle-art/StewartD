-- Active: 1773160310343@@127.0.0.1@5432@chinook_pg
-- Parking Lot*******
-- *                *
-- *                *
--- *****************

-- SETUP:
-- Connect to the server (Azure Data Studio / Database extension/psql)
-- Create a database (I recommend chinook_pg)
-- Execute the Chinook database (from the Chinook_pg.sql file) to create Chinook resources in your server (I recommend doing this from psql)

-- Comment can be done single line with --
-- Comment can be done multi line with /* */

/*
DQL - Data Query Language
Keywords:

SELECT - retrieve data, select the columns from the resulting set
FROM - the table(s) to retrieve data from
WHERE - a conditional filter of the data
GROUP BY - group the data based on one or more columns
HAVING - a conditional filter of the grouped data
ORDER BY - sort the data
*/
--CREATE DATABASE chinook_pg;

SELECT * FROM actor;
SELECT last_name FROM actor;
SELECT * FROM actor WHERE first_name = 'Morgan';
select * from actor where first_name = 'John';

-- BASIC CHALLENGES
-- List all customers (full name, customer id, and country) who are not in the USA
SELECT first_name || ' ' || last_name AS full_name, customer_id, country FROM customer WHERE NOT country = 'USA';

-- List all customers from Brazil
SELECT first_name || ' ' || last_name AS full_name, customer_id, country FROM customer WHERE country = 'Brazil';

-- List all sales agents
SELECT first_name || ' ' || last_name AS full_name, employee_id, title, phone, email 
FROM employee 
WHERE title = 'Sales Support Agent';


-- Retrieve a list of all countries in billing addresses on invoices
SELECT DISTINCT billing_country FROM invoice ORDER BY billing_country ASC; 

-- Retrieve how many invoices there were in 2009, and what was the sales total for that year?
SELECT COUNT(invoice_id) as total_invoices, SUM(total) as total_sales FROM invoice WHERE EXTRACT(YEAR FROM invoice_date) = 2009;

-- (challenge: find the invoice count sales total for every year using one query)
SELECT COUNT(invoice_id) as total_invoices, SUM(total) as total_sales, EXTRACT(YEAR FROM invoice_date) as "year"
FROM invoice GROUP BY "year" ORDER BY "year" ASC;


-- how many line items were there for invoice #37
SELECT COUNT(*), invoice_id 
FROM invoice_line 
WHERE invoice_id = 37 GROUP BY invoice_id;

-- how many invoices per country? BillingCountry  # of invoices -
-- Retrieve the total sales per country, ordered by the highest total sales first.
SELECT COUNT(*) as total_invoices, SUM(total) as total_sales, billing_country 
FROM invoice
GROUP BY billing_country
ORDER BY total_sales DESC;


-- JOINS CHALLENGES
-- Every Album by Artist
SELECT * FROM album al
JOIN artist ar
ON al.artist_id = ar.artist_id;

-- (inner keyword is optional for inner join)
-- All songs of the rock genre
SELECT * FROM track 
JOIN genre 
ON track.genre_id = genre.genre_id 
WHERE genre.name = 'Rock';

-- Show all invoices of customers from brazil (mailing address not billing)
SELECT invoice.invoice_id, invoice.invoice_date, invoice.total, customer.country FROM customer 
JOIN invoice ON customer.customer_id = invoice.customer_id
WHERE customer.country = 'Brazil';


-- Show all invoices together with the name of the sales agent for each one
SELECT invoice.invoice_id, invoice.invoice_date, invoice.total, employee.first_name, employee.last_name 
FROM customer
JOIN invoice ON customer.customer_id = invoice.customer_id
JOIN employee ON customer.support_rep_id = employee.employee_id;

-- Which sales agent made the most sales in 2009?
SELECT EXTRACT(YEAR FROM invoice_date) as "year", e.employee_id, e.first_name, e.last_name, SUM(i.total) as total_sales 
FROM employee e
JOIN customer c on e.employee_id = c.support_rep_id
JOIN invoice i on c.customer_id = i.customer_id
WHERE EXTRACT(YEAR FROM invoice_date) = 2009
GROUP BY EXTRACT(YEAR FROM invoice_date), e.employee_id
ORDER BY total_sales DESC LIMIT 1;


-- How many customers are assigned to each sales agent?
SELECT COUNT(*) as total_customers, e.employee_id, e.first_name, e.last_name
FROM employee e
JOIN customer c on e.employee_id = c.support_rep_id
GROUP BY e.employee_id;

-- Which track was purchased the most in 2010?
SELECT track.name, SUM(invoice_line.quantity) AS total_sold
FROM track
JOIN invoice_line on track.track_id = invoice_line.track_id
JOIN invoice ON invoice.invoice_id = invoice_line.invoice_id
WHERE EXTRACT(YEAR FROM invoice.invoice_date) = 2010
GROUP BY track.name
ORDER BY SUM(invoice_line.quantity) DESC, track.name ASC
LIMIT 1;

-- Show the top three best selling artists.
SELECT ar.name, SUM(invoice_line.quantity) AS total_sold
FROM track
JOIN invoice_line on track.track_id = invoice_line.track_id
JOIN album al on al.album_id = track.album_id
JOIN artist ar on al.artist_id = ar.artist_id
JOIN invoice ON invoice.invoice_id = invoice_line.invoice_id
GROUP BY ar.name
ORDER BY SUM(invoice_line.quantity) DESC
LIMIT 3;

-- Which customers have the same initials as at least one other customer?
SELECT c1.customer_id, c1.first_name, c1.last_name, left(c1.first_name, 1) || left(c1.last_name, 1) as initials, 
    c2.first_name, c2.last_name, c2.customer_id
FROM customer c1
JOIN customer c2 
ON left(c1.first_name, 1) || left(c1.last_name, 1) = left(c2.first_name, 1) || left(c2.last_name, 1) 
AND c2.customer_id != c1.customer_id;

-- Which countries have the most invoices?
SELECT billing_country, COUNT(*) as total_invoices
FROM invoice
GROUP BY billing_country
ORDER BY total_invoices DESC;

-- Which city has the customer with the highest sales total?
SELECT c.customer_id, c.city, SUM(i.total) as total_sales
FROM invoice i
JOIN customer c ON c.customer_id = i.customer_id
GROUP BY c.customer_id
ORDER BY total_sales DESC
LIMIT 1;

-- Who is the highest spending customer?
SELECT c.customer_id, c.first_name, c.last_name, SUM(i.total) as total_sales
FROM invoice i
JOIN customer c ON c.customer_id = i.customer_id
GROUP BY c.customer_id
ORDER BY total_sales DESC
LIMIT 1;

-- Return the email and full name of of all customers who listen to Rock.
SELECT c.first_name || ' ' || c.last_name as full_name, c.email, g.name
FROM customer c
JOIN invoice i on i.customer_id = c.customer_id
JOIN invoice_line l on l.invoice_id = i.invoice_id
JOIN track t on t.track_id = l.track_id
JOIN genre g on g.genre_id = t.genre_id
WHERE g.name = 'Rock';

-- Which artist has written the most Rock songs?
SELECT ar.name, COUNT(*) as total_songs, g.name
FROM track t
JOIN genre g on g.genre_id = t.genre_id
JOIN album al on al.album_id = t.album_id
JOIN artist ar on ar.artist_id = al.artist_id
WHERE g.name = 'Rock'
GROUP BY g.name, ar.artist_id
ORDER BY total_songs DESC
LIMIT 1;

-- Which artist has generated the most revenue?
SELECT ar.name, SUM(l.unit_price * l.quantity) as total_sales
FROM track t
JOIN album al on al.album_id = t.album_id
JOIN artist ar on ar.artist_id = al.artist_id
JOIN invoice_line l on l.track_id = t.track_id
GROUP BY ar.artist_id
ORDER BY total_sales DESC
LIMIT 1;


-- ADVANCED CHALLENGES
-- solve these with a mixture of joins, subqueries, CTE, and set operators.
-- solve at least one of them in two different ways, and see if the execution
-- plan for them is the same, or different.

-- 1. which artists did not make any albums at all?
SELECT * 
FROM artist ar
LEFT JOIN album al ON al.artist_id = ar.artist_id
WHERE al.artist_id IS NULL;

-- 2. which artists did not record any tracks of the Latin genre?
SELECT ar.name
FROM artist ar
JOIN album al ON al.artist_id = ar.artist_id
JOIN track t ON t.album_id = al.album_id
JOIN genre g ON g.genre_id = t.genre_id
WHERE g.name != 'Latin'
GROUP BY ar.name;

-- 3. which video track has the longest length? (use media type table)
SELECT t.name, t.milliseconds, m.name
FROM track t
JOIN media_type m on m.media_type_id = t.media_type_id
WHERE m.name LIKE '%video%'
ORDER BY t.milliseconds DESC
LIMIT 1;

-- 4. boss employee (the one who reports to nobody)
SELECT *
FROM employee
WHERE reports_to IS NULL;

-- 5. how many audio tracks were bought by German customers, and what was
--    the total price paid for them?
SELECT c.country, COUNT(c.customer_id) as total_customers,  SUM(l.unit_price * l.quantity) as total_sales
FROM track t
JOIN invoice_line l ON l.track_id = t.track_id
JOIN invoice i ON i.invoice_id = l.invoice_id
JOIN customer c ON c.customer_id = i.invoice_id
WHERE c.country = 'Germany'
GROUP BY c.country;

-- 6. list the names and countries of the customers supported by an employee
--    who was hired younger than 35.
SELECT c.first_name || ' ' || c.last_name as full_name, c.country, 
e.employee_id, (extract(YEAR FROM e.hire_date) - extract(YEAR FROM e.birth_date)) as employee_age
FROM customer c
JOIN employee e ON e.employee_id = c.support_rep_id
WHERE extract(YEAR FROM e.hire_date) - extract(YEAR FROM e.birth_date) < 35;

-- DML exercises

-- 1. insert two new records into the employee table.
INSERT INTO employee (first_name, last_name, birth_date, hire_date, 
"address", city, "state", country, postal_code, phone, email)
VALUES
('Bob', 'Joe', '2003-04-12'::date::timestamp, CURRENT_DATE, '123 Sesame St', 
'New York', 'NY', 'USA', '60664', '+1 (123) 654-8525', 'bobjoe@revature.com'),
('Billy', 'Bob', '1998-08-22'::date::timestamp, CURRENT_DATE, '123 Sesame St', 
'New York', 'NY', 'USA', '60664', '+1 (123) 654-8525', 'billybob@revature.com');
SELECT * FROM employee WHERE hire_date = CURRENT_DATE;
UPDATE employee 
SET title = 'trainee', reports_to = 7  
WHERE employee_id IN (9, 10);

-- 2. insert two new records into the tracks table.
INSERT INTO track (name, album_id, media_type_id, genre_id, composer, milliseconds, bytes, unit_price)
VALUES
('So This is Love', 4, 2, 3, 'A person', 684245, 65412358, 0.47),
('Yeah', 2, 1, 1, 'Usher', 214741, 55214784, 0.47);
SELECT * FROM track WHERE unit_price = 0.47;

-- 3. update customer Aaron Mitchell's name to Robert Walter
UPDATE customer 
SET first_name = 'Robert', last_name = 'Walter'
WHERE first_name = 'Aaron' AND last_name = 'Mitchell';

SELECT * FROM customer WHERE first_name = 'Robert' AND last_name = 'Walter';

-- 4. delete one of the employees you inserted.
DELETE FROM employee WHERE employee_id = 9;
SELECT * FROM employee WHERE hire_date = CURRENT_DATE;

-- 5. delete customer Robert Walter.
ALTER TABLE invoice_line
DROP CONSTRAINT fk_invoice_line_invoice_id;

ALTER TABLE invoice_line
ADD CONSTRAINT fk_invoice_line_invoice_id
FOREIGN KEY (invoice_id)
REFERENCES invoice(invoice_id)
ON DELETE CASCADE;

ALTER TABLE invoice
DROP CONSTRAINT fk_invoice_customer_id;

ALTER TABLE invoice
ADD CONSTRAINT fk_invoice_customer_id
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id)
ON DELETE CASCADE;

DELETE FROM customer WHERE customer_id = 32;
SELECT * FROM customer WHERE first_name = 'Robert' AND last_name = 'Walter';

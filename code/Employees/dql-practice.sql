### Basic Queries
--List all employees ordered by salary (highest first)
SELECT * FROM employees ORDER BY salary DESC;

-- **Query 3.2:** Find all employees in the Engineering department
SELECT * FROM employees WHERE dept_id=1;

--**Query 3.3:** List employees hired in 2021 or later
SELECT * FROM employees WHERE hire_date > '2020-12-31';

### Filtering and Operators
--**Query 3.4:** Find employees with salary between 60000 and 80000
SELECT * FROM employees WHERE salary BETWEEN 60000 AND 80000;

--**Query 3.5:** Find employees whose email contains 'company'
SELECT * FROM employees WHERE email LIKE '%company%';

--**Query 3.6:** List departments in Buildings A or B
SELECT * FROM departments WHERE "location"='Building A' OR "location"='Building B';

### Aggregate Functions

--**Query 3.7:** Calculate the total salary expense per department
SELECT departments.dept_id, departments.dept_name, SUM(employees.salary) AS total_salary_expense 
FROM employees JOIN departments ON departments.dept_id=employees.dept_id
GROUP BY departments.dept_id, dept_name;

--**Query 3.8:** Find the average, minimum, and maximum salary
SELECT AVG(salary), MIN(salary), MAX(salary) FROM employees;

-- **Query 3.9:** Count employees in each department, only show departments with 2+ employees
SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING COUNT(*) > 2;

### Aliases and Formatting

--**Query 3.10:** Create a report showing full name (first + last), department name, and formatted salary
SELECT 
    e.first_name || ' ' || e.last_name AS full_name,
    d.dept_name,
    TO_CHAR(e.salary, 'FM$999,999,999.00') AS formatted_salary
FROM employees e
JOIN departments d 
    ON e.dept_id = d.dept_id
ORDER BY full_name;
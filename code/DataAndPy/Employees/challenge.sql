### Challenge 4.1
--Find employees who earn more than the average salary.
SELECT * 
FROM employees 
WHERE salary > (
    SELECT AVG(salary) FROM employees);

### Challenge 4.2
--List departments that have at least one project.
SELECT d.dept_id, d.dept_name, COUNT(p.project_id) AS project_count FROM projects as "p" JOIN departments as d ON p.dept_id=d.dept_id GROUP BY d.dept_id HAVING COUNT(p.project_id) > 0;

### Challenge 4.3
--Find the employee with the highest salary in each department.


### Challenge 4.4
--Calculate how long each employee has been with the company (in years and months).
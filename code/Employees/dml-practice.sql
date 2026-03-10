INSERT INTO employees (first_name, last_name, email, salary)
VALUES
('Grace', 'Lee', 'grace.lee@company.com', 58000),
('Ivan', 'Chen', 'ivan@company.com', 61000),
('Julia', 'Kim', 'julia@company.com', 55000);

### Task 2.2: UPDATE Operations
UPDATE employees 
SET salary = salary * 1.1
WHERE dept_id = 1;

UPDATE employees SET email = 'bob.smith@company.com' WHERE emp_id = 2;

### Task 2.3: DELETE Operations

DELETE FROM projects WHERE end_date < CURRENT_DATE;

-- **CAREFUL!** Write (but don't run) a DELETE that would remove all employees without a department. What makes this dangerous?
-- DELETE FROM employees WHERE dept_id IS NULL;
-- Explain why this could be dangerous: There are multiple reasons data could be assigned null. For example, an employee exists, but their department isn't assigned yet.


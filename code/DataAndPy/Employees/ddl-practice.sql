### Task 1.1: Add a Column
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

### Task 1.2: Modify a Column
ALTER TABLE departments ALTER COLUMN budget TYPE DECIMAL(15, 2);

### Task 1.3: Create a New Table
CREATE TABLE training_courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    duration_hours INTEGER,
    instructor VARCHAR(100)
);

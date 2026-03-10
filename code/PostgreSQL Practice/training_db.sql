CREATE DATABASE training_db;

CREATE TABLE associates (
    associate_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hire_date DATE DEFAULT CURRENT_DATE
);

-- DROP TABLE associates;

INSERT INTO associates 
(first_name, last_name, email, hire_date)
VALUES 
('Bob', 'TheBuilder', 'bob@bob.com', '2026-02-23'),
('Billy', 'Bob', 'billybob@bob.com', DEFAULT);

ALTER TABLE associates ADD COLUMN department VARCHAR(50);
ALTER Table associates ALTER COLUMN hire_date SET NOT NULL;
ALTER TABLE associates ALTER COLUMN email TYPE VARCHAR(115);

SELECT * FROM associates;

UPDATE associates SET department = 'Training' WHERE associate_id=1;

UPDATE associates SET department = 'Training';
ALTER Table associates ALTER COLUMN department SET NOT NULL;

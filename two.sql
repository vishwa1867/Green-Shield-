create database two;
use two;
CREATE TABLE takes (
    student_id INT,
    course_id INT,
    grade VARCHAR(2),
    credits DECIMAL(4, 2)
);

-- Insert sample data for student 12345
INSERT INTO takes (student_id, course_id, grade, credits)
VALUES
    (12345, 101, 'A', 3),
    (12345, 102, 'B+', 4),
    (12345, 103, 'A-', 3.5);

CREATE TABLE grade_points (
    grade VARCHAR(2),
    points DECIMAL(4, 2)
);

-- Insert sample data for grade points
INSERT INTO grade_points (grade, points)
VALUES
    ('A', 4),
    ('A-', 3.7),
    ('B+', 3.3),
    ('B', 3),
    -- Add more grade-point mappings
    ('C', 2.5);
    
    
    SELECT SUM(gp.points * t.credits) AS total_grade_points
FROM takes t
JOIN grade_points gp ON t.grade = gp.grade
WHERE t.student_id = 12345;


SELECT SUM(gp.points * t.credits) / SUM(t.credits) AS gpa
FROM takes t
JOIN grade_points gp ON t.grade = gp.grade
WHERE t.student_id = 12345;


SELECT t.student_id, SUM(gp.points * t.credits) / SUM(t.credits) AS gpa
FROM takes t
JOIN grade_points gp ON t.grade = gp.grade
GROUP BY t.student_id;


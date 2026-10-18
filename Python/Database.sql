CREATE TABLE rooms (
	room_id INT PRIMARY KEY,
	room VARCHAR(10)
	);
	
CREATE TABLE students (
	birthday TIMESTAMP,
	student_id INT PRIMARY KEY,
	name VARCHAR(250) NOT NULL,
	room_id INT REFERENCES rooms(room_id),
	sex CHAR(1) NOT NULL
	);
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;



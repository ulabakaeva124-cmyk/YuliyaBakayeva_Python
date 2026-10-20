#Counts the total number of students in each room
query_1 = """
        SELECT room, COUNT(student_id)
        FROM rooms
        INNER JOIN students USING(room_id)
        GROUP BY room;
        """
#Calculates the average age of students for each room
query_2 = """
        SELECT room, ROUND(AVG(EXTRACT(YEAR FROM AGE(birthday))))::float AS avg_age
        FROM rooms
        INNER JOIN students USING(room_id)
        GROUP BY room
        ORDER BY avg_age
        LIMIT 5;
        """
#Finds the minimum and maximum age of students in each room
query_3 = """
        WITH max_min_age (room, min_age, max_age) 
        AS (
	    SELECT room, 
	    MIN(EXTRACT(YEAR FROM AGE(birthday))) AS min_age,
	    MAX(EXTRACT(YEAR FROM AGE(birthday))) AS max_age
	    FROM rooms
		    INNER JOIN students USING(room_id)
	    GROUP BY room
	    )
        SELECT room, min_age::float, 
        max_age::float, 
	    (max_age - min_age)::float AS difference
        FROM max_min_age
        ORDER BY difference DESC
        LIMIT 5;
        """
#Finds rooms that have both male and female students (mixed-gender rooms)
query_4 = """
        SELECT room
        FROM rooms
	    INNER JOIN students USING(room_id)
        GROUP BY room, room_id
        HAVING COUNT(DISTINCT sex) = 2
        ORDER BY room_id;
        """
import json, psycopg2
from psycopg2.extras import DictCursor

class DataReader:
    @staticmethod
    def load_json(file):
        with open(file) as f:
            return json.load(f)

class Database:
    def __init__(self, db_config):
        self.db_config = db_config

    def setup_tables(self):
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cursor:
                table_rooms = """
                CREATE TABLE IF NOT EXISTS rooms (
	            room_id INT PRIMARY KEY,
	            room VARCHAR(255)
	            );
                """
                cursor.execute(table_rooms)
                table_students = """
                CREATE TABLE IF NOT EXISTS students (
	            birthday TIMESTAMP,
	            student_id INT PRIMARY KEY,
	            name VARCHAR(255) NOT NULL,
	            room_id INT REFERENCES rooms(room_id),
	            sex CHAR(1) NOT NULL
	            );
                """
                cursor.execute(table_students)

    def insert_data(self, rooms, students):
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                for room in rooms:
                    sql = f"INSERT INTO rooms(room_id, room) VALUES (%s, %s)"
                    cursor.execute(sql, (room['id'], room['name']))
                    conn.commit()
                for student in students:
                    sql = f"INSERT INTO students(birthday, student_id, name, room_id, sex) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (student['birthday'], student['id'], student['name'], student['room'],
                                   student['sex']))
                    conn.commit()

    def add_indexes(self):
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room_id, sex);")
                conn.commit()

class Query:
    @staticmethod
    def query_result(cursor, query):
        cursor.execute(query)
        query_result = cursor.fetchall()
        return [dict(row) for row in query_result]

class ExportResult:
    @staticmethod
    def export_result(query_result, query_name):
        with open(query_name, 'w') as json_file:
            json.dump(query_result, json_file, indent=4)

db_config = {
    "host": "localhost",
    "user": "admin",
    "password": "admin123",
    "port": 5432,
    "dbname": "Students rooms"
}

query_1 = """
            SELECT room, COUNT(student_id)
            FROM rooms
            INNER JOIN students USING(room_id)
            GROUP BY room;
        """
query_2 = """
        SELECT room, ROUND(AVG(EXTRACT(YEAR FROM AGE(birthday)))) AS avg_age
        FROM rooms
        INNER JOIN students USING(room_id)
        GROUP BY room
        ORDER BY avg_age
        LIMIT 5;
        """
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
        SELECT room, min_age, max_age, 
	    max_age - min_age AS difference
        FROM max_min_age
        ORDER BY difference DESC
        LIMIT 5;
        """
query_4 = """
        SELECT room
        FROM rooms
	    INNER JOIN students USING(room_id)
        GROUP BY room, room_id
        HAVING COUNT(DISTINCT sex) = 2
        ORDER BY room_id;
        """

if __name__ == "__main__":
    rooms_data = DataReader.load_json("rooms.json")
    students_data = DataReader.load_json("students.json")
    db = Database(db_config)
    db.setup_tables()
    #db.insert_data(rooms_data, students_data)
    db.add_indexes()
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            res_1 = Query.query_result(cursor, query_1)
            ExportResult.export_result(res_1, 'query_1.json')
            res_2 = Query.query_result(cursor, query_2)
            ExportResult.export_result(res_2, 'query_2.json')
            res_3 = Query.query_result(cursor, query_3)
            ExportResult.export_result(res_3, 'query_3.json')
            res_4 = Query.query_result(cursor, query_4)
            ExportResult.export_result(res_4, 'query_4.json')
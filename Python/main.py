import json
import psycopg2
from psycopg2.extras import DictCursor
from xml.etree.ElementTree import Element, tostring

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
                    sql = "INSERT INTO rooms(room_id, room) VALUES (%s, %s) ON CONFLICT (room_id) DO NOTHING"
                    cursor.execute(sql, (room['id'], room['name']))
                for student in students:
                    sql = "INSERT INTO students(birthday, student_id, name, room_id, sex) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (student_id) DO NOTHING"
                    cursor.execute(sql, (student['birthday'], student['id'], student['name'], student['room'],
                                   student['sex']))

    def add_indexes(self):
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room_id, sex);")

class Query:
    @staticmethod
    def query_result(cursor, query):
        cursor.execute(query)
        query_result = cursor.fetchall()
        return [dict(row) for row in query_result]

class ExportResult:
    @staticmethod
    def export_json(query_result, query_name):
        with open(query_name, 'w') as json_file:
            json.dump(query_result, json_file, indent=4)

    @staticmethod
    def export_xml(query_result, query_name):
        root_node = Element('result')
        for row in query_result:
            row_node = Element('row')
            for key, value in row.items():
                child_node = Element(key)
                child_node.text = str(value)
                row_node.append(child_node)
            root_node.append(row_node)
        xml_data = tostring(root_node, encoding='unicode')
        with open(query_name, 'w', encoding='utf-8') as xml_file:
            xml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            xml_file.write(xml_data)

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
        SELECT room, ROUND(AVG(EXTRACT(YEAR FROM AGE(birthday))))::float AS avg_age
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
        SELECT room, min_age::float, 
        max_age::float, 
	    (max_age - min_age)::float AS difference
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
    db.insert_data(rooms_data, students_data)
    db.add_indexes()
    user_format = ''
    while user_format not in ('xml', 'json'):
        user_format = input('Choose format (xml or json): ')
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            res_1 = Query.query_result(cursor, query_1)
            res_2 = Query.query_result(cursor, query_2)
            res_3 = Query.query_result(cursor, query_3)
            res_4 = Query.query_result(cursor, query_4)
    if user_format == 'xml':
        ExportResult.export_xml(res_1, 'query_1.xml')
        ExportResult.export_xml(res_2, 'query_2.xml')
        ExportResult.export_xml(res_3, 'query_3.xml')
        ExportResult.export_xml(res_4, 'query_4.xml')
    else:
        ExportResult.export_json(res_1, 'query_1.json')
        ExportResult.export_json(res_2, 'query_2.json')
        ExportResult.export_json(res_3, 'query_3.json')
        ExportResult.export_json(res_4, 'query_4.json')
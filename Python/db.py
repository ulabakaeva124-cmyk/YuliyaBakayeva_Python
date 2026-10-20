import psycopg2
from psycopg2.extras import DictCursor

class Database:
    """
    Class to connect to database and create tables with data

    Attributes:
        db_config (dict): database config
    """
    def __init__(self, db_config: dict) -> None:
        self.db_config = db_config

    def setup_tables(self) -> None:
        """
        Setup tables
        """
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

    def insert_data(self, rooms: list, students:list)-> None:
        """
        Insert data into tables

        Args:
            rooms (dict): room data
            students (dict): student data

        Returns: None
        """
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                for room in rooms:
                    sql = "INSERT INTO rooms(room_id, room) VALUES (%s, %s) ON CONFLICT (room_id) DO NOTHING"
                    cursor.execute(sql, (room['id'], room['name']))
                for student in students:
                    sql = "INSERT INTO students(birthday, student_id, name, room_id, sex) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (student_id) DO NOTHING"
                    cursor.execute(sql, (student['birthday'], student['id'], student['name'], student['room'],
                                   student['sex']))

    def add_indexes(self)-> None:
        """
        Add indexes to tables
        """
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room_id, sex);")

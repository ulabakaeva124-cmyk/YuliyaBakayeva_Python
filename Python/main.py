import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from db import Database
from operations import load_json, query_result, ExportResult
from queries import query_1, query_2, query_3, query_4

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME")
}

if __name__ == "__main__":
    rooms_data = load_json("rooms.json")
    students_data = load_json("students.json")
    db = Database(db_config)
    db.setup_tables()
    db.insert_data(rooms_data, students_data)
    db.add_indexes()
    user_format = ''
    while user_format not in ('xml', 'json'):
        user_format = input('Choose format (xml or json): ')
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            res_1 = query_result(cursor, query_1)
            res_2 = query_result(cursor, query_2)
            res_3 = query_result(cursor, query_3)
            res_4 = query_result(cursor, query_4)
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
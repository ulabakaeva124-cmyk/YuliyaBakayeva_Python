import json
import psycopg2
from xml.etree.ElementTree import Element, tostring

def load_json(file: str)-> list:
    """
    Reading JSON file

    Args:
        file: path to file

    Returns:
        query_result: data from file
    """
    with open(file) as f:
        return json.load(f)

def query_result(cursor: psycopg2.extensions.cursor, query: str)-> list:
    """
    Queries database and returns result

    Args:
        cursor: database cursor
        query: query to execute

    Returns:
        query_result: list of dict
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

class ExportResult:
    """
    Save the query result as XML/JSON file
    """
    @staticmethod
    def export_json(query_result: list, query_name: str)-> None:
        """
        Save the query as JSON file

        Args:
            query_result: list of dict
            query_name: name of future query file
        """
        with open(query_name, 'w') as json_file:
            json.dump(query_result, json_file, indent=4)

    @staticmethod
    def export_xml(query_result:list, query_name:str)-> None:
        """
        Save the query as XML file

        Args:
             query_result: list of dict
             query_name: name of future query file
        """
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
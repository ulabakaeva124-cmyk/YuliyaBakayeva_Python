# YuliyaBakayeva_Python
Student Rooms Data Processor
A Python ETL script that loads student and room data from JSON files, populates a PostgreSQL database, and runs analytical queries. The query results can be exported as JSON or XML files.

Features
Database Setup: Automatically creates rooms and students tables with necessary constraints and indexes.

Data Ingestion: Loads data from rooms.json and students.json using idempotent inserts (ON CONFLICT DO NOTHING).

Analytics: Executes 4 SQL queries to calculate statistics (e.g., room occupancy, average age, age difference, and mixed-gender rooms).

Export: Saves the query results into separate files in your chosen format (json or xml).

Installation & Setup
Clone the repository:

bash
git clone <your-repo-url>
cd <your-repo-folder>
Install dependencies:

bash
pip install psycopg2-binary python-dotenv
Configure environment variables:
Create a .env file in the root directory (you can copy .env.example) and fill in your PostgreSQL credentials:

env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
DB_NAME=your_database_name
Prepare data files:
Ensure you have rooms.json and students.json in the root directory.

Usage
Run the main script:

bash
python main.py
When prompted, choose the export format (xml or json). The script will create files named query_1.xml, query_2.xml, etc. (or .json).

Project Structure
main.py — Entry point of the application.

db.py — Database connection and table management.

utils.py — Helper functions for reading JSON and exporting results.

queries.py — SQL queries used for analytics.
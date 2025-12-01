import sqlite3

def run_sql_file(cursor, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    cursor.executescript(sql_script)

def initialize_database():
    # Create & connect to SQLite DB file
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    print("Running create_tables.sql …")
    run_sql_file(cursor, "create_tables.sql")

    print("Running insert_data.sql …")
    run_sql_file(cursor, "insert_data.sql")

    # Save changes
    conn.commit()
    conn.close()

    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()

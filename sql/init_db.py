import sqlite3
from pathlib import Path

#Paths to the database + SQL schema files
BASE_DIR = Path(__file__).parent                       #folder where this script lives
DB_PATH = BASE_DIR / "database.db"     
SCHEMA_PATH = BASE_DIR / "models.sql"                  #CREATE TABLE statements
DATA_PATH = BASE_DIR / "data.sql"               #INSERT statements

#Execute an entire SQL file
def run_sql_file(conn, path):
    sql_text = path.read_text()
    conn.execute("PRAGMA foreign_keys = ON;")           #enforce FK constraints
    conn.executescript(sql_text)                        #execute SQL file


#Create/reset the database
def main():
    # If DB exists, delete it so we recreate from scratch
    if DB_PATH.exists():
        DB_PATH.unlink()

    # Connect to the new database file
    conn = sqlite3.connect(DB_PATH)

    run_sql_file(conn, SCHEMA_PATH)
    run_sql_file(conn, DATA_PATH)

    conn.close()

    print(f"Database created successfully at: {DB_PATH}")


if __name__ == "__main__":
    main()


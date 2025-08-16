import sqlite3

DB_FILE = "image_metadata.db"

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()      # for performing SQL commands

create_table_sql = """
CREATE TABLE IF NOT EXISTS img_data (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    width INTEGER,
    height INTEGER,
    size_kb REAL,
    format TEXT,
    validation_status TEXT NOT NULL ,
    notes TEXT,
    processed_timestamp DATETIME

);

"""

cursor.execute(create_table_sql)

conn.commit()
conn.close()

print(f"Database {DB_FILE} created successfully!")
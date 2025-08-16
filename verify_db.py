import sqlite3
DB_FILE = "image_metadata.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

total_records = cursor.execute("SELECT COUNT(*) FROM img_data;").fetchone()[0]
print(f"Total records in database: {total_records}")

# Summary of validation statuses
print("\nValidation Summary:")
summary_query = """
SELECT validation_status, COUNT(*)
FROM img_data
GROUP BY validation_status;
"""
for row in cursor.execute(summary_query):
    status, count = row
    print(f"- {status}: {count} files")

conn.close()

from database.connection import get_connection

with get_connection() as conn:
    cursor = conn.execute("PRAGMA table_info(logs)")
    columns = cursor.fetchall()

    print("Logs table columns:")

    for column in columns:
        print(dict(column))
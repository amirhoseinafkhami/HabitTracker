from database.connection import get_connection

def ensure_user(user_id: int):

    with get_connection() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
            """,
            (user_id,)
        )

def create_habit(user_id: int, name: str):
    ensure_user(user_id)

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT OR IGNORE INTO habits (user_id, name)
            VALUES (?, ?)""",
            (user_id, name)
        )

        return cursor.lastrowid

def get_user_habits(user_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            """SELECT habit_id, name
            FROM habits
            WHERE user_id = ?
            ORDER BY habit_id DESC""",
            (user_id,)
        )

        return cursor.fetchall()

def delete_habit(habit_id: int, user_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            """DELETE FROM habits
            WHERE habit_id = ? AND user_id = ?""",
            (habit_id, user_id)
        )

        return cursor.rowcount

delete_habit(1, 123456)
print(get_user_habits(123456))
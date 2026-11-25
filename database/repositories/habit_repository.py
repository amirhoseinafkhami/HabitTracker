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
def get_daily_habits(user_id: int, today: str):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT habits.habit_id,
            habits.name,
            COALESCE(logs.status, 0) AS status
            FROM habits
            LEFT JOIN logs
            ON habits.habit_id = logs.habit_id
            AND logs.date = ?
            WHERE habits.user_id = ?
            ORDER BY habits.habit_id DESC
            """, (today, user_id)
        )

        return cursor.fetchall()

def mark_habit(user_id: int, habit_id: int, today: str, status: int):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO logs (habit_id, date, status)
            SELECT habit_id, ?, ?
            FROM habits
            WHERE habit_id = ? AND user_id = ?
                
            ON CONFLICT(habit_id, date)
            DO UPDATE SET status = excluded.status
            """,(today, status, habit_id, user_id)
        )

        return cursor.rowcount
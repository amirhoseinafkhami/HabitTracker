from database.connection import get_connection

def init_db():

    with get_connection() as conn:

        # user table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY)
                     """)
        # habits table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS habits(
        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,

        FOREIGN KEY (user_id)
            REFERENCES users(user_id)
            ON DELETE CASCADE,

        CHECK (length(trim(name)) > 0))""")
        # logs table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status INTEGER NOT NULL CHECK(status IN (0, 1)),

                FOREIGN KEY (habit_id)
                    REFERENCES habits(habit_id)
                    ON DELETE CASCADE,

                UNIQUE (habit_id, date)
            )""")

        # index for faster user habits lookup
        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_habits_user_id ON habits(user_id)""")

    print("Database initialized successfully")
import psycopg2

conn = psycopg2.connect(
    dbname="snakeusers",
    user="postgres",
    password="12345&bgm",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        level INTEGER DEFAULT 1,
        score INTEGER DEFAULT 0
    );
    """)
    conn.commit()


def get_user(username):
    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    return user_id


def get_user_progress(user_id):
    cur.execute("SELECT level, score FROM users WHERE id = %s;", (user_id,))
    return cur.fetchone()


def save_progress(user_id, level, score):
    cur.execute("""
        UPDATE users SET level = %s, score = %s WHERE id = %s;
    """, (level, score, user_id))
    conn.commit()


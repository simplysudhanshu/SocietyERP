import sqlite3 as sq


def create_connection():
    return sq.connect("apartment")


def add_to_db():
    conn = create_connection()

    conn.execute("INSERT INTO members VALUES ('A-01', 'PATIL');")

    cursor = conn.execute("SELECT * FROM members")

    print(list(cursor))


conn = create_connection()
# conn.execute("DROP TABLE members;")

cursor = conn.execute("SELECT * FROM members")

print(list(cursor))
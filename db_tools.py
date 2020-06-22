import sqlite3 as sq


def create_connection():
    return sq.connect("apartment")


def generate_receipt_id(month: str, year: str):
    max_id = 0
    conn = create_connection()

    query = f"SELECT receipt_id FROM records WHERE date LIKE '%{month}/%';"

    try:
        cursor = conn.execute(query)
    except sq.Error as e:
        print(e)
        return False

    for row in cursor:
        if len(row) > 0:
            last_id = row[0].split("/")[1]

            if int(last_id) > max_id:
                max_id = int(last_id)

    return f"{month}.{year}/{max_id+1}"


def add_to_db(table: str, attributes: list):
    conn = create_connection()
    query = ''

    if table == "members":
        query = f"INSERT INTO members VALUES ('{attributes[0]}', '{attributes[1]}', '{attributes[2]}', {attributes[3]}, '{attributes[4]}');"

    elif table == "records":
        split_date = attributes[0].split("/")
        receipt_id = generate_receipt_id(month=split_date[1], year=split_date[2])

        query = f"INSERT INTO records VALUES ('{receipt_id}', '{attributes[0]}', '{attributes[1]}', {attributes[2]}, '{attributes[3]}', '{attributes[4]}');"

    try:
        conn.execute(query)

    except sq.Error as e:
        print(e)
        return False
    else:
        conn.commit()
        return True


def get_from_db(table: str, attribute: str, key: str = None, value=None):
    conn = create_connection()
    output = []

    if key and value:
        if type(value) == str:
            value = f"'{value}'"

        query = f"SELECT {attribute.lower()} FROM {table.lower()} WHERE {key.lower()} = {value};"
    else:
        query = f"SELECT {attribute.lower()} FROM {table.lower()};"

    try:
        cursor = conn.execute(query)

        for row in cursor:
            output.append(list(row))

    except sq.Error as e:
        print(e)
        return False

    else:
        return output


def update_db(table: str, identifier: str, all_attributes: list):
    conn = create_connection()
    query = ''

    if table == 'members':
        query = f"UPDATE {table} SET name = '{all_attributes[0].lower()}', current = '{all_attributes[1].lower()}', " \
                f"contact = {all_attributes[2]}, email = '{all_attributes[3].lower()}' WHERE flat = '{identifier}'"

    elif table == 'records':
        query = f"UPDATE {table} SET date = '{all_attributes[0].lower()}', flat = '{all_attributes[1].lower()}', " \
                f"amount = {all_attributes[2]}, mode = '{all_attributes[3].lower()}', ref = '{all_attributes[4].lower()}' " \
                f"WHERE receipt_id = '{identifier}'"

    try:
        conn.execute(query)

    except sq.Error as e:
        print(e)
        return False
    else:
        conn.commit()
        return True


def delete_from_db(table: str, key: str = None, value=None):
    conn = create_connection()
    query = f"DELETE FROM  {table} WHERE {key.lower()} = '{value}'"

    try:
        conn.execute(query)

    except sq.Error as e:
        print(e)
        return False
    else:
        conn.commit()
        return True


def get_receipts(date: str = None, flat: str = None, month: str = None):
    conn = create_connection()
    output = []
    query = ''

    if date is not None:
        query = "SELECT r.receipt_id, r.flat, m.name, r.amount, r.mode FROM records r, members m WHERE " \
                f"r.flat = m.flat AND r.date = '{date}';"

    elif flat is not None:
        query = f"SELECT receipt_id, date, amount, mode FROM records WHERE flat = '{flat}';"

    elif month is not None:
        query = "SELECT r.receipt_id, r.date, r.flat, m.name, r.amount, r.mode FROM records r, members m WHERE " \
                f"r.flat = m.flat AND date LIKE '%{month}/%';"

    try:
        cursor = conn.execute(query)
        for row in cursor:
            output.append(row)

    except sq.Error as e:
        print(e)
        return False
    else:
        return output


# PLAY :

# connection = create_connection()

# connection.execute("CREATE TABLE members (flat TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, current TEXT NOT NULL, "
#                    "contact NUMBER NOT NULL, email TEXT NOT NULL);")

# connection.execute("CREATE TABLE records (receipt_id TEXT PRIMARY KEY NOT NULL, date TEXT NOT NULL, flat TEXT NOT NULL, "
#                    "amount REAL NOT NULL, mode TEXT NOT NULL, ref TEXT NOT NULL);")

# connection.execute("DELETE FROM members;")
# connection.execute("DELETE FROM records;")

# conn.execute("DROP TABLE members;")

# connection.commit()

# --

# add_to_db(table='members', attributes=["A-03", "Mr Dhumal", "Mr Patil", 1, "a@xyz"])
# add_to_db(table='records', attributes=["23/02/20", "A-02", 1500, "cash", "cash"])

# update_db(table="members", identifier="A-01", all_attributes=["Mr Patil", "Mr Patil", 1, "a@xyz"])

# print(generate_receipt_id(month=6, year=20))
# print(get_from_db(table="members", attribute="*", key="flat", value="A-01"))

# print(get_receipts(month="01"))

# cursor1 = connection.execute("SELECT * FROM members';")
# print(list(cursor1))

# cursor2 = connection.execute("SELECT * FROM records")
# print(list(cursor2))

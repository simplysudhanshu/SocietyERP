import os
import sqlite3 as sq
import csv
import time


def create_connection():
    return sq.connect("apartment")


def fix_date_back(month: str):
    if month == '':
        return "-"
    else:
        month_combo_value = month.split(" '")
        return f"{month_combo_value[0]}/{month_combo_value[1]}"


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

    return f"{month}.{year}/{max_id + 1}"


def add_to_db(table: str, attributes: list):
    conn = create_connection()
    query = ''

    if table == "members":
        query = f"INSERT INTO members VALUES ('{attributes[0]}', '{attributes[1]}', '{attributes[2]}', {attributes[3]}, '{attributes[4]}');"

    elif table == "records":
        split_date = attributes[0].split("/")
        receipt_id = generate_receipt_id(month=split_date[1], year=split_date[2])

        query = f"INSERT INTO records VALUES ('{receipt_id}', '{attributes[0]}', '{attributes[1]}', " \
                f"'{fix_date_back(attributes[2])}','{fix_date_back(attributes[3])}', {attributes[4]}, {attributes[5]}, " \
                f"'{attributes[6]}', '{attributes[7]}');"

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


def get_statement(date: str = None, flat: str = None, month: str = None):
    conn = create_connection()
    output = []
    query = ''

    if date is not None:
        query = "SELECT r.receipt_id, r.flat, m.name, r.fee_month, r.amount, r.fine, r.mode, r.ref FROM records r, members m WHERE " \
                f"r.flat = m.flat AND r.date = '{date}';"

    elif flat is not None:
        query = "SELECT receipt_id, date, fee_month, amount, fine, mode, ref FROM records WHERE " \
                f"flat = '{flat}';"

    elif month is not None:
        if len(month) == 1:
            month = f"0{int(month)+1}"
        query = "SELECT r.receipt_id, r.date, r.flat, m.name, r.amount, r.fine, r.mode, r.ref FROM records r, members m WHERE " \
                f"r.flat = m.flat AND r.date LIKE '%/{month}/%';"

    try:
        cursor = conn.execute(query)
        for row in cursor:
            output.append(row)

    except sq.Error as e:
        print(e)
        return False
    else:
        return output


def generate_csv():
    conn = create_connection()
    conn.text_factory = str

    user = os.environ['USERPROFILE']
    path = user + '\\Desktop\\SocietyERP'
    if not os.path.exists(path):
        os.makedirs(path)

    cur_members = conn.cursor()
    cur_records = conn.cursor()

    data_members = cur_members.execute("SELECT * FROM members")
    data_records = cur_records.execute(
        "SELECT r.receipt_id, r.date, r.flat, m.name, r.fee_month, r.amount, r.fine, r.mode, r.ref FROM records r, members m WHERE r.flat = m.flat")

    with open(
            f'{path}\\SMGRP_{time.strftime("%d-%m-%Y-%H%M")}_members.csv',
            'w') as f_member:
        writer = csv.writer(f_member)
        writer.writerow(['FLAT', 'NAME', 'CURRENT OCCUPANT', 'CONTACT', 'EMAIL'])
        writer.writerows(data_members)

    with open(
            f'{path}\\SMGRP_{time.strftime("%d-%m-%Y-%H%M")}_records.csv',
            'w') as f_records:
        writer = csv.writer(f_records)
        writer.writerow(['RECEIPT ID', 'DATE', 'FLAT', 'NAME', 'MONTH', 'AMOUNT', 'FINE', 'MODE', 'REFERENCE ID'])
        print(data_records)
        writer.writerows(data_records)
    return f_member.name, f_records.name


# PLAY :

# print(generate_csv())
# connection = create_connection()

# connection.execute("CREATE TABLE members (flat TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL, current TEXT NOT NULL, "
#                    "contact NUMBER NOT NULL, email TEXT NOT NULL);")

# connection.execute("CREATE TABLE records (receipt_id TEXT PRIMARY KEY NOT NULL, date TEXT NOT NULL, flat TEXT NOT NULL, fee_month TEXT NOT NULL, fee_till TEXT, "
#                    "amount REAL NOT NULL, fine READ NOT NULL, mode TEXT NOT NULL, ref TEXT);")

# connection.execute("DELETE FROM members;")
# connection.execute("DELETE FROM records;")

# connection.execute("DROP TABLE members;")
# connection.execute("DROP TABLE records;")

# cursor1 = connection.execute("SELECT r.receipt_id, r.date, r.flat, m.name, r.amount, r.mode FROM records r, members m WHERE r.flat = m.flat AND r.date LIKE '%/06/%';")

# connection.commit()

# --

# add_to_db(table='members', attributes=["A-09", "Mr Kulkarni", "Mr Kulkarni", 1, "a@xyz"])
# add_to_db(table='records', attributes=["23/06/20", "A-10", 1500, "cash", "cash"])

# update_db(table="members", identifier="A-01", all_attributes=["Mr Patil", "Mr Patil", 1, "a@xyz"])

# print(generate_receipt_id(month='6'))
# print(get_from_db(table="members", attribute="name", key="flat", value="A - 1"))

# print(get_receipts(month="06"))

# cursor1 = connection.execute("SELECT * FROM members;")
# for row in cursor1:
#     print(row)

# cursor2 = connection.execute("SELECT * FROM records")
# cursor2 = connection.execute("SELECT * FROM records WHERE flat = 'A - 9' ORDER BY 2 DESC")
#
# for row in cursor2:
#     print(row)

'''
Populating the database:

names = ["Mr D. S. Patil", "Mr C. Y. Carvalho", "Mrs M. A. Kotangle", "Mr B. R. Varpe", "Mr V. A. Dhumal",
         "Mr A. D. Kulkarni", "Mr V. G. Dhapre", "Mrs S. S. Pawar", "Mr P. S. Kulkarni", "Mr R. R. Tahilramani",
         "Mr. S. G. Iyer", "Mr P. S. Babel", "Mr K. J. Sharma", "Mr M. N. Kanchan", "Mr B. B. Mankeshwarkar",
         "Mr A. V. Shrivastava", "Mr K. R. Rathor", "Mr P. K. Das", "Mr V. A. Sutar", "Mr S. S. Chavan",
         "Mr. A. P. Pandey", "Mr. A. N. Mujawar"]

numbers = [9822599523, 0, 7208171228, 9850007465, 9822433024, 9850841850, 8208662242, 9764406444, 9850956132, 0, 9765401804,
           9922420609, 8888405454, 9881995002, 9028318480, 9730014518, 9764975993, 9890453488, 0, 9881499697, 8888887300, 9890310831]

email = "example@xyz"

flats = [f"A - {str(x)}" for x in range(1, 23)]

for index, flat in enumerate(flats):
    add_to_db(table='members', attributes=[flat, names[index], names[index], numbers[index], email])
'''

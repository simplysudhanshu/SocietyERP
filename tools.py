from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
import matplotlib.pyplot as plt
import matplotlib
import datetime

import db_tools

matplotlib.use('Agg')


all_months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
              '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

full_months = ("January", 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December')

all_months_values = list(all_months.values())

flats = [f"A - {str(x)}" for x in range(1, 23)]

currentMonth = datetime.datetime.now().month
currentYear = datetime.datetime.now().year


def create_spacer_item(w: int, h: int):
    return QSpacerItem(w, h, QSizePolicy.Expanding)


def get_name(flat: str):
    return db_tools.get_from_db(table="members", attribute="name", key="flat", value=flat)[0][0]


def fix_date(date: str):
    year, month, date = date.split("-")
    return f"{date}/{month}/{year}"


def fix_date_back(month: str):
    month_combo_value = month.split(" '")

    from_date = f"20{month_combo_value[1]}-{get_month_number(month_combo_value[0])}-0"

    return from_date


def calculate_months(month: str, pending: bool = True, advance: bool = False):
    current_year, current_month, current_day = month.split("-")

    applicable_months = []

    if pending:
        year_beginning = get_nearest_year_end(month=current_month, year=current_year)

        for beginning in year_beginning:
            start_month, start_year = beginning.split("/")

            if int(start_month) == 0 and int(start_year) == int(current_year[2:]):
                end_month = int(current_month)
            else:
                end_month = len(all_months_values)

            for month in all_months_values[int(start_month):end_month]:
                applicable_months.append(f"{month} '{start_year}")

        return applicable_months[::-1]

    elif advance:
        year_beginning = get_nearest_year_end(month=current_month, year=current_year, previous_end=False, next_end=True)

        for beginning in year_beginning:
            end_month, end_year = beginning.split("/")

            if int(end_month) == 11 and int(end_year) == int(current_year[2:]):
                start_month = int(current_month)
            else:
                start_month = 0

            for month in all_months_values[start_month:int(end_month)]:
                applicable_months.append(f"{month} '{end_year}")

        return applicable_months


def get_nearest_year_end(month: str, year: str, previous_end: bool = True, next_end: bool = False):
    year_beginnings = []

    if previous_end:
        if int(month) >= 4:
            year_beginnings.append(f"3/{int(year[-2:]) - 1}")
            year_beginnings.append(f"0/{year[-2:]}")

        else:
            year_beginnings.append(f"3/{int(year[-2:]) - 2}")
            year_beginnings.append(f"0/{int(year[-2:]) - 1}")
            year_beginnings.append(f"0/{year[-2:]}")

    elif next_end:
        if int(month) >= 4:
            year_beginnings.append(f"11/{year[-2:]}")
            year_beginnings.append(f"11/{int(year[-2:]) + 1}")
            year_beginnings.append(f"3/{int(year[-2:]) + 2}")

        else:
            year_beginnings.append(f"11/{year[-2:]}")
            year_beginnings.append(f"3/{int(year[-2:]) + 1}")

    return year_beginnings


def get_month_number(month: str):
    for key, value in all_months.items():
        if value == month:
            return key
    return None


def calculate_fine(month: str, transact_date: str):
    fee_month, fee_year = month.split(" '")
    fee_month = get_month_number(fee_month)

    transact_date_date, transact_month, transact_year = transact_date.split("/")

    transact_number = int(f"{transact_year[-2:]}{transact_month}{transact_date_date}")

    extra_month = 0
    extra_year = 0

    while True:
        test_date = 0

        if len(str(abs(int(fee_month) + extra_month))) == 1:
            test_date = int(f"{fee_year}{fee_month[0]}{int(fee_month[1]) + extra_month}05")

        elif len(str(abs(int(fee_month) + extra_month))) == 2:
            if int(fee_month) + extra_month > 12:
                extra_year = (int(fee_month) + extra_month) // 12
                new_month = (int(fee_month) + extra_month) % 12

                if len(str(abs(extra_month))) == 1:
                    test_date = int(f"{int(fee_year) + extra_year}0{new_month}05")
                else:
                    test_date = int(f"{int(fee_year) + extra_year}{new_month}05")

            else:
                test_date = int(f"{int(fee_year) + extra_year}{int(fee_month) + extra_month}05")

        if test_date >= transact_number:
            return extra_month
        else:
            extra_month += 1


def get_search_content(search_by: str, search_attribute: str):
    content = []
    if search_by == "flat":
        content = db_tools.get_statement(flat=search_attribute)

        for index, row in enumerate(content):
            row = list(row)

            if row[3] != "-":
                row[2] = f"{row[2]} - {row[3]}"

            row.remove(row[3])

            row[1] = datetime.datetime.strptime(row[1], '%d/%m/%Y').strftime('%d %B, %Y')

            content[index] = row

    elif search_by == "date":
        content = db_tools.get_statement(date=search_attribute)

        for index, row in enumerate(content):
            row = list(row)

            if row[4] != "-":
                row[3] = f"{row[3]} - {row[4]}"

            row.remove(row[4])
            content[index] = row

    elif search_by == "month":
        content = db_tools.get_statement(month=search_attribute)

        for index, row in enumerate(content):
            row = list(row)

            if row[5] != "-":
                row[4] = f"{row[4]} - {row[5]}"

            row.remove(row[5])

            row[1] = datetime.datetime.strptime(row[1], '%d/%m/%Y').strftime('%d %B, %Y')

            content[index] = row

    return content


def get_stats_content():
    stats = db_tools.get_members_stats()

    defaulters = []

    for index, row in enumerate(stats):
        row = list(row)

        if row[3] != "-":
            row[2] = row[3]

        row.remove(row[3])

        stats[index] = row

        if row[2] == "-":
            defaulters.append(index)

        else:
            row_month, row_year = row[2].split("/")

            if int(row_year) < int(str(currentYear)[-2:]):
                defaulters.append(index)

            elif int(row_year) == int(str(currentYear)[-2:]):
                if int(get_month_number(row_month)) < currentMonth:
                    defaulters.append(index)

    return stats, defaulters


def get_home_stats():
    stats, defaulters = get_stats_content()
    funds = db_tools.get_funds_stats(month=currentMonth)

    received = 22 - len(defaulters)
    pending = len(defaulters)
    percent = (len(defaulters) * 100) / 22

    labels = 'Received', 'Pending'
    sizes = [100 - percent, percent]
    colors = ['chartreuse', 'red']
    explode = (0, 0)

    plt.clf()
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', wedgeprops={'linewidth': 7, 'edgecolor': 'white'})

    centre_circle = plt.Circle((0, 0), 0.75, color='black', fc='white', linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis('equal')
    plt.savefig("pie.png", bbox_inches='tight', pad_inches=0)

    return {"received": received, "pending": pending, "percent": percent, 'funds': funds}

# calculate_fine(month="May '20", transact_date="06/01/21")

# print(12 % 10, 12 / 10)
#
# a = ["0", "1", "2", "3"]
# print(a)
#
# a[2] = f"{a[2]}-{a[3]}"
# print(a)
#
# a.remove(a[3])
# print(a)

# a = '30/06/2020'
# a = datetime.datetime.strptime(a, '%d/%m/%Y').strftime('%d %B, %Y')
# print(type(a))

# a = ["4", '3', '2', '1']
# b = ['3', '4', '5']
#
# c = b[::-1]
# c.extend([x for x in a if x not in b])
# print(c)

# get_home_stats()

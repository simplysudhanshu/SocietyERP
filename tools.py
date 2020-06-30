from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

import db_tools

all_months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
              '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

all_months_values = list(all_months.values())


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

        if len(str(abs(int(fee_month)+extra_month))) == 1:
            test_date = int(f"{fee_year}{fee_month[0]}{int(fee_month[1]) + extra_month}05")

        elif len(str(abs(int(fee_month)+extra_month))) == 2:
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



# calculate_fine(month="May '20", transact_date="06/01/21")

# print(12 % 10, 12 / 10)

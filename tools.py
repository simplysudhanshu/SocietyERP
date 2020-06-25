from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

import db_tools


def create_spacer_item(w: int, h: int):
    return QSpacerItem(w, h, QSizePolicy.Expanding)


def get_name(flat: str):
    return db_tools.get_from_db(table="members", attribute="name", key="flat", value=flat)[0][0]


def fix_date(date: str):
    year, month, date = date.split("-")
    return f"{date}/{month}/{year}"

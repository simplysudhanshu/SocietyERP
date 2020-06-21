from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, \
    QSpacerItem, QSizePolicy
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from datetime import date
import marathi


flats = [str(x) for x in range(0, 22)]


class home(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.spaceItem = QSpacerItem(150, 60, QSizePolicy.Expanding)

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # --- TITLE
        title_layout = QVBoxLayout()
        title_group = QGroupBox("Co-operative Housing Society")

        title = QLabel(f"{marathi.sh}{marathi.mod}{marathi.r}{marathi.d_velanti} "
                       f"{marathi.m}{marathi.o}{marathi.r}{marathi.y}{marathi.a} "
                       f"{marathi.g}{marathi.o}{marathi.s}{marathi.a}{marathi.v}{marathi.d_velanti} "
                       f"{marathi.r}{marathi.a}{marathi.j} "
                       f"{marathi.p}{marathi.a}{marathi.r}{marathi.mod}{marathi.k}, "
                       f"{marathi.f}{marathi.matra}{marathi.j} - II")
        title.setStyleSheet("font: bold 25pt")
        title.setFixedHeight(80)

        sub_title = QLabel(f"{marathi.k}{marathi.matra}{marathi.sh}{marathi.v}{marathi.n}{marathi.g}{marathi.r}, "
                           f"{marathi.ch}{marathi.p_velanti}{marathi.timb}{marathi.ch}{marathi.v}{marathi.d}, "
                           f"{marathi.p}{marathi.p_ukar}{marathi.nn}{marathi.matra}")
        sub_title.setStyleSheet("font: bold")
        sub_title.setFixedHeight(30)

        app_name = QLabel("MEMBERSHIP FEE COLLECTION PORTAL.")
        app_name.setFixedHeight(30)
        app_name.setStyleSheet("border: 1px solid black;")

        title.setAlignment(Qt.AlignCenter)
        sub_title.setAlignment(Qt.AlignCenter)
        app_name.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(title)
        title_layout.addWidget(sub_title)
        title_layout.addSpacerItem(self.spaceItem)
        title_layout.addWidget(app_name)

        title_group.setLayout(title_layout)

        # --- WELCOME
        welcome_layout = QHBoxLayout()
        welcome = QLabel("Welcome, ")
        name = QLabel("Mr. X")

        welcome_layout.insertStretch(0, 1)
        welcome_layout.addWidget(welcome)
        welcome_layout.addWidget(name)
        welcome_layout.insertStretch(3, 1)

        # --- DATE
        date_label = QLabel(f"{date.today().strftime('%d %B, %Y')}")
        date_label.setAlignment(Qt.AlignRight)

        # comboBox = QComboBox(self)
        # model = comboBox.model()
        #
        # for flat in flats:
        #     item = QStandardItem(f"A - {flat}")
        #     model.appendRow(item)
        #
        # comboBox.setFont(QFont('SansSerif', 10))
        # comboBox.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')

        # --- MEMBERS TAB
        search_button = QPushButton("Search Records")
        add_button = QPushButton("Add Member")

        members_layout = QVBoxLayout()
        members_layout.addWidget(search_button)
        members_layout.addWidget(add_button)

        members_group = QGroupBox("Handling Members :")
        members_group.setLayout(members_layout)

        # ------- FINAL GRID

        grid.addWidget(title_group, 0, 0, 1, 4)
        grid.addLayout(welcome_layout, 1, 0, 1, 3)
        grid.addWidget(date_label, 1, 3, 1, 1)
        grid.addWidget(members_group, 2, 0)

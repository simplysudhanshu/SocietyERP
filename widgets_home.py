from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from datetime import date

from tools import create_spacer_item, get_home_stats
import marathi

from widgets_finance_entry import finance_entry
from widgets_finance_search import finance_search
from widgets_finance_edit import finance_edit
from widgets_stats import stats


flats = [f"A - {str(x)}" for x in range(1, 23)]

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

QSS = '''
QCalendarWidget QAbstractItemView
{ 
    selection-background-color: rgb(215,215,215); 
    selection-color: black;
}
QCalendarWidget QWidget 
{
  color:black;
}
QCalendarWidget QTableView
{
    border-width:1px;
    background-color:white;
}
'''


class center_widget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        current_month = date.today().strftime('%B')

        # --LEVEL ONE GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(50)
        self.setLayout(self.grid)

        # -- HOME MEMBERS PANEL:
        self.home_add_members_button = QPushButton("Add New Member")
        self.home_search_members_button = QPushButton("Search Member Details")

        self.home_add_members_button.setEnabled(False)                                                                  # ENABLE AFTER FUNCTIONALITY
        self.home_search_members_button.setEnabled(False)                                                               # ENABLE AFTER FUNCTIONALITY

        self.home_members_layout = QVBoxLayout()
        self.home_members_layout.addWidget(self.home_add_members_button)
        self.home_members_layout.addWidget(self.home_search_members_button)

        self.home_members_group = QGroupBox("Society Members :")
        self.home_members_group.setLayout(self.home_members_layout)

        self.grid.addWidget(self.home_members_group, 2, 0)

        # -- HOME FINANCE PANEL:
        self.home_add_entry_button = QPushButton("&Add New Entry")
        self.home_search_entry_button = QPushButton("Search Records")
        self.home_edit_entry_button = QPushButton("Edit Records")

        self.home_finance_layout = QVBoxLayout()
        self.home_finance_layout.addWidget(self.home_add_entry_button)
        self.home_finance_layout.addWidget(self.home_search_entry_button)
        self.home_finance_layout.addWidget(self.home_edit_entry_button)

        self.home_finance_group = QGroupBox("Finance :")
        self.home_finance_group.setLayout(self.home_finance_layout)

        self.grid.addWidget(self.home_finance_group, 2, 1)

        # -- HOME STATS PANEL:
        stats_content = get_home_stats()

        self.home_current_stats_label = QLabel()
        stats_label = f"Monthly Fee Status ({current_month}) : {stats_content['received']} received, {stats_content['pending']} pending."
        self.home_current_stats_label.setText(stats_label)

        self.home_current_collection_label = QLabel()
        funds_label = f"Monthly Collection ({current_month}) : {stats_content['funds']} INR."
        self.home_current_collection_label.setText(funds_label)

        self.home_stats_button = QPushButton("Get Detailed Statistics")

        self.home_stats_layout = QVBoxLayout()
        self.home_stats_layout.addWidget(self.home_current_stats_label)
        self.home_stats_layout.addWidget(self.home_current_collection_label)
        self.home_stats_layout.addWidget(self.home_stats_button)

        self.home_stats_group = QGroupBox("Statistics :")
        self.home_stats_group.setLayout(self.home_stats_layout)

        self.grid.addWidget(self.home_stats_group, 2, 2)

        self.home = [self.home_members_group, self.home_finance_group, self.home_stats_group]
        self.active_widget = None

        # -- BUTTONS FUNCTIONS:
        self.home_add_entry_button.clicked.connect(lambda: self.show_Finance_entry())
        self.home_search_entry_button.clicked.connect(lambda: self.show_Finance_search())
        self.home_edit_entry_button.clicked.connect(lambda: self.show_Finance_edit())
        self.home_stats_button.clicked.connect(lambda: self.show_Stats())

        # -- LAUNCHING HOME PAGE:
        self.deploy_home()

    # - TOP LEVEL HOME PAGE + TEMPLATE:
    def deploy_home(self):

        # -- TITLE
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

        app_name = QLabel("MEMBERSHIP FEE COLLECTION PORTAL")
        app_name.setFixedHeight(30)
        app_name.setStyleSheet("border: 1px solid black;")

        title.setAlignment(Qt.AlignCenter)
        sub_title.setAlignment(Qt.AlignCenter)
        app_name.setAlignment(Qt.AlignCenter)

        title_layout.addWidget(title)
        title_layout.addWidget(sub_title)
        title_layout.addSpacerItem(create_spacer_item(w=150, h=30))
        title_layout.addWidget(app_name)

        title_group.setLayout(title_layout)

        # -- HOME BUTTON
        home_button = QPushButton('')
        home_button.setIcon(QIcon('icon.png'))
        home_button.setIconSize(QSize(30, 30))
        home_button.setFixedSize(50, 50)

        home_button.clicked.connect(lambda: self.get_latest_stats())
        home_button.clicked.connect(lambda: self.show_home())

        home_button_layout_h = QHBoxLayout()
        home_button_layout_h.addWidget(home_button)
        home_button_layout_h.addStretch(-1)

        home_button_layout = QVBoxLayout()
        home_button_layout.addLayout(home_button_layout_h)

        # -- WELCOME
        welcome_layout = QHBoxLayout()
        welcome = QLabel("                                       Hello,")
        name = QLabel("Mr. X")

        welcome.setAlignment(Qt.AlignTop)

        name.setAlignment(Qt.AlignTop)
        name.setStyleSheet("font: bold")

        welcome_layout.addWidget(welcome)
        welcome_layout.addWidget(name)

        # -- DATE
        date_label = QLabel(f"{date.today().strftime('%d %B, %Y')}")
        date_label.setAlignment(Qt.AlignRight)

        # -- HOME TEMPLATE GRID
        self.grid.addWidget(title_group, 0, 0, 1, 3)
        self.grid.addLayout(home_button_layout, 1, 0, 1, 2)
        self.grid.addLayout(welcome_layout, 1, 1)
        self.grid.addWidget(date_label, 1, 2, )
        self.grid.addItem(create_spacer_item(w=150, h=50), 3, 0, 1, 3)

    def show_Finance_entry(self):
        for item in self.home:
            item.hide()

        finance_entry_object = finance_entry(self)

        finance_entry_layout = QVBoxLayout()
        finance_entry_layout.addWidget(finance_entry_object)

        finance_entry_group = QGroupBox("NEW TRANSACTION ENTRY")
        finance_entry_group.setLayout(finance_entry_layout)

        self.grid.addWidget(finance_entry_group, 2, 0, 2, 3)
        self.active_widget = finance_entry_group

    def show_Finance_search(self):
        for item in self.home:
            item.hide()

        finance_search_object = finance_search(self)

        finance_search_layout = QVBoxLayout()
        finance_search_layout.addWidget(finance_search_object)

        finance_search_group = QGroupBox("SEARCH ENTRY")
        finance_search_group.setLayout(finance_search_layout)

        self.grid.addWidget(finance_search_group, 2, 0, 2, 3)
        self.active_widget = finance_search_group

    def show_Finance_edit(self):
        for item in self.home:
            item.hide()

        finance_entry_object = finance_edit(self)

        finance_entry_layout = QVBoxLayout()
        finance_entry_layout.addWidget(finance_entry_object)

        finance_entry_group = QGroupBox("EDIT TRANSACTION ENTRY")
        finance_entry_group.setLayout(finance_entry_layout)

        self.grid.addWidget(finance_entry_group, 2, 0, 2, 3)
        self.active_widget = finance_entry_group

    def show_Stats(self):
        for item in self.home:
            item.hide()

        stats_object = stats(self)

        stats_layout = QVBoxLayout()
        stats_layout.addWidget(stats_object)

        stats_group = QGroupBox("STATISTICS")
        stats_group.setLayout(stats_layout)

        self.grid.addWidget(stats_group, 2, 0, 2, 3)
        self.active_widget = stats_group

    def show_home(self):
        if self.active_widget is not None:
            self.active_widget.hide()

        for item in self.home:
            item.show()

    def get_latest_stats(self):
        current_month = date.today().strftime('%B')

        stats_content = get_home_stats()
        stats_label = f"Monthly Fee Status ({current_month}) : {stats_content['received']} received, {stats_content['pending']} pending."
        self.home_current_stats_label.setText(stats_label)

        funds_label = f"Monthly Collection ({current_month}) : {stats_content['funds']} INR."
        self.home_current_collection_label.setText(funds_label)

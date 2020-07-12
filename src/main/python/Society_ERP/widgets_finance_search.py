from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QDateEdit, QFormLayout, QPushButton, QGroupBox, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QStyleFactory

from src.main.python.Society_ERP.tools import flats, full_months, fix_date, get_name, get_search_content


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


class finance_search(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyle(QStyleFactory.create('Fusion'))

        self.setStyleSheet(QSS)

        # -- LEVEL TWO GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(0, 1, 0, 1)
        self.setLayout(self.grid)

        # -- CELL ZERO
        self.flat_label = QLabel("FLAT NO. :")
        self.flat_combo = QComboBox()
        model = self.flat_combo.model()

        for flat in flats:
            model.appendRow(QStandardItem(flat))

        self.flat_combo.setStyleSheet('color: black; selection-background-color: rgb(215,215,215)')

        self.name_label = QLabel("NAME :")
        self.name_value = QLabel("Mr D. S. Patil")

        self.name_label.setStyleSheet("font-size: 15px;")
        self.name_value.setStyleSheet("font-size: 15px;")

        self.flat_combo.currentIndexChanged['QString'].connect(self.set_name)

        self.finance_search_panel_0 = QFormLayout()
        self.finance_search_panel_0.addRow(self.flat_label, self.flat_combo)
        self.finance_search_panel_0.addRow(self.name_label, self.name_value)

        self.finance_search_group_0 = QGroupBox("Search by Flat")
        self.finance_search_group_0.setLayout(self.finance_search_panel_0)
        self.finance_search_group_0.setCheckable(True)
        self.finance_search_group_0.toggled.connect(lambda: self.manage_checkbox(group=self.finance_search_group_0))

        # ---
        self.date_label = QLabel("DATE OF TRANSACTION :")
        self.date_label.setWordWrap(True)

        self.date_line = QDateEdit()
        self.date_line.setCalendarPopup(True)
        self.date_line.setDate(QDate.currentDate())
        self.date_line.setDisplayFormat("dd MMMM, yyyy")

        self.date_desc = QLabel("Records for all transactions done on this particular date.")
        self.date_desc.setStyleSheet("font-size: 15px;")
        self.date_desc.setWordWrap(True)

        self.finance_search_panel_1 = QFormLayout()
        self.finance_search_panel_1.addRow(self.date_label, self.date_line)
        self.finance_search_panel_1.addRow(self.date_desc)

        self.finance_search_group_1 = QGroupBox("Search by Date")
        self.finance_search_group_1.setLayout(self.finance_search_panel_1)
        self.finance_search_group_1.setCheckable(True)
        self.finance_search_group_1.setChecked(False)
        self.finance_search_group_1.toggled.connect(lambda: self.manage_checkbox(group=self.finance_search_group_1))

        # ---
        self.month_label = QLabel("MONTH :")
        self.month_combo = QComboBox()
        model = self.month_combo.model()

        for month in full_months:
            model.appendRow(QStandardItem(month))
        self.month_combo.setStyleSheet('color: black; selection-background-color: rgb(215,215,215)')

        self.month_desc = QLabel("Records for all transactions done in this particular month.")
        self.month_desc.setStyleSheet("font-size: 15px;")
        self.month_desc.setWordWrap(True)

        self.finance_search_panel_2 = QFormLayout()
        self.finance_search_panel_2.addRow(self.month_label, self.month_combo)
        self.finance_search_panel_2.addRow(self.month_desc)

        self.finance_search_group_2 = QGroupBox("Search by Month")
        self.finance_search_group_2.setLayout(self.finance_search_panel_2)
        self.finance_search_group_2.setCheckable(True)
        self.finance_search_group_2.setChecked(False)
        self.finance_search_group_2.toggled.connect(lambda: self.manage_checkbox(group=self.finance_search_group_2))

        self.go_button = QPushButton("SEARCH")
        self.go_button.setStyleSheet("font: bold")
        self.go_button.clicked.connect(lambda: self.set_headers())

        self.finance_search_layout = QVBoxLayout()
        self.finance_search_layout.addWidget(self.finance_search_group_0)
        self.finance_search_layout.addWidget(self.finance_search_group_1)
        self.finance_search_layout.addWidget(self.finance_search_group_2)
        self.finance_search_layout.addWidget(self.go_button)
        self.finance_search_layout.setSpacing(30)
        self.finance_search_layout.setContentsMargins(0, 0, 0, 0)

        # -- CELL ONE
        self.finance_result_table = QTableWidget()

        self.finance_result_layout = QVBoxLayout()
        self.finance_result_layout.addWidget(self.finance_result_table)

        self.finance_search_group_0.setStyle(QStyleFactory.create('Fusion'))
        self.finance_search_group_1.setStyle(QStyleFactory.create('Fusion'))
        self.finance_search_group_2.setStyle(QStyleFactory.create('Fusion'))

        self.flat_combo.setStyle(QStyleFactory.create('Fusion'))
        self.month_combo.setStyle(QStyleFactory.create('Fusion'))
        self.go_button.setStyle(QStyleFactory.create('Fusion'))
        self.finance_result_table.setStyle(QStyleFactory.create('Fusion'))

        # -- FINANCE SEARCH GRID
        self.grid.addLayout(self.finance_search_layout, 0, 0, 2, 1)
        self.grid.addLayout(self.finance_result_layout, 0, 1, 2, 5)

    def manage_checkbox(self, group):
        if group == self.finance_search_group_0 and group.isChecked():
            self.finance_search_group_0.setChecked(True)
            self.finance_search_group_1.setChecked(False)
            self.finance_search_group_2.setChecked(False)

        elif group == self.finance_search_group_1 and group.isChecked():
            self.finance_search_group_0.setChecked(False)
            self.finance_search_group_1.setChecked(True)
            self.finance_search_group_2.setChecked(False)

        elif group == self.finance_search_group_2 and group.isChecked():
            self.finance_search_group_0.setChecked(False)
            self.finance_search_group_1.setChecked(False)
            self.finance_search_group_2.setChecked(True)

    def set_headers(self):
        search_by = None

        if self.finance_search_group_0.isChecked():
            header_labels = ["Receipt ID", "Date", "Fee Month(s)", "Amount", "Fine", "Pay Mode", "Ref. No."]
            search_by = "flat"

        elif self.finance_search_group_1.isChecked():
            header_labels = ["Receipt ID", "Flat", "Name", "Fee Month(s)", "Amount", "Fine", "Pay Mode", "Ref. No."]
            search_by = "date"

        elif self.finance_search_group_2.isChecked():
            header_labels = ["Receipt ID", "Date", "Flat", "Name", "Fee Month(s)", "Amount", "Fine", "Pay Mode", "Ref. No."]
            search_by = "month"

        else:
            header_labels = []
        self.populate_table(search_by=search_by, column_count=len(header_labels), headers=header_labels)

    def populate_table(self, search_by, column_count: int, headers: list):
        self.finance_result_table.clearContents()
        content = []

        if search_by == "flat":
            content = get_search_content(search_by=search_by, search_attribute=self.flat_combo.currentText())

        elif search_by == "date":
            date = self.date_line.date().toPyDate()
            content = get_search_content(search_by=search_by, search_attribute=fix_date(str(date)))

        elif search_by == "month":
            content = get_search_content(search_by=search_by, search_attribute=str(self.month_combo.currentIndex()))

        self.finance_result_table.setRowCount(len(content))
        self.finance_result_table.setColumnCount(column_count)

        self.finance_result_table.setHorizontalHeaderLabels(headers)
        header = self.finance_result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        for index, row in enumerate(content):
            for inner_index, row_content in enumerate(row):
                table_item = QTableWidgetItem(str(row_content))
                table_item.setToolTip(str(row_content))

                if 'A - ' in str(row_content) or inner_index == 0:
                    table_item.setTextAlignment(Qt.AlignCenter)
                self.finance_result_table.setItem(index, inner_index, table_item)

    def set_name(self, flat):
        name = get_name(flat)
        self.name_value.setText(str(name))

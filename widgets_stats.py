from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFormLayout, QGroupBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout

from tools import get_stats_content, get_home_stats


class stats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.bold_font = QFont()
        self.bold_font.setBold(True)

        stats_content = get_home_stats()

        # -- LEVEL TWO GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(0, 1, 0, 1)
        self.setLayout(self.grid)

        # -- CELL ZERO

        self.stats_pie = QLabel()
        self.image = QPixmap('pie.png')
        self.resized_image = self.image.scaled(500, 500, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.stats_pie.setPixmap(self.resized_image)

        self.stats_pie.setAlignment(Qt.AlignCenter)

        self.currency_label = QLabel()
        currency_content = f"FUNDS COLLECTED IN JULY : {stats_content['funds']} INR"
        self.currency_label.setText(currency_content)
        self.currency_label.setWordWrap(True)
        self.currency_label.setStyleSheet("font: bold 10pt")

        self.funds_layout = QFormLayout()
        self.funds_layout.addRow(self.stats_pie)
        self.funds_layout.addRow(self.currency_label)
        self.funds_layout.setVerticalSpacing(10)

        self.funds_group = QGroupBox("Funds Status")
        self.funds_group.setLayout(self.funds_layout)

        # -- CELL ONE
        self.members_group = QGroupBox("Members Status")

        stats_content, defaulters = get_stats_content()

        self.stats_result_table = QTableWidget()

        self.stats_result_table.setRowCount(len(stats_content))
        self.stats_result_table.setColumnCount(3)
        self.stats_result_table.setHorizontalHeaderLabels(["Flat", "Name", "Fees Paid Upto"])

        for index, row in enumerate(stats_content):
            for inner_index, row_content in enumerate(row):
                table_item = QTableWidgetItem(str(row_content))

                if inner_index != 1:
                    table_item.setTextAlignment(Qt.AlignCenter)

                if index in defaulters:
                    table_item.setForeground(QBrush(QColor(249, 56, 34)))

                    if inner_index == 2:
                        table_item.setFont(self.bold_font)

                self.stats_result_table.setItem(index, inner_index, table_item)

        header = self.stats_result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.members_layout = QHBoxLayout()
        self.members_layout.addWidget(self.stats_result_table)

        self.members_group.setLayout(self.members_layout)

        # -- CELL TWO
        self.demo_group2 = QGroupBox("Additional Functions")

        # -- STATS GRID
        self.grid.addWidget(self.funds_group, 0, 0, 2, 1)
        self.grid.addWidget(self.members_group, 0, 1, 2, 2)
        self.grid.addWidget(self.demo_group2, 0, 3, 2, 1)

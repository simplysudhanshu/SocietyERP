import os
import subprocess

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFormLayout, QGroupBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QProgressBar, \
    QStyleFactory, QMessageBox

from src.main.python.Society_ERP.tools import get_stats_content, get_home_stats, flats, generate_files, currentMonth, all_months_values, \
    send_remainder, transfer_responsibility


def backup():
    generate_files(back_up=True, csv=False)
    user = os.environ['USERPROFILE']
    path = user + '\\Desktop\\SocietyERP\\Backup'
    subprocess.Popen(rf'explorer /select,{path}')


def csv():
    generate_files(back_up=False, csv=True)
    user = os.environ['USERPROFILE']
    path = user + '\\Desktop\\SocietyERP\\Excel Files'
    subprocess.Popen(rf'explorer /select,{path}')


class stats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyle(QStyleFactory.create('Fusion'))

        self.bold_font = QFont()
        self.bold_font.setBold(True)

        stats_content = get_home_stats()

        # -- LEVEL TWO GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(0, 1, 0, 1)
        self.setLayout(self.grid)

        # -- CELL ZERO
        self.funds_group = QGroupBox("Funds Status")

        self.stats_pie = QLabel()
        self.image = QPixmap('pie.png')
        self.resized_image = self.image.scaled(500, 500, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.stats_pie.setPixmap(self.resized_image)

        self.stats_pie.setAlignment(Qt.AlignCenter)

        self.currency_label = QLabel()
        currency_content = f"FUNDS COLLECTED IN {all_months_values[currentMonth-1].upper()} : {stats_content['funds']} INR"
        self.currency_label.setText(currency_content)
        self.currency_label.setWordWrap(True)
        self.currency_label.setAlignment(Qt.AlignCenter)
        self.currency_label.setStyleSheet("font: bold 10pt")

        self.funds_layout = QFormLayout()
        self.funds_layout.addRow(self.stats_pie)
        self.funds_layout.addRow(self.currency_label)
        self.funds_layout.setVerticalSpacing(10)

        self.funds_group.setLayout(self.funds_layout)

        # -- CELL ONE
        self.members_group = QGroupBox("Members Status")

        stats_content, self.defaulters = get_stats_content()

        self.stats_result_table = QTableWidget()

        self.stats_result_table.setRowCount(len(stats_content))
        self.stats_result_table.setColumnCount(3)
        self.stats_result_table.setHorizontalHeaderLabels(["Flat", "Name", "Fees Paid Upto"])

        for index, row in enumerate(stats_content):
            for inner_index, row_content in enumerate(row):
                table_item = QTableWidgetItem(str(row_content))

                if inner_index != 1:
                    table_item.setTextAlignment(Qt.AlignCenter)

                if index in self.defaulters:
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
        self.additional_layout = QVBoxLayout()

        self.remainder_group = QGroupBox("Remainders")

        self.backup_group = QGroupBox("Backup")
        self.excel_group = QGroupBox("Excel")

        self.backup_h = QHBoxLayout()
        self.backup_h.addWidget(self.backup_group)
        self.backup_h.addWidget(self.excel_group)

        self.responsibility_group = QGroupBox("Responsibility")

        self.additional_layout.addWidget(self.remainder_group)
        self.additional_layout.addLayout(self.backup_h)
        self.additional_layout.addWidget(self.responsibility_group)
        self.additional_layout.setSpacing(20)
        self.additional_layout.setContentsMargins(0, 0, 0, 0)

        # ---
        self.remainder_desc = QLabel("Send a mail to all the pending members for this month, as a remainder to pay the fees.")
        self.remainder_desc.setWordWrap(True)
        self.remainder_button = QPushButton("Send REMAINDERS")

        self.rbar = QProgressBar()
        self.rbar.setValue(0)
        self.rbar.setMaximum(100)
        self.rbar.setTextVisible(True)
        self.rbar.setFixedSize(472, 15)

        self.remainder_layout = QVBoxLayout()
        self.remainder_layout.addWidget(self.remainder_desc)
        self.remainder_layout.addWidget(self.remainder_button)
        self.remainder_layout.addWidget(self.rbar)
        self.remainder_group.setLayout(self.remainder_layout)
        self.remainder_group.setFixedWidth(500)

        # ---
        self.backup_desc = QLabel("Backup the current state of database, and save it online.")
        self.backup_desc.setWordWrap(True)
        self.backup_button = QPushButton("Generate BACKUP")
        self.backup_button.setToolTip("Backups are automatically generated at the start of every month.")

        self.backup_layout = QVBoxLayout()
        self.backup_layout.addWidget(self.backup_desc)
        self.backup_layout.addWidget(self.backup_button)

        self.backup_group.setLayout(self.backup_layout)

        self.excel_desc = QLabel("Generate an Excel file for current state of database.")
        self.excel_desc.setWordWrap(True)
        self.excel_button = QPushButton("Generate EXCEL")
        self.excel_button.setToolTip("Create Excel files of Members and Records.")

        self.excel_layout = QVBoxLayout()
        self.excel_layout.addWidget(self.excel_desc)
        self.excel_layout.addWidget(self.excel_button)

        self.excel_group.setLayout(self.excel_layout)

        # ---
        self.responsibility_desc = QLabel("Pass on the responsibility of fee collection to a different member.")

        self.responsibility_desc.setWordWrap(True)

        self.responsibility_combo = QComboBox()
        self.responsibility_combo.setStyle(QStyleFactory.create('Fusion'))

        model = self.responsibility_combo.model()

        for flat in flats:
            model.appendRow(QStandardItem(flat))

        self.responsibility_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')
        self.responsibility_combo.setFixedWidth(140)

        self.responsibility_button = QPushButton("TRANSFER")
        self.responsibility_button.setToolTip("This will send a mail with latest database and the software to new member.")

        self.responsibility_button.setStyle(QStyleFactory.create('Fusion'))

        self.responsibility_h = QHBoxLayout()
        self.responsibility_h.addWidget(self.responsibility_combo)
        self.responsibility_h.addWidget(self.responsibility_button)

        self.responsibility_layout = QVBoxLayout()
        self.responsibility_layout.addWidget(self.responsibility_desc)
        self.responsibility_layout.addLayout(self.responsibility_h)

        self.responsibility_group.setLayout(self.responsibility_layout)

        # -- FUNCTIONALITY
        self.backup_button.clicked.connect(backup)
        self.excel_button.clicked.connect(csv)
        self.responsibility_button.clicked.connect(self.transfer)
        self.remainder_button.clicked.connect(self.remainder)

        self.funds_group.setStyle(QStyleFactory.create('Fusion'))
        self.members_group.setStyle(QStyleFactory.create('Fusion'))
        self.stats_result_table.setStyle(QStyleFactory.create('Fusion'))

        # -- STATS GRID
        self.grid.addWidget(self.funds_group, 0, 0, 2, 1)
        self.grid.addWidget(self.members_group, 0, 1, 2, 2)
        self.grid.addLayout(self.additional_layout, 0, 3, 2, 1)

    def transfer(self):
        flat = self.responsibility_combo.currentText()
        transfer_status = transfer_responsibility(flat=flat)

        reply = QMessageBox()
        reply.setIcon(QMessageBox.Warning)

        if transfer_status == "Invalid":
            reply.setText(
                "The member does not have a Valid E-Mail ID. Cannot send the mail.")
        elif not transfer_status:
            reply.setText(
                "The system cannot access the internet. Make sure you have an active connection, or any firewall"
                "feature blocking the access.")
        else:
            reply.setText("Transfer Successful!")

        reply.setStandardButtons(QMessageBox.Ok)
        reply.setWindowTitle("INTERNET")
        reply.exec_()

    def remainder(self):
        self.backup_group.setEnabled(False)
        self.excel_group.setEnabled(False)
        self.responsibility_group.setEnabled(False)

        self.remainder_desc.setText("Sending Remainders.\nSystem WILL NOT RESPOND until its complete.")

        defaulters = [f"A - {x + 1}" for x in self.defaulters]
        self.rbar.setValue(1)

        for index, defaulter in enumerate(defaulters):
            send_remainder(defaulter=defaulter, month=all_months_values[currentMonth - 1])
            self.rbar.setValue((index+1)*100//len(defaulters))

        self.rbar.setValue(100)
        self.backup_group.setEnabled(True)
        self.excel_group.setEnabled(True)
        self.responsibility_group.setEnabled(True)
        self.rbar.setValue(0)

        self.remainder_desc.setText("Send a mail to all the pending members for this month, as a remainder to pay the fees.")
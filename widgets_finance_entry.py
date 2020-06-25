from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QHBoxLayout, QComboBox, QPushButton,\
    QFormLayout, QLineEdit, QRadioButton, QDateEdit, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from datetime import datetime

import receipt
import db_tools
from tools import create_spacer_item, fix_date, get_name

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


class finance_entry(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        intValidator = QIntValidator()

        # -- LEVEL TWO GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.setLayout(self.grid)

        # -- CELL ZERO
        self.receipt_label = QLabel("RECEIPT ID :")
        self.receipt_label.setWordWrap(True)

        self.receipt_id = QLabel()
        self.receipt_id.setStyleSheet("font: bold")
        self.receipt_id.setAlignment(Qt.AlignCenter)

        currentMonth = datetime.now().month
        currentYear = datetime.now().year

        currentReceipt = db_tools.generate_receipt_id(str(currentMonth), str(currentYear))
        self.receipt_id.setText(currentReceipt)

        # ---
        self.flat_label = QLabel("FLAT NO. :")
        self.flat_combo = QComboBox()
        model = self.flat_combo.model()

        for flat in flats:
            model.appendRow(QStandardItem(flat))

        self.flat_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')

        self.flat_combo.currentIndexChanged['QString'].connect(self.set_name)

        # ---
        self.name_label = QLabel("NAME :")
        self.name_value = QLabel("Mr D. S. Patil")
        self.name_value.setFixedWidth(200)

        # ---
        self.finance_entry_layout0 = QFormLayout()
        self.finance_entry_layout0.addRow(self.receipt_label, self.receipt_id)
        self.finance_entry_layout0.addRow(self.flat_label, self.flat_combo)
        self.finance_entry_layout0.addRow(self.name_label, self.name_value)
        self.finance_entry_layout0.setVerticalSpacing(80)

        # -- CELL ONE
        self.date_label = QLabel("DATE OF TRANSACTION :")
        self.date_label.setWordWrap(True)
        self.date_line = QDateEdit()
        self.date_line.setCalendarPopup(True)
        self.date_line.setDate(QDate.currentDate())

        self.setStyleSheet(QSS)

        self.single_radio = QRadioButton("Single Month")
        self.multiple_radio = QRadioButton("Multiple Months")
        self.single_radio.setChecked(True)

        self.single_radio.toggled.connect(lambda: self.months(button=self.single_radio))
        self.multiple_radio.toggled.connect(lambda: self.months(button=self.multiple_radio))

        self.finance_entry_layout1_h1 = QHBoxLayout()
        self.finance_entry_layout1_h1.addWidget(self.date_line)
        self.finance_entry_layout1_h1.addWidget(self.single_radio)
        self.finance_entry_layout1_h1.addWidget(self.multiple_radio)
        self.finance_entry_layout1_h1.setSpacing(30)

        # ---
        self.month_label = QLabel("FEES FOR :")
        self.month_combo = QComboBox()
        model = self.month_combo.model()

        for month in months:
            model.appendRow(QStandardItem(month))
        self.month_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')

        # ---
        self.month_till_label = QLabel("FEES TILL :")
        self.month_till_combo = QComboBox()
        model = self.month_till_combo.model()

        for month in months:
            model.appendRow(QStandardItem(month))
        self.month_till_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')

        self.finance_entry_layout1_h2 = QHBoxLayout()
        self.finance_entry_layout1_h2.addWidget(self.month_combo)
        self.finance_entry_layout1_h2.addWidget(self.month_till_label)
        self.finance_entry_layout1_h2.addWidget(self.month_till_combo)
        self.finance_entry_layout1_h2.setSpacing(30)

        self.month_till_label.setEnabled(False)
        self.month_till_combo.setEnabled(False)

        # ---
        self.amount_label = QLabel("AMOUNT :")
        self.amount_line = QLineEdit()

        self.amount_line.setValidator(intValidator)

        # ---
        self.fine_label = QLabel("FINE :")
        self.fine_line = QLineEdit()

        self.fine_line.setValidator(intValidator)

        self.finance_entry_layout1_h3 = QHBoxLayout()
        self.finance_entry_layout1_h3.addWidget(self.amount_line)
        self.finance_entry_layout1_h3.addWidget(self.fine_label)
        self.finance_entry_layout1_h3.addWidget(self.fine_line)
        self.finance_entry_layout1_h3.setSpacing(30)

        # ---
        self.finance_entry_layout1 = QFormLayout()
        self.finance_entry_layout1.addRow(self.date_label, self.finance_entry_layout1_h1)
        self.finance_entry_layout1.addRow(self.month_label, self.finance_entry_layout1_h2)
        self.finance_entry_layout1.addRow(self.amount_label, self.finance_entry_layout1_h3)
        self.finance_entry_layout1.setVerticalSpacing(80)

        # -- CELL TWO
        self.mode_label = QLabel("PAYMENT MODE :")
        self.mode_label.setWordWrap(True)

        # ---
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Cash")
        self.mode_combo.addItem("Online Funds Transfer")
        self.mode_combo.addItem("Cheque")

        self.mode_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')
        self.mode_combo.currentIndexChanged['QString'].connect(self.mode_selection)

        # ---
        self.ref_label = QLabel("REFERENCE ID :")
        self.ref_label.setWordWrap(True)
        self.ref_line = QLineEdit()

        self.ref_label.setDisabled(True)
        self.ref_line.setDisabled(True)

        self.save_button = QPushButton("SAVE")
        self.save_button.setStyleSheet("font: bold")
        self.save_button.clicked.connect(lambda: self.check_form())

        # ---
        self.finance_entry_layout2 = QFormLayout()
        self.finance_entry_layout2.addRow(self.mode_label, self.mode_combo)
        self.finance_entry_layout2.addRow(self.ref_label, self.ref_line)
        self.finance_entry_layout2.addItem(create_spacer_item(w=10, h=40))
        self.finance_entry_layout2.addRow(self.save_button)
        self.finance_entry_layout2.setVerticalSpacing(80)

        self.finance_entry_group0 = QGroupBox()
        self.finance_entry_group0.setLayout(self.finance_entry_layout0)

        self.finance_entry_group1 = QGroupBox()
        self.finance_entry_group1.setLayout(self.finance_entry_layout1)

        self.finance_entry_group2 = QGroupBox()
        self.finance_entry_group2.setLayout(self.finance_entry_layout2)

        # -- FINANCE ENTRY GRID
        self.grid.addWidget(self.finance_entry_group0, 0, 0, 2, 1)
        self.grid.addWidget(self.finance_entry_group1, 0, 1, 2, 1)
        self.grid.addWidget(self.finance_entry_group2, 0, 2, 2, 1)

    def months(self, button):
        if button.isChecked():
            if button.text() == "Single Month":
                self.month_till_label.setEnabled(False)
                self.month_till_combo.setEnabled(False)

            elif button.text() == "Multiple Months":
                self.month_till_label.setEnabled(True)
                self.month_till_combo.setEnabled(True)

    def mode_selection(self, selection):
        if selection == "Cash":
            self.ref_label.setText("REFERENCE ID :")
            self.ref_label.setDisabled(True)
            self.ref_line.setDisabled(True)

        elif selection == "Cheque":
            self.ref_label.setText("CHEQUE NO. :")
            self.ref_label.setDisabled(False)
            self.ref_line.setDisabled(False)

        elif selection == "Online Funds Transfer":
            self.ref_label.setText("REFERENCE ID :")
            self.ref_label.setDisabled(False)
            self.ref_line.setDisabled(False)

    def check_form(self):
        reply = QMessageBox()

        if len(self.amount_line.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("AMOUNTS field cannot be left empty.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        elif len(self.fine_line.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("FINE field cannot be left empty.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        elif self.ref_line.isEnabled() and len(self.ref_line.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("Please enter the REFERENCE INFORMATION for the transaction.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        else:
            self.add_entry()

            reply.setWindowTitle("SUCCESSFUL ENTRY")
            reply.setIcon(QMessageBox.Information)
            reply.setText("Entry has been recorded.")
            reply.setInformativeText("The entries can still be edited from the 'search' section.")
            reply.setDetailedText("Receipts for all entries will be sent to the members via their registered Email IDs at the end of session.")
            reply.setStandardButtons(QMessageBox.Ok)
            reply.exec_()

            self.name_value.clear()
            self.amount_line.clear()
            self.fine_line.clear()
            self.ref_line.clear()

    def set_name(self, flat):
        name = get_name(flat)
        self.name_value.setText(str(name))

    def add_entry(self):
        date = str(self.date_line.date().toPyDate())
        fee_month = str(self.month_combo.currentText())

        if self.month_till_combo.isEnabled():
            fee_till = self.month_till_combo.currentText()
        else:
            fee_till = ''

        flat = str(self.flat_combo.currentText())
        amount = float(self.amount_line.text())
        fine = float(self.fine_line.text())
        mode = str(self.mode_combo.currentText())

        if self.ref_line.isEnabled():
            ref = self.ref_line.text()
        else:
            ref = ''

        new_receipt = receipt.receipt(date=fix_date(date), flat=flat, month=fee_month, month_till=fee_till, amount=amount, fine=fine, mode=mode, ref=ref)
        new_receipt.add_to_db()

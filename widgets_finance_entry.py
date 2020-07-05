from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QHBoxLayout, QComboBox, QPushButton, \
    QFormLayout, QLineEdit, QRadioButton, QDateEdit, QMessageBox

import db_tools
import receipt
from tools import flats, create_spacer_item, fix_date, get_name, calculate_months, fix_date_back, calculate_fine, payment_exists

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
        self.setStyleSheet(QSS)
        self.current_pending_months = []
        self.current_advance_months = []

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
        self.finance_entry_layout0.setVerticalSpacing(90)

        # -- CELL ONE
        self.date_label = QLabel("DATE OF TRANSACTION :")
        self.date_label.setWordWrap(True)

        self.date_line = QDateEdit()
        self.date_line.setCalendarPopup(True)
        self.date_line.setDate(QDate.currentDate())
        self.date_line.setDisplayFormat("dd MMMM, yyyy")

        self.single_radio = QRadioButton("Single Month")
        self.multiple_radio = QRadioButton("Multiple Months")
        self.single_radio.setChecked(True)

        self.single_radio.toggled.connect(lambda: self.months(button=self.single_radio))
        self.multiple_radio.toggled.connect(lambda: self.months(button=self.multiple_radio))

        self.finance_entry_layout1_h1 = QHBoxLayout()
        self.finance_entry_layout1_h1.addWidget(self.date_line)
        self.finance_entry_layout1_h1.addWidget(self.single_radio)
        self.finance_entry_layout1_h1.addWidget(self.multiple_radio)
        self.finance_entry_layout1_h1.setSpacing(90)

        # ---
        self.month_label = QLabel("FEES FOR :")
        self.month_combo = QComboBox()
        self.set_pending_months()

        self.month_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')

        # ---
        self.month_till_label = QLabel("FEES TILL :")
        self.month_till_label.setAlignment(Qt.AlignCenter)
        self.month_till_combo = QComboBox()

        self.set_advance_months()

        self.month_till_combo.setStyleSheet('text-color: black; selection-background-color: rgb(215,215,215)')

        self.finance_entry_layout1_h2 = QHBoxLayout()
        self.finance_entry_layout1_h2.addWidget(self.month_combo)
        self.finance_entry_layout1_h2.addWidget(self.month_till_label)
        self.finance_entry_layout1_h2.addWidget(self.month_till_combo)
        self.finance_entry_layout1_h2.setSpacing(90)

        self.month_till_label.setEnabled(False)
        self.month_till_combo.setEnabled(False)

        # ---
        self.amount_label = QLabel("AMOUNT :")
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.amount_line = QLineEdit()
        self.amount_line.setText("1500")

        self.amount_line.setValidator(intValidator)

        # ---
        self.fine_label = QLabel("FINE :")
        self.fine_label.setAlignment(Qt.AlignCenter)
        self.fine_line = QLineEdit()
        self.fine_line.setText("0")

        self.fine_line.setValidator(intValidator)
        self.fine_line.setStyleSheet("border: 1px solid red; color: red")

        self.finance_entry_layout1_h3 = QHBoxLayout()
        self.finance_entry_layout1_h3.addWidget(self.amount_line)
        self.finance_entry_layout1_h3.addWidget(self.fine_label)
        self.finance_entry_layout1_h3.addWidget(self.fine_line)
        self.finance_entry_layout1_h3.setSpacing(90)

        # ---
        self.finance_entry_layout1 = QFormLayout()
        self.finance_entry_layout1.addRow(self.date_label, self.finance_entry_layout1_h1)
        self.finance_entry_layout1.addRow(self.month_label, self.finance_entry_layout1_h2)
        self.finance_entry_layout1.addRow(self.amount_label, self.finance_entry_layout1_h3)
        self.finance_entry_layout1.setVerticalSpacing(90)

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

        self.total_label = QLabel(f"TOTAL PAYABLE AMOUNT : {int(self.amount_line.text()) + int(self.fine_line.text())}")
        self.total_label.setWordWrap(True)
        self.total_label.setAlignment(Qt.AlignCenter)

        self.save_button = QPushButton("SAVE")
        self.save_button.setStyleSheet("font: bold")
        self.save_button.clicked.connect(lambda: self.check_form())

        # ---
        self.finance_entry_layout2 = QFormLayout()
        self.finance_entry_layout2.addRow(self.mode_label, self.mode_combo)
        self.finance_entry_layout2.addRow(self.ref_label, self.ref_line)
        self.finance_entry_layout2.addItem(create_spacer_item(w=5, h=30))
        self.finance_entry_layout2.addRow(self.total_label)
        self.finance_entry_layout2.addRow(self.save_button)
        self.finance_entry_layout2.setVerticalSpacing(80)

        self.finance_entry_group0 = QGroupBox()
        self.finance_entry_group0.setLayout(self.finance_entry_layout0)

        self.finance_entry_group1 = QGroupBox()
        self.finance_entry_group1.setLayout(self.finance_entry_layout1)

        self.finance_entry_group2 = QGroupBox()
        self.finance_entry_group2.setLayout(self.finance_entry_layout2)
        self.finance_entry_group2.setFixedWidth(550)

        # -- FUNCTIONALITY:
        self.date_line.dateChanged.connect(lambda: self.set_pending_months(date=str(self.date_line.date().toPyDate())))

        self.month_combo.currentIndexChanged['QString'].connect(self.set_advance_months)

        self.month_combo.currentIndexChanged['QString'].connect(lambda ind: self.calculate_fine('from', ind))
        self.month_till_combo.currentIndexChanged['QString'].connect(lambda ind: self.calculate_fine('till', ind))

        self.month_combo.currentTextChanged.connect(self.calculate_amount)
        self.month_till_combo.currentTextChanged.connect(self.calculate_amount)

        self.amount_line.textChanged.connect(self.set_total)
        self.fine_line.textChanged.connect(self.set_total)

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

        self.calculate_amount()

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

        elif payment_exists(flat=self.flat_combo.currentText(), month=self.month_combo.currentText()):
            reply.setIcon(QMessageBox.Warning)
            reply.setText(f"This member ({self.flat_combo.currentText()}) has already paid the fees for the month of {self.month_combo.currentText()}")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        else:
            if self.month_till_combo.isEnabled():
                fee_till = f" - {self.month_till_combo.currentText()}"
            else:
                fee_till = ''

            if self.ref_line.isEnabled():
                ref = f" - ({self.ref_line.text()})"
            else:
                ref = ''

            detailed_text = f"Date : {fix_date(str(self.date_line.date().toPyDate()))}\n" \
                            f"Fee for : {str(self.month_combo.currentText())}{fee_till}\n" \
                            f"Flat No : {str(self.flat_combo.currentText())}\n" \
                            f"Amount : {float(self.amount_line.text())}\n" \
                            f"Fine : {float(self.fine_line.text())}\n" \
                            f"    -> TOTAL : {str(int(self.amount_line.text()) + int(self.fine_line.text()))} <-\n" \
                            f"Payment Mode : {str(self.mode_combo.currentText())}{ref}"

            reply.setWindowTitle("SUCCESSFUL ENTRY")
            reply.setIcon(QMessageBox.Information)
            reply.setText("ENTRY HAS BEEN RECORDED.\n")
            reply.setInformativeText("Please confirm the details below.")
            reply.setDetailedText(detailed_text)
            confirm_button = reply.addButton('Confirm', QMessageBox.AcceptRole)
            edit_button = reply.addButton('Edit', QMessageBox.RejectRole)

            confirm_button.clicked.connect(lambda: self.final_clicked(button=confirm_button))
            edit_button.clicked.connect(lambda: self.final_clicked(button=edit_button))
            reply.exec_()

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

        new_receipt = receipt.receipt(date=fix_date(date), flat=flat, month=fee_month, month_till=fee_till,
                                      amount=amount, fine=fine, mode=mode, ref=ref)
        new_receipt.add_to_db()

    def final_clicked(self, button):
        if button.text() == "Confirm":
            self.add_entry()

            currentReceipt = db_tools.generate_receipt_id(str(datetime.now().month), str(datetime.now().year))
            self.receipt_id.setText(currentReceipt)
            self.flat_combo.setCurrentIndex(0)
            self.name_value.setText("Mr D. S. Patil")
            self.amount_line.setText('0')
            self.fine_line.setText('0')
            self.ref_line.clear()

    def set_pending_months(self, date: str = None):
        if date is None:
            date = str(self.date_line.date().toPyDate())

        months = calculate_months(month=date, pending=True, advance=False)

        self.current_pending_months = months

        self.month_combo.clear()

        model = self.month_combo.model()
        for month in months:
            model.appendRow(QStandardItem(month))

    def set_advance_months(self, date: str = None):
        if date is None or date == '':
            date = fix_date_back(self.current_pending_months[0])
        else:
            date = fix_date_back(date)

        months = calculate_months(month=date, pending=False, advance=True)

        self.current_advance_months = months

        self.month_till_combo.clear()
        model = self.month_till_combo.model()

        for month in months:
            model.appendRow(QStandardItem(month))

    def calculate_amount(self):
        if self.month_combo.count() == 0 or self.month_till_combo.count() == 0:
            self.amount_line.setText('0')
            return

        else:
            all_possible_months = self.current_advance_months.copy()
            all_possible_months = all_possible_months[::-1]

            all_possible_months.extend([x for x in self.current_pending_months if x not in self.current_advance_months])

            if self.month_till_combo.isEnabled():
                from_index = all_possible_months.index(self.month_combo.currentText())
                till_index = all_possible_months.index(self.month_till_combo.currentText())

                amount = (from_index - till_index + 1) * 1500

            else:
                amount = 1500

            self.amount_line.setText(str(amount))
            self.amount_line.setToolTip(f"Total months : {amount//1500}")

    def calculate_fine(self, from_where: str, month):
        if month == '' and self.month_combo.count() == 0 or self.month_till_combo.count() == 0:
            self.fine_line.setText('0')
            return

        else:
            if self.month_till_combo.isEnabled():
                try:
                    till_index = self.current_pending_months.index(str(self.month_till_combo.currentText()))
                except ValueError:
                    till_index = 0
            else:
                try:
                    till_index = self.current_pending_months.index(str(self.month_combo.currentText()))
                except ValueError:
                    self.fine_line.setText('0')
                    return

            try:
                from_index = self.current_pending_months.index(str(self.month_combo.currentText()))
            except ValueError:
                self.fine_line.setText('0')
                return

            all_fine_months = []

            for month in self.current_pending_months[till_index:from_index+1]:
                all_fine_months.append([month])

            transact_date = str(self.date_line.date().toPyDate())

            total_fine = 0
            for month in all_fine_months:
                fine = calculate_fine(month=month[0], transact_date=fix_date(transact_date))
                month = month.append(fine)

                total_fine += fine*50

            self.fine_line.setText(str(total_fine))
            self.set_fine_tip(all_fine_months=all_fine_months)

    def set_fine_tip(self, all_fine_months: list):
        tool_line = ''

        for month in all_fine_months:
            tool_line += f"{month[0]} x {month[1]}\n"

        self.fine_line.setToolTip(tool_line)

    def set_total(self):
        if len(self.amount_line.text()) > 0:
            amount = int(self.amount_line.text())
        else:
            amount = 0

        if len(self.fine_line.text()) > 0:
            fine = int(self.fine_line.text())
        else:
            fine = 0

        self.total_label.setText(f"TOTAL PAYABLE AMOUNT : {amount + fine}")

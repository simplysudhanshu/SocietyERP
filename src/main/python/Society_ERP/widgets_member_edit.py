from PyQt5.QtGui import QStandardItem, QIntValidator
from PyQt5.QtWidgets import QWidget, QStyleFactory, QGridLayout, QLabel, QComboBox, QGroupBox, QFormLayout, QLineEdit, \
    QPushButton, QMessageBox, QInputDialog

from src.main.python.Society_ERP import db_tools
from src.main.python.Society_ERP.tools import flat_numbers, wings, verify_code, create_spacer_item


class member_edit(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyle(QStyleFactory.create('Fusion'))
        intValidator = QIntValidator()

        # -- LEVEL TWO GRID
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.setLayout(self.grid)

        # -- CELL ZERO
        self.member_desc = QLabel("Choose the details of the flat-holder, to update the information.")

        self.wing_label = QLabel("WING :")
        self.wing_label.setStyle(QStyleFactory.create('Fusion'))

        self.wing_combo = QComboBox()
        self.wing_combo.setStyle(QStyleFactory.create('Fusion'))
        model = self.wing_combo.model()

        for wing in wings:
            model.appendRow(QStandardItem(wing))

        self.wing_combo.setStyleSheet('color: black; selection-background-color: rgb(215,215,215)')
        self.wing_combo.setFixedWidth(180)

        # ---
        self.flat_label = QLabel("FLAT NO. :")
        self.flat_label.setStyle(QStyleFactory.create('Fusion'))

        self.flat_combo = QComboBox()
        self.flat_combo.setStyle(QStyleFactory.create('Fusion'))
        model = self.flat_combo.model()

        model.appendRow(QStandardItem(""))

        for flat in flat_numbers:
            model.appendRow(QStandardItem(flat))

        self.flat_combo.setStyleSheet('color: black; selection-background-color: rgb(215,215,215)')
        self.flat_combo.setCurrentText("")
        self.flat_combo.setFixedWidth(180)

        self.member_search = QFormLayout()
        self.member_search.addRow(self.member_desc)
        self.member_search.addRow(self.wing_label, self.wing_combo)
        self.member_search.addRow(self.flat_label, self.flat_combo)
        self.member_search.setVerticalSpacing(80)
        self.member_search.setContentsMargins(40, 10, 40, 10)

        # -- CELL ONE
        self.name_label = QLabel("Name of flat-holder :")
        self.name_value = QLineEdit()
        self.name_value.setFixedWidth(450)

        self.current_label = QLabel("Current occupant of the flat :")
        self.current_label.setWordWrap(True)
        self.current_value = QLineEdit()
        self.current_value.setFixedWidth(450)

        self.contact_label = QLabel("Contact Details :")
        self.contact_value = QLineEdit()
        self.contact_value.setFixedWidth(450)
        self.contact_value.setValidator(intValidator)

        self.email_label = QLabel("Email ID :")
        self.email_value = QLineEdit()
        self.email_value.setFixedWidth(450)

        self.save_button = QPushButton("SAVE")
        self.save_button.setEnabled(False)
        self.save_button.setFixedWidth(640)
        self.save_button.setToolTip("This will update the master database with new details.")

        self.details = QFormLayout()
        self.details.addRow(self.name_label, self.name_value)
        self.details.addRow(self.current_label, self.current_value)
        self.details.addItem(create_spacer_item(w=10, h=20))
        self.details.addRow(self.contact_label, self.contact_value)
        self.details.addRow(self.email_label, self.email_value)
        self.details.addItem(create_spacer_item(w=10, h=20))
        self.details.addRow(self.save_button)

        self.details.setVerticalSpacing(30)
        self.details.setContentsMargins(100, 10, 100, 10)
        self.details.setHorizontalSpacing(30)

        # -- GROUP BOX
        self.search_group = QGroupBox()
        self.search_group.setLayout(self.member_search)

        self.details_group = QGroupBox()
        self.details_group.setLayout(self.details)

        # -- FUNCTIONALITY
        self.flat_combo.currentIndexChanged['QString'].connect(self.set_member)
        self.save_button.clicked.connect(self.check_form)

        # -- MEMBER EDIT GRID
        self.grid.addWidget(self.search_group, 0, 0, 2, 1)
        self.grid.addWidget(self.details_group, 0, 1, 2, 2)

    def set_member(self, flat):
        name = ""
        current = ""
        contact = ""
        email = ""

        if flat == "":
            self.save_button.setEnabled(False)

        else:
            wing = self.wing_combo.currentText()
            data = db_tools.get_from_db(table="members", attribute="*", key="flat", value=f"{wing} - {flat}")
            if len(data) > 0:

                data = data[0]

                name = data[1]
                current = data[2]
                contact = str(data[3])
                email = data[4]

            self.save_button.setEnabled(True)

        self.name_value.setText(name)
        self.current_value.setText(current)
        self.contact_value.setText(contact)
        self.email_value.setText(email)

    def check_form(self):
        reply = QMessageBox()

        if len(self.name_value.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("NAME field cannot be left empty.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        elif len(self.current_value.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("CURRENT field cannot be left empty.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        elif len(self.contact_value.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("CONTACT field cannot be left empty.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        elif len(self.email_value.text()) == 0:
            reply.setIcon(QMessageBox.Warning)
            reply.setText("EMAIL field cannot be left empty.")
            reply.setStandardButtons(QMessageBox.Retry)
            reply.setWindowTitle("INVALID ENTRY")
            reply.exec_()

        else:
            code, ok = QInputDialog().getText(self, "Security", "Enter the authentication code:")

            if verify_code(code) and ok:

                detailed_text = f"Flat No : {self.wing_combo.currentText()} - {str(self.flat_combo.currentText())}\n"\
                                f"Name : {self.name_value.text()}\n" \
                                f"Current : {self.current_value.text()}\n" \
                                f"Contact : {self.contact_value.text()}\n" \
                                f"Email : {self.email_value.text()}\n" \


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

            else:
                reply.setIcon(QMessageBox.Critical)
                reply.setText("Transaction cannot be edited without the valid code.")
                reply.setWindowTitle("INVALID Code")
                reply.exec_()

    def final_clicked(self, button):
        if button.text() == "Confirm":
            self.update_entry()

            self.flat_combo.setCurrentText("")

    def update_entry(self):
        wing = self.wing_combo.currentText()
        flat = self.flat_combo.currentText()
        name = self.name_value.text()
        current = self.current_value.text()
        contact = self.contact_value.text()
        email = self.email_value.text()

        db_tools.update_db(table="members", identifier=f"{wing} - {flat}", all_attributes=[name, current, contact, email])
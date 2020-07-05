import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QDesktopWidget, QMessageBox)

import widgets_home


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.home = widgets_home.center_widget(self)

        self.initUI()

    def initUI(self):
        self.resize(1550, 950)
        self.setWindowTitle('SMGRP - II')
        self.setWindowIcon(QIcon('icon.png'))
        self.center()

        self.setCentralWidget(self.home)
        self.statusBar().showMessage('SocietyERP')

        self.setStyleSheet("background-color: white; font: 10pt Arial")

        self.showMaximized()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Confirm',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QMainWindow,
                             QDesktopWidget, QMessageBox, QStyleFactory)
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import src.main.python.Society_ERP.widgets_home as widgets_home


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.home = widgets_home.center_widget(self)
        self.setStyle(QStyleFactory.create('Fusion'))
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
    appctxt = ApplicationContext()
    ex = Example()
    ex.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

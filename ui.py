import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QToolTip, QMainWindow,
                             QDesktopWidget, QMessageBox)

import widget_classes


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.home = widget_classes.home(self)

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.resize(1550, 950)
        self.setWindowTitle('SMGRP - II')
        self.setWindowIcon(QIcon('icon.png'))
        self.center()

        self.setCentralWidget(self.home)
        self.statusBar().showMessage('Ready')
        self.setToolTip('This is a <b>QWidget</b> widget')

        self.setStyleSheet("background-color: white; font: 10pt Arial")

        self.show()

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

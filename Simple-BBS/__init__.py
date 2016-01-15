#! coding:utf-8
"""
__init__.py

Created by 0160929 on 2016/01/15 12:26
"""
__version__ = '0.0'

import os
import sys

from PySide.QtGui import *
from PySide.QtCore import *


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("__init__.py")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(640, 480)


def main():
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

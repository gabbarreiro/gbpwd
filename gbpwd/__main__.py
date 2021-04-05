import os

from PySide2.QtWidgets import *

from . import gui

if __name__ == '__main__':
    app = QApplication()

    main = gui.CompleteMainGui()
    main.show()

    app.exec_()

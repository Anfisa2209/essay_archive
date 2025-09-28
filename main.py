# pyuic6 -o forms/python_forms/main_window.py forms/UI_forms/main_window.ui.ui
import sys

from PyQt6.QtWidgets import QApplication

from windows.main_page import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

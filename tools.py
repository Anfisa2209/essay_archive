from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox


cur_dir = Path(__file__).parent
essay_path = cur_dir.parent / "essay_archive_project" / "essays"


def set_parameters(window):
    window.setWindowTitle('Архив сочинений')
    app_icon = QIcon('images/icon.png')
    window.setWindowIcon(app_icon)


def showMessageBox(text, info='', show_buttons=False, icon=QMessageBox.Icon.Warning):
    msg = QMessageBox()
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setIcon(icon)

    if show_buttons:
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Cancel)
        msg.exec()
        return msg.result() == QMessageBox.StandardButton.Yes
    else:
        msg.exec()
        return True


def count_words(filename):
    filename = filename + '.txt'
    try:
        filename = essay_path / filename

        with open(filename, encoding='utf-8') as f:
            words = [word for line in f for word in line.strip().split()]
        return len(words)
    except FileNotFoundError:
        print(f'Файл {filename} не найден')
        return 0



import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from bd.sqlite import get_all_genres, load_essay_data
from forms.python_forms.main_window import Ui_MainWindow
from tools import set_parameters


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        set_parameters(self)
        self.add_essay_btn.clicked.connect(self.add_essay)
        self.view_literature_btn.clicked.connect(self.view_literature)
        self.view_authors_btn.clicked.connect(self.view_authors)
        self.view_essays_btn.clicked.connect(self.view_essays)
        self.ege_essay_btn.clicked.connect(self.open_ege_essays)
        self.final_essay_btn.clicked.connect(self.open_final_essays)
        self.buttons = [self.view_literature_btn, self.view_authors_btn, self.view_essays_btn, self.add_essay_btn]

        genres = ['Выберете тему'] + get_all_genres()
        self.genre_combo_box.addItems(genres)
        self.genre_combo_box.currentIndexChanged.connect(self.genre_selected)

    def add_essay(self):
        self.check_genre()
        from windows.add_essay import EssayWindow
        self.window = EssayWindow(genre=self.genre)
        self.window.show()
        self.close()

    def check_genre(self):
        self.genre = self.genre_combo_box.currentText()
        if self.genre == 'Выберете тему':
            self.genre = None

    def open_final_essays(self):
        from windows.view_essays import MainWindow as EssayWindow
        essay_data = load_essay_data(essay_type='итоговое сочинение')

        self.essay_window = EssayWindow(essay_data)
        self.essay_window.show()
        self.close()

    def open_ege_essays(self):
        from windows.view_essays import MainWindow as EssayWindow
        essay_data = load_essay_data(essay_type='сочинение егэ')

        self.essay_window = EssayWindow(essay_data)
        self.essay_window.show()
        self.close()

    def view_literature(self):
        ...

    def view_authors(self):
        ...

    def view_essays(self):
        self.check_genre()
        from windows.view_essays import MainWindow as EssayWindow
        essay_data = load_essay_data(self.genre)
        self.essay_window = EssayWindow(essay_data)
        self.essay_window.show()
        self.close()

    def genre_selected(self):
        # в выпадающем списке выбрали какую-то тему и хотят прочитать по ней сочинения
        current_genre = self.genre_combo_box.currentText().lower()
        if current_genre == 'выберете тему':
            self.view_essays_btn.setText(f'Посмотреть все \nсочинения')
            self.add_essay_btn.setText(f'Добавить сочинение')
            self.view_authors_btn.setText(f'Посмотреть всех\n авторов')
            self.view_literature_btn.setText("Посмотреть все \nпроизведения")
        else:
            self.view_essays_btn.setText(f'Посмотреть сочинения на тему: \n{current_genre}')
            self.add_essay_btn.setText(f'Добавить сочинение на тему: \n{current_genre}')
            self.view_authors_btn.setText(f'Авторы, пишущие на тему: \n{current_genre}')
            self.view_literature_btn.setText(f'Произведения, с темой: \n{current_genre}')

        for btn in self.buttons:
            btn.adjustSize()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

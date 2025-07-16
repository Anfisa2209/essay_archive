from PyQt6.QtWidgets import (
    QMainWindow, QListWidget, QMessageBox
)

from bd.sqlite import get_all_genres, add_essay, get_all_literature, literature_exists, all_data
from forms.python_forms.add_essay import Ui_MainWindow
from tools import set_parameters, showMessageBox


def selected_info(list_widget: QListWidget):
    # возвращает все данные из QListWidget
    items = [list_widget.item(x).text() for x in range(list_widget.count())]
    return sorted(set(items))


class EssayWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, genre=None, essay_id=0):
        super().__init__()
        self.setupUi(self)
        self.initUI(genre, essay_id)

    def initUI(self, genre, essay_id):
        self.essay_id = essay_id
        if self.essay_id:
            self.fill_data()
        else:
            self.literature_list.setVisible(False)
            self.genre_list.setVisible(False)
        set_parameters(self)

        self.go_home_btn.clicked.connect(self.go_home)
        self.save_btn.clicked.connect(self.save)
        self.literature_combo_box.addItems(['Реальная жизнь/исторический опыт'] + get_all_literature())


        self.genre_list.itemDoubleClicked.connect(self.remove_genre)
        self.literature_list.itemDoubleClicked.connect(self.remove_literature)

        genre_combo_line_edit = self.genre_combo_box.lineEdit()
        literature_combo_line_edit = self.literature_combo_box.lineEdit()
        # Подключаем сигнал нажатия Enter

        genre_combo_line_edit.returnPressed.connect(self.add_genre_to_list)
        literature_combo_line_edit.returnPressed.connect(self.add_literature_to_list)

        genres = get_all_genres()
        self.genre_combo_box.addItems(genres)
        if genre:
            self.genre_combo_box.setCurrentText(genre)
            self.add_genre_to_list()

    def add_genre_to_list(self):
        text = self.genre_combo_box.currentText().strip()
        if not text:
            return

        self.genre_list.addItem(text)
        self.genre_combo_box.lineEdit().clear()

        # Прокрутка к новому элементу
        self.genre_list.scrollToBottom()
        self.update_visible()

    def add_literature_to_list(self):
        text = self.literature_combo_box.currentText().strip()
        if not text:
            return
        self.literature_list.addItem(text)
        if not literature_exists(text):
            self.unknown_author_lbl.setText(f'Кто написал произведение "{text}"? Введите ФИО автора')
            self.unknown_author_lbl.setVisible(True)
            self.unknown_author_edit.setVisible(True)
        self.literature_combo_box.lineEdit().clear()

        # Прокрутка к новому элементу
        self.literature_list.scrollToBottom()
        self.update_visible()

    def remove_genre(self, item):
        # Получаем индекс элемента
        row = self.genre_list.row(item)
        # Удаляем элемент
        self.genre_list.takeItem(row)
        self.update_visible()

    def remove_literature(self, item):
        # Получаем индекс элемента
        row = self.literature_list.row(item)
        # Удаляем элемент
        self.literature_list.takeItem(row)
        self.update_visible()

    def update_visible(self):
        self.genre_list.setVisible(bool(self.genre_list.count()))
        self.literature_list.setVisible(bool(self.literature_list.count()))
        if not self.literature_list.count():
            self.unknown_author_lbl.setVisible(False)
            self.unknown_author_edit.setVisible(False)

    def save(self):
        title = self.title.text().strip('?!*"><\/')
        text = self.essay_text.toPlainText()
        selected_genres = selected_info(self.genre_list)
        selected_literature = selected_info(self.literature_list)
        if not title:
            showMessageBox(text='Незаполненное поле!', info='Введите название сочинения')
            self.title.setStyleSheet('border: rgb(255, 0, 0);')
            return
        if not text:
            showMessageBox(text='Незаполненное поле!', info='Вставьте текст сочинения')
            self.essay_text.setStyleSheet('border: red;')
            return
        if not (selected_genres or selected_literature):
            showMessageBox(text='Незаполненное поле!',
                           info='Выберете, на какую тему написано или какие произведения использовали. '
                                'Выберите из списка или введите нужную информацию, а потом нажмите Enter. '
                                'Чтобы удалить, дважды нажмите на лишний элемент.')
            return

        author = self.unknown_author_edit.text()
        if self.unknown_author_lbl.isVisible():
            unknown_literature = self.unknown_author_lbl.text().split('?')[0].split('"')[1]
        else:
            unknown_literature = ''

        if add_essay(title, text, selected_genres, selected_literature, unknown_literature, author):
            showMessageBox('Успешно!', icon=QMessageBox.Icon.Information)
        else:
            showMessageBox('Что-то пошло нет!')

    def go_home(self):
        from windows.main_page import MainWindow
        self.window = MainWindow()
        self.window.show()
        self.close()

    def closeEvent(self, event):
        ...
        # if self.essay_text.toPlainText() != '':
        #     answer = showMessageBox("Вы уверены, что хотите выйти?",
        #                             info='Если вы выйдите, изменения НЕ будут сохранены', show_buttons=True)
        #     if answer:
        #         event.accept()  # Закрыть окно
        #     else:
        #         event.ignore()  # Оставить окно открытым
        # else:
        #     # Если текста нет, то разрешаем закрытие (это поведение по умолчанию)
        #     event.accept()

    def fill_data(self):
        data = all_data(self.essay_id)
        self.title.setText(data['title'])
        self.essay_text.setText(data['text'])

        # Очищаем списки перед добавлением
        self.genre_list.clear()
        self.literature_list.clear()

        # Добавляем элементы
        if data['genres']:  # Проверяем, что список не пустой
            self.genre_list.addItems(data['genres'])

        if data['literature_list']:  # Проверяем, что список не пустой
            self.literature_list.addItems(data['literature_list'])

        # Обновляем видимость после добавления элементов
        self.update_visible()
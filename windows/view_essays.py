from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QScrollArea, QLabel, QFrame, QSizePolicy, QPushButton, QHBoxLayout
)

from tools import set_parameters


class EssayWidget(QFrame):
    clicked = pyqtSignal(int)  # Сигнал с ID сочинения

    def __init__(self, essay_id, title, topics, word_count, essay_type, parent=None):
        super().__init__(parent)
        self.essay_id = essay_id

        # Настройка стиля блока
        self.setStyleSheet("""
            EssayWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 10px;
            }
            EssayWidget:hover {
                background-color: #f0f0f0;
                border-color: #aaa;
                cursor: pointer;
            }
        """)

        # Основной лейаут
        layout = QVBoxLayout(self)

        # Название
        title_label = QLabel(f"<h3>{title}</h3>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Темы
        topics_text = ", ".join(topics)  # topics - список строк
        topics_label = QLabel(f"<b>Темы:</b> {topics_text}")
        topics_label.setStyleSheet('font-size:14px;')

        # тип сочинения
        essay_type_label = QLabel(f"<b>Тип сочинения:</b> {essay_type}")

        # Количество слов
        count_label = QLabel(f"<b>Кол-во слов:</b> {word_count}")

        # Добавляем элементы
        layout.addWidget(title_label)
        layout.addWidget(topics_label)
        layout.addWidget(essay_type_label)
        layout.addWidget(count_label)

        # Опционально: растягиваем по ширине
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

    def mousePressEvent(self, event):
        """Обработка клика по виджету"""
        self.clicked.emit(self.essay_id)
        self.animate_click()

    def animate_click(self):
        animation = QPropertyAnimation(self, b"color")
        animation.setDuration(200)
        animation.setStartValue(QColor("#e0e0e0"))
        animation.setEndValue(QColor("#f0f0f0"))
        animation.start()


class MainWindow(QMainWindow):
    def __init__(self, essays_data):
        super().__init__()
        set_parameters(self)
        self.setGeometry(300, 50, 933, 753)
        self.setStyleSheet("""
            .QPushButton {
                width: 100px;
                height: 100px;
                background-color: #e6ad85;
                margin: 10px;
                border-radius: 5px;
                font-size: 20px;
                word-wrap: break-word;
                cursor: Pointing-Hand;   
            }
            .QPushButton:hover {
                background-color: rgb(201, 152, 117);
            }
            .QWidget {
                background-color: rgb(240, 221, 192);
            }
        """)

        # Основные виджеты
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Создаем кнопку "На главную" и добавляем ее в layout
        self.go_back_btn = QPushButton('На главную')
        self.go_back_btn.setFixedSize(141, 61)
        self.go_back_btn.clicked.connect(self.open_home_page)

        # Создаем горизонтальный layout для кнопки (чтобы можно было выровнять слева)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.go_back_btn)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        button_layout.setContentsMargins(20, 20, 0, 20)

        main_layout.addLayout(button_layout)

        # Создаем прокручиваемую область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Контейнер для блоков
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Проверяем, есть ли сочинения
        if not essays_data:
            # Если сочинений нет, показываем сообщение
            no_essays_label = QLabel("Сочинений по этой теме еще нет")
            no_essays_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_essays_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: #666;
                    padding: 50px;
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
            container_layout.addWidget(no_essays_label)
        else:
            # Создаем блоки для каждого сочинения
            for essay in essays_data:
                essay_id, title, topics, word_count, essay_type = essay
                widget = EssayWidget(essay_id, title, topics, word_count, essay_type)
                widget.clicked.connect(self.open_essay)
                container_layout.addWidget(widget)

        # Настройка прокрутки
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        self.setCentralWidget(main_widget)

    def open_essay(self, essay_id):
        """Обработчик клика по сочинению"""
        from windows.add_essay import EssayWindow
        self.essay_window = EssayWindow(essay_id=essay_id)
        self.essay_window.show()
        self.close()

    def open_home_page(self):
        from windows.main_page import MainWindow
        self.window = MainWindow()
        self.window.show()
        self.close()

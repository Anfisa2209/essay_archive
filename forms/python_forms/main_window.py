# Form implementation generated from reading ui file './forms/UI_forms/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.9.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(300, 50, 933, 753)
        MainWindow.setStyleSheet(".QPushButton {\n"
                                 "    width: 100px;\n"
                                 "    height: 100px;\n"
                                 "    background-color:#e6ad85;\n"
                                 "    margin: 10px;\n"
                                 "    border-radius: 5px;\n"
                                 "    font-size:20px;\n"
                                 "    word-wrap: break-word;\n"
                                 "    cursor: Pointing-Hand;   \n"
                                 "}\n"
                                 ".QPushButton:hover {\n"
                                 "    background-color: rgb(201, 152, 117);\n"
                                 "}\n"
                                 ".QWidget {\n"
                                 "background-color: rgb(240, 221, 192);\n"
                                 "\n"
                                 "}"
                                 )
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(140, 100, 641, 511))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.genre_combo_box = QtWidgets.QComboBox(parent=self.widget)
        self.genre_combo_box.setMinimumSize(QtCore.QSize(0, 50))
        self.genre_combo_box.setMaximumSize(QtCore.QSize(16777215, 50))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.genre_combo_box.setFont(font)

        self.genre_combo_box.setCurrentText("")
        self.genre_combo_box.setObjectName("genre_combo_box")
        self.verticalLayout.addWidget(self.genre_combo_box)
        spacerItem = QtWidgets.QSpacerItem(5, 10, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.add_essay_btn = QtWidgets.QPushButton(parent=self.widget)
        self.add_essay_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_essay_btn.setMouseTracking(False)
        self.add_essay_btn.setObjectName("add_essay_btn")
        self.gridLayout.addWidget(self.add_essay_btn, 0, 0, 1, 1)
        self.view_literature_btn = QtWidgets.QPushButton(parent=self.widget)
        self.view_literature_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.view_literature_btn.setObjectName("view_literature_btn")
        self.gridLayout.addWidget(self.view_literature_btn, 1, 0, 1, 1)
        self.view_authors_btn = QtWidgets.QPushButton(parent=self.widget)
        self.view_authors_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.view_authors_btn.setObjectName("view_authors_btn")
        self.gridLayout.addWidget(self.view_authors_btn, 1, 1, 1, 1)
        self.view_essays_btn = QtWidgets.QPushButton(parent=self.widget)
        self.view_essays_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.view_essays_btn.setObjectName("view_essays_btn")
        self.gridLayout.addWidget(self.view_essays_btn, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_essay_btn.setText(_translate("MainWindow", "Добавить сочинение"))
        self.view_literature_btn.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.view_literature_btn.setText(_translate("MainWindow", "Посмотреть все \n"
                                                                  "произведения"))
        self.view_authors_btn.setText(_translate("MainWindow", "Посмотреть всех\n авторов"))
        self.view_essays_btn.setText(_translate("MainWindow", "Посмотреть все \n"
                                                              "сочинения"))

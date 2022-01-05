import sys
import os
import platform
import time
import tkinter.filedialog

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

from modules import *
from widgets import *
from ui_splash_screen import Ui_SplashScreen
from noresult import Ui_NoResult
from sqlalchemy import *
import sqlalchemy.sql.default_comparator
import sqlalchemy.dialects.sqlite

widgets = None
counter = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        DBFunctions.start(self)

        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        title = "Калькулятор марковских процессов"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("ASD.ico"))

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)

        widgets.input_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_draw.clicked.connect(self.buttonClick)
        widgets.btn_calculate.clicked.connect(self.buttonClick)
        widgets.btn_add.clicked.connect(self.buttonClick)
        widgets.btn_minus.clicked.connect(self.buttonClick)
        widgets.btn_clear.clicked.connect(self.buttonClick)
        widgets.btn_edit.clicked.connect(self.buttonClick)
        widgets.btn_save_2.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_theme.clicked.connect(self.buttonClick)

        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        self.show()

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    def buttonClick(self, useCustomTheme):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_theme":
            if Settings.CHANGE_THEME:
                themeFile = "themes\light.qss"
                UIFunctions.theme(self, themeFile, True)
                AppFunctions.setThemeHack(self)
                Settings.CHANGE_THEME = False
                self.ui.btn_theme.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-moon.png);")
            else:
                Settings.CHANGE_THEME = True
                themeFile = "themes\dark.qss"
                UIFunctions.theme(self, themeFile, True)
                AppFunctions.setThemeHack(self)
                self.ui.btn_theme.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-lightbulb.png);")

        if btnName == "btn_calculate":
            try:
                UIFunctions.printresult(self)
                widgets.stackedWidget.setCurrentWidget(widgets.calculation)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            except Exception:
                print("Нет решений")
                self.main = NoResult(True)
                self.main.show()

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_save":
            path=tkinter.filedialog.askopenfilename()
            AppFunctions.serialize(self,path)

        if btnName == "btn_new":
            path = tkinter.filedialog.askopenfilename()
            AppFunctions.deserialize(self,path)
            UIFunctions.tableafterinsert(self)

        if btnName == "btn_edit":
            self.ui.input_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.ui.input_table.selectRow(self.ui.input_table.rowCount()-1)

        if btnName == "btn_save_2":
                self.ui.input_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                UIFunctions.tabletodb(self)

        if btnName == "btn_draw":
            try:
                AppFunctions.drawgraph(self)
                UIFunctions.picturer(self)
                widgets.stackedWidget.setCurrentWidget(widgets.draw)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            except:
                print("Нет решений")
                self.main = NoResult(False)
                self.main.show()

        if btnName == "btn_add":
            UIFunctions.addrow(self)

        if btnName == "btn_minus":
            UIFunctions.deleterow(self)
            DBFunctions.delete(self)

        if btnName == "btn_clear":
            UIFunctions.cleartable(self)
            for i in range(len(DBFunctions.select(self))):
                DBFunctions.delete(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        
        self.timer.start(55)

        self.ui.label_description.setText("<strong>Одну</strong> секунду")
        QtCore.QTimer.singleShot(1500,
                                 lambda: self.ui.label_description.setText("<strong>Загрузка</strong> базы данных"))
        QtCore.QTimer.singleShot(3000,
                                 lambda: self.ui.label_description.setText("<strong>Загрузка</strong> интерфейса"))
        QtCore.QTimer.singleShot(4500, lambda: self.ui.label_description.setText("<strong>Почти</strong> готово"))

        self.show()

    def progress(self):
        global counter

        self.ui.progressBar.setValue(counter)

        if counter > 100:
            self.timer.stop()
            self.main = MainWindow()
            self.main.show()
            self.close()

        counter += 1


class NoResult(QMainWindow):
    def __init__(self, flag):
        QMainWindow.__init__(self)
        self.ui = Ui_NoResult()
        self.ui.setupUi(self)
        title = "Ошибка"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("ASD.ico"))
        if flag:
            self.ui.label.setText("Нет решений")
        else:
            self.ui.label.setText("Построить граф невозможно")
            self.ui.label.setFixedWidth(1000)
            self.setFixedWidth(715)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())

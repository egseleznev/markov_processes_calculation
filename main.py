import sys, os, platform, time, tkinter.filedialog, PySide6.QtWidgets, sqlalchemy.sql.default_comparator, sqlalchemy.dialects.sqlite
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
        widgets.input_table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.input_table_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        transitions_delegate = TransitionsTableDelegate(self.ui.input_table)
        self.ui.input_table.setItemDelegate(transitions_delegate)
        UIFunctions.deleterow(self, 0); UIFunctions.deleterow(self, 1)
        UIFunctions.addrow(self,0);  UIFunctions.addrow(self,1);


        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_draw.clicked.connect(self.buttonClick)
        widgets.btn_calculate.clicked.connect(self.buttonClick)
        widgets.btn_add.clicked.connect(self.buttonClick)
        widgets.btn_minus.clicked.connect(self.buttonClick)
        widgets.btn_clear.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_theme.clicked.connect(self.buttonClick)
        widgets.btn_pdf.clicked.connect(self.buttonClick)
        widgets.btn_add_3.clicked.connect(self.buttonClick)
        widgets.btn_minus_3.clicked.connect(self.buttonClick)
        widgets.btn_clear_3.clicked.connect(self.buttonClick)
        widgets.btn_label.clicked.connect(self.buttonClick)
        widgets.btn_pdf_2.clicked.connect(self.buttonClick)


        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        self.show()

        useCustomTheme = False
        themeFile = "themes\light.qss"
        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_pdf_2":
            try:
                AppFunctions.printpdf(self,0)
            except:
                self.main = NoResult(2)
                self.main.show()

        if btnName == "btn_label":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_theme":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, "btn_draw")
            UIFunctions.resetStyle(self, "btn_calculate")
            widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
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

        if btnName == "btn_pdf":
            try:
                AppFunctions.printpdf(self, 1)
            except:
                self.main = NoResult(2)
                self.main.show()

        if btnName == "btn_calculate":
            try:
                UIFunctions.clean_db(self)
                UIFunctions.tabletodb(self)
                UIFunctions.printresult(self)
                self.ui.result_table.sortByColumn(1, Qt.DescendingOrder)
                widgets.stackedWidget.setCurrentWidget(widgets.calculation)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            except Exception:
                self.main = NoResult(1)

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_save":
            try:
                UIFunctions.clean_db(self)
                UIFunctions.tabletodb(self)
                path = tkinter.filedialog.asksaveasfilename(initialfile='save.data')
                AppFunctions.serialize(self, path)
            except:
                self.main = NoResult(2)
                self.main.show()


        if btnName == "btn_new":
            try:
                widgets.stackedWidget.setCurrentWidget(widgets.home)
                UIFunctions.resetStyle(self, "btn_draw")
                UIFunctions.resetStyle(self, "btn_calculate")
                widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
                path = tkinter.filedialog.askopenfilename()
                UIFunctions.clean_db(self)
                UIFunctions.clean_tables(self)
                AppFunctions.deserialize(self,path)
                UIFunctions.tableafterinsert(self)
            except:
                self.main = NoResult(2)
                self.main.show()
                UIFunctions.deleterow(self, 0);
                UIFunctions.deleterow(self, 1)
                UIFunctions.addrow(self, 0);
                UIFunctions.addrow(self, 1);

        if btnName == "btn_draw":
            try:
                UIFunctions.copydesc(self)
                UIFunctions.clean_db(self)
                UIFunctions.tabletodb(self)
                AppFunctions.drawgraph(self)
                UIFunctions.picturer(self)
                self.ui.input_table_5.sortItems(0, Qt.AscendingOrder)
                widgets.stackedWidget.setCurrentWidget(widgets.draw)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            except:
                self.main = NoResult(0)
                self.main.show()

        if btnName == "btn_add":
            if self.ui.input_table.rowCount() != 0:
                UIFunctions.clean_db(self)
                UIFunctions.tabletodb(self)
            UIFunctions.addrow(self, 1)

        if btnName == "btn_minus":
            try:
                if self.ui.input_table.rowCount() != 0:
                    UIFunctions.clean_db(self)
                    UIFunctions.tabletodb(self)
                UIFunctions.deleteselectedrow(self, 1)
                DBFunctions.deletetransition(self)
            except:
                print("Нет решений")
                self.main = NoResult(3)
                self.main.show()

        if btnName == "btn_clear":
            UIFunctions.cleartable(self, 1)
            for i in range(len(DBFunctions.selecttransition(self))):
                DBFunctions.deletetransition(self)
            UIFunctions.deleterow(self, 1)
            UIFunctions.addrow(self, 1)

        if btnName == "btn_add_3":
            if self.ui.input_table_2.rowCount() != 0:
                UIFunctions.clean_db(self)
                UIFunctions.tabletodb(self)
            UIFunctions.addrow(self, 0)

        if btnName == "btn_minus_3":
            try:
                if self.ui.input_table_2.rowCount() != 0:
                    UIFunctions.clean_db(self)
                    UIFunctions.tabletodb(self)
                UIFunctions.deleteselectedrow(self, 0)
                DBFunctions.deletedescription(self)
                UIFunctions.ifdeleted(self)
            except:
                print("Нет решений")
                self.main = NoResult(3)
                self.main.show()

        if btnName == "btn_clear_3":
            UIFunctions.cleartable(self, 0)
            for i in range(len(DBFunctions.selectdescription(self))):
                DBFunctions.deletedescription(self)
            UIFunctions.deleterow(self, 0)
            UIFunctions.addrow(self, 0)

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

        self.timer.start(45)

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
        if flag == 1:
            self.ui.label.setText("Нет решений")
        if flag == 0:
            self.ui.label.setText("Построить граф невозможно")
            self.ui.label.setFixedWidth(1000)
            self.setFixedWidth(715)
        if flag == 2:
            self.ui.label.setText("Попробуйте еще раз, выбрав файл")
            self.ui.label.setFixedWidth(1100)
            self.setFixedWidth(850)
        if flag == 3:
            self.ui.label.setText("Выберите строку, которую необходимо удалить")
            self.ui.label.setFixedWidth(1250)
            self.setFixedWidth(1100)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())

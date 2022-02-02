from main import *
from . import Settings
from .app_functions import *

GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

class UIFunctions(MainWindow):
    flag = True;
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    def returStatus(self):
        return GLOBAL_STATE

    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def toggleMenu(self, enable):
        if enable:
            width = self.ui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH
            standard = 60

            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    def toggleLeftBox(self, enable):
        if enable:

            width = self.ui.extraLeftBox.width()
            widthRightBox = 0
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            style = self.ui.toggleLeftBox.styleSheet()

            if width == 0:
                widthExtended = maxExtend
                self.ui.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.ui.settingsTopBtn.styleSheet()
                    self.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))

        UIFunctions.start_box_animation(self, width, widthRightBox, "left")


    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0

        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0

        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.start()

    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    def selectStandardMenu(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    def resetStyle(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.ui.styleSheet.setStyleSheet(str)

    def tabletodb(self):
        for i in range(self.ui.input_table.rowCount()):
            DBFunctions.inserttransition(self,self.ui.input_table.item(i, 0).text(),self.ui.input_table.item(i, 1).text(),self.ui.input_table.item(i, 2).text())
        for i in range(self.ui.input_table_2.rowCount()):
            DBFunctions.insertdescription(self,self.ui.input_table_2.item(i, 0).text(), self.ui.input_table_2.item(i, 1).text())

    def copydesc(self):
        self.ui.input_table_5.setFixedHeight(100)
        self.ui.input_table_5.setRowCount(1)
        data = DBFunctions.selectdescription(self)
        for i in range(len(data)):
            if (i != 0):
                self.ui.input_table_5.setRowCount(self.ui.input_table_5.rowCount() + 1)
            self.ui.input_table_5.setFixedHeight((self.ui.input_table_5.height() + 20))
            self.ui.input_table_5.setItem(i, 0, QTableWidgetItem(str(data[i]).split("~~")[0]))
            self.ui.input_table_5.setItem(i, 1, QTableWidgetItem(str(data[i]).split("~~")[1]))

    def tableafterinsert(self):
        data = DBFunctions.selecttransition(self)
        for i in range(len(data)):
            if (i != 0):
                self.ui.input_table.setRowCount(self.ui.input_table.rowCount() + 1)
            self.ui.input_table.setFixedHeight((self.ui.input_table.height() + 20))
            self.ui.input_table.setItem(i, 0, QTableWidgetItem(str(data[i])[0]))
            self.ui.input_table.setItem(i, 1, QTableWidgetItem(str(data[i])[2]))
            self.ui.input_table.setItem(i, 2, QTableWidgetItem(str(data[i])[4]))
        data = DBFunctions.selectdescription(self)
        for i in range(len(data)):
            if (i != 0):
                self.ui.input_table_2.setRowCount(self.ui.input_table_2.rowCount() + 1)
            self.ui.input_table_2.setFixedHeight((self.ui.input_table_2.height() + 20))
            item = QTableWidgetItem(QTableWidgetItem(str(data[i]).split("~~")[0]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.input_table_2.setItem(i, 0, item)
            self.ui.input_table_2.setItem(i, 1, QTableWidgetItem(str(data[i]).split("~~")[1]))

    def printresult(self):
        self.ui.result_table.clearContents()
        self.ui.result_table.setRowCount(0)
        self.ui.result_table.setFixedHeight(100)
        data = DBFunctions.selectdescription(self)
        result=AppFunctions.calculate(self)
        for i in range(len(result)):
            self.ui.result_table.setFixedHeight((self.ui.result_table.height()+25))
            self.ui.result_table.setRowCount(self.ui.result_table.rowCount() + 1)
            for j in range(len(data)):
                if i == int(str(data[j]).split("~~")[0])-1:
                    self.ui.result_table.setItem(i, 0, QTableWidgetItem(str(data[j]).split("~~")[1]))
                    self.ui.result_table.setItem(i, 1, QTableWidgetItem(str(result[i])))

    def clean_tables(self):
        UIFunctions.cleartable(self, 0)
        UIFunctions.cleartable(self, 1)

    def clean_db(self):
        for i in range(len(DBFunctions.selecttransition(self))):
            DBFunctions.deletetransition(self)
        for i in range(len(DBFunctions.selectdescription(self))):
            DBFunctions.deletedescription(self)

    def picturer(self):
        #self.ui.graph_label.setText("")
        #pixmap=QPixmap("graph.png")
        #self.ui.graph_label.setPixmap(pixmap)
        self.ui.btn_label.setIcon(QIcon('graph.png'))
        self.ui.btn_label.setIconSize(QSize(800, 600))
        self.show()

    def addrow(self, flag):
        if flag:
            self.ui.input_table.setFixedHeight((self.ui.input_table.height() + 20))
            self.ui.input_table.insertRow(self.ui.input_table.rowCount())
            length = self.ui.input_table.rowCount();
            self.ui.input_table.setItem(length-1, 0, QTableWidgetItem("1"))
            self.ui.input_table.setItem(length-1, 1, QTableWidgetItem("1"))
            self.ui.input_table.setItem(length-1, 2, QTableWidgetItem("1"))
            self.ui.input_table.selectRow(self.ui.input_table.rowCount()+1)
        else:
            self.ui.input_table_2.setFixedHeight((self.ui.input_table_2.height() + 20))
            self.ui.input_table_2.insertRow(self.ui.input_table_2.rowCount())
            length = self.ui.input_table_2.rowCount()
            item =QTableWidgetItem(str(self.ui.input_table_2.rowCount()))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.input_table_2.setItem(length-1, 0, QTableWidgetItem(item))
            if length == 1:
                self.ui.input_table_2.setItem(length-1, 1, QTableWidgetItem("Введите описание состояния здесь"))
            else:
                self.ui.input_table_2.setItem(length - 1, 1, QTableWidgetItem(""))

    def deleterow(self, flag):
        if flag:
            self.ui.input_table.removeRow(self.ui.input_table.rowCount()-1)
            self.ui.input_table.setFixedHeight((self.ui.input_table.height() - 20))
            self.ui.input_table.selectRow(self.ui.input_table.rowCount())
        else:
            self.ui.input_table_2.removeRow(self.ui.input_table_2.rowCount()-1)
            self.ui.input_table_2.setFixedHeight((self.ui.input_table_2.height() - 20))
            self.ui.input_table_2.selectRow(self.ui.input_table_2.rowCount())


    def ifdeleted(self):
        self.ui.input_table_2.selectRow(0)
        length = self.ui.input_table_2.rowCount()
        for i in range(length):
            if int(self.ui.input_table_2.item(i, 0).text()) != i+1:
                for j in range(self.ui.input_table.rowCount()):
                    if self.ui.input_table.item(j, 0).text() != "#":
                        if int(self.ui.input_table.item(j, 0).text()) == int(self.ui.input_table_2.item(i, 0).text()):
                            self.ui.input_table.setItem(j, 0, QTableWidgetItem(str(int(self.ui.input_table_2.item(i, 0).text())-1)))
                    if self.ui.input_table.item(j, 1).text() != "#":
                        if int(self.ui.input_table.item(j, 1).text()) == int(self.ui.input_table_2.item(i, 0).text()):
                            self.ui.input_table.setItem(j, 1, QTableWidgetItem(str(int(self.ui.input_table_2.item(i, 0).text())-1)))

            item = QTableWidgetItem(str(i+1))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.input_table_2.setItem(i, 0, item)

    def deleteselectedrow(self, flag):
        if flag:
                self.ui.input_table.removeRow(self.ui.input_table.selectionModel().selectedRows()[0].row())
                self.ui.input_table.setFixedHeight((self.ui.input_table.height() - 20))
                self.ui.input_table.selectRow(self.ui.input_table.rowCount())
        else:

                for i in range(self.ui.input_table.rowCount()):
                   if self.ui.input_table.item(i, 0).text() != "#":
                        if int(self.ui.input_table.item(i, 0).text()) == int(self.ui.input_table_2.item(self.ui.input_table_2.selectionModel().selectedRows()[0].row(),0).text()):
                            self.ui.input_table.setItem(i, 0, QTableWidgetItem("#"))
                   if self.ui.input_table.item(i, 1).text() != "#":
                        if int(self.ui.input_table.item(i, 1).text()) == int(self.ui.input_table_2.item(self.ui.input_table_2.selectionModel().selectedRows()[0].row(),0).text()):
                            self.ui.input_table.setItem(i, 1, QTableWidgetItem("#"))

                self.ui.input_table_2.removeRow(self.ui.input_table_2.selectionModel().selectedRows()[0].row())
                self.ui.input_table_2.setFixedHeight((self.ui.input_table_2.height() - 20))
                self.ui.input_table_2.selectRow(self.ui.input_table_2.rowCount())

    def cleartable(self, flag):
        if flag:
            self.ui.input_table.setFixedHeight(100)
            self.ui.input_table.setRowCount(0)
            self.ui.input_table.setRowCount(1)
        else:
            self.ui.input_table_2.setFixedHeight(100)
            self.ui.input_table_2.setRowCount(0)
            self.ui.input_table_2.setRowCount(1)

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))
        self.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            def moveWindow(event):
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()
            self.ui.titleRightInfo.mouseMoveEvent = moveWindow

            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        self.ui.closeAppBtn.clicked.connect(lambda: self.close())
        for i in range(len(DBFunctions.selecttransition(self))):
            DBFunctions.deletetransition(self)
        for i in range(len(DBFunctions.selectdescription(self))):
            DBFunctions.deletedescription(self)

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)


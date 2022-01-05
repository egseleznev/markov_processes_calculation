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
            DBFunctions.insert(self,self.ui.input_table.item(i, 0).text(),self.ui.input_table.item(i, 1).text(),self.ui.input_table.item(i, 2).text())

    def tableafterinsert(self):
        data = DBFunctions.select(self)
        for i in range(len(data)):
            if (i != 0):
                self.ui.input_table.setRowCount(self.ui.input_table.rowCount() + 1)
            self.ui.input_table.setFixedHeight((self.ui.input_table.height() + 20))
            self.ui.input_table.setItem(i, 0, QTableWidgetItem(str(data[i])[0]))
            self.ui.input_table.setItem(i, 1, QTableWidgetItem(str(data[i])[2]))
            self.ui.input_table.setItem(i, 2, QTableWidgetItem(str(data[i])[4]))

    def printresult(self):
        self.ui.result_table.clearContents()
        self.ui.result_table.setRowCount(0)
        self.ui.result_table.setFixedHeight(100)
        result=AppFunctions.calculate(self)
        for i in range(len(result)):
            self.ui.result_table.setFixedHeight((self.ui.result_table.height()+25))
            self.ui.result_table.setRowCount(self.ui.result_table.rowCount() + 1)
            self.ui.result_table.setItem(i, 0, QTableWidgetItem(str(i+1)));
            self.ui.result_table.setItem(i, 1, QTableWidgetItem(str(result[i])))

    def picturer(self):
        self.ui.graph_label.setText("")
        pixmap=QPixmap("graph.png")
        self.ui.graph_label.setPixmap(pixmap)
        self.show()

    def addrow(self):
        self.ui.input_table.setFixedHeight((self.ui.input_table.height() + 20))
        self.ui.input_table.insertRow(self.ui.input_table.rowCount())
        self.ui.input_table.setItem(self.ui.input_table.rowCount(), 0, QTableWidgetItem(str(1)))
        self.ui.input_table.setItem(self.ui.input_table.rowCount(), 1, QTableWidgetItem(str(1)))
        self.ui.input_table.setItem(self.ui.input_table.rowCount(), 2, QTableWidgetItem(str(1)))
        self.ui.input_table.selectRow(self.ui.input_table.rowCount()+1)

    def deleterow(self):
        self.ui.input_table.removeRow(self.ui.input_table.rowCount()-1)
        self.ui.input_table.setFixedHeight((self.ui.input_table.height() - 20))

    def cleartable(self):
        self.ui.input_table.setFixedHeight(50)
        for i in range(self.ui.input_table.rowCount()):
            self.ui.input_table.removeRow(i - 1)

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

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)


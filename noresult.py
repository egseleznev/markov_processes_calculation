# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerMidLpy.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QWidget)

class Ui_NoResult(object):
    def setupUi(self, NoResult):
        if not NoResult.objectName():
            NoResult.setObjectName(u"NoResult")
        NoResult.resize(400, 200)
        NoResult.setStyleSheet(u"background-color: rgb(168, 166, 255);")
        self.label = QLabel(NoResult)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 70, 241, 51))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(40, 44, 52, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush2)
        brush3 = QBrush(QColor(240, 240, 240, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush3)
        brush4 = QBrush(QColor(120, 120, 120, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label.setPalette(palette)
        font = QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.label.setFont(font)

        self.retranslateUi(NoResult)

        QMetaObject.connectSlotsByName(NoResult)
    # setupUi

    def retranslateUi(self, NoResult):
        NoResult.setWindowTitle(QCoreApplication.translate("NoResult", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("NoResult", u"\u041d\u0435\u0442 \u0440\u0435\u0448\u0435\u043d\u0438\u0439", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

class Ui_ErrorWindow(object):
    def setupUi(self, ErrorWindow):
        if not ErrorWindow.objectName():
            ErrorWindow.setObjectName(u"ErrorWindow")
        ErrorWindow.resize(600, 300)
        icon = QIcon()
        icon.addFile(u":/icon_64x64.ico", QSize(), QIcon.Normal, QIcon.Off)
        ErrorWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(ErrorWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label)

        ErrorWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ErrorWindow)

        QMetaObject.connectSlotsByName(ErrorWindow)
    # setupUi

    def retranslateUi(self, ErrorWindow):
        ErrorWindow.setWindowTitle(QCoreApplication.translate("ErrorWindow", u"Joulescope UI Error", None))
        self.label.setText(QCoreApplication.translate("ErrorWindow", u"TextLabel", None))
    # retranslateUi


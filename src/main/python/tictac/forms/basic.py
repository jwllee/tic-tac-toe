# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/basic.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BasicGameWidget(object):
    def setupUi(self, BasicGameWidget):
        BasicGameWidget.setObjectName("BasicGameWidget")
        BasicGameWidget.resize(652, 736)
        self.GameInfoWidget = QtWidgets.QWidget(BasicGameWidget)
        self.GameInfoWidget.setGeometry(QtCore.QRect(79, 30, 501, 111))
        self.GameInfoWidget.setObjectName("GameInfoWidget")
        self.BoardWidget = QtWidgets.QWidget(BasicGameWidget)
        self.BoardWidget.setGeometry(QtCore.QRect(80, 180, 500, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BoardWidget.sizePolicy().hasHeightForWidth())
        self.BoardWidget.setSizePolicy(sizePolicy)
        self.BoardWidget.setObjectName("BoardWidget")

        self.retranslateUi(BasicGameWidget)
        QtCore.QMetaObject.connectSlotsByName(BasicGameWidget)

    def retranslateUi(self, BasicGameWidget):
        _translate = QtCore.QCoreApplication.translate
        BasicGameWidget.setWindowTitle(_translate("BasicGameWidget", "Form"))


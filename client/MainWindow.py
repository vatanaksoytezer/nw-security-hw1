# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(635, 521)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.currentKeyLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentKeyLabel.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.currentKeyLabel.setObjectName("currentKeyLabel")
        self.runClientButton = QtWidgets.QPushButton(self.centralwidget)
        self.runClientButton.setGeometry(QtCore.QRect(520, 50, 93, 28))
        self.runClientButton.setObjectName("runClientButton")
        self.rekeyButton = QtWidgets.QPushButton(self.centralwidget)
        self.rekeyButton.setGeometry(QtCore.QRect(420, 50, 93, 28))
        self.rekeyButton.setObjectName("rekeyButton")
        self.commandPlainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.commandPlainTextEdit.setGeometry(QtCore.QRect(130, 10, 491, 31))
        self.commandPlainTextEdit.setObjectName("commandPlainTextEdit")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(10, 10, 111, 28))
        self.sendButton.setObjectName("sendButton")
        self.prevKeyLabel = QtWidgets.QLabel(self.centralwidget)
        self.prevKeyLabel.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.prevKeyLabel.setObjectName("prevKeyLabel")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 110, 591, 341))
        self.textBrowser.setObjectName("textBrowser")
        self.prevKeyEmptyLabel = QtWidgets.QLabel(self.centralwidget)
        self.prevKeyEmptyLabel.setGeometry(QtCore.QRect(100, 50, 311, 16))
        self.prevKeyEmptyLabel.setText("")
        self.prevKeyEmptyLabel.setObjectName("prevKeyEmptyLabel")
        self.currentKeyEmptyLabel = QtWidgets.QLabel(self.centralwidget)
        self.currentKeyEmptyLabel.setGeometry(QtCore.QRect(100, 70, 311, 16))
        self.currentKeyEmptyLabel.setText("")
        self.currentKeyEmptyLabel.setObjectName("currentKeyEmptyLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 635, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client"))
        self.currentKeyLabel.setText(_translate("MainWindow", "Current Key:"))
        self.runClientButton.setText(_translate("MainWindow", "Run Client"))
        self.rekeyButton.setText(_translate("MainWindow", "Rekey"))
        self.sendButton.setText(_translate("MainWindow", "Send Data"))
        self.prevKeyLabel.setText(_translate("MainWindow", "Previous Key:"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadingScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loadingScreenForm(object):
    def setupUi(self, loadingScreenForm):
        loadingScreenForm.setObjectName("loadingScreenForm")
        loadingScreenForm.resize(455, 311)
        self.label = QtWidgets.QLabel(loadingScreenForm)
        self.label.setGeometry(QtCore.QRect(170, 20, 131, 121))
        self.label.setStyleSheet("border-image: url(:/images/logo.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(loadingScreenForm)
        self.progressBar.setGeometry(QtCore.QRect(30, 200, 401, 31))
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    border-radius: 10px;\n"
"    background-color: rgb(78, 93, 100);\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    background-color: rgb(162, 202, 214);\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(loadingScreenForm)
        QtCore.QMetaObject.connectSlotsByName(loadingScreenForm)

    def retranslateUi(self, loadingScreenForm):
        _translate = QtCore.QCoreApplication.translate
        loadingScreenForm.setWindowTitle(_translate("loadingScreenForm", "Form"))
import res, sys


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loadingScreenForm = QtWidgets.QWidget()
    ui = Ui_loadingScreenForm()
    ui.setupUi(loadingScreenForm)
    loadingScreenForm.show()
    sys.exit(app.exec_())

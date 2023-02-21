# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'studLogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys, res

class Ui_studLoginWindow(object):
    def setupUi(self, studLoginWindow):
        studLoginWindow.setObjectName("studLoginWindow")
        studLoginWindow.resize(378, 502)
        studLoginWindow.setFixedSize(378, 502)
        # to remove close,minimize,maximize button
        studLoginWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # to remove the constant background of the app
        studLoginWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(studLoginWindow)
        self.centralwidget.setStyleSheet("*{\n"
"border: none;\n"
"background-color: transparent;\n"
"background: transparent;\n"
"padding: 0;\n"
"margin: 0;\n"
"color: #fff;\n"
"}\n"
"#frame{\n"
"border-image: url(:/images/back1.png);\n"
"border-radius: 20px;\n"
"}\n"
"#frame_4{\n"
"background-color:rgba(0,0,0,175);\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"#label, #label_2, #label_3, #label_4{\n"
"color: rgba(255, 255, 255,210);\n"
"}\n"
"QPushButton#closeButton,#loginStudButton,#backButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba();\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"QPushButton#closeButton:hover, #loginStudButton:hover, #backButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#closeButton:pressed, #loginStudButton:pressed, #backButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105, 118, 132, 200)\n"
"}\n"
"#studEmail_lineEdit, #studPass_lineEdit{\n"
"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color: rgb(255, 255, 255);\n"
"padding-bottom:7px\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 30, 291, 411))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame_4)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.frame_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.closeButton = QtWidgets.QPushButton(self.widget_3)
        self.closeButton.setStyleSheet("")
        self.closeButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon)
        self.closeButton.setIconSize(QtCore.QSize(25, 25))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_2.addWidget(self.widget_3, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.widget_7 = QtWidgets.QWidget(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.widget_7.setFont(font)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(20)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label = QtWidgets.QLabel(self.widget_7)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_10.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.label_4 = QtWidgets.QLabel(self.widget_7)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.widget_7, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.widget_6 = QtWidgets.QWidget(self.frame_2)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_9.setContentsMargins(40, 10, 40, 0)
        self.verticalLayout_9.setSpacing(20)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.studEmail_lineEdit = QtWidgets.QLineEdit(self.widget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studEmail_lineEdit.setFont(font)
        self.studEmail_lineEdit.setStyleSheet("")
        self.studEmail_lineEdit.setText("")
        self.studEmail_lineEdit.setObjectName("studEmail_lineEdit")
        self.verticalLayout_9.addWidget(self.studEmail_lineEdit)
        self.studPass_lineEdit = QtWidgets.QLineEdit(self.widget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studPass_lineEdit.setFont(font)
        self.studPass_lineEdit.setStyleSheet("")
        self.studPass_lineEdit.setText("")
        self.studPass_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.studPass_lineEdit.setObjectName("studPass_lineEdit")
        self.verticalLayout_9.addWidget(self.studPass_lineEdit)
        self.verticalLayout_2.addWidget(self.widget_6)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame_4)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_5 = QtWidgets.QWidget(self.frame_3)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.widget_5)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.loginStudButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loginStudButton.setFont(font)
        self.loginStudButton.setStyleSheet("    padding: 10px 40px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;")
        self.loginStudButton.setIconSize(QtCore.QSize(12, 12))
        self.loginStudButton.setAutoDefault(False)
        self.loginStudButton.setDefault(False)
        self.loginStudButton.setFlat(False)
        self.loginStudButton.setObjectName("loginStudButton")
        self.horizontalLayout_3.addWidget(self.loginStudButton)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_4 = QtWidgets.QWidget(self.widget_5)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.backButton = QtWidgets.QPushButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy)
        self.backButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet("    padding: 10px 10px;\n"
"")
        self.backButton.setIconSize(QtCore.QSize(16, 16))
        self.backButton.setObjectName("backButton")
        self.horizontalLayout_4.addWidget(self.backButton)
        self.horizontalLayout.addWidget(self.widget_4)
        self.verticalLayout_3.addWidget(self.widget_5, 0, QtCore.Qt.AlignHCenter)
        self.widget_2 = QtWidgets.QWidget(self.frame_3)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(8)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.toForgotPassStudButton = QtWidgets.QPushButton(self.widget_2)
        self.toForgotPassStudButton.setStyleSheet("QPushButton#toForgotPassStudButton{\n"
"    color:rgba(255,255,255,140)\n"
"}\n"
"QPushButton#toForgotPassStudButton:pressed{\n"
"    color: rgba(251, 153, 93, 1);\n"
"}\n"
"")
        self.toForgotPassStudButton.setDefault(False)
        self.toForgotPassStudButton.setFlat(True)
        self.toForgotPassStudButton.setObjectName("toForgotPassStudButton")
        self.verticalLayout_5.addWidget(self.toForgotPassStudButton, 0, QtCore.Qt.AlignBottom)
        self.toRegisterStudButton = QtWidgets.QPushButton(self.widget_2)
        self.toRegisterStudButton.setStyleSheet("QPushButton#toRegisterStudButton{\n"
"    color:rgba(255,255,255,140)\n"
"}\n"
"QPushButton#toRegisterStudButton:pressed{\n"
"    color: rgba(251, 153, 93, 1);\n"
"}\n"
"")
        self.toRegisterStudButton.setFlat(True)
        self.toRegisterStudButton.setObjectName("toRegisterStudButton")
        self.verticalLayout_5.addWidget(self.toRegisterStudButton, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_3.addWidget(self.widget_2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.frame_3, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_8.addWidget(self.frame_4)
        studLoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(studLoginWindow)
        QtCore.QMetaObject.connectSlotsByName(studLoginWindow)

    def retranslateUi(self, studLoginWindow):
        _translate = QtCore.QCoreApplication.translate
        studLoginWindow.setWindowTitle(_translate("studLoginWindow", "MainWindow"))
        self.label.setText(_translate("studLoginWindow", "Mathguro"))
        self.label_4.setText(_translate("studLoginWindow", "Student\'s Log In"))
        self.studEmail_lineEdit.setPlaceholderText(_translate("studLoginWindow", "Email:"))
        self.studPass_lineEdit.setPlaceholderText(_translate("studLoginWindow", "Password:"))
        self.loginStudButton.setText(_translate("studLoginWindow", "Log In"))
        self.backButton.setText(_translate("studLoginWindow", "Back"))
        self.toForgotPassStudButton.setText(_translate("studLoginWindow", "Forgot your Email or Password ?"))
        self.toRegisterStudButton.setText(_translate("studLoginWindow", "Don\'t have and Account? Register Here"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    studLoginWindow = QtWidgets.QMainWindow()
    ui = Ui_studLoginWindow()
    ui.setupUi(studLoginWindow)
    studLoginWindow.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data\studTeach.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_studTeachWindow(object):
    def setupUi(self, studTeachWindow):
        studTeachWindow.setObjectName("studTeachWindow")
        studTeachWindow.resize(285, 424)
        studTeachWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(studTeachWindow)
        self.centralwidget.setStyleSheet("*{\n"
"border: none;\n"
"background-color: transparent;\n"
"background: transparent;\n"
"padding: 0;\n"
"margin: 0;\n"
"color: #fff\n"
"}\n"
"#frame{\n"
"border-image: url(:/images/back1.png);\n"
"border-radius: 20px;\n"
"}\n"
"#frame_4{\n"
"background-color:rgba(0,0,0,150);\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"#label, #label_2, #label_3{\n"
"color: rgba(255, 255, 255,210);\n"
"}\n"
"QPushButton#closeButton,#toStudButton,#toTeachButton,#toAdminButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba();\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"QPushButton#closeButton:hover, #toStudButton:hover, #toTeachButton:hover,#toAdminButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#closeButton:pressed, #toStudButton:pressed, #toTeachButton:pressed,#toAdminButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105, 118, 132, 200)\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame = QtWidgets.QFrame(self.centralwidget)
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
        self.widget_7 = QtWidgets.QWidget(self.frame_4)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(30)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_2 = QtWidgets.QFrame(self.widget_7)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(25)
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
        self.verticalLayout_2.addWidget(self.widget_3, 0, QtCore.Qt.AlignRight)
        self.label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget = QtWidgets.QWidget(self.frame_2)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.widget)
        self.verticalLayout_11.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.widget_7)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 28)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_5 = QtWidgets.QWidget(self.frame_3)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.toStudButton = QtWidgets.QPushButton(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toStudButton.sizePolicy().hasHeightForWidth())
        self.toStudButton.setSizePolicy(sizePolicy)
        self.toStudButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.toStudButton.setFont(font)
        self.toStudButton.setStyleSheet("    padding: 10px 20px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;")
        self.toStudButton.setIconSize(QtCore.QSize(16, 16))
        self.toStudButton.setObjectName("toStudButton")
        self.verticalLayout_7.addWidget(self.toStudButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.widget_5)
        self.widget_4 = QtWidgets.QWidget(self.frame_3)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.widget_4)
        self.widget_2 = QtWidgets.QWidget(self.frame_3)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.toTeachButton = QtWidgets.QPushButton(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.toTeachButton.setFont(font)
        self.toTeachButton.setStyleSheet("    padding: 10px 20px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;")
        self.toTeachButton.setIconSize(QtCore.QSize(12, 12))
        self.toTeachButton.setAutoDefault(False)
        self.toTeachButton.setDefault(False)
        self.toTeachButton.setFlat(False)
        self.toTeachButton.setObjectName("toTeachButton")
        self.verticalLayout_5.addWidget(self.toTeachButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.widget_2)
        self.widget_6 = QtWidgets.QWidget(self.frame_3)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.toAdminButton = QtWidgets.QPushButton(self.widget_6)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.toAdminButton.setFont(font)
        self.toAdminButton.setStyleSheet("    padding: 10px 20px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;")
        self.toAdminButton.setObjectName("toAdminButton")
        self.verticalLayout_9.addWidget(self.toAdminButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.widget_6)
        self.verticalLayout_11.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.widget_7)
        self.verticalLayout_8.addWidget(self.frame_4)
        self.verticalLayout_10.addWidget(self.frame)
        studTeachWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(studTeachWindow)
        QtCore.QMetaObject.connectSlotsByName(studTeachWindow)

    def retranslateUi(self, studTeachWindow):
        _translate = QtCore.QCoreApplication.translate
        studTeachWindow.setWindowTitle(_translate("studTeachWindow", "MainWindow"))
        self.label.setText(_translate("studTeachWindow", "PreCalGuro"))
        self.label_2.setText(_translate("studTeachWindow", "Are you a"))
        self.toStudButton.setText(_translate("studTeachWindow", " Student "))
        self.label_3.setText(_translate("studTeachWindow", "or"))
        self.toTeachButton.setText(_translate("studTeachWindow", " Teacher "))
        self.toAdminButton.setText(_translate("studTeachWindow", "Admin"))
import sys
sys.path.append("assets")
import res
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    studTeachWindow = QtWidgets.QMainWindow()
    ui = Ui_studTeachWindow()
    ui.setupUi(studTeachWindow)
    studTeachWindow.show()
    sys.exit(app.exec_())

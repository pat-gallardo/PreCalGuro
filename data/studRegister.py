# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data\studRegister.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_studRegisterWindow(object):
    def setupUi(self, studRegisterWindow):
        studRegisterWindow.setObjectName("studRegisterWindow")
        studRegisterWindow.resize(303, 646)
        self.centralwidget = QtWidgets.QWidget(studRegisterWindow)
        self.centralwidget.setStyleSheet("*{\n"
"border: none;\n"
"background-color: transparent;\n"
"background: transparent;\n"
"padding: 0;\n"
"margin: 0;\n"
"color: #fff\n"
"}\n"
"\n"
"#frame{\n"
"border-image: url(:/images/back1.png);\n"
"}\n"
"#frame_4{\n"
"background-color:rgba(0,0,0,175);\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"#label, #label_2, #label_3, #label_4{\n"
"color: rgba(255, 255, 255,210);\n"
"}\n"
"QPushButton#closeButton,#registerStudButton,#backButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba();\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"QPushButton#closeButton:hover,#registerStudButton:hover,#backButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#closeButton:pressed,#registerStudButton:pressed,#backButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105, 118, 132, 200)\n"
"}\n"
"#studEmail_lineEdit, #studPass_lineEdit, #studLast_lineEdit, #studSchool_lineEdit\n"
", #studSec_lineEdit, #studMiddle_lineEdit, #studFirst_lineEdit, #studSchoolID_lineEdit{\n"
"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color: rgb(255, 255, 255);\n"
"padding-bottom:7px\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        self.frame.setFont(font)
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
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.frame_2 = QtWidgets.QFrame(self.frame_6)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
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
        self.widget_7 = QtWidgets.QWidget(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.widget_7.setFont(font)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 5)
        self.verticalLayout_10.setSpacing(20)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label = QtWidgets.QLabel(self.widget_7)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_10.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_4 = QtWidgets.QLabel(self.widget_7)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.verticalLayout_2.addWidget(self.widget_7, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_19.addWidget(self.frame_2, 0, QtCore.Qt.AlignTop)
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout_4.setSpacing(30)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_6 = QtWidgets.QWidget(self.frame_5)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_6.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_6.setSpacing(15)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_12 = QtWidgets.QWidget(self.widget_6)
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_29.setSpacing(25)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.widget_8 = QtWidgets.QWidget(self.widget_12)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_9 = QtWidgets.QWidget(self.widget_8)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_9.setContentsMargins(30, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.studFirst_lineEdit = QtWidgets.QLineEdit(self.widget_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studFirst_lineEdit.setFont(font)
        self.studFirst_lineEdit.setStyleSheet("")
        self.studFirst_lineEdit.setText("")
        self.studFirst_lineEdit.setObjectName("studFirst_lineEdit")
        self.verticalLayout_9.addWidget(self.studFirst_lineEdit)
        self.horizontalLayout_5.addWidget(self.widget_9)
        self.widget_10 = QtWidgets.QWidget(self.widget_8)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_7.setContentsMargins(0, 0, 30, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.studMiddle_lineEdit = QtWidgets.QLineEdit(self.widget_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studMiddle_lineEdit.setFont(font)
        self.studMiddle_lineEdit.setStyleSheet("")
        self.studMiddle_lineEdit.setText("")
        self.studMiddle_lineEdit.setObjectName("studMiddle_lineEdit")
        self.verticalLayout_7.addWidget(self.studMiddle_lineEdit)
        self.horizontalLayout_5.addWidget(self.widget_10, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_29.addWidget(self.widget_8)
        self.verticalLayout_6.addWidget(self.widget_12)
        self.widget_11 = QtWidgets.QWidget(self.widget_6)
        self.widget_11.setObjectName("widget_11")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_11)
        self.verticalLayout_11.setContentsMargins(30, 0, 30, 0)
        self.verticalLayout_11.setSpacing(8)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.warningFname = QtWidgets.QWidget(self.widget_11)
        self.warningFname.setObjectName("warningFname")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.warningFname)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_14 = QtWidgets.QLabel(self.warningFname)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setTextFormat(QtCore.Qt.RichText)
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_15.addWidget(self.label_14)
        self.verticalLayout_11.addWidget(self.warningFname)
        self.frame_7 = QtWidgets.QFrame(self.widget_11)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.studLast_lineEdit = QtWidgets.QLineEdit(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studLast_lineEdit.setFont(font)
        self.studLast_lineEdit.setStyleSheet("")
        self.studLast_lineEdit.setText("")
        self.studLast_lineEdit.setObjectName("studLast_lineEdit")
        self.verticalLayout_22.addWidget(self.studLast_lineEdit)
        self.verticalLayout_11.addWidget(self.frame_7)
        self.warningLname = QtWidgets.QWidget(self.widget_11)
        self.warningLname.setObjectName("warningLname")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.warningLname)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.warningLname)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setTextFormat(QtCore.Qt.RichText)
        self.label_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_16.addWidget(self.label_15)
        self.verticalLayout_11.addWidget(self.warningLname)
        self.frame_8 = QtWidgets.QFrame(self.widget_11)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.studSec_comboBox = QtWidgets.QComboBox(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studSec_comboBox.setFont(font)
        self.studSec_comboBox.setStyleSheet("background-color: rgb(29, 89, 98);\n"
"padding-left: 3px;")
        self.studSec_comboBox.setObjectName("studSec_comboBox")
        self.studSec_comboBox.addItem("")
        self.studSec_comboBox.addItem("")
        self.studSec_comboBox.addItem("")
        self.studSec_comboBox.addItem("")
        self.studSec_comboBox.addItem("")
        self.studSec_comboBox.addItem("")
        self.horizontalLayout_6.addWidget(self.studSec_comboBox)
        self.verticalLayout_11.addWidget(self.frame_8)
        self.warningYrSec = QtWidgets.QWidget(self.widget_11)
        self.warningYrSec.setObjectName("warningYrSec")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.warningYrSec)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_16 = QtWidgets.QLabel(self.warningYrSec)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setTextFormat(QtCore.Qt.RichText)
        self.label_16.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_17.addWidget(self.label_16)
        self.verticalLayout_11.addWidget(self.warningYrSec)
        self.frame_12 = QtWidgets.QFrame(self.widget_11)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.studSchoolID_lineEdit = QtWidgets.QLineEdit(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studSchoolID_lineEdit.setFont(font)
        self.studSchoolID_lineEdit.setStyleSheet("")
        self.studSchoolID_lineEdit.setText("")
        self.studSchoolID_lineEdit.setObjectName("studSchoolID_lineEdit")
        self.verticalLayout_23.addWidget(self.studSchoolID_lineEdit)
        self.verticalLayout_11.addWidget(self.frame_12)
        self.warningStudID = QtWidgets.QFrame(self.widget_11)
        self.warningStudID.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.warningStudID.setFrameShadow(QtWidgets.QFrame.Raised)
        self.warningStudID.setObjectName("warningStudID")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.warningStudID)
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_2 = QtWidgets.QLabel(self.warningStudID)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_27.addWidget(self.label_2)
        self.verticalLayout_11.addWidget(self.warningStudID)
        self.warningSchool = QtWidgets.QWidget(self.widget_11)
        self.warningSchool.setObjectName("warningSchool")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.warningSchool)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_11.addWidget(self.warningSchool)
        self.frame_10 = QtWidgets.QFrame(self.widget_11)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.studEmail_lineEdit = QtWidgets.QLineEdit(self.frame_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studEmail_lineEdit.setFont(font)
        self.studEmail_lineEdit.setStyleSheet("")
        self.studEmail_lineEdit.setText("")
        self.studEmail_lineEdit.setObjectName("studEmail_lineEdit")
        self.verticalLayout_25.addWidget(self.studEmail_lineEdit)
        self.verticalLayout_11.addWidget(self.frame_10)
        self.warningEmail = QtWidgets.QWidget(self.widget_11)
        self.warningEmail.setObjectName("warningEmail")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.warningEmail)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.label_18 = QtWidgets.QLabel(self.warningEmail)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setTextFormat(QtCore.Qt.RichText)
        self.label_18.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_20.addWidget(self.label_18)
        self.verticalLayout_11.addWidget(self.warningEmail)
        self.warningEmailInUsed = QtWidgets.QWidget(self.widget_11)
        self.warningEmailInUsed.setObjectName("warningEmailInUsed")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.warningEmailInUsed)
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.label_20 = QtWidgets.QLabel(self.warningEmailInUsed)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setTextFormat(QtCore.Qt.RichText)
        self.label_20.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_28.addWidget(self.label_20)
        self.verticalLayout_11.addWidget(self.warningEmailInUsed)
        self.frame_11 = QtWidgets.QFrame(self.widget_11)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.studPass_lineEdit = QtWidgets.QLineEdit(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.studPass_lineEdit.setFont(font)
        self.studPass_lineEdit.setStyleSheet("")
        self.studPass_lineEdit.setText("")
        self.studPass_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.studPass_lineEdit.setObjectName("studPass_lineEdit")
        self.verticalLayout_26.addWidget(self.studPass_lineEdit)
        self.verticalLayout_11.addWidget(self.frame_11)
        self.warningPass = QtWidgets.QWidget(self.widget_11)
        self.warningPass.setObjectName("warningPass")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.warningPass)
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_19 = QtWidgets.QLabel(self.warningPass)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_19.setFont(font)
        self.label_19.setTextFormat(QtCore.Qt.RichText)
        self.label_19.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_21.addWidget(self.label_19)
        self.verticalLayout_11.addWidget(self.warningPass)
        self.verticalLayout_6.addWidget(self.widget_11)
        self.verticalLayout_4.addWidget(self.widget_6)
        self.verticalLayout_19.addWidget(self.frame_5)
        self.frame_3 = QtWidgets.QFrame(self.frame_6)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 20)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.warningContainer = QtWidgets.QWidget(self.frame_3)
        self.warningContainer.setObjectName("warningContainer")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.warningContainer)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.warningContainerMenu = QtWidgets.QStackedWidget(self.warningContainer)
        self.warningContainerMenu.setObjectName("warningContainerMenu")
        self.errorWidget = QtWidgets.QWidget()
        self.errorWidget.setObjectName("errorWidget")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.errorWidget)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_12 = QtWidgets.QLabel(self.errorWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setTextFormat(QtCore.Qt.RichText)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_13.addWidget(self.label_12)
        self.warningContainerMenu.addWidget(self.errorWidget)
        self.acceptWidget = QtWidgets.QWidget()
        self.acceptWidget.setObjectName("acceptWidget")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.acceptWidget)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_13 = QtWidgets.QLabel(self.acceptWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setTextFormat(QtCore.Qt.RichText)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_14.addWidget(self.label_13)
        self.warningContainerMenu.addWidget(self.acceptWidget)
        self.verticalLayout_12.addWidget(self.warningContainerMenu)
        self.verticalLayout_3.addWidget(self.warningContainer)
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
        self.registerStudButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.registerStudButton.setFont(font)
        self.registerStudButton.setStyleSheet("    padding: 10px 25px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;")
        self.registerStudButton.setIconSize(QtCore.QSize(12, 12))
        self.registerStudButton.setAutoDefault(False)
        self.registerStudButton.setDefault(False)
        self.registerStudButton.setFlat(False)
        self.registerStudButton.setObjectName("registerStudButton")
        self.horizontalLayout_3.addWidget(self.registerStudButton)
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
        font.setFamily("MS Sans Serif")
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
        self.widget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.toLoginStudButton = QtWidgets.QPushButton(self.widget_2)
        self.toLoginStudButton.setStyleSheet("QPushButton#toLoginStudButton{\n"
"    color:rgba(255,255,255,140)\n"
"}\n"
"QPushButton#toLoginStudButton:pressed{\n"
"    color: rgba(251, 153, 93, 1);\n"
"}\n"
"")
        self.toLoginStudButton.setFlat(False)
        self.toLoginStudButton.setObjectName("toLoginStudButton")
        self.verticalLayout_5.addWidget(self.toLoginStudButton, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_3.addWidget(self.widget_2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_19.addWidget(self.frame_3, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.frame_6)
        self.verticalLayout_8.addWidget(self.frame_4)
        self.verticalLayout_24.addWidget(self.frame)
        studRegisterWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(studRegisterWindow)
        self.warningContainerMenu.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(studRegisterWindow)

    def retranslateUi(self, studRegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        studRegisterWindow.setWindowTitle(_translate("studRegisterWindow", "MainWindow"))
        self.label.setText(_translate("studRegisterWindow", "PreCalGuro"))
        self.label_4.setText(_translate("studRegisterWindow", "Student\'s Register"))
        self.studFirst_lineEdit.setToolTip(_translate("studRegisterWindow", "Required*"))
        self.studFirst_lineEdit.setPlaceholderText(_translate("studRegisterWindow", "First Name:"))
        self.studMiddle_lineEdit.setToolTip(_translate("studRegisterWindow", "Required*"))
        self.studMiddle_lineEdit.setPlaceholderText(_translate("studRegisterWindow", "M.I:"))
        self.label_14.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your First Name</span></p></body></html>"))
        self.studLast_lineEdit.setToolTip(_translate("studRegisterWindow", "Required*"))
        self.studLast_lineEdit.setPlaceholderText(_translate("studRegisterWindow", "Last Name:"))
        self.label_15.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your Last Name</span></p></body></html>"))
        self.studSec_comboBox.setItemText(0, _translate("studRegisterWindow", "Section"))
        self.studSec_comboBox.setItemText(1, _translate("studRegisterWindow", "A"))
        self.studSec_comboBox.setItemText(2, _translate("studRegisterWindow", "B"))
        self.studSec_comboBox.setItemText(3, _translate("studRegisterWindow", "C"))
        self.studSec_comboBox.setItemText(4, _translate("studRegisterWindow", "D"))
        self.studSec_comboBox.setItemText(5, _translate("studRegisterWindow", "E"))
        self.label_16.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please choose your Section.</span></p></body></html>"))
        self.studSchoolID_lineEdit.setToolTip(_translate("studRegisterWindow", "Required*"))
        self.studSchoolID_lineEdit.setPlaceholderText(_translate("studRegisterWindow", "LRN:"))
        self.label_2.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your LRN.</span></p></body></html>"))
        self.studEmail_lineEdit.setToolTip(_translate("studRegisterWindow", "Required*"))
        self.studEmail_lineEdit.setPlaceholderText(_translate("studRegisterWindow", "Email:"))
        self.label_18.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your Valid Email</span></p></body></html>"))
        self.label_20.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Email already in used</span></p></body></html>"))
        self.studPass_lineEdit.setToolTip(_translate("studRegisterWindow", "Required*"))
        self.studPass_lineEdit.setPlaceholderText(_translate("studRegisterWindow", "Password:"))
        self.label_19.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" font-size:8pt; color:#ff9393;\">Must be 8 or more alphanumeric characters</span></p></body></html>"))
        self.label_12.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter the required information</span></p></body></html>"))
        self.label_13.setText(_translate("studRegisterWindow", "<html><head/><body><p><span style=\" color:#9eff99;\">Account Registered</span></p></body></html>"))
        self.registerStudButton.setText(_translate("studRegisterWindow", "Register"))
        self.backButton.setText(_translate("studRegisterWindow", "Back"))
        self.toLoginStudButton.setText(_translate("studRegisterWindow", "Already have an Account? Log In Here"))
import sys
sys.path.append("assets")
import res
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    studRegisterWindow = QtWidgets.QMainWindow()
    ui = Ui_studRegisterWindow()
    ui.setupUi(studRegisterWindow)
    studRegisterWindow.show()
    sys.exit(app.exec_())

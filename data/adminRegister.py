# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data\adminRegister.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_adminRegisterWindow(object):
    def setupUi(self, adminRegisterWindow):
        adminRegisterWindow.setObjectName("adminRegisterWindow")
        adminRegisterWindow.resize(303, 516)
        self.centralwidget = QtWidgets.QWidget(adminRegisterWindow)
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
"QPushButton#closeButton,#registerAdminButton,#backButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba();\n"
"    color:rgba(255,255,255,210);\n"
"    border-radius:5px;\n"
"}\n"
"QPushButton#closeButton:hover,#registerAdminButton:hover,#backButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0.505682, y1:0.989, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#closeButton:pressed,#registerAdminButton:pressed,#backButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(105, 118, 132, 200)\n"
"}\n"
"#adminEmail_lineEdit, #adminPass_lineEdit, #adminLast_lineEdit\n"
", #adminMiddle_lineEdit, #adminFirst_lineEdit{\n"
"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(105, 118, 132, 255);\n"
"color: rgb(255, 255, 255);\n"
"padding-bottom:7px\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
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
        self.verticalLayout_2.addWidget(self.widget_3, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
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
        self.verticalLayout_19.addWidget(self.frame_2)
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_6 = QtWidgets.QWidget(self.frame_5)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_6.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_6.setSpacing(15)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_12 = QtWidgets.QWidget(self.widget_6)
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
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
        self.adminFirst_lineEdit = QtWidgets.QLineEdit(self.widget_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.adminFirst_lineEdit.setFont(font)
        self.adminFirst_lineEdit.setStyleSheet("")
        self.adminFirst_lineEdit.setText("")
        self.adminFirst_lineEdit.setObjectName("adminFirst_lineEdit")
        self.verticalLayout_9.addWidget(self.adminFirst_lineEdit)
        self.horizontalLayout_5.addWidget(self.widget_9)
        self.widget_10 = QtWidgets.QWidget(self.widget_8)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_7.setContentsMargins(0, 0, 30, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.adminMiddle_lineEdit = QtWidgets.QLineEdit(self.widget_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.adminMiddle_lineEdit.setFont(font)
        self.adminMiddle_lineEdit.setStyleSheet("")
        self.adminMiddle_lineEdit.setText("")
        self.adminMiddle_lineEdit.setObjectName("adminMiddle_lineEdit")
        self.verticalLayout_7.addWidget(self.adminMiddle_lineEdit)
        self.horizontalLayout_5.addWidget(self.widget_10, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_18.addWidget(self.widget_8)
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
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.adminLast_lineEdit = QtWidgets.QLineEdit(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.adminLast_lineEdit.setFont(font)
        self.adminLast_lineEdit.setStyleSheet("")
        self.adminLast_lineEdit.setText("")
        self.adminLast_lineEdit.setObjectName("adminLast_lineEdit")
        self.verticalLayout_24.addWidget(self.adminLast_lineEdit)
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
        self.frame_10 = QtWidgets.QFrame(self.widget_11)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.adminEmail_lineEdit = QtWidgets.QLineEdit(self.frame_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.adminEmail_lineEdit.setFont(font)
        self.adminEmail_lineEdit.setStyleSheet("")
        self.adminEmail_lineEdit.setText("")
        self.adminEmail_lineEdit.setObjectName("adminEmail_lineEdit")
        self.verticalLayout_22.addWidget(self.adminEmail_lineEdit)
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
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.warningEmailInUsed)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.label_20 = QtWidgets.QLabel(self.warningEmailInUsed)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setTextFormat(QtCore.Qt.RichText)
        self.label_20.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_25.addWidget(self.label_20)
        self.verticalLayout_11.addWidget(self.warningEmailInUsed)
        self.frame_11 = QtWidgets.QFrame(self.widget_11)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.adminPass_lineEdit = QtWidgets.QLineEdit(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.adminPass_lineEdit.setFont(font)
        self.adminPass_lineEdit.setStyleSheet("")
        self.adminPass_lineEdit.setText("")
        self.adminPass_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.adminPass_lineEdit.setObjectName("adminPass_lineEdit")
        self.verticalLayout_23.addWidget(self.adminPass_lineEdit)
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
        self.registerAdminButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.registerAdminButton.setFont(font)
        self.registerAdminButton.setStyleSheet("    padding: 10px 25px;\n"
"    border-top-left-radius: 10px;\n"
"    border-bottom-left-radius: 10px;")
        self.registerAdminButton.setIconSize(QtCore.QSize(12, 12))
        self.registerAdminButton.setAutoDefault(False)
        self.registerAdminButton.setDefault(False)
        self.registerAdminButton.setFlat(False)
        self.registerAdminButton.setObjectName("registerAdminButton")
        self.horizontalLayout_3.addWidget(self.registerAdminButton)
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
        self.verticalLayout_3.addWidget(self.widget_2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_19.addWidget(self.frame_3, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.frame_6)
        self.verticalLayout_8.addWidget(self.frame_4)
        self.verticalLayout_17.addWidget(self.frame)
        adminRegisterWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(adminRegisterWindow)
        self.warningContainerMenu.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(adminRegisterWindow)

    def retranslateUi(self, adminRegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        adminRegisterWindow.setWindowTitle(_translate("adminRegisterWindow", "MainWindow"))
        self.label.setText(_translate("adminRegisterWindow", "PreCalGuro"))
        self.label_4.setText(_translate("adminRegisterWindow", "Admin Register"))
        self.adminFirst_lineEdit.setToolTip(_translate("adminRegisterWindow", "Required*"))
        self.adminFirst_lineEdit.setPlaceholderText(_translate("adminRegisterWindow", "First Name:"))
        self.adminMiddle_lineEdit.setToolTip(_translate("adminRegisterWindow", "Required*"))
        self.adminMiddle_lineEdit.setPlaceholderText(_translate("adminRegisterWindow", "M.I:"))
        self.label_14.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your First Name</span></p></body></html>"))
        self.adminLast_lineEdit.setToolTip(_translate("adminRegisterWindow", "Required*"))
        self.adminLast_lineEdit.setPlaceholderText(_translate("adminRegisterWindow", "Last Name:"))
        self.label_15.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your Last Name</span></p></body></html>"))
        self.adminEmail_lineEdit.setToolTip(_translate("adminRegisterWindow", "Required*"))
        self.adminEmail_lineEdit.setPlaceholderText(_translate("adminRegisterWindow", "Email:"))
        self.label_18.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter your Valid Email</span></p></body></html>"))
        self.label_20.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Email already in used</span></p></body></html>"))
        self.adminPass_lineEdit.setToolTip(_translate("adminRegisterWindow", "Required*"))
        self.adminPass_lineEdit.setPlaceholderText(_translate("adminRegisterWindow", "Password:"))
        self.label_19.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" font-size:8pt; color:#ff9393;\">Must be 8 or more alphanumeric characters</span></p></body></html>"))
        self.label_12.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" color:#ff9393;\">Please enter the required information</span></p></body></html>"))
        self.label_13.setText(_translate("adminRegisterWindow", "<html><head/><body><p><span style=\" color:#9eff99;\">Account Registered</span></p></body></html>"))
        self.registerAdminButton.setText(_translate("adminRegisterWindow", "Register"))
        self.backButton.setText(_translate("adminRegisterWindow", "Back"))
import sys
sys.path.append("assets")
import res
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    adminRegisterWindow = QtWidgets.QMainWindow()
    ui = Ui_adminRegisterWindow()
    ui.setupUi(adminRegisterWindow)
    adminRegisterWindow.show()
    sys.exit(app.exec_())

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi

from studTeach import Ui_studTeachWindow
from studLogin import Ui_studLoginWindow
from studRegister import Ui_studRegisterWindow
from teachLogin import Ui_teachLoginWindow
from teachRegister import Ui_teachRegisterWindow
from dashboard import Ui_dashboardWindow
import time

import pyrebase

#dummyemail@gmail.com
#thisispass

firebaseConfig = {'apiKey': "AIzaSyDyihbb440Vb2o0CIMINI_UfQLRln0uvXs",
  'authDomain': "mathguro-46712.firebaseapp.com",
  'databaseURL':"https://mathguro-46712.firebaseio.com",
  'projectId': "mathguro-46712",
  'storageBucket': "mathguro-46712.appspot.com",
  'messagingSenderId': "24039260333",
  'appId': "1:24039260333:web:673adf358560ef3cbe4624",
  'measurementId': "G-YP2867V22T"}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

class toStudTeach(QMainWindow):
    def __init__(self):
        super(toStudTeach, self).__init__()
        self.ui = Ui_studTeachWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("studTeach.ui",self)

        self.toStudButton.clicked.connect(self.toStud)
        self.closeButton.clicked.connect(self.toExitProg)
        self.toTeachButton.clicked.connect(self.toTeach)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def toStud(self):
        self.toLogin = toStudLogin()
        self.toLogin.show()
        self.hide()
    
    def toTeach(self):
        self.toLogin = toTeachLogin()
        self.toLogin.show()
        self.hide()

    def toExitProg(self):
        sys.exit()


class toStudLogin(QMainWindow):
    def __init__(self):
        super(toStudLogin, self).__init__()
        self.ui = Ui_studLoginWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("studLogin.ui",self)

        self.warning_Widget.setVisible(False)

        self.closeButton.clicked.connect(self.toExitProg)
        self.backButton.clicked.connect(self.toBack)
        self.loginStudButton.clicked.connect(self.login)
        self.toRegisterStudButton.clicked.connect(self.toRegister)
        # self.toForgotPassStudButton.clicked.connect(self.toForgot)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def login(self):
        email = self.studEmail_lineEdit.text()
        password = self.studPass_lineEdit.text()

        try:
            login= auth.sign_in_with_email_and_password(email,password)
            print("Login Successfully")
            print(auth.get_account_info(login['idToken']))

            print(email)
            print(password)
            self.hide()
            self.toLogin = function()
            self.toLogin.loading()

        except:
            # self.rightMenuContainer.setVisible(False)
            self.warning_Widget.setVisible(True)
            print("Invalid email or password.")



    def toRegister(self):
        self.toRegis = toStudRegister()
        self.toRegis.show()
        self.hide()

    def toBack(self):
        self.toGoBack = toStudTeach()
        self.toGoBack.show()
        self.hide()

    def toExitProg(self):
        sys.exit()

class toStudRegister(QMainWindow):
    def __init__(self):
        super(toStudRegister, self).__init__()
        self.ui = Ui_studRegisterWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("studRegister.ui",self)

        self.warningFname.setVisible(False)
        self.warningLname.setVisible(False)
        self.warningYrSec.setVisible(False)
        self.warningSchool.setVisible(False)
        self.warningEmail.setVisible(False)
        self.warningPass.setVisible(False)
        self.warningContainer.setVisible(False)

        self.closeButton.clicked.connect(self.toExitProg)
        self.backButton.clicked.connect(self.toBack)
        self.registerStudButton.clicked.connect(self.register)
        self.toLoginStudButton.clicked.connect(self.toBack)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def register(self):
        self.fnameError = 0
        self.lnameError = 0
        self.yrSecError = 0
        self.schoolError = 0
        self.emailError = 0
        self.passError = 0

        fname = self.studFirst_lineEdit.text()
        mname = self.studMiddle_lineEdit.text()
        lname = self.studLast_lineEdit.text()
        school = self.studSchool_lineEdit.text()
        yrSec = self.studYrSec_lineEdit.text()

        email = self.studEmail_lineEdit.text()
        password = self.studPass_lineEdit.text()

# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if yrSec == "":
            self.yrSecError = 1
        if school == "":
            self.schoolError = 1
        if email == "":
            self.emailError = 1
        if password == "" and password.isdigit() == False and len(password)+1 < 8:
            self.passError = 1

        if self.fnameError == 1:
            self.warningFname.setVisible(True)
        if self.lnameError == 1:
            self.warningLname.setVisible(True)
        if self.yrSecError == 1:
            self.warningYrSec.setVisible(True)
        if self.schoolError == 1:
            self.warningSchool.setVisible(True)        
        if self.emailError == 1:
            self.warningEmail.setVisible(True)
        if self.passError == 1:
            self.warningPass.setVisible(True)  

        if self.fnameError == 1 or self.lnameError == 1 or self.yrSecError == 1 or self.schoolError == 1 or self.emailError == 1 or self.passError == 1:
            self.frame.setGeometry(QtCore.QRect(40, 50, 295, 591))
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(0)

            self.fnameError = 0
            self.lnameError = 0
            self.yrSecError = 0
            self.schoolError = 0
            self.emailError = 0
            self.passError = 0
        else:
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(1)
            print(fname)
            print(mname)
            print(lname)
            print(yrSec)
            print(school)
            print(email)
            print(password)

            # self.toLogins = toStudRegister()
            # self.toLogins.show()
            # self.hide()

    def toBack(self):
        self.toGoBack = toStudLogin()
        self.toGoBack.show()
        self.hide()

    def toExitProg(self):
        sys.exit()


class toTeachLogin(QMainWindow):
    def __init__(self):
        super(toTeachLogin, self).__init__()
        self.ui = Ui_teachLoginWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("teachLogin.ui",self)

        self.warning_Widget.setVisible(False)

        self.closeButton.clicked.connect(self.toExitProg)
        self.backButton.clicked.connect(self.toBack)
        self.loginTeachButton.clicked.connect(self.login)
        self.toRegisterTeachButton.clicked.connect(self.toRegister)
        # self.toForgotPassTeachButton.clicked.connect(self.toForgot)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def login(self):
        email = self.teachEmail_lineEdit.text()
        password = self.teachPass_lineEdit.text()

        try:
            # login= auth.sign_in_with_email_and_password(email,password)
            # print("Login Successfully")
            # print(auth.get_account_info(login['idToken']))

            print(email)
            print(password)
            self.hide()
            self.toLogin = function()
            self.toLogin.loading()

        except:
            # self.rightMenuContainer.setVisible(False)
            self.warning_Widget.setVisible(True)
            print("Invalid email or password.")



    def toRegister(self):
        self.toRegis = toTeachRegister()
        self.toRegis.show()
        self.hide()

    def toBack(self):
        self.toGoBack = toStudTeach()
        self.toGoBack.show()
        self.hide()

    def toExitProg(self):
        sys.exit()

class toTeachRegister(QMainWindow):
    def __init__(self):
        super(toTeachRegister, self).__init__()
        self.ui = Ui_teachRegisterWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("teachRegister.ui",self)

        self.warningFname.setVisible(False)
        self.warningLname.setVisible(False)
        self.warningYrSec.setVisible(False)
        self.warningSchool.setVisible(False)
        self.warningEmail.setVisible(False)
        self.warningPass.setVisible(False)
        self.warningContainer.setVisible(False)

        self.closeButton.clicked.connect(self.toExitProg)
        self.backButton.clicked.connect(self.toBack)
        self.registerTeachButton.clicked.connect(self.register)
        self.toLoginTeachButton.clicked.connect(self.toBack)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def register(self):
        self.fnameError = 0
        self.lnameError = 0
        self.teachIDError = 0
        self.schoolError = 0
        self.emailError = 0
        self.passError = 0

        fname = self.teachFirst_lineEdit.text()
        mname = self.teachMiddle_lineEdit.text()
        lname = self.teachLast_lineEdit.text()
        school = self.teachSchool_lineEdit.text()
        teachID = self.teachID_lineEdit.text()

        email = self.teachEmail_lineEdit.text()
        password = self.teachPass_lineEdit.text()

# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if teachID == "":
            self.teachIDError = 1
        if school == "":
            self.schoolError = 1
        if email == "":
            self.emailError = 1
        if password == "" and password.isdigit() == False and len(password)+1 < 8:
            self.passError = 1

        if self.fnameError == 1:
            self.warningFname.setVisible(True)
        if self.lnameError == 1:
            self.warningLname.setVisible(True)
        if self.teachIDError == 1:
            self.warningYrSec.setVisible(True)
        if self.schoolError == 1:
            self.warningSchool.setVisible(True)        
        if self.emailError == 1:
            self.warningEmail.setVisible(True)
        if self.passError == 1:
            self.warningPass.setVisible(True)  

        if self.fnameError == 1 or self.lnameError == 1 or self.teachIDError == 1 or self.schoolError == 1 or self.emailError == 1 or self.passError == 1:
            self.frame.setGeometry(QtCore.QRect(50, 30, 295, 591))
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(0)

            self.fnameError = 0
            self.lnameError = 0
            self.teachIDError = 0
            self.schoolError = 0
            self.emailError = 0
            self.passError = 0
        else:
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(1)
            print(fname)
            print(mname)
            print(lname)
            print(teachID)
            print(school)
            print(email)
            print(password)

    def toBack(self):
        self.toGoBack = toTeachLogin()
        self.toGoBack.show()
        self.hide()

    def toExitProg(self):
        sys.exit()

class toDashboard(QMainWindow):
    def __init__(self):
        super(toDashboard, self).__init__()
        self.ui = Ui_dashboardWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.offset = None

        loadUi("dashboard.ui",self)
        self.leftMenuNum = 0
        self.centerMenuNum = 0
        self.rightMenuNum = 0
        self.infoMenuNum = 0
        self.popMenuNum = 0
        self.restoreWindow = 0
        self.maxWindow = False

        if self.centerMenuNum == 0:
            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(0)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start() 

            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(0)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 
        
        if self.rightMenuNum == 0:
            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(0)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start() 

            self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer2.setDuration(500)
            self.animaRightContainer2.setStartValue(0)
            self.animaRightContainer2.setEndValue(0)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 


        # self.rightMenuContainer.setVisible(False)
        self.lessonsContainer.setVisible(False)

        self.closeBtn.clicked.connect(self.toExitProg)
        self.restoreBtn.clicked.connect(self.bigWindow)
        self.minimizeBtn.clicked.connect(self.hideWindow)
        self.closeCenterMenu_pushButton.clicked.connect(self.hideCenterMenu)

        # LEFT SIDE BUTTONS
        self.menu_pushButton.clicked.connect(self.showLeftMenu)
        self.home_pushButton.clicked.connect(self.showHome)
        self.dataAnalysis_pushButton.clicked.connect(self.showModules)
        self.reports_pushButton.clicked.connect(self.showProgress)
        self.settings_pushButton.clicked.connect(self.showSettings)
        self.information_pushButton.clicked.connect(self.showInformation)
        self.help_pushButton.clicked.connect(self.showHelp)

        # MODULES BUTTONS
        self.limits_pushButton.clicked.connect(self.showLimitModules)
        self.parabola_pushButton.clicked.connect(self.showHyperbolaModules)
        self.hyperbola_pushButton.clicked.connect(self.showParabolaModules)

        # TOP SIDE BUTTONS
        self.profileMenu_pushButton.clicked.connect(self.showProfile)
        self.moreMenu_pushButton.clicked.connect(self.showMore)
        self.notification_pushButton.clicked.connect(self.showNotif)
        self.closeRightMenu_pushButton.clicked.connect(self.hideRightMenu)

        QSizeGrip(self.sizeGrip)

    def hideWindow(self):
        self.showMinimized()  
    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1

        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def showNotif(self):
        if self.rightMenuNum == 0:
            self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
            self.animaRightContainer2.setDuration(500)
            self.animaRightContainer2.setStartValue(0)
            self.animaRightContainer2.setEndValue(295)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 

            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(295)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start()
            
            self.rightMenuNum == 1
        self.rightMenuPages.setCurrentIndex(2)

    def showProfile(self):
        if self.rightMenuNum == 0:
            self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
            self.animaRightContainer2.setDuration(500)
            self.animaRightContainer2.setStartValue(0)
            self.animaRightContainer2.setEndValue(295)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 

            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(295)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start()
            
            self.rightMenuNum = 1
        self.rightMenuPages.setCurrentIndex(0)
    def showMore(self):
        if self.rightMenuNum == 0:
            self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
            self.animaRightContainer2.setDuration(500)
            self.animaRightContainer2.setStartValue(0)
            self.animaRightContainer2.setEndValue(295)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 

            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(295)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start()
            
            self.rightMenuNum = 1
        self.rightMenuPages.setCurrentIndex(1)

    def showLimitModules(self):
        self.lessonsMenuPages.setCurrentIndex(0)
        self.lessonsContainer.setVisible(True)

    def showHyperbolaModules(self):
        self.lessonsMenuPages.setCurrentIndex(2)
        self.lessonsContainer.setVisible(True)


    def showParabolaModules(self):
        self.lessonsMenuPages.setCurrentIndex(1)
        self.lessonsContainer.setVisible(True)


    def showHome(self):
        self.menuPages.setCurrentIndex(0)
        self.lessonsContainer.setVisible(False)
    def showModules(self):
        self.menuPages.setCurrentIndex(1)
    def showProgress(self):
        self.menuPages.setCurrentIndex(2)
        self.lessonsContainer.setVisible(False)

    def showSettings(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(228)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(228)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start()
            
            self.centerMenuNum = 1
        self.centerMenuPages.setCurrentIndex(0)
    
    def showInformation(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(228)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(228)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start()
            
            self.centerMenuNum = 1
        self.centerMenuPages.setCurrentIndex(2)
        
    def showHelp(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(228)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(228)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start()
            
            self.centerMenuNum = 1
        self.centerMenuPages.setCurrentIndex(1)

    def showLeftMenu(self):
        if self.leftMenuNum == 0:
            self.animation1 = QtCore.QPropertyAnimation(self.leftMenuContainer , b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(45)
            self.animation1.setEndValue(120)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start() 

            self.animation2 = QtCore.QPropertyAnimation(self.leftMenuContainer, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(45)
            self.animation2.setEndValue(120)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation2.start()

            self.leftMenuNum = 1
        else:
            self.animation1 = QtCore.QPropertyAnimation(self.leftMenuContainer, b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(120)
            self.animation1.setEndValue(45)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start() 

            self.animation2 = QtCore.QPropertyAnimation(self.leftMenuContainer, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(120)
            self.animation2.setEndValue(45)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation2.start()

            self.leftMenuNum = 0

        # pass

    def mousePressEvent(self, event):
        if self.maxWindow == True:
            pass
        else:
            if event.button() == QtCore.Qt.LeftButton:
                self.offset = event.pos()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.maxWindow == True:
            pass
        else:   
            if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.maxWindow == True:
            pass
        else:
            self.offset = None
            super().mouseReleaseEvent(event)

    def hideCenterMenu(self):
        self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
        self.animaCenterContainer1.setDuration(500)
        self.animaCenterContainer1.setStartValue(0)
        self.animaCenterContainer1.setEndValue(0)
        self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animaCenterContainer1.start() 

        self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
        self.animaCenterContainer2.setDuration(500)
        self.animaCenterContainer2.setStartValue(0)
        self.animaCenterContainer2.setEndValue(0)
        self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animaCenterContainer2.start() 
        self.centerMenuNum = 0

    def hideRightMenu(self):
        self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
        self.animaRightContainer1.setDuration(500)
        self.animaRightContainer1.setStartValue(0)
        self.animaRightContainer1.setEndValue(0)
        self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animaRightContainer1.start() 

        self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
        self.animaRightContainer2.setDuration(500)
        self.animaRightContainer2.setStartValue(0)
        self.animaRightContainer2.setEndValue(0)
        self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animaRightContainer2.start() 
        self.rightMenuNum = 0 

    def toExitProg(self):
        sys.exit()
 
class loadingScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("loadingScreen.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        pixmap = QPixmap("load1.jpg")
        self.setPixmap(pixmap)

    def progress(self):
        for i in range(100):
            time.sleep(0.1)
            self.progressBar.setValue(i)

class function:
    def loading(self):
        self.screen = splashScreen()
        self.screen.show()
        for i in range(100):
            self.screen.progressBar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.1)
        self.screen.close()
        self.next = toDashboard()
        self.next.show()

class splashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("loadingScreen.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        pixmap = QPixmap("load1.jpg")
        self.setPixmap(pixmap)
    def mousePressEvent(self, event):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # loading = loadingScreen()
    # loading.show()
    # loading.progress()
    w = toStudTeach()
    # w = toStudLogin()
    w.show()
    # loading.finish(w)
    sys.exit(app.exec_())








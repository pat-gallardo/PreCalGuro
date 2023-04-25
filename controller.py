import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
from PyQt5.QtSvg import QSvgWidget
from io import BytesIO

import matplotlib.pyplot as plt

from data.studTeach import Ui_studTeachWindow
from data.studLogin import Ui_studLoginWindow
from data.studRegister import Ui_studRegisterWindow
from data.teachLogin import Ui_teachLoginWindow
from data.teachRegister import Ui_teachRegisterWindow
from data.dashboard import Ui_dashboardWindow
from data.dashboardTeach import Ui_dashboardTeachWindow
from data.forgotPassBoth import Ui_forgotPassBothWindow
from data.updateInfo import Ui_updateInfoDialog
from data.lessonDashboard import Ui_topicLessonMainWindow
from data.warningToLogout import Ui_logoutDialog

from data.graph import * 
from data.training import *
import data.scores
from data.questions import display_random_question
import time

import pyrebase
import openai

# account to be used for STUDENT
# stud87313
# dummyemail@gmail.com
# thisispass

# account to be used for TEACHER
# 560498750
# dummybot@gmail.com
# passisthis

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

openai.api_key = os.getenv("OPENAI_API_KEY")

idKey = "stud87313"
submit_unit1 = False
submit_unit2 = False
pre_assess_total_items = 0
post_assess_total_items = 0
unitTest1_total_items = 0
unitTest2_total_items = 0

new_unitTest1 = True
new_unitTest2 = True
new_preAssess = True
new_postAssess = True

firebaseConfig = { "apiKey": "AIzaSyDyihbb440Vb2o0CIMINI_UfQLRln0uvXs",
  "authDomain": "mathguro-46712.firebaseapp.com",
  "databaseURL": "https://mathguro-46712-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "mathguro-46712",
  "storageBucket": "mathguro-46712.appspot.com",
  "messagingSenderId": "24039260333",
  "appId": "1:24039260333:web:673adf358560ef3cbe4624",
  "measurementId": "G-YP2867V22T"}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db=firebase.database()

# uid = userInput
#auth.delete_user(uid) // DELETE A USER IN AUTHENTICATION

# Dont mind about this warning, gumagamit kase ako ng auto-py-to-exe to produce an .exe file
# ang ginagawa niya if matagal mag load ang App, (true yan since masyadong mabigat ang app natin)
# mag viview sya ng splashscreen image lang
if getattr(sys, 'frozen', False):
    import pyi_splash

class toStudTeach(QMainWindow):
    def __init__(self):
        super(toStudTeach, self).__init__()
        self.ui = Ui_studTeachWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/studTeach.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

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

        loadUi("data/studLogin.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.warning_Widget.setVisible(False)

        self.closeButton.clicked.connect(self.toExitProg)
        self.backButton.clicked.connect(self.toBack)
        self.loginStudButton.clicked.connect(self.login)
        self.toRegisterStudButton.clicked.connect(self.toRegister)
        self.toForgotPassStudButton.clicked.connect(self.toForgot)

    def toForgot(self):
        self.toForg = toStudForgotPass()
        self.toForg.show()
        self.hide()

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
        studSchoolID = self.studID_lineEdit.text()
        global idKey
        idKey = studSchoolID

        try:
                # DITO CHECK STUD ID
            teachKey = db.child("student").get()
            for keyAccess in teachKey.each():
                if keyAccess.val()["studentSchoolID"] == studSchoolID:
                    print("Correct ID")

                    login= auth.sign_in_with_email_and_password(email,password)
                    login = auth.refresh(login['refreshToken'])
                    # now we have a fresh token
                    login['idToken']
                    print("Login Successfully")
                    print(auth.get_account_info(login['idToken']))

                    print(email)
                    print(password)
                    
                    self.hide()
                    self.toLogin = splashScreen()
                    self.toLogin.show()
                    self.toLogin.progress()  

                else:
                    self.warning_Widget.setVisible(True)
                    self.warningPages.setCurrentIndex(0)
                    print("Invalid email or password.")

        except:
                self.warning_Widget.setVisible(True)
                self.warningPages.setCurrentIndex(0)
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

class toStudForgotPass(QMainWindow):
    def __init__(self):
        super(toStudForgotPass, self).__init__()
        self.ui = Ui_forgotPassBothWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/forgotPassBoth.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.forgotPassPages.setCurrentIndex(0)
        self.warningStudEmail.setVisible(False)
        self.studWarnContainer.setVisible(False)
        self.studCheckEmail_Button.clicked.connect(self.toCheckEmail)
        self.backButton.clicked.connect(self.toBack)

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

    def toCheckEmail(self):
        emailCheck = self.studCheckEmail_lineEdit.text()

        try:
            all_student = db.child("student").get()
            for student in all_student.each():
                if student.val()["email"] == emailCheck:
                    print("correct email")
                    # TO SEND EMAIL TO RESET PASSWORD
                    auth.send_password_reset_email(emailCheck)
                    self.studWarnContainer.setVisible(True)  
                    self.studWarnSubContainer.setCurrentIndex(1)      
                else:
                    self.warningStudEmail.setVisible(True)
                    self.studWarnContainer.setVisible(True)
        except:
            self.warningStudEmail.setVisible(True)
            self.studWarnContainer.setVisible(True)

    def toBack(self):
        self.toLogin = toStudLogin()
        self.toLogin.show()
        self.hide()

class toStudRegister(QMainWindow):
    def __init__(self):
        super(toStudRegister, self).__init__()
        self.ui = Ui_studRegisterWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/studRegister.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.warningFname.setVisible(False)
        self.warningLname.setVisible(False)
        self.warningYrSec.setVisible(False)
        self.warningSchool.setVisible(False)
        self.warningEmail.setVisible(False)
        self.warningPass.setVisible(False)
        self.warningContainer.setVisible(False)
        self.warningStudID.setVisible(False)

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
        self.studIDError = 0

        fname = self.studFirst_lineEdit.text()
        mname = self.studMiddle_lineEdit.text()
        lname = self.studLast_lineEdit.text()
        school = self.studSchool_lineEdit.text()
        section = self.studSec_lineEdit.text()
        course = self.studGrd_comboBox.currentText()
        year = self.studYr_comboBox.currentText()
        studentSchoolID = self.studSchoolID_lineEdit.text()
        isActive = "1"
        email = self.studEmail_lineEdit.text()
        password = self.studPass_lineEdit.text()

# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if section == "" or year == "Year" or course == "Course":
            self.yrSecError = 1
        if school == "":
            self.schoolError = 1
        if email == "":
            self.emailError = 1
        if password == "" and password.isdigit() == False and len(password)+1 < 8:
            self.passError = 1
        if studentSchoolID == "":
            self.studIDError = 1

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
        if self.studIDError == 1:
            self.warningStudID.setVisible(True)

        if self.fnameError == 1 or self.lnameError == 1 or self.yrSecError == 1 or self.schoolError == 1 or self.emailError == 1 or self.passError == 1:
            self.frame.setGeometry(QtCore.QRect(40, 50, 295, 610))
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(0)
            self.fnameError = 0
            self.lnameError = 0
            self.yrSecError = 0
            self.schoolError = 0
            self.emailError = 0
            self.passError = 0
            self.studIDError = 0
        else:
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(1)
            self.studFirst_lineEdit.clear()
            self.studMiddle_lineEdit.clear()
            self.studLast_lineEdit.clear()
            self.studSchool_lineEdit.clear()
            self.studSec_lineEdit.clear()
            self.studSchoolID_lineEdit.clear()
            self.studEmail_lineEdit.clear()
            self.studPass_lineEdit.clear()
            print(fname)
            print(mname)
            print(lname)
            print(course)
            print(year)
            print(section)
            print(studentSchoolID)
            print(isActive)
            print(school)
            print(email)
            print(password)

            reigster= auth.create_user_with_email_and_password(email, password)
            
            data ={"fname":fname,"mname":mname,"lname":lname, "course":course
       ,"year":year,"section":section,"studentSchoolID":studentSchoolID,"school":school,"email":email
       ,"isActive":isActive, "assessment_score":"0", "post_assessment_score":"0", "post_assessment_score1":"0",
       "assessment_score1":"0","unitTest1_score":"0", "unitTest2_score":"0"}
            db.child("student").push(data)

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

        loadUi("data/teachLogin.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.warning_Widget.setVisible(False)

        self.closeButton.clicked.connect(self.toExitProg)
        self.backButton.clicked.connect(self.toBack)
        self.loginTeachButton.clicked.connect(self.login)
        self.toRegisterTeachButton.clicked.connect(self.toRegister)
        self.toForgotPassTeachButton.clicked.connect(self.toForgot)

    def toForgot(self):
        self.toForg = toTeachForgotPass()
        self.toForg.show()
        self.hide()

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
        teachSchoolID = self.teachID_lineEdit.text()
        global idKey
        idKey = teachSchoolID

        try:
            teachKey = db.child("teacher").get()
            for keyAccess in teachKey.each():
                if keyAccess.val()["teachSchoolID"] == teachSchoolID:
                    print("yes")

                    login= auth.sign_in_with_email_and_password(email,password)
                    login = auth.refresh(login['refreshToken'])
                    # now we have a fresh token
                    login['idToken']
                    print("Login Successfully")
                    print(auth.get_account_info(login['idToken']))

                    print(email)
                    print(password)
                    
                    self.toLogin = toSplashScreen()
                    self.toLogin.show()
                    self.toLogin.progress()
                else:
                    self.warning_Widget.setVisible(True)
                    print("Invalid email or password.")
        except:
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

class toTeachForgotPass(QMainWindow):
    def __init__(self):
        super(toTeachForgotPass, self).__init__()
        self.ui = Ui_forgotPassBothWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/forgotPassBoth.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.forgotPassPages.setCurrentIndex(1)
        self.warningTeachEmail.setVisible(False)
        self.teachWarnContainer.setVisible(False)
        self.teachCheckEmail_Button.clicked.connect(self.toCheckEmail)
        self.backButton_2.clicked.connect(self.toBack)

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

    def toCheckEmail(self):
        emailCheck = self.teachCheckEmail_lineEdit.text()

        try:
            all_teacher = db.child("teacher").get()
            for teacher in all_teacher.each():
                if teacher.val()["email"] == emailCheck:
                    print("correct email")
                    # TO SEND EMAIL TO RESET PASSWORD
                    auth.send_password_reset_email(emailCheck)
                    self.teachWarnContainer.setVisible(True)  
                    self.teachWarnSubContainer.setCurrentIndex(1)      
                else:
                    self.warningTeachEmail.setVisible(True)
                    self.teachWarnContainer.setVisible(True)
        except:
            self.warningTeachEmail.setVisible(True)
            self.teachWarnContainer.setVisible(True)

    def toBack(self):
        self.toLogin = toTeachLogin()
        self.toLogin.show()
        self.hide()

class toTeachRegister(QMainWindow):
    def __init__(self):
        super(toTeachRegister, self).__init__()
        self.ui = Ui_teachRegisterWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/teachRegister.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

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
        teachSchoolID = self.teachID_lineEdit.text()
        course = self.teachGrd_comboBox.currentText()
        isActive = "1"

        email = self.teachEmail_lineEdit.text()
        password = self.teachPass_lineEdit.text()

# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if teachSchoolID == "" or course == "Course":
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
            self.frame.setGeometry(QtCore.QRect(50, 30, 295,620))
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
            self.teachFirst_lineEdit.clear()
            self.teachMiddle_lineEdit.clear()
            self.teachLast_lineEdit.clear()
            self.teachSchool_lineEdit.clear()
            self.teachSec_lineEdit.clear()
            self.teachSchoolID_lineEdit.clear()
            self.teachEmail_lineEdit.clear()
            self.teachPass_lineEdit.clear()
            print(fname)
            print(mname)
            print(lname)
            print(course)
            print(teachSchoolID)
            print(isActive)
            print(school)
            print(email)
            print(password)

            reigster= auth.create_user_with_email_and_password(email, password)

            data ={"fname":fname,"mname":mname,"lname":lname, "course":course
       ,"teachSchoolID":teachSchoolID,"school":school,"email":email
       ,"isActive":isActive}
            db.child("teacher").push(data)

    def toBack(self):
        self.toGoBack = toTeachLogin()
        self.toGoBack.show()
        self.hide()

    def toExitProg(self):
        sys.exit()

class toStudUpdateProfile(QDialog):
    def __init__(self):
        super(toStudUpdateProfile, self).__init__()
        self.ui = Ui_updateInfoDialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/updateInfo.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"

        self.setWindowTitle(title)
        self.updateInfoPages.setCurrentIndex(0)
        self.studWarnFirstContainer.setVisible(False)
        self.studWarnLastContainer.setVisible(False)
        self.studWarnSchoolContainer.setVisible(False)
        self.studWarnContainer.setVisible(False)
        self.updateStudButton.clicked.connect(self.toUpdateProfile)
        self.backButton.clicked.connect(self.toBack)

        self.setWindowModality(Qt.ApplicationModal)

    def toUpdateProfile(self):
        self.fnameError = 0
        self.lnameError = 0
        self.schoolError = 0

        fname = self.updStudFirst_lineEdit.text()
        mname = self.updStudMiddle_lineEdit.text()
        lname = self.updStudLast_lineEdit.text()
        school = self.updStudSchool_lineEdit.text()

# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if school == "":
            self.schoolError = 1

        if self.fnameError == 1:
            self.studWarnFirstContainer.setVisible(True)
        if self.lnameError == 1:
            self.studWarnLastContainer.setVisible(True)
        if self.schoolError == 1:
            self.studWarnSchoolContainer.setVisible(True)        

        if self.fnameError == 1 or self.lnameError == 1 or self.schoolError == 1:
            self.studWarnContainer.setVisible(True)
            self.studWarnSubContainer.setCurrentIndex(0)

            self.fnameError = 0
            self.lnameError = 0
            self.teachIDError = 0
            self.schoolError = 0
        else:
            self.studWarnContainer.setVisible(True)
            self.studWarnSubContainer.setCurrentIndex(1)

            self.updStudFirst_lineEdit.clear()
            self.updStudMiddle_lineEdit.clear()
            self.updStudLast_lineEdit.clear()
            self.updStudSchool_lineEdit.clear()

            print(fname)
            print(mname)
            print(lname)
            print(school)

            studKey = db.child("student").get()
            for keyAccess in studKey.each():
                if keyAccess.val()["studentSchoolID"] == idKey:
                    keyID = keyAccess.key()
            db.child("student").child(keyID).update({"fname":fname, "mname":mname,
                                                     "lname":lname, "school":school})
            self.hide()
            self.next = toDashboard()
            self.next.show()

    def toBack(self):
            self.hide()
            self.next = toDashboard()
            self.next.show()

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

#############################################################################################
class toDashboard(QMainWindow):
    def __init__(self):
        super(toDashboard, self).__init__()
        self.ui = Ui_dashboardWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.offset = None

        loadUi("data/dashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        print(idKey)

        

        pre_quest = []
        post_quest = []
        unit_test1_quest = []
        unit_test2_quest = []
        list_of_sol =[]

        pre_total_score = 0
        post_total_score = 0
        unit_test1_total_score = 0
        unit_test2_total_score = 0

        # RNGED PRE-ASSESSMENT QUESTIONS
        # circle_ans, circle_solu,  returned_circle = display_random_question.pre_assess_circle()
        # parabola_ans, parabola_solu, returned_parabola = display_random_question.pre_assess_parabola()
        # ellipse_ans, ellipse_solu, returned_ellipse = display_random_question.pre_assess_ellipse()
        # hyperbola_ans, hyperbola_solu, returned_hyperbola = display_random_question.pre_assess_hyper()
        # substitution_ans, substitution_solu, returned_substitution = display_random_question.pre_assess_subs()
        # elimination_ans, elimination_solu, returned_elimination = display_random_question.pre_assess_elim()

        # pre_quest.append(returned_circle)
        # pre_quest.append(returned_parabola)
        # pre_quest.append(returned_ellipse)
        # pre_quest.append(returned_hyperbola)
        # pre_quest.append(returned_elimination)
        # pre_quest.append(returned_substitution)

        # list_of_sol.append(circle_ans)
        # list_of_sol.append(circle_solu)
        # list_of_sol.append(parabola_ans)
        # list_of_sol.append(parabola_solu)
        # list_of_sol.append(ellipse_ans)
        # list_of_sol.append(ellipse_solu)
        # list_of_sol.append(hyperbola_ans)
        # list_of_sol.append(hyperbola_solu)
        # list_of_sol.append(substitution_ans)
        # list_of_sol.append(substitution_solu)
        # list_of_sol.append(elimination_ans)
        # list_of_sol.append(elimination_solu)

        # pre_question1, pre_question2, pre_question3, pre_question4, pre_question5 = display_random_question.random_questions(pre_quest)

        # pre_answerScore1, pre_answerId1, pre_solutionScore1, pre_solutionId1 = display_random_question.get_scores_for_pre(pre_question1)
        # pre_answerScore2, pre_answerId2, pre_solutionScore2, pre_solutionId2 = display_random_question.get_scores_for_pre(pre_question2)
        # pre_answerScore3, pre_answerId3, pre_solutionScore3, pre_solutionId3 = display_random_question.get_scores_for_pre(pre_question3)
        # pre_answerScore4, pre_answerId4, pre_solutionScore4, pre_solutionId4 = display_random_question.get_scores_for_pre(pre_question4)
        # pre_answerScore5, pre_answerId5, pre_solutionScore5, pre_solutionId5 = display_random_question.get_scores_for_pre(pre_question5)

        # pre_allItem_score = int(pre_answerScore1) + int(pre_answerScore2) + int(pre_answerScore3) + int(pre_answerScore4) + int(pre_answerScore5) + int(pre_solutionScore1) + int(pre_solutionScore2) + int(pre_solutionScore3) + int(pre_solutionScore4) + int(pre_solutionScore5)

        # # RNGED POST-ASSESSMENT QUESTIONS
        # circle_ans1, circle_solu1,  returned_circle1 = display_random_question.post_assess_circle()
        # parabola_ans1, parabola_solu1, returned_parabola1 = display_random_question.pre_assess_parabola()
        # ellipse_ans1, ellipse_solu1, returned_ellipse1 = display_random_question.post_assess_ellipse()
        # hyperbola_ans1, hyperbola_solu1, returned_hyperbola1 = display_random_question.post_assess_hyper()
        # substitution_ans1, substitution_solu1, returned_substitution1 = display_random_question.post_assess_subs()
        # elimination_ans1, elimination_solu1, returned_elimination1 = display_random_question.post_assess_elim()

        # post_quest.append(returned_circle1)
        # post_quest.append(returned_parabola1)
        # post_quest.append(returned_ellipse1)
        # post_quest.append(returned_hyperbola1)
        # post_quest.append(returned_elimination1)
        # post_quest.append(returned_substitution1)

        # list_of_sol.append(circle_ans1)
        # list_of_sol.append(circle_solu1)
        # list_of_sol.append(parabola_ans1)
        # list_of_sol.append(parabola_solu1)
        # list_of_sol.append(ellipse_ans1)
        # list_of_sol.append(ellipse_solu1)
        # list_of_sol.append(hyperbola_ans1)
        # list_of_sol.append(hyperbola_solu1)
        # list_of_sol.append(substitution_ans1)
        # list_of_sol.append(substitution_solu1)
        # list_of_sol.append(elimination_ans1)
        # list_of_sol.append(elimination_solu1)

        # post_question1, post_question2, post_question3, post_question4, post_question5= display_random_question.random_questions(post_quest)

        # post_answerScore1, post_answerId1, post_solutionScore1, post_solutionId1 = display_random_question.get_scores_for_post(post_question1)
        # post_answerScore2, post_answerId2, post_solutionScore2, post_solutionId2 = display_random_question.get_scores_for_post(post_question2)
        # post_answerScore3, post_answerId3, post_solutionScore3, post_solutionId3 = display_random_question.get_scores_for_post(post_question3)
        # post_answerScore4, post_answerId4, post_solutionScore4, post_solutionId4 = display_random_question.get_scores_for_post(post_question4)
        # post_answerScore5, post_answerId5, post_solutionScore5, post_solutionId5 = display_random_question.get_scores_for_post(post_question5)

        # post_allItem_score = int(post_answerScore1) + int(post_answerScore2) + int(post_answerScore3) + int(post_answerScore4) + int(post_answerScore5) + int(post_solutionScore1) + int(post_solutionScore2) + int(post_solutionScore3) + int(post_solutionScore4) + int(post_solutionScore5)

        # # RNGED UNIT TEST 1 QUESTIONS
        # circle_ans2, circle_solu2,  returned_circle2 = display_random_question.unit_test_circle()
        # parabola_ans2, parabola_solu2, returned_parabola2 = display_random_question.unit_test_parabola()
        # ellipse_ans2, ellipse_solu2, returned_ellipse2 = display_random_question.unit_test_ellipse()
        # hyperbola_ans2, hyperbola_solu2, returned_hyperbola2 = display_random_question.unit_test_hyper()

        # unit_test1_quest.append(returned_circle2)
        # unit_test1_quest.append(returned_parabola2)
        # unit_test1_quest.append(returned_ellipse2)
        # unit_test1_quest.append(returned_hyperbola2)

        # list_of_sol.append(circle_ans2)
        # list_of_sol.append(circle_solu2)
        # list_of_sol.append(parabola_ans2)
        # list_of_sol.append(parabola_solu2)
        # list_of_sol.append(ellipse_ans2)
        # list_of_sol.append(ellipse_solu2)
        # list_of_sol.append(hyperbola_ans2)
        # list_of_sol.append(hyperbola_solu2)

        # unit_test1_question1, unit_test1_question2, unit_test1_question3, unit_test1_question4, unit_test1_question5, unit_test1_question6, unit_test1_question7, unit_test1_question8 ,unit_test1_question9 ,unit_test1_question10= display_random_question.random_questions_2(unit_test1_quest)

        # unit_test1_answerScore1, unit_test1_answerId1, unit_test1_solutionScore1, unit_test1_solutionId1 = display_random_question.get_scores_for_unit1(unit_test1_question1)
        # unit_test1_answerScore2, unit_test1_answerId2, unit_test1_solutionScore2, unit_test1_solutionId2 = display_random_question.get_scores_for_unit1(unit_test1_question2)
        # unit_test1_answerScore3, unit_test1_answerId3, unit_test1_solutionScore3, unit_test1_solutionId3 = display_random_question.get_scores_for_unit1(unit_test1_question3)
        # unit_test1_answerScore4, unit_test1_answerId4, unit_test1_solutionScore4, unit_test1_solutionId4 = display_random_question.get_scores_for_unit1(unit_test1_question4)
        # unit_test1_answerScore5, unit_test1_answerId5, unit_test1_solutionScore5, unit_test1_solutionId5 = display_random_question.get_scores_for_unit1(unit_test1_question5)
        # unit_test1_answerScore6, unit_test1_answerId6, unit_test1_solutionScore6, unit_test1_solutionId6 = display_random_question.get_scores_for_unit1(unit_test1_question6)
        # unit_test1_answerScore7, unit_test1_answerId7, unit_test1_solutionScore7, unit_test1_solutionId7 = display_random_question.get_scores_for_unit1(unit_test1_question7)
        # unit_test1_answerScore8, unit_test1_answerId8, unit_test1_solutionScore8, unit_test1_solutionId8 = display_random_question.get_scores_for_unit1(unit_test1_question8)
        # unit_test1_answerScore9, unit_test1_answerId9, unit_test1_solutionScore9, unit_test1_solutionId9 = display_random_question.get_scores_for_unit1(unit_test1_question9)
        # unit_test1_answerScore10, unit_test1_answerId10, unit_test1_solutionScore10, unit_test1_solutionId10 = display_random_question.get_scores_for_unit1(unit_test1_question10)

        # unit1_allItem_score = int(unit_test1_answerScore1) + int(unit_test1_answerScore2) + int(unit_test1_answerScore3) + int(unit_test1_answerScore4) + int(unit_test1_answerScore5) + int(unit_test1_answerScore6) + int(unit_test1_answerScore7) + int(unit_test1_answerScore8) + int(unit_test1_answerScore9) + int(unit_test1_answerScore10) + int(unit_test1_solutionScore1) + int(unit_test1_solutionScore2) + int(unit_test1_solutionScore3) + int(unit_test1_solutionScore4) + int(unit_test1_solutionScore5) + int(unit_test1_solutionScore6) + int(unit_test1_solutionScore7) + int(unit_test1_solutionScore8) + int(unit_test1_solutionScore9) + int(unit_test1_solutionScore10)

        # display_random_question.to_json(list_of_sol)

        
        all_students = db.child("student").get()
        for student in all_students.each():
            if student.val()["studentSchoolID"] == idKey:

                studFname = (student.val()["fname"])
                studMname = (student.val()["mname"])
                studLname = (student.val()["lname"])
                studCourse = (student.val()["course"])
                studYear = (student.val()["year"])
                studSection = (student.val()["section"])
                studSchool = (student.val()["school"])
                studAssessment_score = (student.val()["assessment_score"])
                studPostAssessment_score = (student.val()["post_assessment_score"])
                studUnitTest1_score =(student.val()["unitTest1_score"])
                studUnitTest2_score =(student.val()["unitTest2_score"])

        # print(studID)
        self.profNameLineEdit.insertPlainText(studLname.upper())
        self.profNameLineEdit.insertPlainText(", ")
        self.profNameLineEdit.insertPlainText(studFname.upper())
        self.profNameLineEdit.insertPlainText(" ")
        self.profNameLineEdit.insertPlainText(studMname.upper())
        self.profCourseLineEdit.insertPlainText(studCourse.upper())
        self.profCourseLineEdit.insertPlainText(" ")
        self.profCourseLineEdit.insertPlainText(studYear.upper())
        self.profCourseLineEdit.insertPlainText(" ")
        self.profCourseLineEdit.insertPlainText(studSection.upper())
        self.profSchoolLineEdit.insertPlainText(studSchool.upper())

        ave_assess = (int(studAssessment_score) / 15) * 100    
        if ave_assess > 80:
            assess_result=("Outstanding")
        elif ave_assess > 60:
            assess_result=("Very Good")
        elif ave_assess > 40:
            assess_result=("Good")
        else:
            assess_result=("Needs Improvement")

        ave_assess = (int(studPostAssessment_score) / 15) * 100    
        if ave_assess > 80:
            postassess_result=("Outstanding")
        elif ave_assess > 60:
            postassess_result=("Very Good")
        elif ave_assess > 40:
            postassess_result=("Good")
        else:
            postassess_result=("Needs Improvement")

        self.show_scorePreAssessMsg_label.setText(assess_result)
        self.show_scorePostAssessMsg_label.setText(postassess_result)

        self.preAssess1_label.setText(str(studAssessment_score)+"/25")
        self.preAssess2_label.setText(str(studAssessment_score)+"/25")
        self.postAssess1_label.setText(str(studPostAssessment_score)+"/25")
        self.postAssess2_label.setText(str(studPostAssessment_score)+"/25")
        self.show_scoreUnit1_label.setText(str(studUnitTest1_score)+"/50")
        self.show_scoreUnit2_label.setText(str(studUnitTest2_score)+"/50")

        self.preAssess1_progressBar.setValue(int(studAssessment_score))
        self.preAssess1_progressBar.setMaximum(25)
        self.preAssess2_progressBar.setValue(int(studAssessment_score))
        self.preAssess2_progressBar.setMaximum(25)
        self.postAssess1_progressBar.setValue(int(studAssessment_score))
        self.postAssess1_progressBar.setMaximum(25)
        self.postAssess2_progressBar.setValue(int(studAssessment_score))
        self.postAssess2_progressBar.setMaximum(25)
        self.unitTest1_progressBar.setValue(int(studUnitTest1_score))
        self.unitTest1_progressBar.setMaximum(50)
        self.unitTest2_progressBar.setValue(int(studUnitTest2_score))
        self.unitTest2_progressBar.setMaximum(50)
        
        self.leftMenuNum = 0
        self.centerMenuNum = 0
        self.rightMenuNum = 0
        self.infoMenuNum = 0
        self.popMenuNum = 0
        self.restoreWindow = 0
        self.maxWindow = False
        # LESSONS COUNTER
        self.lesson1_1Count = 0
        self.lesson1_2Count = 0
        self.lesson2_1Count = 0
        self.lesson2_2Count = 0
        self.lesson3_1Count = 0
        self.lesson3_3Count = 0
        self.lesson3_4Count = 0

        self.chatbot_session = 0
        self.chatbot_count = 0
        self.user_count = 0

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
        self.lesson1_1Container.setVisible(False)
        self.lesson2_1Container.setVisible(False)

        self.lessonInfo1Container.setVisible(False)
        self.lessonInfo2Container.setVisible(False)

        self.assessment_pushButton.clicked.connect(self.assessmentWindow)

        self.closeBtn.clicked.connect(self.showMinimized)
        self.restoreBtn.clicked.connect(self.bigWindow)
        self.minimizeBtn.clicked.connect(self.hideWindow)
        self.closeCenterMenu_pushButton.clicked.connect(self.hideCenterMenu)

        # LEFT SIDE BUTTONS
        self.menu_pushButton.clicked.connect(self.showLeftMenu)
        self.home_pushButton.clicked.connect(self.showHome)
        self.dataAnalysis_pushButton.clicked.connect(self.showModules)
        self.reports_pushButton.clicked.connect(self.showProgress)
        self.information_pushButton.clicked.connect(self.showInformation)
        self.help_pushButton.clicked.connect(self.showHelp)

        # MODULES BUTTONS
        self.module1_pushButton.clicked.connect(self.showModule1)
        self.module2_pushButton.clicked.connect(self.showModule2)
        self.postTest_pushButton.clicked.connect(self.postAssessmentWindow)

        # TOP SIDE BUTTONS
        self.profileMenu_pushButton.clicked.connect(self.showProfile)
        self.notification_pushButton.clicked.connect(self.showNotif)
        self.closeRightMenu_pushButton.clicked.connect(self.hideRightMenu)

        # PROFILE BUTTONS
        self.updateAcc_pushButton.clicked.connect(self.updateProfile)
        self.logoutAcc_pushButton.clicked.connect(self.logoutProfile)

        # CHAT BUTTONS
        self.sendChat_Button.clicked.connect(self.sendMessage)
        self.checkEquation_Button.clicked.connect(self.checkEquat)

        # MATH EQUATION BUTTONS
        self.func1_pushButton.clicked.connect(self.powerOf)
        self.func2_pushButton.clicked.connect(self.powerOfN)
        self.func3_pushButton.clicked.connect(self.sqrtOfN)
        self.func4_pushButton.clicked.connect(self.degOfN)
        self.func5_pushButton.clicked.connect(self.primeOfN)
        self.func6_pushButton.clicked.connect(self.fracN)
        self.func7_pushButton.clicked.connect(self.leftParenthesis)
        self.func8_pushButton.clicked.connect(self.rightParenthesis)
        self.func9_pushButton.clicked.connect(self.piMath)
        self.func10_pushButton.clicked.connect(self.summation)
        self.func11_pushButton.clicked.connect(self.infinity)
        self.func12_pushButton.clicked.connect(self.theta)
        self.func13_pushButton.clicked.connect(self.sinMath)
        self.func14_pushButton.clicked.connect(self.cosMath)
        self.func15_pushButton.clicked.connect(self.tanMath)
        self.func16_pushButton.clicked.connect(self.cotMath)
        self.func17_pushButton.clicked.connect(self.cscMath)
        self.func18_pushButton.clicked.connect(self.secMath)
        self.func19_pushButton.clicked.connect(self.addMath)
        self.func20_pushButton.clicked.connect(self.subtractMath)
        self.func21_pushButton.clicked.connect(self.multiplyMath)
        self.func22_pushButton.clicked.connect(self.divideMath)
        self.func23_pushButton.clicked.connect(self.decimalMath)
        self.func24_pushButton.clicked.connect(self.inverseMath)

        # TOPIC BUTTONS    
        self.lesson1_1ApushButton.clicked.connect(self.lesson1_1A)
        self.lesson1_1BpushButton.clicked.connect(self.lesson1_1B)
        self.lesson1_1CpushButton.clicked.connect(self.lesson1_1C)
        self.lesson1_1DpushButton.clicked.connect(self.lesson1_1D)
        self.lesson1_1TestpushButton.clicked.connect(self.lesson1_1Test)

        self.lesson2_1ApushButton.clicked.connect(self.lesson2_1A)
        self.lesson2_1BpushButton.clicked.connect(self.lesson2_1B)
        self.lesson2_1CpushButton.clicked.connect(self.lesson2_1C)
        self.lesson2_1TestpushButton.clicked.connect(self.lesson2_1Test)

        # PROCEED BUTTONS OF TOPICS      
        self.proceedLesson1_1A_pushButton.clicked.connect(self.lessons_circle)
        self.proceedLesson1_1B_pushButton.clicked.connect(self.lessons_parabola)
        self.proceedLesson1_1C_pushButton.clicked.connect(self.lessons_ellipse)
        self.proceedLesson1_1D_pushButton.clicked.connect(self.lessons_hyperbola)

        self.proceedLesson1_2A_pushButton.clicked.connect(self.lessons_substitute)
        self.proceedLesson1_2B_pushButton.clicked.connect(self.lessons_eliminate)
        self.proceedLesson1_2C_pushButton.clicked.connect(self.lessons_graphSolApp)

        # UNIT TESTS
        self.proceedLesson1_1Test_pushButton.clicked.connect(self.unitTest1)
        self.proceedLesson1_2Test_pushButton.clicked.connect(self.unitTest2)
        QSizeGrip(self.sizeGrip)

    def assessmentWindow(self):
        self.hide()
        self.assessment = assessmentWindow()
        self.assessment.show()
    def postAssessmentWindow(self):
        self.hide()
        all_students = db.child("student").get()
        for student in all_students.each():
            if student.val()["studentSchoolID"] == idKey:
                studUnitTest1_score =(student.val()["unitTest1_score"])
                studUnitTest2_score =(student.val()["unitTest2_score"])
                
        ave_unitTest1 = (int(studUnitTest1_score) / 50) * 100  
        ave_unitTest2 = (int(studUnitTest2_score) / 50) * 100  
        if ave_unitTest1 > 80 and ave_unitTest2 > 80:
            self.postAssessment = postAssessmentWindow_accept()
        else:
            self.postAssessment = postAssessmentWindow_failed()
        self.postAssessment.show()

# PROCEED BUTTON OF TOPICS FUNCTIONS
    def lessons_circle(self):
        self.hide()
        self.circle = topicLesson1()
        self.circle.show()
    def lessons_parabola(self):
        self.hide()
        self.parabola = topicLesson2()
        self.parabola.show()
    def lessons_ellipse(self):
        self.hide()
        self.ellipse = topicLesson3()
        self.ellipse.show()
    def lessons_hyperbola(self):
        self.hide()
        self.hyperbola= topicLesson4()
        self.hyperbola.show()
    def lessons_substitute(self):
        self.hide()
        self.substitute = topicLesson5()
        self.substitute.show()
    def lessons_eliminate(self):
        self.hide()
        self.eliminate = topicLesson6()
        self.eliminate.show()
    def lessons_graphSolApp(self):
        self.hide()
        self.graphSolApp = topicLesson7()
        self.graphSolApp.show()

# UNIT TEST 
    def unitTest1(self):
        global submit_unit1
        submit_unit1 = False
        data.scores.check_unit1_q1_sol = ""
        data.scores.check_unit1_q1_ans = ""
        data.scores.check_unit1_q2_sol = ""
        data.scores.check_unit1_q2_center_ans = ""
        data.scores.check_unit1_q2_radius_ans = ""
        data.scores.check_unit1_q3_sol = ""
        data.scores.check_unit1_q3_vertex_ans = ""
        data.scores.check_unit1_q3_focus_ans= ""
        data.scores.check_unit1_q4_sol= ""
        data.scores.check_unit1_q4_vertex_ans= ""
        data.scores.check_unit1_q4_focus_ans= ""
        data.scores.check_unit1_q5_sol= ""
        data.scores.check_unit1_q5_center_ans= ""
        data.scores.check_unit1_q6_sol= ""
        data.scores.check_unit1_q6_foci1_ans= ""
        data.scores.check_unit1_q6_foci2_ans= ""
        data.scores.check_unit1_q7_sol= ""
        data.scores.check_unit1_q7_vertex1_ans= ""
        data.scores.check_unit1_q7_vertex2_ans= ""
        data.scores.check_unit1_q8_sol= ""
        data.scores.check_unit1_q8_center_ans= ""
        data.scores.check_unit1_q9_sol= ""
        data.scores.check_unit1_q9_minorAxis_ans= ""
        data.scores.check_unit1_q10_sol= ""
        data.scores.check_unit1_q10_standEquat_ans= ""

        self.hide()
        self.unitTestConics = unitTest_1()
        self.unitTestConics.show()
    def unitTest2(self):
        global submit_unit2
        submit_unit2 = False
        data.scores.check_unit2_q1_sol = ""
        data.scores.check_unit2_q1_ans = ""
        data.scores.check_unit2_q2_sol = ""
        data.scores.check_unit2_q2_ans = ""
        data.scores.check_unit2_q3_sol = ""
        data.scores.check_unit2_q3_ans = ""
        data.scores.check_unit2_q4_sol = ""
        data.scores.check_unit2_q4_ans = ""
        data.scores.check_unit2_q5_sol = ""
        data.scores.check_unit2_q5_ans = ""
        data.scores.check_unit2_q6_sol = ""
        data.scores.check_unit2_q6_ans = ""
        data.scores.check_unit2_q7_sol = ""
        data.scores.check_unit2_q7_ans = ""
        data.scores.check_unit2_q8_sol = ""
        data.scores.check_unit2_q8_ans = ""
        data.scores.check_unit2_q9_sol = ""
        data.scores.check_unit2_q9_ans = ""
        data.scores.check_unit2_q10_sol = ""
        data.scores.check_unit2_q10_ans = ""

        self.hide()
        self.unitTestSys = unitTest_2()
        self.unitTestSys.show()

# PROFILE BUTTON FUNCTIONS
    def updateProfile(self):
        self.hide()
        self.toUpdateProf = toStudUpdateProfile()
        self.toUpdateProf.show()
    def logoutProfile(self):
        self.toLogoutStud = toStudLogout(self)
        self.toLogoutStud.show()

# LESSON BUTTON FUNCTIONS
    def lesson1_1A(self):
        self.lessonInfoSubContainer.setCurrentIndex(1)
    def lesson1_1B(self):
        self.lessonInfoSubContainer.setCurrentIndex(2)
    def lesson1_1C(self):
        self.lessonInfoSubContainer.setCurrentIndex(3)
    def lesson1_1D(self):
        self.lessonInfoSubContainer.setCurrentIndex(4)
    def lesson1_1Test(self):
        self.lessonInfoSubContainer.setCurrentIndex(5)

    def lesson2_1A(self):   
        self.lessonInfo2SubContainer.setCurrentIndex(1)
    def lesson2_1B(self):   
        self.lessonInfo2SubContainer.setCurrentIndex(2)
    def lesson2_1C(self):   
        self.lessonInfo2SubContainer.setCurrentIndex(3)
    def lesson2_1Test(self):   
        self.lessonInfo2SubContainer.setCurrentIndex(4)

    # MATH EQUATION BUTTON FUNCTIONS
    def powerOf(self):
        word = "^2"
        self.chatSends_TextEdit.insertPlainText(word)
    def powerOfN(self):
        word = "^{n}"
        self.chatSends_TextEdit.insertPlainText(word)
    def sqrtOfN(self):
        word = "\sqrt[x]{y}"
        self.chatSends_TextEdit.insertPlainText(word)
    def degOfN(self):
        word = "x^{\circ }"
        self.chatSends_TextEdit.insertPlainText(word)
    def primeOfN(self):
        word = "\left(x\\right)^'"
        self.chatSends_TextEdit.insertPlainText(word)
    def fracN(self):
        word = "\\frac{x}{y}"
        self.chatSends_TextEdit.insertPlainText(word)
    def leftParenthesis(self):
        word = "("
        self.chatSends_TextEdit.insertPlainText(word)
    def rightParenthesis(self):
        word = ")"
        self.chatSends_TextEdit.insertPlainText(word)
    def piMath(self):
        word = "\pi"
        self.chatSends_TextEdit.insertPlainText(word)
    def summation(self):
        word = "\sum_{n=0}^{\infty}"
        self.chatSends_TextEdit.insertPlainText(word)
    def infinity(self):
        word = "\infty"
        self.chatSends_TextEdit.insertPlainText(word)
    def theta(self):
        word = "\\theta"
        self.chatSends_TextEdit.insertPlainText(word)
    def sinMath(self):
        word = "\sin ^x"
        self.chatSends_TextEdit.insertPlainText(word)
    def cosMath(self):
        word = "\cos ^x"
        self.chatSends_TextEdit.insertPlainText(word)
    def tanMath(self):
        word = "\\tan ^x"
        self.chatSends_TextEdit.insertPlainText(word)
    def cotMath(self):
        word = "\cot ^x"
        self.chatSends_TextEdit.insertPlainText(word)
    def cscMath(self):
        word = "\csc ^x"
        self.chatSends_TextEdit.insertPlainText(word)
    def secMath(self):
        word = "\sec ^x"
        self.chatSends_TextEdit.insertPlainText(word)
    def addMath(self):
        word = "+"
        self.chatSends_TextEdit.insertPlainText(word)
    def subtractMath(self):
        word = "-"
        self.chatSends_TextEdit.insertPlainText(word)
    def multiplyMath(self):
        word = "*"
        self.chatSends_TextEdit.insertPlainText(word)
    def divideMath(self):
        word = "/"
        self.chatSends_TextEdit.insertPlainText(word)
    def decimalMath(self):
        word = "."
        self.chatSends_TextEdit.insertPlainText(word)
    def inverseMath(self):
        word = "inverse"
        self.chatSends_TextEdit.insertPlainText(word)

    def checkEquat(self):
        def tex2svg(formula, fontsize=40, dpi=300):
        # """Render TeX formula to SVG.
        # Args:
        #     formula (str): TeX formula.
        #     fontsize (int, optional): Font size.
        #     dpi (int, optional): DPI.
        # Returns:
        #     str: SVG render.
        # """
            fig = plt.figure(figsize=(0.01, 0.01))
            fig.text(50, 0, (r"$%s$" %formula), fontsize=fontsize)

            output = BytesIO()
            fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                        bbox_inches="tight", pad_inches=0.0, facecolor='auto'
                        , edgecolor = "auto", backend=None)
            plt.close(fig)

            output.seek(0)
            return output.read()
        
        def errorFunc(formula, fontsize=20, dpi=300):
        # """Render TeX formula to SVG.
        # Args:
        #     formula (str): TeX formula.
        #     fontsize (int, optional): Font size.
        #     dpi (int, optional): DPI.
        # Returns:
        #     str: SVG render.
        # """
            fig = plt.figure(figsize=(0.01, 0.01))
            fig.text(50, 0, "There is an error\nin your input.\nEither a\n-Double backslash \neg.(\\\\right),\n-Incomplete figures in parameters \neg.(\left( , {\circ  )\n-Blank Input\neg.( )", fontsize=fontsize)

            output = BytesIO()
            fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                        bbox_inches="tight", pad_inches=0.0, facecolor='auto'
                        , edgecolor = "auto", backend=None)
            plt.close(fig)

            output.seek(0)
            return output.read()
        
        # matplotlib: force computer modern font set
        
        plt.rc("'mathtext', fontset='cm'")
        word = self.chatSends_TextEdit.toPlainText()
        # print(word)
        FORMULA = (word)
        self.svg = QSvgWidget()

        try:
            self.svg.load(tex2svg(FORMULA))
            self.svg.show()
        except:
            self.svg.load(errorFunc(FORMULA))
            self.svg.show()


    def sendMessage(self):

        if self.chatbot_session == 1:
            newUserWidget = "widgetUser_" + str(self.chatbot_count)
            newUserTextEdit = "textEditUser_" + str(self.chatbot_count)

            newBotWidget = "widgetBot_" + str(self.chatbot_count)
            newBotTextEdit = "textEditBot_" + str(self.chatbot_count)

            # USER CHAT CONTAINER
            self.widget_11 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
            self.widget_11.setStyleSheet("background-color: rgb(0, 52, 76);")
            self.widget_11.setObjectName(newUserWidget)
            self.verticalLayout_84 = QtWidgets.QVBoxLayout(self.widget_11)
            self.verticalLayout_84.setObjectName("verticalLayout_84")
            self.textEdit = QtWidgets.QTextEdit(self.widget_11)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
            self.textEdit.setSizePolicy(sizePolicy)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.textEdit.setFont(font)
            self.textEdit.setStyleSheet("")
            self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.textEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
            self.textEdit.setReadOnly(True)
            self.textEdit.setPlaceholderText("")
            self.textEdit.setObjectName(newUserTextEdit)
            self.verticalLayout_84.addWidget(self.textEdit)
            self.verticalLayout_83.addWidget(self.widget_11)

            user_message = self.chatSends_TextEdit.toPlainText()
            self.chatSends_TextEdit.clear()
            self.textEdit.insertPlainText(user_message)

            # BOT CHAT CONTAINER
            self.widget_12 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
            self.widget_12.setStyleSheet("background-color: rgb(122, 186, 200);")
            self.widget_12.setObjectName(newBotWidget)
            self.verticalLayout_85 = QtWidgets.QVBoxLayout(self.widget_12)
            self.verticalLayout_85.setObjectName("verticalLayout_85")
            self.textEdit_2 = QtWidgets.QTextEdit(self.widget_12)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
            self.textEdit_2.setSizePolicy(sizePolicy)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.textEdit_2.setFont(font)
            self.textEdit_2.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.textEdit_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.textEdit_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.textEdit_2.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
            self.textEdit_2.setReadOnly(True)
            self.textEdit_2.setPlaceholderText("")
            self.textEdit_2.setObjectName(newBotTextEdit)
            self.verticalLayout_85.addWidget(self.textEdit_2)
            self.verticalLayout_83.addWidget(self.widget_12)

            with open("data/precalc_keywords.txt", "r", encoding='utf-8') as f:
                precalc_keywords = [line.strip() for line in f]

            if any(keyword in user_message.lower() for keyword in precalc_keywords):

                completions = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_message,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7
                )
                chatbot_response = completions.choices[0].text
                print(chatbot_response)
                self.textEdit_2.insertPlainText(chatbot_response)
            else:
                chatbot_denied="Sorry, I can only help with precalculus-related questions."
                self.textEdit_2.insertPlainText(chatbot_denied)

            self.chatbot_count = self.chatbot_count + 1

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
            self.animaRightContainer2.setEndValue(250)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 

            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(250)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start()
            
            self.rightMenuNum == 1
        self.chatbot_session = 1
        self.rightMenuPages.setCurrentIndex(2)

    def showProfile(self):
        if self.rightMenuNum == 0:
            self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
            self.animaRightContainer2.setDuration(500)
            self.animaRightContainer2.setStartValue(0)
            self.animaRightContainer2.setEndValue(250)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 

            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(250)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start()
            
            self.rightMenuNum = 1
        self.rightMenuPages.setCurrentIndex(0)

    def showModule1(self):
        self.moduleMenuPages.setCurrentIndex(0)
        self.lesson1_1Container.setVisible(True)
        self.lessonsContainer.setVisible(True)
        self.lessonInfo1Container.setVisible(True)
        self.lessonInfoSubContainer.setCurrentIndex(0)

    def showModule2(self):
        self.moduleMenuPages.setCurrentIndex(1)
        self.lesson2_1Container.setVisible(True)
        self.lessonsContainer.setVisible(True)
        self.lessonInfo2Container.setVisible(True)
        self.lessonInfo2SubContainer.setCurrentIndex(0)

    def showModule3(self):
        self.moduleMenuPages.setCurrentIndex(2)
        self.lessonsContainer.setVisible(True)

    def showHome(self):
        self.menuPages.setCurrentIndex(0)
        self.lessonsContainer.setVisible(False)
    def showModules(self):
        self.menuPages.setCurrentIndex(1)
    def showProgress(self):
        self.menuPages.setCurrentIndex(2)
        self.lessonsContainer.setVisible(False)
    
    def showInformation(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(200)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(200)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start()
            
            self.centerMenuNum = 1
        self.centerMenuPages.setCurrentIndex(2)
        
    def showHelp(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(200)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(200)
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

        self.chatbot_session == 0

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

class toStudLogout(QDialog):
    def __init__(self, parent):
        super(toStudLogout, self).__init__(parent)
        self.ui = Ui_logoutDialog()
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.setWindowModality(Qt.ApplicationModal)

        self.yes_pushButton.clicked.connect(self.yesFunction)
        self.no_pushButton.clicked.connect(self.noFunction)

    def yesFunction(self):
        print("YES PRESSED")
        self.hide()
        self.parent().hide()
        self.toGoBack = toStudTeach()
        self.toGoBack.show()
    
    def noFunction(self):
        self.hide()
        print("NO PRESSED")
        
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

class splashScreen(QMainWindow):
    def __init__(self):
        super(splashScreen, self).__init__()
        loadUi("data/loadingScreen1.ui", self)

        self.setWindowIcon(QIcon(resource_path("assets/images/logo.png")))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.setWindowFlag(Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        pass

    def progress(self):
        for i in range(100):
            self.progressBar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.1)
        self.close()
        self.next = toDashboard()
        self.next.show()

class topicLesson1(QMainWindow):
    def __init__(self):
        super(topicLesson1, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(0)

        self.parabolaEx1PlotButton.clicked.connect(self.parabolaGraph1)
        self.parabolaEx2PlotButton.clicked.connect(self.parabolaGraph2)
        self.ellipseEx1PlotButton.clicked.connect(self.ellipseGraph1)
        self.ellipseEx2PlotButton.clicked.connect(self.ellipseGraph2)
        self.hyperbolaEx1aPlotButton.clicked.connect(self.hyperbolaGraph1)
        self.hyperbolaEx1bPlotButton.clicked.connect(self.hyperbolaGraph2)
        
        self.nextPage1Button.clicked.connect(self.nextPage0)
        self.nextPage2Button.clicked.connect(self.nextPage1)
        self.nextPage3Button.clicked.connect(self.nextPage2)
        self.nextPage4Button.clicked.connect(self.nextPage3)

        self.prevPage2Button.clicked.connect(self.prevPage0)
        self.prevPage3Button.clicked.connect(self.prevPage1)
        self.prevPage4Button.clicked.connect(self.prevPage2)
        self.prevPage5Button.clicked.connect(self.prevPage3)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0
    
    def parabolaGraph1(self):
        self.parab = parabolaGraph1Window()
        self.parab.show()
    def parabolaGraph2(self):
        self.parab = parabolaGraph2Window()
        self.parab.show()
    def ellipseGraph1(self):
        self.ellipse = ellipseGraph1Window()
        self.ellipse.show()
    def ellipseGraph2(self):
        self.ellipse = ellipseGraph2Window()
        self.ellipse.show()
    def hyperbolaGraph1(self):
        self.hyper = hyperbolaGraph1Window()
        self.hyper.show()
    def hyperbolaGraph2(self):
        self.hyper = hyperbolaGraph2Window()
        self.hyper.show()
    def nextPage0(self):
        self.topicPages.setCurrentIndex(1)
    def nextPage1(self):
        self.topicPages.setCurrentIndex(2)
    def nextPage2(self):
        self.topicPages.setCurrentIndex(3)
    def nextPage3(self):
        self.topicPages.setCurrentIndex(4)

    def prevPage0(self):
        self.topicPages.setCurrentIndex(0)
    def prevPage1(self):
        self.topicPages.setCurrentIndex(1)
    def prevPage2(self):
        self.topicPages.setCurrentIndex(2)
    def prevPage3(self):
        self.topicPages.setCurrentIndex(3)

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class topicLesson2(QMainWindow):
    def __init__(self):
        super(topicLesson2, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(2)

        self.parabolaEx1PlotButton.clicked.connect(self.parabolaGraph1)
        self.parabolaEx2PlotButton.clicked.connect(self.parabolaGraph2)
        self.ellipseEx1PlotButton.clicked.connect(self.ellipseGraph1)
        self.ellipseEx2PlotButton.clicked.connect(self.ellipseGraph2)
        self.hyperbolaEx1aPlotButton.clicked.connect(self.hyperbolaGraph1)
        self.hyperbolaEx1bPlotButton.clicked.connect(self.hyperbolaGraph2)

        self.nextPage1Button.clicked.connect(self.nextPage0)
        self.nextPage2Button.clicked.connect(self.nextPage1)
        self.nextPage3Button.clicked.connect(self.nextPage2)
        self.nextPage4Button.clicked.connect(self.nextPage3)

        self.prevPage2Button.clicked.connect(self.prevPage0)
        self.prevPage3Button.clicked.connect(self.prevPage1)
        self.prevPage4Button.clicked.connect(self.prevPage2)
        self.prevPage5Button.clicked.connect(self.prevPage3)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def parabolaGraph1(self):
        self.parab = parabolaGraph1Window()
        self.parab.show()
    def parabolaGraph2(self):
        self.parab = parabolaGraph2Window()
        self.parab.show()
    def ellipseGraph1(self):
        self.ellipse = ellipseGraph1Window()
        self.ellipse.show()
    def ellipseGraph2(self):
        self.ellipse = ellipseGraph2Window()
        self.ellipse.show()
    def hyperbolaGraph1(self):
        self.hyper = hyperbolaGraph1Window()
        self.hyper.show()
    def hyperbolaGraph2(self):
        self.hyper = hyperbolaGraph2Window()
        self.hyper.show()

    def nextPage0(self):
        self.topicPages.setCurrentIndex(1)
    def nextPage1(self):
        self.topicPages.setCurrentIndex(2)
    def nextPage2(self):
        self.topicPages.setCurrentIndex(3)
    def nextPage3(self):
        self.topicPages.setCurrentIndex(4)

    def prevPage0(self):
        self.topicPages.setCurrentIndex(0)
    def prevPage1(self):
        self.topicPages.setCurrentIndex(1)
    def prevPage2(self):
        self.topicPages.setCurrentIndex(2)
    def prevPage3(self):
        self.topicPages.setCurrentIndex(3)

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class topicLesson3(QMainWindow):
    def __init__(self):
        super(topicLesson3, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(3)

        self.parabolaEx1PlotButton.clicked.connect(self.parabolaGraph1)
        self.parabolaEx2PlotButton.clicked.connect(self.parabolaGraph2)
        self.ellipseEx1PlotButton.clicked.connect(self.ellipseGraph1)
        self.ellipseEx2PlotButton.clicked.connect(self.ellipseGraph2)
        self.hyperbolaEx1aPlotButton.clicked.connect(self.hyperbolaGraph1)
        self.hyperbolaEx1bPlotButton.clicked.connect(self.hyperbolaGraph2)

        self.nextPage1Button.clicked.connect(self.nextPage0)
        self.nextPage2Button.clicked.connect(self.nextPage1)
        self.nextPage3Button.clicked.connect(self.nextPage2)
        self.nextPage4Button.clicked.connect(self.nextPage3)

        self.prevPage2Button.clicked.connect(self.prevPage0)
        self.prevPage3Button.clicked.connect(self.prevPage1)
        self.prevPage4Button.clicked.connect(self.prevPage2)
        self.prevPage5Button.clicked.connect(self.prevPage3)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False
    
    def parabolaGraph1(self):
        self.parab = parabolaGraph1Window()
        self.parab.show()
    def parabolaGraph2(self):
        self.parab = parabolaGraph2Window()
        self.parab.show()
    def ellipseGraph1(self):
        self.ellipse = ellipseGraph1Window()
        self.ellipse.show()
    def ellipseGraph2(self):
        self.ellipse = ellipseGraph2Window()
        self.ellipse.show()
    def hyperbolaGraph1(self):
        self.hyper = hyperbolaGraph1Window()
        self.hyper.show()
    def hyperbolaGraph2(self):
        self.hyper = hyperbolaGraph2Window()
        self.hyper.show()

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def nextPage0(self):
        self.topicPages.setCurrentIndex(1)
    def nextPage1(self):
        self.topicPages.setCurrentIndex(2)
    def nextPage2(self):
        self.topicPages.setCurrentIndex(3)
    def nextPage3(self):
        self.topicPages.setCurrentIndex(4)

    def prevPage0(self):
        self.topicPages.setCurrentIndex(0)
    def prevPage1(self):
        self.topicPages.setCurrentIndex(1)
    def prevPage2(self):
        self.topicPages.setCurrentIndex(2)
    def prevPage3(self):
        self.topicPages.setCurrentIndex(3)

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class topicLesson4(QMainWindow):
    def __init__(self):
        super(topicLesson4, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(4)

        self.parabolaEx1PlotButton.clicked.connect(self.parabolaGraph1)
        self.parabolaEx2PlotButton.clicked.connect(self.parabolaGraph2)
        self.ellipseEx1PlotButton.clicked.connect(self.ellipseGraph1)
        self.ellipseEx2PlotButton.clicked.connect(self.ellipseGraph2)
        self.hyperbolaEx1aPlotButton.clicked.connect(self.hyperbolaGraph1)
        self.hyperbolaEx1bPlotButton.clicked.connect(self.hyperbolaGraph2)

        self.nextPage1Button.clicked.connect(self.nextPage0)
        self.nextPage2Button.clicked.connect(self.nextPage1)
        self.nextPage3Button.clicked.connect(self.nextPage2)
        self.nextPage4Button.clicked.connect(self.nextPage3)

        self.prevPage2Button.clicked.connect(self.prevPage0)
        self.prevPage3Button.clicked.connect(self.prevPage1)
        self.prevPage4Button.clicked.connect(self.prevPage2)
        self.prevPage5Button.clicked.connect(self.prevPage3)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def parabolaGraph1(self):
        self.parab = parabolaGraph1Window()
        self.parab.show()
    def parabolaGraph2(self):
        self.parab = parabolaGraph2Window()
        self.parab.show()
    def ellipseGraph1(self):
        self.ellipse = ellipseGraph1Window()
        self.ellipse.show()
    def ellipseGraph2(self):
        self.ellipse = ellipseGraph2Window()
        self.ellipse.show()
    def hyperbolaGraph1(self):
        self.hyper = hyperbolaGraph1Window()
        self.hyper.show()
    def hyperbolaGraph2(self):
        self.hyper = hyperbolaGraph2Window()
        self.hyper.show()

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def nextPage0(self):
        self.topicPages.setCurrentIndex(1)
    def nextPage1(self):
        self.topicPages.setCurrentIndex(2)
    def nextPage2(self):
        self.topicPages.setCurrentIndex(3)
    def nextPage3(self):
        self.topicPages.setCurrentIndex(4)

    def prevPage0(self):
        self.topicPages.setCurrentIndex(0)
    def prevPage1(self):
        self.topicPages.setCurrentIndex(1)
    def prevPage2(self):
        self.topicPages.setCurrentIndex(2)
    def prevPage3(self):
        self.topicPages.setCurrentIndex(3)

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class topicLesson5(QMainWindow):
    def __init__(self):
        super(topicLesson5, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(6)

        self.nextPage6Button.clicked.connect(self.nextPage6)
        self.nextPage7Button.clicked.connect(self.nextPage7)
        self.nextPage8Button.clicked.connect(self.nextPage8)

        self.prevPage7Button.clicked.connect(self.prevPage7)
        self.prevPage8Button.clicked.connect(self.prevPage8)
        self.prevPage9Button.clicked.connect(self.prevPage9)
        
        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def nextPage6(self):
        self.topicPages.setCurrentIndex(7)
    def nextPage7(self):
        self.topicPages.setCurrentIndex(8)
    def nextPage8(self):
        self.topicPages.setCurrentIndex(9)
    def prevPage7(self):
        self.topicPages.setCurrentIndex(6)
    def prevPage8(self):
        self.topicPages.setCurrentIndex(7)
    def prevPage9(self):
        self.topicPages.setCurrentIndex(8)
    
    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class topicLesson6(QMainWindow):
    def __init__(self):
        super(topicLesson6, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(8)

        self.nextPage6Button.clicked.connect(self.nextPage6)
        self.nextPage7Button.clicked.connect(self.nextPage7)
        self.nextPage8Button.clicked.connect(self.nextPage8)

        self.prevPage7Button.clicked.connect(self.prevPage7)
        self.prevPage8Button.clicked.connect(self.prevPage8)
        self.prevPage9Button.clicked.connect(self.prevPage9)
        
        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def nextPage6(self):
        self.topicPages.setCurrentIndex(7)
    def nextPage7(self):
        self.topicPages.setCurrentIndex(8)
    def nextPage8(self):
        self.topicPages.setCurrentIndex(9)
    def prevPage7(self):
        self.topicPages.setCurrentIndex(6)
    def prevPage8(self):
        self.topicPages.setCurrentIndex(7)
    def prevPage9(self):
        self.topicPages.setCurrentIndex(8)

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class topicLesson7(QMainWindow):
    def __init__(self):
        super(topicLesson7, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(9)

        self.nextPage6Button.clicked.connect(self.nextPage6)
        self.nextPage7Button.clicked.connect(self.nextPage7)
        self.nextPage8Button.clicked.connect(self.nextPage8)

        self.prevPage7Button.clicked.connect(self.prevPage7)
        self.prevPage8Button.clicked.connect(self.prevPage8)
        self.prevPage9Button.clicked.connect(self.prevPage9)
        
        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def nextPage6(self):
        self.topicPages.setCurrentIndex(7)
    def nextPage7(self):
        self.topicPages.setCurrentIndex(8)
    def nextPage8(self):
        self.topicPages.setCurrentIndex(9)
    def prevPage7(self):
        self.topicPages.setCurrentIndex(6)
    def prevPage8(self):
        self.topicPages.setCurrentIndex(7)
    def prevPage9(self):
        self.topicPages.setCurrentIndex(8)

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
    
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

class assessmentWindow(QMainWindow):
    def __init__(self):
        super(assessmentWindow, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(11)

        self.assessTest_Button.clicked.connect(self.submitAssessment)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
        
    def submitAssessment(self):
        # Question 1 , answer and solution
        assess_sol_Q1 = self.assessQ1Sol_textEdit.toPlainText()
        assess_ans_Q1 = self.assessQ1_textEdit.text()
        # Question 2 , answer and solution
        assess_sol_Q2 = self.assessQ2Sol_textEdit.toPlainText()
        assess_ans_Q2 = self.assessQ2_textEdit.text()
        # Question 3 , answer and solution
        assess_sol_Q3 = self.assessQ3Sol_textEdit.toPlainText()
        assess_ans_Q3 = self.assessQ3_textEdit.text()
        # Question 4 , answer and solution
        assess_sol_Q4 = self.assessQ4Sol_textEdit.toPlainText()
        assess_ans_Q4 = self.assessQ4_textEdit.text()
        # Question 5 , answer and solution
        assess_sol_Q5 = self.assessQ5Sol_textEdit.toPlainText()
        assess_ans_Q5 = self.assessQ5_textEdit.text()
        
        # Checking of answer and calculating of score
        data.scores.assess_score = 0
        # Question 1, solution and answer
        question = "question_21_Solution"
        check_assess_q1_sol = chat(question, assess_sol_Q1)
        question = "question_21_Answer"
        check_assess_q1_ans = chat(question, assess_ans_Q1)
                
        if check_assess_q1_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q1_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 2, solution and answer
        question = "question_22_Solution"
        check_assess_q2_sol = chat(question, assess_sol_Q2)
        question = "question_22_Answer"
        check_assess_q2_ans = chat(question, assess_ans_Q2)

        if check_assess_q2_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q2_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 3, solution and answer
        question = "question_23_Solution"
        check_assess_q3_sol = chat(question, assess_sol_Q3)
        question = "question_23_Answer"
        check_assess_q3_ans = chat(question, assess_ans_Q3)

        if check_assess_q3_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q3_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 4, solution and answer
        question = "question_24_Solution"
        check_assess_q4_sol = chat(question, assess_sol_Q4)
        question = "question_24_Answer"
        check_assess_q4_ans = chat(question, assess_ans_Q4)

        if check_assess_q4_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q4_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 5, solution and answer
        question = "question_25_Solution"
        check_assess_q5_sol = chat(question, assess_sol_Q5)
        question = "question_25_Answer"
        check_assess_q5_ans = chat(question, assess_ans_Q5)

        if check_assess_q5_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q5_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1
        
        print(data.scores.assess_score)
        studKey = db.child("student").get()
        for keyAccess in studKey.each():
            if keyAccess.val()["studentSchoolID"] == idKey:
                keyID = keyAccess.key()
        db.child("student").child(keyID).update({"assessment_score":str(data.scores.assess_score)})
        
        self.hide()
        self.back = toDashboard()
        self.back.show()

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

class unitTest_1(QMainWindow):
    def __init__(self):
        super(unitTest_1, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)
        
        self.topicPages.setCurrentIndex(5)

        self.submitTest_Button.clicked.connect(self.submitTest)
        self.back_Button.clicked.connect(self.toDashboardPage)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)
        
        self.showScore_widget.setVisible(False)
        self.showlessonScore_widget.setVisible(False)
        self.unitTest1Submit_container.setCurrentIndex(0)

        self.restoreWindow = 0
        self.maxWindow = False
        
        if submit_unit1 == True:
            self.showScore_widget.setVisible(True)
            # self.showlessonScore_widget.setVisible(True)
            self.unitTest1Submit_container.setCurrentIndex(1)
            self.show_scoreUnit1_label.setText(str(data.scores.unit1_score))
            self.show_score1_label.setText(str(data.scores.circ_score))
            self.show_score2_label.setText(str(data.scores.parab_score))
            self.show_score3_label.setText(str(data.scores.ellip_score))
            self.show_score4_label.setText(str(data.scores.hyperb_score))
# # question 1
            self.unitTestQ1Sol_textEdit.setReadOnly(True) 
            if data.scores.check_unit1_q1_sol == "incorrect":
                self.sol1_label.setStyleSheet("background-color: red")
            else:
                self.sol1_label.setStyleSheet("background-color: green")
            self.unitTestQ1Center_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q1_ans == "incorrect":
                self.ans1_label.setStyleSheet("background-color: red")
            else:
                self.ans1_label.setStyleSheet("background-color: green")
# question 2
            self.unitTestQ2Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q2_sol == "incorrect":
                self.sol2_label.setStyleSheet("background-color: red")
            else:
                self.sol2_label.setStyleSheet("background-color: green")
            self.unitTestQ2Center_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q2_center_ans == "incorrect":
                self.ans2Center_label.setStyleSheet("background-color: red")
            else:
                self.ans2Center_label.setStyleSheet("background-color: green")
            # self.unitTestQ2Radius_textEdit.setReadOnly(True)
            # if data.scores.check_unit1_q2_radius_ans == "incorrect":
            #     self.ans2Radius_label.setStyleSheet("background-color: red")
            # else:
            #     self.ans2Radius_label.setStyleSheet("background-color: green")
# question 3
            self.unitTestQ3Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q3_sol == "incorrect":
                self.sol3_label.setStyleSheet("background-color: red")
            else:
                self.sol3_label.setStyleSheet("background-color: green")
            self.unitTestQ3Vertex_textEdit.setReadOnly(True) 
            if data.scores.check_unit1_q3_vertex_ans == "incorrect":
                self.ans3Vertex_label.setStyleSheet("background-color: red")
            else:
                self.ans3Vertex_label.setStyleSheet("background-color: green")
            # self.unitTestQ3Focus_textEdit.setReadOnly(True)
            # if data.scores.check_unit1_q3_focus_ans == "incorrect":
            #     self.ans3Focus_label.setStyleSheet("background-color: red")
            # else:
            #     self.ans3Focus_label.setStyleSheet("background-color: green")
# question 4            
            self.unitTestQ4Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q4_sol == "incorrect":
                self.sol4_label.setStyleSheet("background-color: red")
            else:
                self.sol4_label.setStyleSheet("background-color: green")
            self.unitTestQ4Vertex_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q4_vertex_ans == "incorrect":
                self.ans4Vertex_label.setStyleSheet("background-color: red")
            else:
                self.ans4Vertex_label.setStyleSheet("background-color: green")
            # self.unitTestQ4Focus_textEdit.setReadOnly(True)
            # if data.scores.check_unit1_q4_focus_ans == "incorrect":
            #     self.ans4Focus_label.setStyleSheet("background-color: red")
            # else:
            #     self.ans4Focus_label.setStyleSheet("background-color: green")
# question 5
            self.unitTestQ5Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q5_sol == "incorrect":
                self.sol5_label.setStyleSheet("background-color: red")
            else:
                self.sol5_label.setStyleSheet("background-color: green")
            self.unitTestQ5Center_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q5_center_ans == "incorrect":
                self.ans5_label.setStyleSheet("background-color: red")
            else:
                self.ans5_label.setStyleSheet("background-color: green")
# question 6
            self.unitTestQ6Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q6_sol == "incorrect":
                self.sol6_label.setStyleSheet("background-color: red")
            else:
                self.sol6_label.setStyleSheet("background-color: green")
            self.unitTestQ6Foci1_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q6_foci1_ans == "incorrect":
                self.ans6Foci1_label.setStyleSheet("background-color: red")
            else:
                self.ans6Foci1_label.setStyleSheet("background-color: green")
            # self.unitTestQ6Foci2_textEdit.setReadOnly(True)
            # if data.scores.check_unit1_q6_foci2_ans == "incorrect":
            #     self.ans6Foci2_label.setStyleSheet("background-color: red")
            # else:
            #     self.ans6Foci2_label.setStyleSheet("background-color: green")
# question 7
            self.unitTestQ7Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q7_sol == "incorrect":
                self.sol7_label.setStyleSheet("background-color: red")
            else:
                self.sol7_label.setStyleSheet("background-color: green")
            self.unitTestQ7Vertex1_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q7_vertex1_ans== "incorrect":
                self.ans7Vertex1_label.setStyleSheet("background-color: red")
            else:
                self.ans7Vertex1_label.setStyleSheet("background-color: green")
            # self.unitTestQ7Vertex2_textEdit.setReadOnly(True)
            # if data.scores.check_unit1_q7_vertex2_ans== "incorrect":
            #     self.ans7Vertex2_label.setStyleSheet("background-color: red")
            # else:
            #     self.ans7Vertex2_label.setStyleSheet("background-color: green")
# question 8
            self.unitTestQ8Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q8_sol == "incorrect":
                self.sol8_label.setStyleSheet("background-color: red")
            else:
                self.sol8_label.setStyleSheet("background-color: green")
            self.unitTestQ8Center_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q8_center_ans == "incorrect":
                self.ans8_label.setStyleSheet("background-color: red")
            else:
                self.ans8_label.setStyleSheet("background-color: green")
# question 9
            self.unitTestQ9Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q9_sol == "incorrect":
                self.sol9_label.setStyleSheet("background-color: red")
            else:
                self.sol9_label.setStyleSheet("background-color: green")
            self.unitTestQ9MinAxis_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q9_minorAxis_ans == "incorrect":
                self.ans9_label.setStyleSheet("background-color: red")
            else:
                self.ans9_label.setStyleSheet("background-color: green")
# question 10
            self.unitTestQ10Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q10_sol == "incorrect":
                self.sol10_label.setStyleSheet("background-color: red")
            else:
                self.sol10_label.setStyleSheet("background-color: green")
            self.unitTestQ10StandEquat_textEdit.setReadOnly(True)
            if data.scores.check_unit1_q10_standEquat_ans == "incorrect":
                self.ans10_label.setStyleSheet("background-color: red")
            else:
                self.ans10_label.setStyleSheet("background-color: green")

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()

    def submitTest(self):
        # Question 1 , answer and solution
        solution_Unit1_Q1 = self.unitTestQ1Sol_textEdit.toPlainText()
        answer1_Unit1_Q1 = self.unitTestQ1Center_textEdit.text()
        # Question 2 , answer and solution
        solution_Unit1_Q2 = self.unitTestQ2Sol_textEdit.toPlainText()
        answer1_Unit1_Q2 = self.unitTestQ2Center_textEdit.text()
        # answer2_Unit1_Q2 = self.unitTestQ2Radius_textEdit.text()
        # Question 3 , answer and solution
        solution_Unit1_Q3 = self.unitTestQ3Sol_textEdit.toPlainText()
        answer1_Unit1_Q3 = self.unitTestQ3Vertex_textEdit.text()
        # answer2_Unit1_Q3 = self.unitTestQ3Focus_textEdit.text()
        # Question 4 , answer and solution
        solution_Unit1_Q4 = self.unitTestQ4Sol_textEdit.toPlainText()
        answer1_Unit1_Q4 = self.unitTestQ4Vertex_textEdit.text()
        # answer2_Unit1_Q4 = self.unitTestQ4Focus_textEdit.text()
        # Question 5 , answer and solution
        solution_Unit1_Q5 = self.unitTestQ5Sol_textEdit.toPlainText()
        answer1_Unit1_Q5 = self.unitTestQ5Center_textEdit.text()
        # Question 6 , answer and solution
        solution_Unit1_Q6 = self.unitTestQ6Sol_textEdit.toPlainText()
        answer1_Unit1_Q6 = self.unitTestQ6Foci1_textEdit.text()
        # answer2_Unit1_Q6 = self.unitTestQ6Foci2_textEdit.text()
        # Question 7 , answer and solution
        solution_Unit1_Q7 = self.unitTestQ7Sol_textEdit.toPlainText()
        answer1_Unit1_Q7 = self.unitTestQ7Vertex1_textEdit.text()
        # answer2_Unit1_Q7 = self.unitTestQ7Vertex2_textEdit.text()
        # Question 8 , answer and solution
        solution_Unit1_Q8 = self.unitTestQ8Sol_textEdit.toPlainText()
        answer1_Unit1_Q8 = self.unitTestQ8Center_textEdit.text()
        # Question 9 , answer and solution
        solution_Unit1_Q9 = self.unitTestQ9Sol_textEdit.toPlainText()
        answer1_Unit1_Q9 = self.unitTestQ9MinAxis_textEdit.text()
        # Question 10 , answer and solution
        solution_Unit1_Q10 = self.unitTestQ10Sol_textEdit.toPlainText()
        answer1_Unit1_Q10 = self.unitTestQ10StandEquat_textEdit.text()        

        # Checking of answer and calculating of score
        data.scores.unit1_score = 0
        data.scores.circ_score = 0
        data.scores.parab_score = 0
        data.scores.ellip_score = 0
        data.scores.hyperb_score = 0

        # Question 1, solution and answer
        question = "question_1_Solution"
        check_unit1_q1_sol = chat(question, solution_Unit1_Q1)
        data.scores.check_unit1_q1_sol= check_unit1_q1_sol
         
        question = "question_1_Answer"
        check_unit1_q1_ans = chat(question, answer1_Unit1_Q1)
        data.scores.check_unit1_q1_ans = check_unit1_q1_ans

        if check_unit1_q1_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.circ_score = data.scores.circ_score + 4
        if check_unit1_q1_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1  
            data.scores.circ_score = data.scores.circ_score + 1

        # Question 2, solution and answer
        question = "question_2_Solution"
        check_unit1_q2_sol = chat(question, solution_Unit1_Q2)
        data.scores.check_unit1_q2_sol = check_unit1_q2_sol
        question = "question_2_Center_Answer"
        check_unit1_q2_center_ans = chat(question, answer1_Unit1_Q2)
        data.scores.check_unit1_q2_center_ans = check_unit1_q2_center_ans
        # question = "question_2_Radius_Answer"
        # check_unit1_q2_radius_ans = chat(question, answer2_Unit1_Q2)
        # data.scores.check_unit1_q2_radius_ans = check_unit1_q2_radius_ans

        if check_unit1_q2_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.circ_score = data.scores.circ_score + 4
        if check_unit1_q2_center_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.circ_score = data.scores.circ_score + 1
        # if check_unit1_q2_radius_ans == "correct":
        #     data.scores.unit1_score = data.scores.unit1_score + 1  
        #     data.scores.circ_score = data.scores.circ_score + 1

        # Question 3, solution and answer
        question = "question_3_Solution"
        check_unit1_q3_sol = chat(question, solution_Unit1_Q3)
        data.scores.check_unit1_q3_sol = check_unit1_q3_sol
        question = "question_3_Vertex"
        check_unit1_q3_vertex_ans = chat(question, answer1_Unit1_Q3)
        data.scores.check_unit1_q3_vertex_ans = check_unit1_q3_vertex_ans
        # question = "question_3_Focus"
        # check_unit1_q3_focus_ans = chat(question, answer2_Unit1_Q3)
        # data.scores.check_unit1_q3_focus_ans = check_unit1_q3_focus_ans

        if check_unit1_q3_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.parab_score = data.scores.parab_score + 4
        if check_unit1_q3_vertex_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.parab_score = data.scores.parab_score + 1
        # if check_unit1_q3_focus_ans == "correct":
        #     data.scores.unit1_score = data.scores.unit1_score + 1
        #     data.scores.parab_score = data.scores.parab_score + 1    

        # Question 4, solution and answer
        question = "question_4_Solution"
        check_unit1_q4_sol = chat(question, solution_Unit1_Q4)
        data.scores.check_unit1_q4_sol = check_unit1_q4_sol
        question = "question_4_Vertex"
        check_unit1_q4_vertex_ans = chat(question, answer1_Unit1_Q4)
        data.scores.check_unit1_q4_vertex_ans = check_unit1_q4_vertex_ans
        # question = "question_4_Focus"
        # check_unit1_q4_focus_ans = chat(question, answer2_Unit1_Q4)
        # data.scores.check_unit1_q4_focus_ans = check_unit1_q4_focus_ans

        if check_unit1_q4_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.parab_score = data.scores.parab_score + 4
        if check_unit1_q4_vertex_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.parab_score = data.scores.parab_score + 1
        # if check_unit1_q4_focus_ans == "correct":
        #     data.scores.unit1_score = data.scores.unit1_score + 1
        #     data.scores.parab_score = data.scores.parab_score + 1

        # Question 5, solution and answer
        question = "question_5_Solution"
        check_unit1_q5_sol = chat(question, solution_Unit1_Q5)
        data.scores.check_unit1_q5_sol = check_unit1_q5_sol
        question = "question_5_Center"
        check_unit1_q5_center_ans = chat(question, answer1_Unit1_Q5)
        data.scores.check_unit1_q5_center_ans = check_unit1_q5_center_ans

        if check_unit1_q5_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score+ 4
            data.scores.ellip_score = data.scores.ellip_score + 4
        if check_unit1_q5_center_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.ellip_score = data.scores.ellip_score + 1

        # Question 6, solution and answer
        question = "question_6_Solution"
        check_unit1_q6_sol = chat(question, solution_Unit1_Q6)
        data.scores.check_unit1_q6_sol = check_unit1_q6_sol
        question = "question_6_Foci1"
        check_unit1_q6_foci1_ans = chat(question, answer1_Unit1_Q6)
        data.scores.check_unit1_q6_foci1_ans = check_unit1_q6_foci1_ans
        # question = "question_6_Foci2"
        # check_unit1_q6_foci2_ans = chat(question, answer2_Unit1_Q6)
        # data.scores.check_unit1_q6_foci2_ans = check_unit1_q6_foci2_ans

        if check_unit1_q6_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.ellip_score = data.scores.ellip_score + 4
        if check_unit1_q6_foci1_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.ellip_score = data.scores.ellip_score + 1
        # if check_unit1_q6_foci2_ans == "correct":
        #     data.scores.unit1_score = data.scores.unit1_score + 1  
        #     data.scores.ellip_score = data.scores.ellip_score + 1

        # Question 7, solution and answer
        question = "question_7_Solution"
        check_unit1_q7_sol = chat(question, solution_Unit1_Q7)
        data.scores.check_unit1_q7_sol = check_unit1_q7_sol
        question = "question_7_Vertex1"
        check_unit1_q7_vertex1_ans = chat(question, answer1_Unit1_Q7)
        data.scores.check_unit1_q7_vertex1_ans = check_unit1_q7_vertex1_ans
        # question = "question_7_Vertex2"
        # check_unit1_q7_vertex2_ans = chat(question, answer2_Unit1_Q7)
        # data.scores.check_unit1_q7_vertex2_ans = check_unit1_q7_vertex2_ans

        if check_unit1_q7_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.hyperb_score = data.scores.hyperb_score + 4
        if check_unit1_q7_vertex1_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.hyperb_score = data.scores.hyperb_score + 1
        # if check_unit1_q7_vertex2_ans == "correct":
        #     data.scores.unit1_score = data.scores.unit1_score + 1    
        #     data.scores.hyperb_score = data.scores.hyperb_score + 1    

        # Question 8, solution and answer
        question = "question_8_Solution"
        check_unit1_q8_sol = chat(question, solution_Unit1_Q8)
        data.scores.check_unit1_q8_sol = check_unit1_q8_sol
        question = "question_8_Center"
        check_unit1_q8_center_ans = chat(question, answer1_Unit1_Q8)
        data.scores.check_unit1_q8_center_ans = check_unit1_q8_center_ans

        if check_unit1_q8_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.hyperb_score = data.scores.hyperb_score + 4
        if check_unit1_q8_center_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.hyperb_score = data.scores.hyperb_score + 1

        # Question 9, solution and answer
        question = "question_9_Solution"
        check_unit1_q9_sol = chat(question, solution_Unit1_Q9)
        data.scores.check_unit1_q9_sol = check_unit1_q9_sol 
        question = "question_9_MinorAxis"
        check_unit1_q9_minorAxis_ans = chat(question, answer1_Unit1_Q9)
        data.scores.check_unit1_q9_minorAxis_ans = check_unit1_q9_minorAxis_ans

        if check_unit1_q9_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.hyperb_score = data.scores.hyperb_score + 4
        if check_unit1_q9_minorAxis_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.hyperb_score = data.scores.hyperb_score + 1

        # Question 10, solution and answer
        question = "question_10_Solution"
        check_unit1_q10_sol = chat(question, solution_Unit1_Q10)
        data.scores.check_unit1_q10_sol = check_unit1_q10_sol
        question = "question_10_Foci1"
        check_unit1_q10_standEquat_ans = chat(question, answer1_Unit1_Q10)
        data.scores.check_unit1_q10_standEquat_ans = check_unit1_q10_standEquat_ans

        if check_unit1_q10_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.parab_score = data.scores.parab_score + 4
        if check_unit1_q10_standEquat_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.parab_score = data.scores.parab_score + 1
        
        print(data.scores.unit1_score)
        studKey = db.child("student").get()
        for keyAccess in studKey.each():
            if keyAccess.val()["studentSchoolID"] == idKey:
                keyID = keyAccess.key()
        db.child("student").child(keyID).update({"unitTest1_score":str(data.scores.unit1_score)})

        global submit_unit1
        submit_unit1 = True

        self.hide()
        self.reload = unitTest_1()
        self.reload.show()

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

class unitTest_2(QMainWindow):
    def __init__(self):
        super(unitTest_2, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        unit_test2_quest = []
        list_of_sol = []

        if new_unitTest2 == True:
            substitution_ans2, substitution_solu2, returned_substitution2 = display_random_question.unit_test_subs()
            elimination_ans2, elimination_solu2, returned_elimination2 = display_random_question.unit_test_elim()

            unit_test2_quest.append(returned_elimination2)
            unit_test2_quest.append(returned_substitution2)

            list_of_sol.append(substitution_ans2)
            list_of_sol.append(substitution_solu2)
            list_of_sol.append(elimination_ans2)
            list_of_sol.append(elimination_solu2)

            unit_test2_question1, unit_test2_question2, unit_test2_question3, unit_test2_question4, unit_test2_question5, unit_test2_question6, unit_test2_question7, unit_test2_question8 ,unit_test2_question9 ,unit_test2_question10= display_random_question.random_questions_2(unit_test2_quest)
            
            #the random generated question will find their corresponding answerScore, answerId, solutionScore and solutionId
            unit_test2_answerScore1, unit_test2_answerId1, unit_test2_solutionScore1, unit_test2_solutionId1 = display_random_question.get_scores_for_unit2(unit_test2_question1)
            unit_test2_answerScore2, unit_test2_answerId2, unit_test2_solutionScore2, unit_test2_solutionId2 = display_random_question.get_scores_for_unit2(unit_test2_question2)
            unit_test2_answerScore3, unit_test2_answerId3, unit_test2_solutionScore3, unit_test2_solutionId3 = display_random_question.get_scores_for_unit2(unit_test2_question3)
            unit_test2_answerScore4, unit_test2_answerId4, unit_test2_solutionScore4, unit_test2_solutionId4 = display_random_question.get_scores_for_unit2(unit_test2_question4)
            unit_test2_answerScore5, unit_test2_answerId5, unit_test2_solutionScore5, unit_test2_solutionId5 = display_random_question.get_scores_for_unit2(unit_test2_question5)
            unit_test2_answerScore6, unit_test2_answerId6, unit_test2_solutionScore6, unit_test2_solutionId6 = display_random_question.get_scores_for_unit2(unit_test2_question6)
            unit_test2_answerScore7, unit_test2_answerId7, unit_test2_solutionScore7, unit_test2_solutionId7 = display_random_question.get_scores_for_unit2(unit_test2_question7)
            unit_test2_answerScore8, unit_test2_answerId8, unit_test2_solutionScore8, unit_test2_solutionId8 = display_random_question.get_scores_for_unit2(unit_test2_question8)
            unit_test2_answerScore9, unit_test2_answerId9, unit_test2_solutionScore9, unit_test2_solutionId9 = display_random_question.get_scores_for_unit2(unit_test2_question9)
            unit_test2_answerScore10, unit_test2_answerId10, unit_test2_solutionScore10, unit_test2_solutionId10 = display_random_question.get_scores_for_unit2(unit_test2_question10)
            
            #total number of score per items will be stored here
            unit2_allItem_score = int(unit_test2_answerScore1) + int(unit_test2_answerScore2) + int(unit_test2_answerScore3) + int(unit_test2_answerScore4) + int(unit_test2_answerScore5) + int(unit_test2_answerScore6) + int(unit_test2_answerScore7) + int(unit_test2_answerScore8) + int(unit_test2_answerScore9) + int(unit_test2_answerScore10) + int(unit_test2_solutionScore1) + int(unit_test2_solutionScore2) + int(unit_test2_solutionScore3) + int(unit_test2_solutionScore4) + int(unit_test2_solutionScore5) + int(unit_test2_solutionScore6) + int(unit_test2_solutionScore7) + int(unit_test2_solutionScore8) + int(unit_test2_solutionScore9) + int(unit_test2_solutionScore10)

        self.topicPages.setCurrentIndex(10)

        self.submitTest1_Button.clicked.connect(self.submitTest2)
        self.back1_Button.clicked.connect(self.toDashboardPage)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False
        self.showScore2_widget.setVisible(False)
        self.showlessonScore2_widget.setVisible(False)

        if submit_unit2 == True:
            self.showScore2_widget.setVisible(True)
            self.showlessonScore2_widget.setVisible(True)
            self.unitTest2Submit_container.setCurrentIndex(1)
            self.show_scoreUnit2_label.setText(str(data.scores.unit2_score))
            self.show_score1_label_2.setText(str(data.scores.substi_score))
            self.show_score2_label_2.setText(str(data.scores.elimin_score))
# question 1
            self.unitTest2Q1Sol_textEdit.setReadOnly(True) 
            if data.scores.check_unit2_q1_sol == "incorrect":
                self.sol11_label.setStyleSheet("background-color: red")
            else:
                self.sol11_label.setStyleSheet("background-color: green")
            self.unitTest2Q1_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q1_ans == "incorrect":
                self.ans11_label.setStyleSheet("background-color: red")
            else:
                self.ans11_label.setStyleSheet("background-color: green")
# question 2
            self.unitTest2Q2Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q2_sol == "incorrect":
                self.sol12_label.setStyleSheet("background-color: red")
            else:
                self.sol12_label.setStyleSheet("background-color: green")
            self.unitTest2Q2_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q2_ans == "incorrect":
                self.ans12_label.setStyleSheet("background-color: red")
            else:
                self.ans12_label.setStyleSheet("background-color: green")
# question 3
            self.unitTest2Q3Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q3_sol == "incorrect":
                self.sol13_label.setStyleSheet("background-color: red")
            else:
                self.sol13_label.setStyleSheet("background-color: green")
            self.unitTest2Q3_textEdit.setReadOnly(True) 
            if data.scores.check_unit2_q3_ans == "incorrect":
                self.ans13_label.setStyleSheet("background-color: red")
            else:
                self.ans13_label.setStyleSheet("background-color: green")
# question 4            
            self.unitTest2Q4Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q4_sol == "incorrect":
                self.sol14_label.setStyleSheet("background-color: red")
            else:
                self.sol14_label.setStyleSheet("background-color: green")
            self.unitTest2Q4_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q4_ans == "incorrect":
                self.ans14_label.setStyleSheet("background-color: red")
            else:
                self.ans14_label.setStyleSheet("background-color: green")
# question 5
            self.unitTest2Q5Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q5_sol == "incorrect":
                self.sol15_label.setStyleSheet("background-color: red")
            else:
                self.sol15_label.setStyleSheet("background-color: green")
            self.unitTest2Q5_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q5_ans == "incorrect":
                self.ans15_label.setStyleSheet("background-color: red")
            else:
                self.ans15_label.setStyleSheet("background-color: green")
# question 6
            self.unitTest2Q6Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q6_sol == "incorrect":
                self.sol16_label.setStyleSheet("background-color: red")
            else:
                self.sol16_label.setStyleSheet("background-color: green")
            self.unitTest2Q6_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q6_ans == "incorrect":
                self.ans16_label.setStyleSheet("background-color: red")
            else:
                self.ans16_label.setStyleSheet("background-color: green")
# question 7
            self.unitTest2Q7Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q7_sol == "incorrect":
                self.sol17_label.setStyleSheet("background-color: red")
            else:
                self.sol17_label.setStyleSheet("background-color: green")
            self.unitTest2Q7_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q7_ans== "incorrect":
                self.ans17_label.setStyleSheet("background-color: red")
            else:
                self.ans17_label.setStyleSheet("background-color: green")
# question 8
            self.unitTest2Q8Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q8_sol == "incorrect":
                self.sol18_label.setStyleSheet("background-color: red")
            else:
                self.sol18_label.setStyleSheet("background-color: green")
            self.unitTest2Q8_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q8_ans == "incorrect":
                self.ans18_label.setStyleSheet("background-color: red")
            else:
                self.ans18_label.setStyleSheet("background-color: green")
# question 9
            self.unitTest2Q9Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q9_sol == "incorrect":
                self.sol19_label.setStyleSheet("background-color: red")
            else:
                self.sol19_label.setStyleSheet("background-color: green")
            self.unitTest2Q9_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q9_ans == "incorrect":
                self.ans19_label.setStyleSheet("background-color: red")
            else:
                self.ans19_label.setStyleSheet("background-color: green")
# question 10
            self.unitTest2Q10Sol_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q10_sol == "incorrect":
                self.sol20_label.setStyleSheet("background-color: red")
            else:
                self.sol20_label.setStyleSheet("background-color: green")
            self.unitTest2Q10_textEdit.setReadOnly(True)
            if data.scores.check_unit2_q10_ans == "incorrect":
                self.ans20_label.setStyleSheet("background-color: red")
            else:
                self.ans20_label.setStyleSheet("background-color: green")

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()

    def submitTest2(self):
        # Question 1 , answer and solution
        solution_Unit2_Q1 = self.unitTest2Q1Sol_textEdit.toPlainText()
        answer1_Unit2_Q1 = self.unitTest2Q1_textEdit.text()
        # Question 2 , answer and solution
        solution_Unit2_Q2 = self.unitTest2Q2Sol_textEdit.toPlainText()
        answer1_Unit2_Q2 = self.unitTest2Q2_textEdit.text()
        # Question 3 , answer and solution
        solution_Unit2_Q3 = self.unitTest2Q3Sol_textEdit.toPlainText()
        answer1_Unit2_Q3 = self.unitTest2Q3_textEdit.text()
        # Question 4 , answer and solution
        solution_Unit2_Q4 = self.unitTest2Q4Sol_textEdit.toPlainText()
        answer1_Unit2_Q4 = self.unitTest2Q4_textEdit.text()
        # Question 5 , answer and solution
        solution_Unit2_Q5 = self.unitTest2Q5Sol_textEdit.toPlainText()
        answer1_Unit2_Q5 = self.unitTest2Q5_textEdit.text()
        # Question 6 , answer and solution
        solution_Unit2_Q6 = self.unitTest2Q6Sol_textEdit.toPlainText()
        answer1_Unit2_Q6 = self.unitTest2Q6_textEdit.text()
        # Question 7 , answer and solution
        solution_Unit2_Q7 = self.unitTest2Q7Sol_textEdit.toPlainText()
        answer1_Unit2_Q7 = self.unitTest2Q7_textEdit.text()
        # Question 8 , answer and solution
        solution_Unit2_Q8 = self.unitTest2Q8Sol_textEdit.toPlainText()
        answer1_Unit2_Q8 = self.unitTest2Q8_textEdit.text()
        # Question 9 , answer and solution
        solution_Unit2_Q9 = self.unitTest2Q9Sol_textEdit.toPlainText()
        answer1_Unit2_Q9 = self.unitTest2Q9_textEdit.text()
        # Question 10 , answer and solution
        solution_Unit2_Q10 = self.unitTest2Q10Sol_textEdit.toPlainText()
        answer1_Unit2_Q10 = self.unitTest2Q10_textEdit.text()

        # Checking of answer and calculating of score
        data.scores.unit2_score = 0
        data.scores.substi_score = 0
        data.scores.elimin_score = 0

        # Question 1, solution and answer
        question = "question_11_Solution"
        check_unit2_q1_sol = chat(question, solution_Unit2_Q1)
        data.scores.check_unit2_q1_sol = check_unit2_q1_sol
        question = "question_11_Answer"
        check_unit2_q1_ans = chat(question, answer1_Unit2_Q1)
        data.scores.check_unit2_q1_ans = check_unit2_q1_ans

        if check_unit2_q1_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q1_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1

        # Question 2, solution and answer
        question = "question_12_Solution"
        check_unit2_q2_sol = chat(question, solution_Unit2_Q2)
        data.scores.check_unit2_q2_sol = check_unit2_q2_sol
        question = "question_12_Answer"
        check_unit2_q2_ans = chat(question, answer1_Unit2_Q2)
        data.scores.check_unit2_q2_ans = check_unit2_q2_ans

        if check_unit2_q2_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q2_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1  

        # Question 3, solution and answer
        question = "question_13_Solution"
        check_unit2_q3_sol = chat(question, solution_Unit2_Q3)
        data.scores.check_unit2_q3_sol = check_unit2_q3_sol
        question = "question_13_Answer"
        check_unit2_q3_ans = chat(question, answer1_Unit2_Q3)
        data.scores.check_unit2_q3_ans = check_unit2_q3_ans

        if check_unit2_q3_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q3_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1  

        # Question 4, solution and answer
        question = "question_14_Solution"
        check_unit2_q4_sol = chat(question, solution_Unit2_Q4)
        data.scores.check_unit2_q4_sol = check_unit2_q4_sol
        question = "question_14_Answer"
        check_unit2_q4_ans = chat(question, answer1_Unit2_Q4)
        data.scores.check_unit2_q4_ans = check_unit2_q4_ans

        if check_unit2_q4_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q4_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1  

        # Question 5, solution and answer
        question = "question_15_Solution"
        check_unit2_q5_sol = chat(question, solution_Unit2_Q5)
        data.scores.check_unit2_q5_sol = check_unit2_q5_sol
        question = "question_15_Answer"
        check_unit2_q5_ans = chat(question, answer1_Unit2_Q5)
        data.scores.check_unit2_q5_ans = check_unit2_q5_ans

        if check_unit2_q5_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q5_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1 

        # Question 6, solution and answer
        question = "question_16_Solution"
        check_unit2_q6_sol = chat(question, solution_Unit2_Q6)
        data.scores.check_unit2_q6_sol = check_unit2_q6_sol
        question = "question_16_Answer"
        check_unit2_q6_ans = chat(question, answer1_Unit2_Q6)
        data.scores.check_unit2_q6_ans = check_unit2_q6_ans

        if check_unit2_q6_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q6_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 7, solution and answer
        question = "question_17_Solution"
        check_unit2_q7_sol = chat(question, solution_Unit2_Q7)
        data.scores.check_unit2_q7_sol = check_unit2_q7_sol
        question = "question_17_Answer"
        check_unit2_q7_ans = chat(question, answer1_Unit2_Q7)
        data.scores.check_unit2_q7_ans = check_unit2_q7_ans

        if check_unit2_q7_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q7_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 8, solution and answer
        question = "question_18_Solution"
        check_unit2_q8_sol = chat(question, solution_Unit2_Q8)
        data.scores.check_unit2_q8_sol = check_unit2_q8_sol
        question = "question_18_Answer"
        check_unit2_q8_ans = chat(question, answer1_Unit2_Q8)
        data.scores.check_unit2_q8_ans = check_unit2_q8_ans

        if check_unit2_q8_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q8_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 9, solution and answer
        question = "question_19_Solution"
        check_unit2_q9_sol = chat(question, solution_Unit2_Q9)
        data.scores.check_unit2_q9_sol = check_unit2_q9_sol
        question = "question_19_Answer"
        check_unit2_q9_ans = chat(question, answer1_Unit2_Q9)
        data.scores.check_unit2_q9_ans = check_unit2_q9_ans

        if check_unit2_q9_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q9_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 10, solution and answer
        question = "question_20_Solution"
        check_unit2_q10_sol = chat(question, solution_Unit2_Q10)
        data.scores.check_unit2_q10_sol = check_unit2_q10_sol
        question = "question_20_Answer"
        check_unit2_q10_ans = chat(question, answer1_Unit2_Q10)
        data.scores.check_unit2_q10_ans = check_unit2_q10_ans

        if check_unit2_q10_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q10_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        print(data.scores.unit2_score)
        studKey = db.child("student").get()
        for keyAccess in studKey.each():
            if keyAccess.val()["studentSchoolID"] == idKey:
                keyID = keyAccess.key()
        db.child("student").child(keyID).update({"unitTest2_score":str(data.scores.unit2_score)})

        global submit_unit2, new_unitTest2
        submit_unit2 = True
        new_unitTest2 = True

        self.hide()
        self.reload = unitTest_2()
        self.reload.show()

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
    
class postAssessmentWindow_accept(QMainWindow):
    def __init__(self):
        super(postAssessmentWindow_accept, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(13)

        self.postassessTest_Button.clicked.connect(self.submitAssessment)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()
        
    def submitAssessment(self):
        # Question 1 , answer and solution
        postassess_sol_Q1 = self.postassessQ1Sol_textEdit.toPlainText()
        postassess_ans_Q1 = self.postassessQ1_textEdit.text()
        # Question 2 , answer and solution
        postassess_sol_Q2 = self.postassessQ2Sol_textEdit.toPlainText()
        postassess_ans_Q2 = self.postassessQ2_textEdit.text()
        # Question 3 , answer and solution
        postassess_sol_Q3 = self.postassessQ3Sol_textEdit.toPlainText()
        postassess_ans_Q3 = self.postassessQ3_textEdit.text()
        # Question 4 , answer and solution
        postassess_sol_Q4 = self.postassessQ4Sol_textEdit.toPlainText()
        postassess_ans_Q4 = self.postassessQ4_textEdit.text()
        # Question 5 , answer and solution
        postassess_sol_Q5 = self.postassessQ5Sol_textEdit.toPlainText()
        postassess_ans_Q5 = self.postassessQ5_textEdit.text()
        
        # Checking of answer and calculating of score
        data.scores.postassess_score = 0
        # Question 1, solution and answer
        question = "question_26_Solution"
        check_assess_q1_sol = chat(question, postassess_sol_Q1)
        question = "question_26_Answer"
        check_assess_q1_ans = chat(question, postassess_ans_Q1)
                
        if check_assess_q1_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q1_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 2, solution and answer
        question = "question_27_Solution"
        check_assess_q2_sol = chat(question, postassess_sol_Q2)
        question = "question_27_Answer"
        check_assess_q2_ans = chat(question, postassess_ans_Q2)

        if check_assess_q2_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q2_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 3, solution and answer
        question = "question_28_Solution"
        check_assess_q3_sol = chat(question, postassess_sol_Q3)
        question = "question_28_Answer"
        check_assess_q3_ans = chat(question, postassess_ans_Q3)

        if check_assess_q3_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q3_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 4, solution and answer
        question = "question_29_Solution"
        check_assess_q4_sol = chat(question, postassess_sol_Q4)
        question = "question_29_Answer"
        check_assess_q4_ans = chat(question, postassess_ans_Q4)

        if check_assess_q4_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q4_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 5, solution and answer
        question = "question_30_Solution"
        check_assess_q5_sol = chat(question, postassess_sol_Q5)
        question = "question_30_Answer"
        check_assess_q5_ans = chat(question, postassess_ans_Q5)

        if check_assess_q5_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q5_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1
        
        print(data.scores.postassess_score)
        studKey = db.child("student").get()
        for keyAccess in studKey.each():
            if keyAccess.val()["studentSchoolID"] == idKey:
                keyID = keyAccess.key()
        db.child("student").child(keyID).update({"post_assessment_score":str(data.scores.postassess_score)})
        
        self.hide()
        self.back = toDashboard()
        self.back.show()

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

class postAssessmentWindow_failed(QMainWindow):
    def __init__(self):
        super(postAssessmentWindow_failed, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(12)

        self.backButton.clicked.connect(self.toDashboardPage)
        self.closeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.bigWindow)
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.restoreWindow = 0
        self.maxWindow = False

    def bigWindow(self):
        if self.restoreWindow == 0:
            self.showMaximized()
            self.maxWindow = True
            self.restoreWindow = 1
        else:           
            self.showNormal()  
            self.maxWindow = False
            self.restoreWindow = 0

    def toDashboardPage(self):
        self.hide()
        self.back = toDashboard()
        self.back.show()

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

#################################################################################################

class toTeachUpdateProfile(QDialog):
    def __init__(self):
        super(toTeachUpdateProfile, self).__init__()
        self.ui = Ui_updateInfoDialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/updateInfo.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)

        self.updateInfoPages.setCurrentIndex(1)
        self.teachWarnFirstContainer.setVisible(False)
        self.teachWarnLastContainer.setVisible(False)
        self.teachWarnSchoolContainer.setVisible(False)
        self.teachWarnContainer.setVisible(False)
        self.updateTeachButton.clicked.connect(self.toUpdateProfile)
        self.backButton_5.clicked.connect(self.toBack)

        self.setWindowModality(Qt.ApplicationModal)

    def toUpdateProfile(self):
        self.fnameError = 0
        self.lnameError = 0
        self.schoolError = 0

        fname = self.updTeachFirst_lineEdit.text()
        mname = self.updTeachMiddle_lineEdit.text()
        lname = self.updTeachLast_lineEdit.text()
        school = self.updTeachSchool_lineEdit.text()

# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if school == "":
            self.schoolError = 1

        if self.fnameError == 1:
            self.teachWarnFirstContainer.setVisible(True)
        if self.lnameError == 1:
            self.teachWarnLastContainer.setVisible(True)
        if self.schoolError == 1:
            self.teachWarnSchoolContainer.setVisible(True)        

        if self.fnameError == 1 or self.lnameError == 1 or self.schoolError == 1:
            self.teachWarnContainer.setVisible(True)
            self.teachWarnSubContainer.setCurrentIndex(0)

            self.fnameError = 0
            self.lnameError = 0
            self.teachIDError = 0
            self.schoolError = 0
        else:
            self.teachWarnContainer.setVisible(True)
            self.teachWarnSubContainer.setCurrentIndex(1)

            self.updTeachFirst_lineEdit.clear()
            self.updTeachMiddle_lineEdit.clear()
            self.updTeachLast_lineEdit.clear()
            self.updTeachSchool_lineEdit.clear()

            print(fname)
            print(mname)
            print(lname)
            print(school)

            teachKey = db.child("teacher").get()
            for keyAccess in teachKey.each():
                if keyAccess.val()["teachSchoolID"] == idKey:
                    keyID = keyAccess.key()
            db.child("teacher").child(keyID).update({"fname":fname, "mname":mname,
                                                     "lname":lname, "school":school})
            self.hide()
            self.next = toDashboardTeach()
            self.next.show()

    def toBack(self):
        self.hide()
        self.next = toDashboardTeach()
        self.next.show()

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


########################################################################################
class toDashboardTeach(QMainWindow):
    def __init__(self):
        super(toDashboardTeach, self).__init__()
        self.ui = Ui_dashboardTeachWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.offset = None

        loadUi("data/dashboardTeach.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)

        all_teacher = db.child("teacher").get()
        for teacher in all_teacher.each():
            if teacher.val()["teachSchoolID"] == idKey:
                # print(student.key())
                # print(student.val())
                teachFname = (teacher.val()["fname"])
                teachMname = (teacher.val()["mname"])
                teachLname = (teacher.val()["lname"])
                teachCourse = (teacher.val()["course"])
                teachSchool = (teacher.val()["school"])

        # print(studID)
        self.profNameLineEdit.insertPlainText(teachLname.upper())
        self.profNameLineEdit.insertPlainText(", ")
        self.profNameLineEdit.insertPlainText(teachFname.upper())
        self.profNameLineEdit.insertPlainText(" ")
        self.profNameLineEdit.insertPlainText(teachMname.upper())
        self.profCourseLineEdit.insertPlainText(teachCourse.upper())
        self.profSchoolLineEdit.insertPlainText(teachSchool.upper())
        
        # self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Str)
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(2,200)
        self.tableWidget.setColumnWidth(3,200)
        self.tableWidget.setColumnWidth(4,200)
        self.tableWidget.setColumnWidth(5,200)
        self.tableWidget.setColumnWidth(6,500)

        self.tableWidget_2.setColumnWidth(0,200)
        self.tableWidget_2.setColumnWidth(1,200)
        self.tableWidget_2.setColumnWidth(2,200)
        self.tableWidget_2.setColumnWidth(3,200)
        self.tableWidget_2.setColumnWidth(4,200)
        self.tableWidget_2.setColumnWidth(5,200)
        self.tableWidget_2.setColumnWidth(6,200)
        self.tableWidget_2.setColumnWidth(7,200)

        self.loadData()
        self.loadGrades()

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
        # self.lessonsContainer.setVisible(False)

        self.closeBtn.clicked.connect(self.showMinimized)
        self.restoreBtn.clicked.connect(self.bigWindow)
        self.minimizeBtn.clicked.connect(self.hideWindow)
        self.closeCenterMenu_pushButton.clicked.connect(self.hideCenterMenu)

        # LEFT SIDE BUTTONS
        self.menu_pushButton.clicked.connect(self.showLeftMenu)
        self.home_pushButton.clicked.connect(self.showHome)
        self.dataAnalysis_pushButton.clicked.connect(self.showModules)
        self.reports_pushButton.clicked.connect(self.showProgress)
        self.information_pushButton.clicked.connect(self.showInformation)
        self.help_pushButton.clicked.connect(self.showHelp)

        # TOP SIDE BUTTONS
        self.profileMenu_pushButton.clicked.connect(self.showProfile)
        self.closeRightMenu_pushButton.clicked.connect(self.hideRightMenu)
        
        # PROFILE BUTTON FUNCTIONS 
        self.updateAcc_pushButton.clicked.connect(self.updateProfile)
        self.logoutAcc_pushButton.clicked.connect(self.logoutProfile)

        QSizeGrip(self.sizeGrip)

    def loadData(self):
        row = 0
        rowCount = 0
        all_students = db.child("student").get()
        for student in all_students.each():
            rowCount = rowCount + 1
        self.tableWidget.setRowCount(rowCount)

        for student in all_students.each():
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(student.val()["lname"]).upper()))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(student.val()["fname"]).upper()))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(student.val()["mname"]).upper()))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(student.val()["course"]).upper()))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(student.val()["year"]).upper()))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(student.val()["section"]).upper()))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(student.val()["school"]).upper()))
                row = row + 1 

    def loadGrades(self):
            row = 0
            rowCount = 0
            all_students = db.child("student").get()
            for student in all_students.each():
                rowCount = rowCount + 1
            self.tableWidget_2.setRowCount(rowCount)

            for student in all_students.each():
                    self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(student.val()["lname"]).upper()))
                    self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(student.val()["fname"]).upper()))
                    self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(student.val()["mname"]).upper()))
                    self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(student.val()["unitTest1_score"]).upper()))
                    self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(str(student.val()["unitTest2_score"]).upper()))
                    self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(str(student.val()["assessment_score"]).upper()))
                    self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem(str(student.val()["post_assessment_score"]).upper()))
                    row = row + 1 

        # PROFILE BUTTON FUNCTIONS
    def updateProfile(self):
        self.hide()
        self.toUpdateProf = toTeachUpdateProfile()
        self.toUpdateProf.show()
    def logoutProfile(self):
        self.tologoutProf = toTeachLogout(self)
        self.tologoutProf.show()

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

    def showProfile(self):
        if self.rightMenuNum == 0:
            self.animaRightContainer2 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"maximumWidth")
            self.animaRightContainer2.setDuration(500)
            self.animaRightContainer2.setStartValue(0)
            self.animaRightContainer2.setEndValue(250)
            self.animaRightContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer2.start() 

            self.animaRightContainer1 = QtCore.QPropertyAnimation(self.rightMenuContainer, b"minimumWidth")
            self.animaRightContainer1.setDuration(500)
            self.animaRightContainer1.setStartValue(0)
            self.animaRightContainer1.setEndValue(250)
            self.animaRightContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaRightContainer1.start()
            
            self.rightMenuNum = 1
        self.rightMenuPages.setCurrentIndex(0)

    def showModule1(self):
        self.moduleMenuPages.setCurrentIndex(0)
        self.lessonsContainer.setVisible(True)

    def showModule2(self):
        self.moduleMenuPages.setCurrentIndex(1)
        self.lessonsContainer.setVisible(True)

    def showModule3(self):
        self.moduleMenuPages.setCurrentIndex(2)
        self.lessonsContainer.setVisible(True)

    def showHome(self):
        self.menuPages.setCurrentIndex(0)
        # self.lessonsContainer.setVisible(False)
    def showModules(self):
        self.menuPages.setCurrentIndex(1)
    def showProgress(self):
        self.menuPages.setCurrentIndex(2)
    
    def showInformation(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(200)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(200)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start()
            
            self.centerMenuNum = 1
        self.centerMenuPages.setCurrentIndex(2)
        
    def showHelp(self):
        if self.centerMenuNum == 0:
            self.animaCenterContainer2 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"maximumWidth")
            self.animaCenterContainer2.setDuration(500)
            self.animaCenterContainer2.setStartValue(0)
            self.animaCenterContainer2.setEndValue(200)
            self.animaCenterContainer2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer2.start() 

            self.animaCenterContainer1 = QtCore.QPropertyAnimation(self.centerMenuContainer, b"minimumWidth")
            self.animaCenterContainer1.setDuration(500)
            self.animaCenterContainer1.setStartValue(0)
            self.animaCenterContainer1.setEndValue(200)
            self.animaCenterContainer1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animaCenterContainer1.start()
            
            self.centerMenuNum = 1
        self.centerMenuPages.setCurrentIndex(1)

    def showLeftMenu(self):
        if self.leftMenuNum == 0:
            self.animation1 = QtCore.QPropertyAnimation(self.leftMenuContainer , b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(45)
            self.animation1.setEndValue(150)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start() 

            self.animation2 = QtCore.QPropertyAnimation(self.leftMenuContainer, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(45)
            self.animation2.setEndValue(150)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation2.start()

            self.leftMenuNum = 1
        else:
            self.animation1 = QtCore.QPropertyAnimation(self.leftMenuContainer, b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(150)
            self.animation1.setEndValue(45)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start() 

            self.animation2 = QtCore.QPropertyAnimation(self.leftMenuContainer, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(150)
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

class toTeachLogout(QDialog):
    def __init__(self, parent):
        super(toTeachLogout, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)

        self.setWindowModality(Qt.ApplicationModal)

        self.yes_pushButton.clicked.connect(self.yesFunction)
        self.no_pushButton.clicked.connect(self.noFunction)

    def yesFunction(self):
        print("YES PRESSED")
        self.hide()
        self.parent().hide()
        self.toGoBack = toStudTeach()
        self.toGoBack.show()
    
    def noFunction(self):
        self.hide()
        print("NO PRESSED")
        
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

class toSplashScreen(QMainWindow):
    def __init__(self):
        super(toSplashScreen, self).__init__()

        loadUi("data/loadingScreen1.ui", self)
        self.setWindowIcon(QIcon(resource_path("assets/images/logo.png")))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)

        self.setWindowFlag(Qt.FramelessWindowHint)
    def mousePressEvent(self, event):
        pass

    def progress(self):
        for i in range(100):
            self.progressBar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.1)
        self.close()
        print("yes")
        self.next = toDashboardTeach()
        self.next.show()
##################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = toStudTeach()
    # w = toDashboard()
    w.show()
    sys.exit(app.exec_())

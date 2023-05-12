import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from PyQt5.QtChart import *
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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

openai.api_key = os.getenv("OPENAI_API_KEY")
idKey = ""
submit_unit1 = False
submit_unit2 = False
pre_assess_total_items = 0
post_assess_total_items = 0
unitTest1_total_items = 0
unitTest2_total_items = 0
fromLesson1 = 0
fromLesson2 = 0
fromPost = 0
fromQuestion = 0
new_unitTest1 = True
new_unitTest2 = True
new_preAssess = True
new_postAssess = True
questionId_save = ""
pre_count = ""
post_count = ""
studKey = ""
willLogout = 0


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

#auth.delete_user(uid) // DELETE A USER IN AUTHENTICATION

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
        load_ai()

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
        global willLogout
        willLogout = 0
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
                    login= auth.sign_in_with_email_and_password(email,password)
                    login = auth.refresh(login['refreshToken'])
                    # now we have a fresh token
                    login['idToken']                    
                    self.hide()
                    self.toLogin = splashScreen()
                    self.toLogin.show()
                    self.toLogin.progress()  

                else:
                    self.warning_Widget.setVisible(True)
                    self.warningPages.setCurrentIndex(0)
        except:
                self.warning_Widget.setVisible(True)
                self.warningPages.setCurrentIndex(0)

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
        self.warningEmailInUsed.setVisible(False)

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
        self.emailCheck_ifPair = 0

        fname = self.studFirst_lineEdit.text()
        mname = self.studMiddle_lineEdit.text()
        lname = self.studLast_lineEdit.text()
        school = self.studSchool_lineEdit.text()
        section = self.studSec_comboBox.currentText()
        course = self.studGrd_comboBox.currentText()
        year = self.studYr_comboBox.currentText()
        studentSchoolID = self.studSchoolID_lineEdit.text()
        isActive = "1"
        email = self.studEmail_lineEdit.text()
        password = self.studPass_lineEdit.text()

        all_students = db.child("student").get()
        for student in all_students.each():
            if student.val()["email"] == email:
                self.emailCheck_ifPair = 1
# REGISTER CHECKING
        if fname == "":
            self.fnameError = 1
        if mname == "":
            mname = ""
        if lname == "":
            self.lnameError = 1
        if section == "Section" or year == "Year" or course == "Strand":
            self.yrSecError = 1
        if school == "":
            self.schoolError = 1
        if email == "" :
            self.emailError = 1
        if password == "" or password.isdigit() == False or len(password)+1 < 8:
            self.passError = 1
        if studentSchoolID == "":
            self.studIDError = 1

        if self.emailCheck_ifPair == 1:
            self.warningEmailInUsed.setVisible(True)
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

        if self.fnameError == 1 or self.lnameError == 1 or self.yrSecError == 1 or self.schoolError == 1 or self.emailError == 1 or self.passError == 1 or self.emailCheck_ifPair == 1:
            self.frame.setGeometry(QtCore.QRect(40, 50, 295, 680))
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(0)
            self.fnameError = 0
            self.lnameError = 0
            self.yrSecError = 0
            self.schoolError = 0
            self.emailError = 0
            self.passError = 0
            self.studIDError = 0
            self.emailCheck_ifPair = 0
        else:
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(1)
            self.studFirst_lineEdit.clear()
            self.studMiddle_lineEdit.clear()
            self.studLast_lineEdit.clear()
            self.studSchool_lineEdit.clear()
            self.studSchoolID_lineEdit.clear()
            self.studEmail_lineEdit.clear()
            self.studPass_lineEdit.clear()
            reigster= auth.create_user_with_email_and_password(email, password)
            
            data ={"fname":fname,"mname":mname,"lname":lname, "course":course
       ,"year":year,"section":section,"studentSchoolID":studentSchoolID,"school":school,"email":email
       ,"isActive":isActive, "assessment_score":"0", "assessment_count":"0", "post_assessment_count":"0","post_assessment_score":"0", "post_assessment_score1":"0",
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
        global willLogout
        willLogout = 0
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
                    login= auth.sign_in_with_email_and_password(email,password)
                    login = auth.refresh(login['refreshToken'])
                    # now we have a fresh token
                    login['idToken']
                    self.hide()
                    self.toLogin = toSplashScreen()
                    self.toLogin.show()
                    self.toLogin.progress()
                else:
                    self.warning_Widget.setVisible(True)
        except:
            self.warning_Widget.setVisible(True)

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
        self.warningEmailInUsed.setVisible(False)

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
        self.emailCheck_ifPair = 0

        fname = self.teachFirst_lineEdit.text()
        mname = self.teachMiddle_lineEdit.text()
        lname = self.teachLast_lineEdit.text()
        school = self.teachSchool_lineEdit.text()
        teachSchoolID = self.teachID_lineEdit.text()
        course = self.teachGrd_comboBox.currentText()
        isActive = "1"

        email = self.teachEmail_lineEdit.text()
        password = self.teachPass_lineEdit.text()

        all_teacher = db.child("teacher").get()
        for teacher in all_teacher.each():
            if teacher.val()["email"] == email:
                self.emailCheck_ifPair = 1
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
        if password == "" or password.isdigit() == False or len(password)+1 < 8:
            self.passError = 1

        if self.emailCheck_ifPair == 1:
            self.warningEmailInUsed.setVisible(True)
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

        if self.fnameError == 1 or self.lnameError == 1 or self.teachIDError == 1 or self.schoolError == 1 or self.emailError == 1 or self.passError == 1 or self.emailCheck_ifPair == 1:
            self.frame.setGeometry(QtCore.QRect(50, 30, 295,680))
            self.warningContainer.setVisible(True)
            self.warningContainerMenu.setCurrentIndex(0)

            self.emailCheck_ifPair = 0
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

def load_ai():
    list_of_sol = []
    circle_ans, circle_solu,  returned_circle = display_random_question.pre_assess_circle()
    parabola_ans, parabola_solu, returned_parabola = display_random_question.pre_assess_parabola()
    ellipse_ans, ellipse_solu, returned_ellipse = display_random_question.pre_assess_ellipse()
    hyperbola_ans, hyperbola_solu, returned_hyperbola = display_random_question.pre_assess_hyper()
    substitution_ans, substitution_solu, returned_substitution = display_random_question.pre_assess_subs()
    elimination_ans, elimination_solu, returned_elimination = display_random_question.pre_assess_elim()

    circle_ans1, circle_solu1,  returned_circle1 = display_random_question.post_assess_circle()
    parabola_ans1, parabola_solu1, returned_parabola1 = display_random_question.post_assess_parabola()
    ellipse_ans1, ellipse_solu1, returned_ellipse1 = display_random_question.post_assess_ellipse()
    hyperbola_ans1, hyperbola_solu1, returned_hyperbola1 = display_random_question.post_assess_hyper()
    substitution_ans1, substitution_solu1, returned_substitution1 = display_random_question.post_assess_subs()
    elimination_ans1, elimination_solu1, returned_elimination1 = display_random_question.post_assess_elim()

    circle_ans2, circle_solu2,  returned_circle2 = display_random_question.unit_test_circle()
    parabola_ans2, parabola_solu2, returned_parabola2 = display_random_question.unit_test_parabola()
    ellipse_ans2, ellipse_solu2, returned_ellipse2= display_random_question.unit_test_ellipse()
    hyperbola_ans2, hyperbola_solu2, returned_hyperbola2= display_random_question.unit_test_hyper()

    substitution_ans2, substitution_solu2, returned_substitution2 = display_random_question.unit_test_subs()
    elimination_ans2, elimination_solu2, returned_elimination2 = display_random_question.unit_test_elim()
    
    list_of_sol.append(circle_ans)
    list_of_sol.append(circle_solu)
    list_of_sol.append(parabola_ans)
    list_of_sol.append(parabola_solu)
    list_of_sol.append(ellipse_ans)
    list_of_sol.append(ellipse_solu)
    list_of_sol.append(hyperbola_ans)
    list_of_sol.append(hyperbola_solu)
    list_of_sol.append(substitution_ans)
    list_of_sol.append(substitution_solu)
    list_of_sol.append(elimination_ans)
    list_of_sol.append(elimination_solu)

    list_of_sol.append(circle_ans1)
    list_of_sol.append(circle_solu1)
    list_of_sol.append(parabola_ans1)
    list_of_sol.append(parabola_solu1)
    list_of_sol.append(ellipse_ans1)
    list_of_sol.append(ellipse_solu1)
    list_of_sol.append(hyperbola_ans1)
    list_of_sol.append(hyperbola_solu1)
    list_of_sol.append(substitution_ans1)
    list_of_sol.append(substitution_solu1)
    list_of_sol.append(elimination_ans1)
    list_of_sol.append(elimination_solu1)

    list_of_sol.append(circle_ans2)
    list_of_sol.append(circle_solu2)
    list_of_sol.append(parabola_ans2)
    list_of_sol.append(parabola_solu2)
    list_of_sol.append(ellipse_ans2)
    list_of_sol.append(ellipse_solu2)
    list_of_sol.append(hyperbola_ans2)
    list_of_sol.append(hyperbola_solu2)

    list_of_sol.append(substitution_ans2)
    list_of_sol.append(substitution_solu2)
    list_of_sol.append(elimination_ans2)
    list_of_sol.append(elimination_solu2)

    display_random_question.to_json(list_of_sol)

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

        global new_unitTest1, new_unitTest2, new_preAssess, new_postAssess, fromLesson1, fromLesson2, fromPost
        new_unitTest1 = True
        new_unitTest2 = True
        new_preAssess = True
        new_postAssess = True
       
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
                studAssessment_score1 = (student.val()["assessment_score1"])
                studPostAssessment_score1 = (student.val()["post_assessment_score1"])
                studUnitTest1_score =(student.val()["unitTest1_score"])
                studUnitTest2_score =(student.val()["unitTest2_score"])
                global post_count, pre_count, studKey
                studKey = (student.val())
                post_count = (student.val()["post_assessment_count"])
                pre_count = (student.val()["assessment_count"])
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

        ave_assess = (int(studAssessment_score) / 30) * 100    
        if ave_assess > 80:
            assess_result=("Outstanding")
        elif ave_assess > 60:
            assess_result=("Very Good")
        elif ave_assess > 40:
            assess_result=("Good")
        else:
            assess_result=("Needs Improvement")

        ave_assess = (int(studPostAssessment_score) / 30) * 100    
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

        self.preAssess1_label.setText(str(studAssessment_score)+"/30")
        self.preAssess1_progressBar.setValue(int(studAssessment_score))
        self.preAssess1_progressBar.setMaximum(30)
            
        self.preAssess2_label.setText(str(studAssessment_score1)+"/30")
        self.preAssess2_progressBar.setValue(int(studAssessment_score1))
        self.preAssess2_progressBar.setMaximum(30)

        self.postAssess1_label.setText(str(studPostAssessment_score)+"/30")
        self.postAssess1_progressBar.setValue(int(studPostAssessment_score))
        self.postAssess1_progressBar.setMaximum(30)

        self.postAssess2_label.setText(str(studPostAssessment_score1)+"/30")
        self.postAssess2_progressBar.setValue(int(studPostAssessment_score1))
        self.postAssess2_progressBar.setMaximum(30)

        self.show_scoreUnit1_label.setText(str(studUnitTest1_score)+"/60")
        self.unitTest1_progressBar.setValue(int(studUnitTest1_score))
        self.unitTest1_progressBar.setMaximum(60)

        self.show_scoreUnit2_label.setText(str(studUnitTest2_score)+"/60")
        self.unitTest2_progressBar.setValue(int(studUnitTest2_score))
        self.unitTest2_progressBar.setMaximum(60)
        
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
            if willLogout == 0:
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
            else:
                pass
        
        if self.rightMenuNum == 0:
            if willLogout == 0:
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
            else:
                pass
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

        if fromLesson1 == 1:
            self.showModule1()
            self.menuPages.setCurrentIndex(1)
            fromLesson1 = 0
        if fromLesson2 == 1:
            self.showModule2()
            self.menuPages.setCurrentIndex(1)
            fromLesson2 = 0
        if fromPost == 1:
            self.menuPages.setCurrentIndex(1)
            fromPost = 0

        QSizeGrip(self.sizeGrip)

    def assessmentWindow(self):
        if willLogout == 0:
            self.hide()
            self.assessment = assessmentWindow()
            self.assessment.show()
        else:
            pass
    def postAssessmentWindow(self):
        if willLogout == 0:
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
        else:
            pass

# PROCEED BUTTON OF TOPICS FUNCTIONS
    def lessons_circle(self):
        if willLogout == 0:
            self.hide()
            self.circle = topicLesson1()
            self.circle.show()
        else:
            pass
    def lessons_parabola(self):
        if willLogout == 0:
            self.hide()
            self.parabola = topicLesson2()
            self.parabola.show()
        else:
            pass
    def lessons_ellipse(self):
        if willLogout == 0:
            self.hide()
            self.ellipse = topicLesson3()
            self.ellipse.show()
        else:
            pass
    def lessons_hyperbola(self):
        if willLogout == 0:
            self.hide()
            self.hyperbola= topicLesson4()
            self.hyperbola.show()
        else:
            pass
    def lessons_substitute(self):
        if willLogout == 0:
            self.hide()
            self.substitute = topicLesson5()
            self.substitute.show()
        else:
            pass
    def lessons_eliminate(self):
        if willLogout == 0:
            self.hide()
            self.eliminate = topicLesson6()
            self.eliminate.show()
        else:
            pass
    def lessons_graphSolApp(self):
        if willLogout == 0:
            self.hide()
            self.graphSolApp = topicLesson7()
            self.graphSolApp.show()
        else:
            pass

# UNIT TEST 
    def unitTest1(self):
        if willLogout == 0:
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
        else:
            pass
    def unitTest2(self):
        if willLogout == 0:
            global submit_unit2, new_unitTest2
            submit_unit2 = False
            new_unitTest2 = True
            
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
        else:
            pass
# PROFILE BUTTON FUNCTIONS
    def updateProfile(self):
        if willLogout == 0:
            self.hide()
            self.toUpdateProf = toStudUpdateProfile()
            self.toUpdateProf.show()
        else:
            pass
    def logoutProfile(self):
        if willLogout == 0:
            self.toLogoutStud = toStudLogout(self)
            self.toLogoutStud.show()
        else:
            pass
# LESSON BUTTON FUNCTIONS
    def lesson1_1A(self):
        if willLogout == 0:
            self.lessonInfoSubContainer.setCurrentIndex(1)
        else:
            pass
    def lesson1_1B(self):
        if willLogout == 0:
            self.lessonInfoSubContainer.setCurrentIndex(2)
        else:
            pass
    def lesson1_1C(self):
        if willLogout == 0:
            self.lessonInfoSubContainer.setCurrentIndex(3)
        else:
            pass
    def lesson1_1D(self):
        if willLogout == 0:
            self.lessonInfoSubContainer.setCurrentIndex(4)
        else:
            pass
    def lesson1_1Test(self):
        if willLogout == 0:
            self.lessonInfoSubContainer.setCurrentIndex(5)
        else:
            pass
    def lesson2_1A(self): 
        if willLogout == 0:
            self.lessonInfo2SubContainer.setCurrentIndex(1)
        else:
            pass
    def lesson2_1B(self):
        if willLogout == 0:   
            self.lessonInfo2SubContainer.setCurrentIndex(2)
        else:
            pass
    def lesson2_1C(self):   
        if willLogout == 0:
            self.lessonInfo2SubContainer.setCurrentIndex(3)
        else:
            pass
    def lesson2_1Test(self):   
        if willLogout == 0:
            self.lessonInfo2SubContainer.setCurrentIndex(4)
        else:
            pass

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
            fig = plt.figure(figsize=(0.01, 0.01))
            fig.text(50, 0, "There is an error\nin your input.\nEither a\n-Double backslash \neg.(\\\\right),\n-Incomplete figures in parameters \neg.(\left( , {\circ  )\n-Blank Input\neg.( )", fontsize=fontsize)

            output = BytesIO()
            fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                        bbox_inches="tight", pad_inches=0.0, facecolor='auto'
                        , edgecolor = "auto", backend=None)
            plt.close(fig)

            output.seek(0)
            return output.read()
        plt.rc("'mathtext', fontset='cm'")
        word = self.chatSends_TextEdit.toPlainText()
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
                self.textEdit_2.insertPlainText(chatbot_response)
            else:
                chatbot_denied="Sorry, I can only help with precalculus-related questions."
                self.textEdit_2.insertPlainText(chatbot_denied)

            self.chatbot_count = self.chatbot_count + 1

    def hideWindow(self):
        self.showMinimized()  
    def bigWindow(self):
        if willLogout == 0:
            if self.restoreWindow == 0:
                self.showMaximized()
                self.maxWindow = True
                self.restoreWindow = 1

            else:           
                self.showNormal()  
                self.maxWindow = False
                self.restoreWindow = 0
        else:
            pass

    def showNotif(self):
        if willLogout == 0:
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
        else:
            pass

    def showProfile(self):
        if willLogout == 0:
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
        else:
            pass

    def showModule1(self):
        if willLogout == 0:
            self.moduleMenuPages.setCurrentIndex(0)
            self.lesson1_1Container.setVisible(True)
            self.lessonsContainer.setVisible(True)
            self.lessonInfo1Container.setVisible(True)
            self.lessonInfoSubContainer.setCurrentIndex(0)
        else:
            pass

    def showModule2(self):
        if willLogout == 0:
            self.moduleMenuPages.setCurrentIndex(1)
            self.lesson2_1Container.setVisible(True)
            self.lessonsContainer.setVisible(True)
            self.lessonInfo2Container.setVisible(True)
            self.lessonInfo2SubContainer.setCurrentIndex(0)
        else:
            pass
    def showModule3(self):
        if willLogout == 0:
            self.moduleMenuPages.setCurrentIndex(2)
            self.lessonsContainer.setVisible(True)
        else:
            pass

    def showHome(self):
        if willLogout == 0:
            self.menuPages.setCurrentIndex(0)
            self.lessonsContainer.setVisible(False)
        else:
            pass
    def showModules(self):
        if willLogout == 0:
            self.menuPages.setCurrentIndex(1)
        else:
            pass
    def showProgress(self):
        if willLogout == 0:
            self.menuPages.setCurrentIndex(2)
            self.lessonsContainer.setVisible(False)
        else:
            pass
    
    def showInformation(self):
        if willLogout == 0:
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
        else:
            pass
        
    def showHelp(self):
        if willLogout == 0:
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
        else:
            pass

    def showLeftMenu(self):
        if willLogout == 0:
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
        else:
            pass

    def hideCenterMenu(self):
        if willLogout == 0:
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
        else:
            pass

    def hideRightMenu(self):
        if willLogout == 0:
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
        else:
            pass

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

        self.logoutUpdatePages.setCurrentIndex(0)
        global willLogout
        willLogout = 1
        self.yes_pushButton.clicked.connect(self.yesFunction)
        self.no_pushButton.clicked.connect(self.noFunction)

    def yesFunction(self):
        self.hide()
        self.parent().hide()
        self.toGoBack = toStudTeach()
        self.toGoBack.show()
    
    def noFunction(self):
        self.hide()
        global willLogout 
        willLogout = 0
        
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
        global fromLesson1
        fromLesson1 = 1
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
        global fromLesson1
        fromLesson1 = 1
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
        global fromLesson1
        fromLesson1 = 1
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
        global fromLesson1
        fromLesson1 = 1
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
        global fromLesson2
        fromLesson2 = 1
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
        global fromLesson2
        fromLesson2 = 1
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
        global fromLesson2
        fromLesson2 = 1
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

        if new_preAssess == True:
            pre_assess_all = []
            pre_assess_each_quest1 = []
            pre_assess_each_quest2 = []
            pre_assess_each_quest3 = []
            pre_assess_each_quest4 = []
            pre_assess_each_quest5 = []
            pre_assess_each_quest6 = []

            circle_ans, circle_solu,  returned_circle = display_random_question.pre_assess_circle()
            parabola_ans, parabola_solu, returned_parabola = display_random_question.pre_assess_parabola()
            ellipse_ans, ellipse_solu, returned_ellipse = display_random_question.pre_assess_ellipse()
            hyperbola_ans, hyperbola_solu, returned_hyperbola = display_random_question.pre_assess_hyper()
            substitution_ans, substitution_solu, returned_substitution = display_random_question.pre_assess_subs()
            elimination_ans, elimination_solu, returned_elimination = display_random_question.pre_assess_elim()

            pre_assess_each_quest1.append(returned_circle[0])
            pre_assess_each_quest1.append(returned_circle[1])
            pre_assess_each_quest1.append(returned_circle[2])

            pre_assess_each_quest2.append(returned_parabola[0])
            pre_assess_each_quest2.append(returned_parabola[1])
            pre_assess_each_quest2.append(returned_parabola[2])

            pre_assess_each_quest3.append(returned_ellipse[0])
            pre_assess_each_quest3.append(returned_ellipse[1])
            pre_assess_each_quest3.append(returned_ellipse[2])

            pre_assess_each_quest4.append(returned_hyperbola[0])
            pre_assess_each_quest4.append(returned_hyperbola[1])
            pre_assess_each_quest4.append(returned_hyperbola[2])

            pre_assess_each_quest5.append(returned_substitution[0])
            pre_assess_each_quest5.append(returned_substitution[1])
            pre_assess_each_quest5.append(returned_substitution[2])

            pre_assess_each_quest6.append(returned_elimination[0])
            pre_assess_each_quest6.append(returned_elimination[1])
            pre_assess_each_quest6.append(returned_elimination[2])

            pre_assess_all.append(pre_assess_each_quest1)
            pre_assess_all.append(pre_assess_each_quest2)
            pre_assess_all.append(pre_assess_each_quest3)
            pre_assess_all.append(pre_assess_each_quest4)
            pre_assess_all.append(pre_assess_each_quest5)
            pre_assess_all.append(pre_assess_each_quest6)
            
            pre_question1, pre_question2, pre_question3, pre_question4, pre_question5 = display_random_question.random_questions(pre_assess_all)

            data.scores.pre_question1 = pre_question1[0]
            data.scores.pre_question2 = pre_question2[0]
            data.scores.pre_question3 = pre_question3[0]
            data.scores.pre_question4 = pre_question4[0]
            data.scores.pre_question5 = pre_question5[0]

            data.scores.pre1_solutionId = pre_question1[1]
            data.scores.pre1_answerId = pre_question1[2]
            data.scores.pre2_solutionId = pre_question2[1]
            data.scores.pre2_answerId = pre_question2[2]
            data.scores.pre3_solutionId = pre_question3[1]
            data.scores.pre3_answerId = pre_question3[2]
            data.scores.pre4_solutionId = pre_question4[1]
            data.scores.pre4_answerId = pre_question4[2]
            data.scores.pre5_solutionId = pre_question5[1]
            data.scores.pre5_answerId = pre_question5[2]

        self.pre_Q1_label.setText("1."+ data.scores.pre_question1)
        self.pre_Q2_label.setText("2."+ data.scores.pre_question2)
        self.pre_Q3_label.setText("3."+ data.scores.pre_question3)
        self.pre_Q4_label.setText("4."+ data.scores.pre_question4)
        self.pre_Q5_label.setText("5."+ data.scores.pre_question5)

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
        global new_preAssess
        new_preAssess = True
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
        question = data.scores.pre1_solutionId
        check_assess_q1_sol = chat(question, assess_sol_Q1)
        question = data.scores.pre1_answerId
        check_assess_q1_ans = chat(question, assess_ans_Q1)
                
        if check_assess_q1_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q1_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 2, solution and answer
        question = data.scores.pre2_solutionId
        check_assess_q2_sol = chat(question, assess_sol_Q2)
        question = data.scores.pre2_answerId
        check_assess_q2_ans = chat(question, assess_ans_Q2)

        if check_assess_q2_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q2_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 3, solution and answer
        question = data.scores.pre3_solutionId
        check_assess_q3_sol = chat(question, assess_sol_Q3)
        question = data.scores.pre3_answerId
        check_assess_q3_ans = chat(question, assess_ans_Q3)

        if check_assess_q3_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q3_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 4, solution and answer
        question = data.scores.pre4_solutionId
        check_assess_q4_sol = chat(question, assess_sol_Q4)
        question = data.scores.pre4_answerId
        check_assess_q4_ans = chat(question, assess_ans_Q4)

        if check_assess_q4_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q4_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1

        # Question 5, solution and answer
        question = data.scores.pre5_solutionId
        check_assess_q5_sol = chat(question, assess_sol_Q5)
        question = data.scores.pre5_answerId
        check_assess_q5_ans = chat(question, assess_ans_Q5)

        if check_assess_q5_sol == "correct":
            data.scores.assess_score = data.scores.assess_score + 4
        if check_assess_q5_ans == "correct":
            data.scores.assess_score = data.scores.assess_score + 1
        
        print(data.scores.assess_score)
        if pre_count == "0":
            studKey = db.child("student").get()
            for keyAccess in studKey.each():
                if keyAccess.val()["studentSchoolID"] == idKey:
                    keyID = keyAccess.key()
            db.child("student").child(keyID).update({"assessment_score":str(data.scores.assess_score),"assessment_count":"1"})
        if pre_count == "1":
            studKey = db.child("student").get()
            for keyAccess in studKey.each():
                if keyAccess.val()["studentSchoolID"] == idKey:
                    keyID = keyAccess.key()
            db.child("student").child(keyID).update({"assessment_score1":str(data.scores.assess_score),"assessment_count":"0"})
        global new_preAssess
        new_preAssess = False

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

        if new_unitTest1 == True:
            # # RNGED UNIT TEST 1 QUESTIONS
            unit_test1_all = []
            unit_test1_each_quest1 = []
            unit_test1_each_quest2 = []
            unit_test1_each_quest3 = []
            unit_test1_each_quest4 = []
            unit_test1_each_quest5 = []
            unit_test1_each_quest6 = []
            unit_test1_each_quest7 = []
            unit_test1_each_quest8 = []
            unit_test1_each_quest9 = []
            unit_test1_each_quest10 = []
            unit_test1_each_quest11 = []
            unit_test1_each_quest12 = []

            circle_ans2, circle_solu2,  returned_circle2 = display_random_question.unit_test_circle()
            parabola_ans2, parabola_solu2, returned_parabola2 = display_random_question.unit_test_parabola()
            ellipse_ans2, ellipse_solu2, returned_ellipse2= display_random_question.unit_test_ellipse()
            hyperbola_ans2, hyperbola_solu2, returned_hyperbola2= display_random_question.unit_test_hyper()

            unit_test1_each_quest1.append(returned_circle2[0])
            unit_test1_each_quest1.append(returned_circle2[1])
            unit_test1_each_quest1.append(returned_circle2[2])
            unit_test1_each_quest2.append(returned_circle2[3])
            unit_test1_each_quest2.append(returned_circle2[4])
            unit_test1_each_quest2.append(returned_circle2[5])
            unit_test1_each_quest3.append(returned_circle2[6])
            unit_test1_each_quest3.append(returned_circle2[7])
            unit_test1_each_quest3.append(returned_circle2[8])

            unit_test1_each_quest4.append(returned_parabola2[0])
            unit_test1_each_quest4.append(returned_parabola2[1])
            unit_test1_each_quest4.append(returned_parabola2[2])
            unit_test1_each_quest5.append(returned_parabola2[3])
            unit_test1_each_quest5.append(returned_parabola2[4])
            unit_test1_each_quest5.append(returned_parabola2[5])
            unit_test1_each_quest6.append(returned_parabola2[6])
            unit_test1_each_quest6.append(returned_parabola2[7])
            unit_test1_each_quest6.append(returned_parabola2[8])

            unit_test1_each_quest7.append(returned_ellipse2[0])
            unit_test1_each_quest7.append(returned_ellipse2[1])
            unit_test1_each_quest7.append(returned_ellipse2[2])
            unit_test1_each_quest8.append(returned_ellipse2[3])
            unit_test1_each_quest8.append(returned_ellipse2[4])
            unit_test1_each_quest8.append(returned_ellipse2[5])
            unit_test1_each_quest9.append(returned_ellipse2[6])
            unit_test1_each_quest9.append(returned_ellipse2[7])
            unit_test1_each_quest9.append(returned_ellipse2[8])

            unit_test1_each_quest10.append(returned_hyperbola2[0])
            unit_test1_each_quest10.append(returned_hyperbola2[1])
            unit_test1_each_quest10.append(returned_hyperbola2[2])
            unit_test1_each_quest11.append(returned_hyperbola2[3])
            unit_test1_each_quest11.append(returned_hyperbola2[4])
            unit_test1_each_quest11.append(returned_hyperbola2[5])
            unit_test1_each_quest12.append(returned_hyperbola2[6])
            unit_test1_each_quest12.append(returned_hyperbola2[7])
            unit_test1_each_quest12.append(returned_hyperbola2[8])

            unit_test1_all.append(unit_test1_each_quest1)
            unit_test1_all.append(unit_test1_each_quest2)
            unit_test1_all.append(unit_test1_each_quest3)
            unit_test1_all.append(unit_test1_each_quest4)
            unit_test1_all.append(unit_test1_each_quest5)
            unit_test1_all.append(unit_test1_each_quest6)
            unit_test1_all.append(unit_test1_each_quest7)
            unit_test1_all.append(unit_test1_each_quest8)
            unit_test1_all.append(unit_test1_each_quest9)
            unit_test1_all.append(unit_test1_each_quest10)
            unit_test1_all.append(unit_test1_each_quest11)
            unit_test1_all.append(unit_test1_each_quest12)

            unit_test1_question1, unit_test1_question2, unit_test1_question3, unit_test1_question4, unit_test1_question5, unit_test1_question6, unit_test1_question7, unit_test1_question8 ,unit_test1_question9 ,unit_test1_question10= display_random_question.random_questions_2(unit_test1_all)

            data.scores.unit_test1_question1 = unit_test1_question1[0]
            data.scores.unit_test1_question2 = unit_test1_question2[0]
            data.scores.unit_test1_question3 = unit_test1_question3[0]
            data.scores.unit_test1_question4 = unit_test1_question4[0]
            data.scores.unit_test1_question5 = unit_test1_question5[0]
            data.scores.unit_test1_question6 = unit_test1_question6[0]
            data.scores.unit_test1_question7 = unit_test1_question7[0]
            data.scores.unit_test1_question8 = unit_test1_question8[0]
            data.scores.unit_test1_question9 = unit_test1_question9[0]
            data.scores.unit_test1_question10 = unit_test1_question10[0]

            data.scores.unit1_1_solutionId = unit_test1_question1[1]
            data.scores.unit1_1_answerId =unit_test1_question1[2]
            data.scores.unit1_2_solutionId = unit_test1_question2[1]
            data.scores.unit1_2_answerId =unit_test1_question2[2]
            data.scores.unit1_3_solutionId = unit_test1_question3[1]
            data.scores.unit1_3_answerId =unit_test1_question3[2]
            data.scores.unit1_4_solutionId = unit_test1_question4[1]
            data.scores.unit1_4_answerId =unit_test1_question4[2]
            data.scores.unit1_5_solutionId = unit_test1_question5[1]
            data.scores.unit1_5_answerId =unit_test1_question5[2]
            data.scores.unit1_6_solutionId = unit_test1_question6[1]
            data.scores.unit1_6_answerId =unit_test1_question6[2]
            data.scores.unit1_7_solutionId = unit_test1_question7[1]
            data.scores.unit1_7_answerId =unit_test1_question7[2]
            data.scores.unit1_8_solutionId = unit_test1_question8[1]
            data.scores.unit1_8_answerId =unit_test1_question8[2]
            data.scores.unit1_9_solutionId = unit_test1_question9[1]
            data.scores.unit1_9_answerId =unit_test1_question9[2]
            data.scores.unit1_10_solutionId = unit_test1_question10[1]
            data.scores.unit1_10_answerId =unit_test1_question10[2]

        self.unitTest1_Q1_label.setText("1."+ data.scores.unit_test1_question1)
        self.unitTest1_Q2_label.setText("2."+ data.scores.unit_test1_question2)
        self.unitTest1_Q3_label.setText("3."+ data.scores.unit_test1_question3)
        self.unitTest1_Q4_label.setText("4."+ data.scores.unit_test1_question4)
        self.unitTest1_Q5_label.setText("5."+ data.scores.unit_test1_question5)
        self.unitTest1_Q6_label.setText("6."+ data.scores.unit_test1_question6)
        self.unitTest1_Q7_label.setText("7."+ data.scores.unit_test1_question7)
        self.unitTest1_Q8_label.setText("8."+ data.scores.unit_test1_question8)
        self.unitTest1_Q9_label.setText("9."+ data.scores.unit_test1_question9)
        self.unitTest1_Q10_label.setText("10."+ data.scores.unit_test1_question10)
        
        if submit_unit1 == True:
            self.showScore_widget.setVisible(True)
            # self.showlessonScore_widget.setVisible(True)
            self.unitTest1Submit_container.setCurrentIndex(1)
            self.show_scoreUnit1_label.setText(str(data.scores.unit1_score))
            self.show_score1_label.setText(str(data.scores.circ_score))
            self.show_score2_label.setText(str(data.scores.parab_score))
            self.show_score3_label.setText(str(data.scores.ellip_score))
            self.show_score4_label.setText(str(data.scores.hyperb_score))

            self.unitTestQ1Sol_textEdit.setText(data.scores.unit_test1_saved_solution1)
            self.unitTestQ1Center_textEdit.setText(data.scores.unit_test1_saved_answer1)
            self.unitTestQ2Sol_textEdit.setText(data.scores.unit_test1_saved_solution2)
            self.unitTestQ2Center_textEdit.setText(data.scores.unit_test1_saved_answer2)
            self.unitTestQ3Sol_textEdit.setText(data.scores.unit_test1_saved_solution3)
            self.unitTestQ3Vertex_textEdit.setText(data.scores.unit_test1_saved_answer3)
            self.unitTestQ4Sol_textEdit.setText(data.scores.unit_test1_saved_solution4)
            self.unitTestQ4Vertex_textEdit.setText(data.scores.unit_test1_saved_answer4)
            self.unitTestQ5Sol_textEdit.setText(data.scores.unit_test1_saved_solution5)
            self.unitTestQ5Center_textEdit.setText(data.scores.unit_test1_saved_answer5)
            self.unitTestQ6Sol_textEdit.setText(data.scores.unit_test1_saved_solution6)
            self.unitTestQ6Foci1_textEdit.setText(data.scores.unit_test1_saved_answer6)
            self.unitTestQ7Sol_textEdit.setText(data.scores.unit_test1_saved_solution7)
            self.unitTestQ7Vertex1_textEdit.setText(data.scores.unit_test1_saved_answer7)
            self.unitTestQ8Sol_textEdit.setText(data.scores.unit_test1_saved_solution8)
            self.unitTestQ8Center_textEdit.setText(data.scores.unit_test1_saved_answer8)
            self.unitTestQ9Sol_textEdit.setText(data.scores.unit_test1_saved_solution9)
            self.unitTestQ9MinAxis_textEdit.setText(data.scores.unit_test1_saved_answer9)
            self.unitTestQ10Sol_textEdit.setText(data.scores.unit_test1_saved_solution10)
            self.unitTestQ10StandEquat_textEdit.setText(data.scores.unit_test1_saved_answer10)
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
        global fromLesson1, new_unitTest1
        fromLesson1 = 1
        new_unitTest1 = True
        self.back = toDashboard()
        self.back.show()

    def submitTest(self):
        # Question 1 , answer and solution
        solution_Unit1_Q1 = self.unitTestQ1Sol_textEdit.toPlainText()
        answer1_Unit1_Q1 = self.unitTestQ1Center_textEdit.text()
        data.scores.unit_test1_saved_solution1 = solution_Unit1_Q1
        data.scores.unit_test1_saved_answer1 = answer1_Unit1_Q1
        # Question 2 , answer and solution
        solution_Unit1_Q2 = self.unitTestQ2Sol_textEdit.toPlainText()
        answer1_Unit1_Q2 = self.unitTestQ2Center_textEdit.text()
        data.scores.unit_test1_saved_solution2 = solution_Unit1_Q2
        data.scores.unit_test1_saved_answer2 = answer1_Unit1_Q2
        # Question 3 , answer and solution
        solution_Unit1_Q3 = self.unitTestQ3Sol_textEdit.toPlainText()
        answer1_Unit1_Q3 = self.unitTestQ3Vertex_textEdit.text()
        data.scores.unit_test1_saved_solution3 = solution_Unit1_Q3
        data.scores.unit_test1_saved_answer3 = answer1_Unit1_Q3
        # Question 4 , answer and solution
        solution_Unit1_Q4 = self.unitTestQ4Sol_textEdit.toPlainText()
        answer1_Unit1_Q4 = self.unitTestQ4Vertex_textEdit.text()
        data.scores.unit_test1_saved_solution4 = solution_Unit1_Q4
        data.scores.unit_test1_saved_answer4 = answer1_Unit1_Q4
        # Question 5 , answer and solution
        solution_Unit1_Q5 = self.unitTestQ5Sol_textEdit.toPlainText()
        answer1_Unit1_Q5 = self.unitTestQ5Center_textEdit.text()
        data.scores.unit_test1_saved_solution5 = solution_Unit1_Q5
        data.scores.unit_test1_saved_answer5 = answer1_Unit1_Q5
        # Question 6 , answer and solution
        solution_Unit1_Q6 = self.unitTestQ6Sol_textEdit.toPlainText()
        answer1_Unit1_Q6 = self.unitTestQ6Foci1_textEdit.text()
        data.scores.unit_test1_saved_solution6 = solution_Unit1_Q6
        data.scores.unit_test1_saved_answer6 = answer1_Unit1_Q6
        # Question 7 , answer and solution
        solution_Unit1_Q7 = self.unitTestQ7Sol_textEdit.toPlainText()
        answer1_Unit1_Q7 = self.unitTestQ7Vertex1_textEdit.text()
        data.scores.unit_test1_saved_solution7 = solution_Unit1_Q7
        data.scores.unit_test1_saved_answer7 = answer1_Unit1_Q7
        # Question 8 , answer and solution
        solution_Unit1_Q8 = self.unitTestQ8Sol_textEdit.toPlainText()
        answer1_Unit1_Q8 = self.unitTestQ8Center_textEdit.text()
        data.scores.unit_test1_saved_solution8 = solution_Unit1_Q8
        data.scores.unit_test1_saved_answer8 = answer1_Unit1_Q8
        # Question 9 , answer and solution
        solution_Unit1_Q9 = self.unitTestQ9Sol_textEdit.toPlainText()
        answer1_Unit1_Q9 = self.unitTestQ9MinAxis_textEdit.text()
        data.scores.unit_test1_saved_solution9 = solution_Unit1_Q9
        data.scores.unit_test1_saved_answer9 = answer1_Unit1_Q9
        # Question 10 , answer and solution
        solution_Unit1_Q10 = self.unitTestQ10Sol_textEdit.toPlainText()
        answer1_Unit1_Q10 = self.unitTestQ10StandEquat_textEdit.text()    
        data.scores.unit_test1_saved_solution10 = solution_Unit1_Q10
        data.scores.unit_test1_saved_answer10 = answer1_Unit1_Q10

        # Checking of answer and calculating of score
        data.scores.unit1_score = 0
        data.scores.circ_score = 0
        data.scores.parab_score = 0
        data.scores.ellip_score = 0
        data.scores.hyperb_score = 0

        # Question 1, solution and answer
        question = data.scores.unit1_1_solutionId
        check_unit1_q1_sol = chat(question, solution_Unit1_Q1)
        data.scores.check_unit1_q1_sol= check_unit1_q1_sol
         
        question = data.scores.unit1_1_answerId
        check_unit1_q1_ans = chat(question, answer1_Unit1_Q1)
        data.scores.check_unit1_q1_ans = check_unit1_q1_ans

        if check_unit1_q1_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.circ_score = data.scores.circ_score + 4
        if check_unit1_q1_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1  
            data.scores.circ_score = data.scores.circ_score + 1

        # Question 2, solution and answer
        question = data.scores.unit1_2_solutionId
        check_unit1_q2_sol = chat(question, solution_Unit1_Q2)
        data.scores.check_unit1_q2_sol = check_unit1_q2_sol
        question = data.scores.unit1_2_answerId
        check_unit1_q2_center_ans = chat(question, answer1_Unit1_Q2)
        data.scores.check_unit1_q2_center_ans = check_unit1_q2_center_ans

        if check_unit1_q2_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.circ_score = data.scores.circ_score + 4
        if check_unit1_q2_center_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.circ_score = data.scores.circ_score + 1

        # Question 3, solution and answer
        question = data.scores.unit1_3_solutionId
        check_unit1_q3_sol = chat(question, solution_Unit1_Q3)
        data.scores.check_unit1_q3_sol = check_unit1_q3_sol
        question = data.scores.unit1_3_answerId
        check_unit1_q3_vertex_ans = chat(question, answer1_Unit1_Q3)
        data.scores.check_unit1_q3_vertex_ans = check_unit1_q3_vertex_ans

        if check_unit1_q3_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.parab_score = data.scores.parab_score + 4
        if check_unit1_q3_vertex_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.parab_score = data.scores.parab_score + 1  

        # Question 4, solution and answer
        question = data.scores.unit1_4_solutionId
        check_unit1_q4_sol = chat(question, solution_Unit1_Q4)
        data.scores.check_unit1_q4_sol = check_unit1_q4_sol
        question = data.scores.unit1_4_answerId
        check_unit1_q4_vertex_ans = chat(question, answer1_Unit1_Q4)
        data.scores.check_unit1_q4_vertex_ans = check_unit1_q4_vertex_ans

        if check_unit1_q4_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.parab_score = data.scores.parab_score + 4
        if check_unit1_q4_vertex_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.parab_score = data.scores.parab_score + 1

        # Question 5, solution and answer
        question = data.scores.unit1_5_solutionId
        check_unit1_q5_sol = chat(question, solution_Unit1_Q5)
        data.scores.check_unit1_q5_sol = check_unit1_q5_sol
        question = data.scores.unit1_5_answerId
        check_unit1_q5_center_ans = chat(question, answer1_Unit1_Q5)
        data.scores.check_unit1_q5_center_ans = check_unit1_q5_center_ans

        if check_unit1_q5_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score+ 4
            data.scores.ellip_score = data.scores.ellip_score + 4
        if check_unit1_q5_center_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.ellip_score = data.scores.ellip_score + 1

        # Question 6, solution and answer
        question = data.scores.unit1_6_solutionId
        check_unit1_q6_sol = chat(question, solution_Unit1_Q6)
        data.scores.check_unit1_q6_sol = check_unit1_q6_sol
        question = data.scores.unit1_6_answerId
        check_unit1_q6_foci1_ans = chat(question, answer1_Unit1_Q6)
        data.scores.check_unit1_q6_foci1_ans = check_unit1_q6_foci1_ans

        if check_unit1_q6_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.ellip_score = data.scores.ellip_score + 4
        if check_unit1_q6_foci1_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.ellip_score = data.scores.ellip_score + 1

        # Question 7, solution and answer
        question = data.scores.unit1_7_solutionId
        check_unit1_q7_sol = chat(question, solution_Unit1_Q7)
        data.scores.check_unit1_q7_sol = check_unit1_q7_sol
        question = data.scores.unit1_7_answerId
        check_unit1_q7_vertex1_ans = chat(question, answer1_Unit1_Q7)
        data.scores.check_unit1_q7_vertex1_ans = check_unit1_q7_vertex1_ans

        if check_unit1_q7_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.hyperb_score = data.scores.hyperb_score + 4
        if check_unit1_q7_vertex1_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.hyperb_score = data.scores.hyperb_score + 1   

        # Question 8, solution and answer
        question = data.scores.unit1_8_solutionId
        check_unit1_q8_sol = chat(question, solution_Unit1_Q8)
        data.scores.check_unit1_q8_sol = check_unit1_q8_sol
        question = data.scores.unit1_8_answerId
        check_unit1_q8_center_ans = chat(question, answer1_Unit1_Q8)
        data.scores.check_unit1_q8_center_ans = check_unit1_q8_center_ans

        if check_unit1_q8_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.hyperb_score = data.scores.hyperb_score + 4
        if check_unit1_q8_center_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.hyperb_score = data.scores.hyperb_score + 1

        # Question 9, solution and answer
        question = data.scores.unit1_9_solutionId
        check_unit1_q9_sol = chat(question, solution_Unit1_Q9)
        data.scores.check_unit1_q9_sol = check_unit1_q9_sol 
        question =data.scores.unit1_9_answerId
        check_unit1_q9_minorAxis_ans = chat(question, answer1_Unit1_Q9)
        data.scores.check_unit1_q9_minorAxis_ans = check_unit1_q9_minorAxis_ans

        if check_unit1_q9_sol == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 4
            data.scores.hyperb_score = data.scores.hyperb_score + 4
        if check_unit1_q9_minorAxis_ans == "correct":
            data.scores.unit1_score = data.scores.unit1_score + 1
            data.scores.hyperb_score = data.scores.hyperb_score + 1

        # Question 10, solution and answer
        question = data.scores.unit1_10_solutionId
        check_unit1_q10_sol = chat(question, solution_Unit1_Q10)
        data.scores.check_unit1_q10_sol = check_unit1_q10_sol
        question = data.scores.unit1_10_answerId
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

        global submit_unit1, new_unitTest1
        submit_unit1 = True
        new_unitTest1 = False

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

        self.topicPages.setCurrentIndex(10)

        unit_test2_quest = []
        list_of_sol = []

        if new_unitTest2 == True:
            unit_test2_all = []
            unit_test2_each_quest1 = []
            unit_test2_each_quest2 = []
            unit_test2_each_quest3 = []
            unit_test2_each_quest4 = []
            unit_test2_each_quest5 = []
            unit_test2_each_quest6 = []
            unit_test2_each_quest7 = []
            unit_test2_each_quest8 = []
            unit_test2_each_quest9 = []
            unit_test2_each_quest10 = []

            substitution_ans2, substitution_solu2, returned_substitution2 = display_random_question.unit_test_subs()
            elimination_ans2, elimination_solu2, returned_elimination2 = display_random_question.unit_test_elim()

            unit_test2_each_quest1.append(returned_substitution2[0])
            unit_test2_each_quest1.append(returned_substitution2[1])
            unit_test2_each_quest1.append(returned_substitution2[2])
            unit_test2_each_quest2.append(returned_substitution2[3])
            unit_test2_each_quest2.append(returned_substitution2[4])
            unit_test2_each_quest2.append(returned_substitution2[5])
            unit_test2_each_quest3.append(returned_substitution2[6])
            unit_test2_each_quest3.append(returned_substitution2[7])
            unit_test2_each_quest3.append(returned_substitution2[8])
            unit_test2_each_quest4.append(returned_substitution2[9])
            unit_test2_each_quest4.append(returned_substitution2[10])
            unit_test2_each_quest4.append(returned_substitution2[11])
            unit_test2_each_quest5.append(returned_substitution2[12])
            unit_test2_each_quest5.append(returned_substitution2[13])
            unit_test2_each_quest5.append(returned_substitution2[14])

            unit_test2_each_quest6.append(returned_elimination2[0])
            unit_test2_each_quest6.append(returned_elimination2[1])
            unit_test2_each_quest6.append(returned_elimination2[2])
            unit_test2_each_quest7.append(returned_elimination2[3])
            unit_test2_each_quest7.append(returned_elimination2[4])
            unit_test2_each_quest7.append(returned_elimination2[5])
            unit_test2_each_quest8.append(returned_elimination2[6])
            unit_test2_each_quest8.append(returned_elimination2[7])
            unit_test2_each_quest8.append(returned_elimination2[8])
            unit_test2_each_quest9.append(returned_elimination2[9])
            unit_test2_each_quest9.append(returned_elimination2[10])
            unit_test2_each_quest9.append(returned_elimination2[11])
            unit_test2_each_quest10.append(returned_elimination2[12])
            unit_test2_each_quest10.append(returned_elimination2[13])
            unit_test2_each_quest10.append(returned_elimination2[14])

            unit_test2_all.append(unit_test2_each_quest1)
            unit_test2_all.append(unit_test2_each_quest2)
            unit_test2_all.append(unit_test2_each_quest3)
            unit_test2_all.append(unit_test2_each_quest4)
            unit_test2_all.append(unit_test2_each_quest5)
            unit_test2_all.append(unit_test2_each_quest6)
            unit_test2_all.append(unit_test2_each_quest7)
            unit_test2_all.append(unit_test2_each_quest8)
            unit_test2_all.append(unit_test2_each_quest9)
            unit_test2_all.append(unit_test2_each_quest10)

            unit_test2_question1, unit_test2_question2, unit_test2_question3, unit_test2_question4, unit_test2_question5, unit_test2_question6, unit_test2_question7, unit_test2_question8 ,unit_test2_question9 ,unit_test2_question10= display_random_question.random_questions_2(unit_test2_all)
            
            data.scores.unit_test2_question1 = unit_test2_question1[0]
            data.scores.unit_test2_question2 = unit_test2_question2[0]
            data.scores.unit_test2_question3 = unit_test2_question3[0]
            data.scores.unit_test2_question4 = unit_test2_question4[0]
            data.scores.unit_test2_question5 = unit_test2_question5[0]
            data.scores.unit_test2_question6 = unit_test2_question6[0]
            data.scores.unit_test2_question7 = unit_test2_question7[0]
            data.scores.unit_test2_question8 = unit_test2_question8[0]
            data.scores.unit_test2_question9 = unit_test2_question9[0]
            data.scores.unit_test2_question10 = unit_test2_question10[0]

            data.scores.unit2_1_solutionId = unit_test2_question1[1]
            data.scores.unit2_1_answerId =unit_test2_question1[2]
            data.scores.unit2_2_solutionId = unit_test2_question2[1]
            data.scores.unit2_2_answerId =unit_test2_question2[2]
            data.scores.unit2_3_solutionId = unit_test2_question3[1]
            data.scores.unit2_3_answerId =unit_test2_question3[2]
            data.scores.unit2_4_solutionId = unit_test2_question4[1]
            data.scores.unit2_4_answerId =unit_test2_question4[2]
            data.scores.unit2_5_solutionId = unit_test2_question5[1]
            data.scores.unit2_5_answerId =unit_test2_question5[2]
            data.scores.unit2_6_solutionId = unit_test2_question6[1]
            data.scores.unit2_6_answerId =unit_test2_question6[2]
            data.scores.unit2_7_solutionId = unit_test2_question7[1]
            data.scores.unit2_7_answerId =unit_test2_question7[2]
            data.scores.unit2_8_solutionId = unit_test2_question8[1]
            data.scores.unit2_8_answerId =unit_test2_question8[2]
            data.scores.unit2_9_solutionId = unit_test2_question9[1]
            data.scores.unit2_9_answerId =unit_test2_question9[2]
            data.scores.unit2_10_solutionId = unit_test2_question10[1]
            data.scores.unit2_10_answerId =unit_test2_question10[2]

        self.unitTest2_Q1_label.setText("1."+ data.scores.unit_test2_question1)
        self.unitTest2_Q2_label.setText("2."+ data.scores.unit_test2_question2)
        self.unitTest2_Q3_label.setText("3."+ data.scores.unit_test2_question3)
        self.unitTest2_Q4_label.setText("4."+ data.scores.unit_test2_question4)
        self.unitTest2_Q5_label.setText("5."+ data.scores.unit_test2_question5)
        self.unitTest2_Q6_label.setText("6."+ data.scores.unit_test2_question6)
        self.unitTest2_Q7_label.setText("7."+ data.scores.unit_test2_question7)
        self.unitTest2_Q8_label.setText("8."+ data.scores.unit_test2_question8)
        self.unitTest2_Q9_label.setText("9."+ data.scores.unit_test2_question9)
        self.unitTest2_Q10_label.setText("10."+ data.scores.unit_test2_question10)

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
            self.unitTest2Submit_container.setCurrentIndex(1)
            self.show_scoreUnit2_label.setText(str(data.scores.unit2_score))

            self.unitTest2Q1Sol_textEdit.setText(data.scores.unit_test2_saved_solution1)
            self.unitTest2Q1_textEdit.setText(data.scores.unit_test2_saved_answer1)
            self.unitTest2Q2Sol_textEdit.setText(data.scores.unit_test2_saved_solution2)
            self.unitTest2Q2_textEdit.setText(data.scores.unit_test2_saved_answer2)
            self.unitTest2Q3Sol_textEdit.setText(data.scores.unit_test2_saved_solution3)
            self.unitTest2Q3_textEdit.setText(data.scores.unit_test2_saved_answer3)
            self.unitTest2Q4Sol_textEdit.setText(data.scores.unit_test2_saved_solution4)
            self.unitTest2Q4_textEdit.setText(data.scores.unit_test2_saved_answer4)
            self.unitTest2Q5Sol_textEdit.setText(data.scores.unit_test2_saved_solution5)
            self.unitTest2Q5_textEdit.setText(data.scores.unit_test2_saved_answer5)
            self.unitTest2Q6Sol_textEdit.setText(data.scores.unit_test2_saved_solution6)
            self.unitTest2Q6_textEdit.setText(data.scores.unit_test2_saved_answer6)
            self.unitTest2Q7Sol_textEdit.setText(data.scores.unit_test2_saved_solution7)
            self.unitTest2Q7_textEdit.setText(data.scores.unit_test2_saved_answer7)
            self.unitTest2Q8Sol_textEdit.setText(data.scores.unit_test2_saved_solution8)
            self.unitTest2Q8_textEdit.setText(data.scores.unit_test2_saved_answer8)
            self.unitTest2Q9Sol_textEdit.setText(data.scores.unit_test2_saved_solution9)
            self.unitTest2Q9_textEdit.setText(data.scores.unit_test2_saved_answer9)
            self.unitTest2Q10Sol_textEdit.setText(data.scores.unit_test2_saved_solution10)
            self.unitTest2Q10_textEdit.setText(data.scores.unit_test2_saved_answer10)
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
        global fromLesson2, new_unitTest2
        fromLesson2 = 1
        new_unitTest2 = True
        self.back = toDashboard()
        self.back.show()

    def submitTest2(self):
        # Question 1 , answer and solution
        solution_Unit2_Q1 = self.unitTest2Q1Sol_textEdit.toPlainText()
        answer1_Unit2_Q1 = self.unitTest2Q1_textEdit.text()
        data.scores.unit_test2_saved_solution1 = solution_Unit2_Q1
        data.scores.unit_test2_saved_answer1 = answer1_Unit2_Q1
        # Question 2 , answer and solution
        solution_Unit2_Q2 = self.unitTest2Q2Sol_textEdit.toPlainText()
        answer1_Unit2_Q2 = self.unitTest2Q2_textEdit.text()
        data.scores.unit_test2_saved_solution2 = solution_Unit2_Q2
        data.scores.unit_test2_saved_answer2 = answer1_Unit2_Q2
        # Question 3 , answer and solution
        solution_Unit2_Q3 = self.unitTest2Q3Sol_textEdit.toPlainText()
        answer1_Unit2_Q3 = self.unitTest2Q3_textEdit.text()
        data.scores.unit_test2_saved_solution3 = solution_Unit2_Q3
        data.scores.unit_test2_saved_answer3 = answer1_Unit2_Q3
        # Question 4 , answer and solution
        solution_Unit2_Q4 = self.unitTest2Q4Sol_textEdit.toPlainText()
        answer1_Unit2_Q4 = self.unitTest2Q4_textEdit.text()
        data.scores.unit_test2_saved_solution4 = solution_Unit2_Q4
        data.scores.unit_test2_saved_answer4 = answer1_Unit2_Q4
        # Question 5 , answer and solution
        solution_Unit2_Q5 = self.unitTest2Q5Sol_textEdit.toPlainText()
        answer1_Unit2_Q5 = self.unitTest2Q5_textEdit.text()
        data.scores.unit_test2_saved_solution5 = solution_Unit2_Q5
        data.scores.unit_test2_saved_answer5 = answer1_Unit2_Q5
        # Question 6 , answer and solution
        solution_Unit2_Q6 = self.unitTest2Q6Sol_textEdit.toPlainText()
        answer1_Unit2_Q6 = self.unitTest2Q6_textEdit.text()
        data.scores.unit_test2_saved_solution6 = solution_Unit2_Q6
        data.scores.unit_test2_saved_answer6 = answer1_Unit2_Q6
        # Question 7 , answer and solution
        solution_Unit2_Q7 = self.unitTest2Q7Sol_textEdit.toPlainText()
        answer1_Unit2_Q7 = self.unitTest2Q7_textEdit.text()
        data.scores.unit_test2_saved_solution7 = solution_Unit2_Q7
        data.scores.unit_test2_saved_answer7 = answer1_Unit2_Q7
        # Question 8 , answer and solution
        solution_Unit2_Q8 = self.unitTest2Q8Sol_textEdit.toPlainText()
        answer1_Unit2_Q8 = self.unitTest2Q8_textEdit.text()
        data.scores.unit_test2_saved_solution8 = solution_Unit2_Q8
        data.scores.unit_test2_saved_answer8 = answer1_Unit2_Q8
        # Question 9 , answer and solution
        solution_Unit2_Q9 = self.unitTest2Q9Sol_textEdit.toPlainText()
        answer1_Unit2_Q9 = self.unitTest2Q9_textEdit.text()
        data.scores.unit_test2_saved_solution9 = solution_Unit2_Q9
        data.scores.unit_test2_saved_answer9 = answer1_Unit2_Q9
        # Question 10 , answer and solution
        solution_Unit2_Q10 = self.unitTest2Q10Sol_textEdit.toPlainText()
        answer1_Unit2_Q10 = self.unitTest2Q10_textEdit.text()
        data.scores.unit_test2_saved_solution10 = solution_Unit2_Q10
        data.scores.unit_test2_saved_answer10 = answer1_Unit2_Q10

        # Checking of answer and calculating of score
        data.scores.unit2_score = 0
        data.scores.substi_score = 0
        data.scores.elimin_score = 0

        # Question 1, solution and answer
        question = data.scores.unit2_1_solutionId
        check_unit2_q1_sol = chat(question, solution_Unit2_Q1)
        data.scores.check_unit2_q1_sol = check_unit2_q1_sol
        question = data.scores.unit2_1_answerId
        check_unit2_q1_ans = chat(question, answer1_Unit2_Q1)
        data.scores.check_unit2_q1_ans = check_unit2_q1_ans

        if check_unit2_q1_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q1_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1

        # Question 2, solution and answer
        question = data.scores.unit2_2_solutionId
        check_unit2_q2_sol = chat(question, solution_Unit2_Q2)
        data.scores.check_unit2_q2_sol = check_unit2_q2_sol
        question = data.scores.unit2_2_answerId
        check_unit2_q2_ans = chat(question, answer1_Unit2_Q2)
        data.scores.check_unit2_q2_ans = check_unit2_q2_ans

        if check_unit2_q2_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q2_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1  

        # Question 3, solution and answer
        question = data.scores.unit2_3_solutionId
        check_unit2_q3_sol = chat(question, solution_Unit2_Q3)
        data.scores.check_unit2_q3_sol = check_unit2_q3_sol
        question = data.scores.unit2_3_answerId
        check_unit2_q3_ans = chat(question, answer1_Unit2_Q3)
        data.scores.check_unit2_q3_ans = check_unit2_q3_ans

        if check_unit2_q3_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q3_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1  

        # Question 4, solution and answer
        question = data.scores.unit2_4_solutionId
        check_unit2_q4_sol = chat(question, solution_Unit2_Q4)
        data.scores.check_unit2_q4_sol = check_unit2_q4_sol
        question = data.scores.unit2_4_answerId
        check_unit2_q4_ans = chat(question, answer1_Unit2_Q4)
        data.scores.check_unit2_q4_ans = check_unit2_q4_ans

        if check_unit2_q4_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q4_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1  

        # Question 5, solution and answer
        question = data.scores.unit2_5_solutionId
        check_unit2_q5_sol = chat(question, solution_Unit2_Q5)
        data.scores.check_unit2_q5_sol = check_unit2_q5_sol
        question = data.scores.unit2_5_answerId
        check_unit2_q5_ans = chat(question, answer1_Unit2_Q5)
        data.scores.check_unit2_q5_ans = check_unit2_q5_ans

        if check_unit2_q5_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.substi_score = data.scores.substi_score + 4
        if check_unit2_q5_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.substi_score = data.scores.substi_score + 1 

        # Question 6, solution and answer
        question = data.scores.unit2_6_solutionId
        check_unit2_q6_sol = chat(question, solution_Unit2_Q6)
        data.scores.check_unit2_q6_sol = check_unit2_q6_sol
        question = data.scores.unit2_6_answerId
        check_unit2_q6_ans = chat(question, answer1_Unit2_Q6)
        data.scores.check_unit2_q6_ans = check_unit2_q6_ans

        if check_unit2_q6_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q6_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 7, solution and answer
        question = data.scores.unit2_7_solutionId
        check_unit2_q7_sol = chat(question, solution_Unit2_Q7)
        data.scores.check_unit2_q7_sol = check_unit2_q7_sol
        question = data.scores.unit2_7_answerId
        check_unit2_q7_ans = chat(question, answer1_Unit2_Q7)
        data.scores.check_unit2_q7_ans = check_unit2_q7_ans

        if check_unit2_q7_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q7_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 8, solution and answer
        question = data.scores.unit2_8_solutionId
        check_unit2_q8_sol = chat(question, solution_Unit2_Q8)
        data.scores.check_unit2_q8_sol = check_unit2_q8_sol
        question = data.scores.unit2_8_answerId
        check_unit2_q8_ans = chat(question, answer1_Unit2_Q8)
        data.scores.check_unit2_q8_ans = check_unit2_q8_ans

        if check_unit2_q8_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q8_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 9, solution and answer
        question = data.scores.unit2_9_solutionId
        check_unit2_q9_sol = chat(question, solution_Unit2_Q9)
        data.scores.check_unit2_q9_sol = check_unit2_q9_sol
        question = data.scores.unit2_9_answerId
        check_unit2_q9_ans = chat(question, answer1_Unit2_Q9)
        data.scores.check_unit2_q9_ans = check_unit2_q9_ans

        if check_unit2_q9_sol == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 4 
            data.scores.elimin_score = data.scores.elimin_score + 4
        if check_unit2_q9_ans == "correct":
            data.scores.unit2_score = data.scores.unit2_score + 1 
            data.scores.elimin_score = data.scores.elimin_score + 1  

        # Question 10, solution and answer
        question = data.scores.unit2_10_solutionId
        check_unit2_q10_sol = chat(question, solution_Unit2_Q10)
        data.scores.check_unit2_q10_sol = check_unit2_q10_sol
        question = data.scores.unit2_10_answerId
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
        new_unitTest2 = False

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

        if new_postAssess == True:
            post_assess_all = []
            post_assess_each_quest1 = []
            post_assess_each_quest2 = []
            post_assess_each_quest3 = []
            post_assess_each_quest4 = []
            post_assess_each_quest5 = []
            post_assess_each_quest6 = []

            circle_ans1, circle_solu1,  returned_circle1 = display_random_question.post_assess_circle()
            parabola_ans1, parabola_solu1, returned_parabola1 = display_random_question.post_assess_parabola()
            ellipse_ans1, ellipse_solu1, returned_ellipse1 = display_random_question.post_assess_ellipse()
            hyperbola_ans1, hyperbola_solu1, returned_hyperbola1 = display_random_question.post_assess_hyper()
            substitution_ans1, substitution_solu1, returned_substitution1 = display_random_question.post_assess_subs()
            elimination_ans1, elimination_solu1, returned_elimination1 = display_random_question.post_assess_elim()

            post_assess_each_quest1.append(returned_circle1[0])
            post_assess_each_quest1.append(returned_circle1[1])
            post_assess_each_quest1.append(returned_circle1[2])

            post_assess_each_quest2.append(returned_parabola1[0])
            post_assess_each_quest2.append(returned_parabola1[1])
            post_assess_each_quest2.append(returned_parabola1[2])

            post_assess_each_quest3.append(returned_ellipse1[0])
            post_assess_each_quest3.append(returned_ellipse1[1])
            post_assess_each_quest3.append(returned_ellipse1[2])

            post_assess_each_quest4.append(returned_hyperbola1[0])
            post_assess_each_quest4.append(returned_hyperbola1[1])
            post_assess_each_quest4.append(returned_hyperbola1[2])

            post_assess_each_quest5.append(returned_substitution1[0])
            post_assess_each_quest5.append(returned_substitution1[1])
            post_assess_each_quest5.append(returned_substitution1[2])

            post_assess_each_quest6.append(returned_elimination1[0])
            post_assess_each_quest6.append(returned_elimination1[1])
            post_assess_each_quest6.append(returned_elimination1[2])

            post_assess_all.append(post_assess_each_quest1)
            post_assess_all.append(post_assess_each_quest2)
            post_assess_all.append(post_assess_each_quest3)
            post_assess_all.append(post_assess_each_quest4)
            post_assess_all.append(post_assess_each_quest5)
            post_assess_all.append(post_assess_each_quest6)

            post_question1, post_question2, post_question3, post_question4, post_question5= display_random_question.random_questions(post_assess_all)

            data.scores.post_question1 = post_question1[0]
            data.scores.post_question2 = post_question2[0]
            data.scores.post_question3 = post_question3[0]
            data.scores.post_question4 = post_question4[0]
            data.scores.post_question5 = post_question5[0]

            data.scores.post1_solutionId = post_question1[1]
            data.scores.post1_answerId = post_question1[2]
            data.scores.post2_solutionId = post_question2[1]
            data.scores.post2_answerId = post_question2[2]
            data.scores.post3_solutionId = post_question3[1]
            data.scores.post3_answerId = post_question3[2]
            data.scores.post4_solutionId = post_question4[1]
            data.scores.post4_answerId = post_question4[2]
            data.scores.post5_solutionId = post_question5[1]
            data.scores.post5_answerId = post_question5[2]

        self.post_Q1_label.setText("1."+ data.scores.post_question1)
        self.post_Q2_label.setText("2."+ data.scores.post_question2)
        self.post_Q3_label.setText("3."+ data.scores.post_question3)
        self.post_Q4_label.setText("4."+ data.scores.post_question4)
        self.post_Q5_label.setText("5."+ data.scores.post_question5)

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
        global fromLesson2, new_postAssess
        fromLesson2 = 1
        new_postAssess = True
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
        question = data.scores.post1_solutionId
        check_assess_q1_sol = chat(question, postassess_sol_Q1)
        question = data.scores.post1_answerId
        check_assess_q1_ans = chat(question, postassess_ans_Q1)
                
        if check_assess_q1_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q1_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 2, solution and answer
        question = data.scores.post2_solutionId
        check_assess_q2_sol = chat(question, postassess_sol_Q2)
        question = data.scores.post2_answerId
        check_assess_q2_ans = chat(question, postassess_ans_Q2)

        if check_assess_q2_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q2_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 3, solution and answer
        question = data.scores.post3_solutionId
        check_assess_q3_sol = chat(question, postassess_sol_Q3)
        question = data.scores.post3_answerId
        check_assess_q3_ans = chat(question, postassess_ans_Q3)

        if check_assess_q3_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q3_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 4, solution and answer
        question = data.scores.post4_solutionId
        check_assess_q4_sol = chat(question, postassess_sol_Q4)
        question = data.scores.post4_answerId
        check_assess_q4_ans = chat(question, postassess_ans_Q4)

        if check_assess_q4_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q4_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1

        # Question 5, solution and answer
        question = data.scores.post5_solutionId
        check_assess_q5_sol = chat(question, postassess_sol_Q5)
        question = data.scores.post5_answerId
        check_assess_q5_ans = chat(question, postassess_ans_Q5)

        if check_assess_q5_sol == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 4
        if check_assess_q5_ans == "correct":
            data.scores.postassess_score =  data.scores.postassess_score + 1
        
        print(data.scores.postassess_score)
        if post_count == "0":
            studKey = db.child("student").get()
            for keyAccess in studKey.each():
                if keyAccess.val()["studentSchoolID"] == idKey:
                    keyID = keyAccess.key()
            db.child("student").child(keyID).update({"post_assessment_score":str(data.scores.postassess_score),"post_assessment_count":"1"})
        if post_count == "1":
            studKey = db.child("student").get()
            for keyAccess in studKey.each():
                if keyAccess.val()["studentSchoolID"] == idKey:
                    keyID = keyAccess.key()
            db.child("student").child(keyID).update({"post_assessment_score1":str(data.scores.postassess_score),"post_assessment_count":"0"})

        global new_postAssess
        new_postAssess = False

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
        global fromLesson2
        fromLesson2 = 1
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
                teachFname = (teacher.val()["fname"])
                teachMname = (teacher.val()["mname"])
                teachLname = (teacher.val()["lname"])
                teachCourse = (teacher.val()["course"])
                teachSchool = (teacher.val()["school"])
        self.profNameLineEdit.insertPlainText(teachLname.upper())
        self.profNameLineEdit.insertPlainText(", ")
        self.profNameLineEdit.insertPlainText(teachFname.upper())
        self.profNameLineEdit.insertPlainText(" ")
        self.profNameLineEdit.insertPlainText(teachMname.upper())
        self.profCourseLineEdit.insertPlainText(teachCourse.upper())
        self.profSchoolLineEdit.insertPlainText(teachSchool.upper())
        
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

        global fromQuestion
        if fromQuestion == 1:
            self.showProgress()
            fromQuestion = 0

        self.leftMenuNum = 0
        self.centerMenuNum = 0
        self.rightMenuNum = 0
        self.infoMenuNum = 0
        self.popMenuNum = 0
        self.restoreWindow = 0
        self.maxWindow = False
        self.willLogout = True
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

        self.unit1_create_pushButton.clicked.connect(self.create_unit1)
        self.unit2_create_pushButton.clicked.connect(self.create_unit2)
        self.pre_create_pushButton.clicked.connect(self.create_pre)
        self.post_create_pushButton.clicked.connect(self.create_post)

        self.unit1_update_pushButton.clicked.connect(self.update_unit1)
        self.unit2_update_pushButton.clicked.connect(self.update_unit2)
        self.pre_update_pushButton.clicked.connect(self.update_pre)
        self.post_update_pushButton.clicked.connect(self.update_post)

        self.unit1_delete_pushButton.clicked.connect(self.delete_unit1)
        self.unit2_delete_pushButton.clicked.connect(self.delete_unit2)
        self.pre_delete_pushButton.clicked.connect(self.delete_pre)
        self.post_delete_pushButton.clicked.connect(self.delete_post)

        QSizeGrip(self.sizeGrip)        

    def create_unit1(self):
        if willLogout == 0:
            self.hide()
            self.createUnit1 = create_unit1Question()
            self.createUnit1.show()
        else:
            pass
    def create_unit2(self):
        if willLogout == 0:
            self.hide()
            self.createUnit1 = create_unit2Question()
            self.createUnit1.show()
        else:
            pass
    def create_pre(self):
        if willLogout == 0:
            self.hide()
            self.createUnit1 = create_preQuestion()
            self.createUnit1.show()
        else:
            pass
    def create_post(self):
        if willLogout == 0:
            self.hide()
            self.createUnit1 = create_postQuestion()
            self.createUnit1.show()
        else:
            pass
    def update_unit1(self):
        if willLogout == 0:
            self.updateUnit1 = update_unit1Question(self)
            self.updateUnit1.show()
        else:
            pass
    def update_unit2(self):
        if willLogout == 0:
            self.updateUnit2 = update_unit2Question(self)
            self.updateUnit2.show()
            
    def update_pre(self):
        if willLogout == 0:
            self.updatePre = update_preQuestion(self)
            self.updatePre.show()
    def update_post(self):
        if willLogout == 0:
            self.updatePre = update_postQuestion(self)
            self.updatePre.show()   
    def delete_unit1(self):
        if willLogout == 0:
            self.deleteUnit1 = delete_unit1Question(self)
            self.deleteUnit1.show()
        else:
            pass

    def delete_unit2(self):
        if willLogout == 0:
            self.deleteUnit2 = delete_unit2Question(self)
            self.deleteUnit2.show()
        else:
            pass
    def delete_pre(self):
            if willLogout == 0:
                self.deletePre = delete_preQuestion(self)
                self.deletePre.show()
            else:
                pass
    def delete_post(self):
            if willLogout == 0:
                self.deletePre = delete_postQuestion(self)
                self.deletePre.show()
            else:
                pass
    def loadData(self):
        row = 0
        rowCount = 0
        student_A = 0
        student_B = 0
        student_C = 0
        student_D = 0
        student_E = 0
        student_total = 0
        preAssess_less10 = 0
        preAssess_less20 = 0
        preAssess_less30 = 0
        preAssess_total = 0
        postAssess_less10 = 0
        postAssess_less20 = 0
        postAssess_less30 = 0
        postAssess_total = 0
        unit1_less10 = 0
        unit1_less20 = 0
        unit1_less30 = 0
        unit1_less40 = 0
        unit1_less50 = 0
        unit1_less60 = 0
        unit1_total = 0
        unit2_less10 = 0
        unit2_less20 = 0
        unit2_less30 = 0
        unit2_less40 = 0
        unit2_less50 = 0
        unit2_less60 = 0
        unit2_total = 0
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
                self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(student.val()["unitTest1_score"]).upper()))
                self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(student.val()["unitTest2_score"]).upper()))
                self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(student.val()["assessment_score"]).upper()))
                self.tableWidget.setItem(row, 10, QtWidgets.QTableWidgetItem(str(student.val()["post_assessment_score"]).upper()))    
                row = row + 1 
                if student.val()["section"] == "A":
                    student_A = student_A + 1
                    student_total = student_total + 1
                if student.val()["section"] == "B":
                    student_B = student_B + 1
                    student_total = student_total + 1
                if student.val()["section"] == "C":
                    student_C = student_C + 1
                    student_total = student_total + 1
                if student.val()["section"] == "D":
                    student_D = student_D + 1
                    student_total = student_total + 1
                if student.val()["section"] == "E":
                    student_E = student_E + 1  
                    student_total = student_total + 1

                if int(student.val()["unitTest1_score"]) <= 10:
                    unit1_less10 = unit1_less10 + 1
                elif int(student.val()["unitTest1_score"]) <= 20:
                    unit1_less20 = unit1_less20 + 1
                elif int(student.val()["unitTest1_score"]) <= 30:
                    unit1_less30 = unit1_less30 + 1
                elif int(student.val()["unitTest1_score"]) <= 40:
                    unit1_less40 = unit1_less40 + 1
                elif int(student.val()["unitTest1_score"]) <= 50:
                    unit1_less50 = unit1_less50 + 1
                elif int(student.val()["unitTest1_score"]) <= 60:
                    unit1_less60 = unit1_less60 + 1
                
                if int(student.val()["unitTest2_score"]) <= 10:
                    unit2_less10 = unit2_less10 + 1
                elif int(student.val()["unitTest2_score"]) <= 20:
                    unit2_less20 = unit2_less20 + 1
                elif int(student.val()["unitTest2_score"]) <= 30:
                    unit2_less30 = unit2_less30 + 1
                elif int(student.val()["unitTest2_score"]) <= 40:
                    unit2_less40 = unit2_less40 + 1
                elif int(student.val()["unitTest2_score"]) <= 50:
                    unit2_less50 = unit2_less50 + 1
                elif int(student.val()["unitTest2_score"]) <= 60:
                    unit2_less60 = unit2_less60 + 1
                
                if int(student.val()["assessment_score"]) <= 10:
                    preAssess_less10 = preAssess_less10 + 1
                elif int(student.val()["assessment_score"]) <= 20:
                    preAssess_less20 = preAssess_less20 + 1
                elif int(student.val()["assessment_score"]) <= 30:
                    preAssess_less30 = preAssess_less30 + 1
                
                if int(student.val()["post_assessment_score"]) <= 10:
                    postAssess_less10 = postAssess_less10 + 1
                elif int(student.val()["post_assessment_score"]) <= 20:
                    postAssess_less20 = postAssess_less20 + 1
                elif int(student.val()["post_assessment_score"]) <= 30:
                    postAssess_less30 = postAssess_less30 + 1

        self.label_45.setText(str(student_A))
        self.label_46.setText(str(student_B))
        self.label_47.setText(str(student_C))
        self.label_48.setText(str(student_D))
        self.label_49.setText(str(student_E))
        self.label_50.setText(str(student_total))

        self.label_56.setText(str(preAssess_less10))
        self.label_55.setText(str(preAssess_less20))
        self.label_54.setText(str(preAssess_less30))
        self.label_72.setText(str(preAssess_total))

        self.label_64.setText(str(unit1_less10))
        self.label_65.setText(str(unit1_less20))
        self.label_66.setText(str(unit1_less30))
        self.label_67.setText(str(unit1_less40))
        self.label_68.setText(str(unit1_less50))
        self.label_69.setText(str(unit1_less60))
        self.label_76.setText(str(unit1_total))

        self.label_85.setText(str(unit2_less10))
        self.label_86.setText(str(unit2_less20))
        self.label_87.setText(str(unit2_less30))
        self.label_88.setText(str(unit2_less40))
        self.label_89.setText(str(unit2_less50))
        self.label_90.setText(str(unit2_less60))
        self.label_91.setText(str(unit2_total))

        self.label_96.setText(str(postAssess_less10))
        self.label_97.setText(str(postAssess_less20))
        self.label_98.setText(str(postAssess_less30))
        self.label_100.setText(str(postAssess_total))

        series = QtChart.QPieSeries()
        series.append('A', student_A)
        series.append('B', student_B)
        series.append('C', student_C)
        series.append('D', student_D)
        series.append('E', student_E)

        sliceA = series.slices()[0]
        sliceA.setBrush(QtGui.QColor("#ff0000"))
        sliceB = series.slices()[1]
        sliceB.setBrush(QtGui.QColor("#0000ff"))
        sliceC = series.slices()[2]
        sliceC.setBrush(QtGui.QColor("#b6b600"))
        sliceD = series.slices()[3]
        sliceD.setBrush(QtGui.QColor("#00aa00"))
        sliceE = series.slices()[4]
        sliceE.setBrush(QtGui.QColor("#f44d00"))

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()

        chartview = QtChart.QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.charts_widget.setContentsMargins(0, 0, 0, 0)
        lay = QtWidgets.QHBoxLayout(self.charts_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(chartview)

        series1 = QtChart.QPieSeries()
        series1.append('< 10', unit1_less10)
        series1.append('< 20', unit1_less20)
        series1.append('< 30', unit1_less30)
        series1.append('< 40', unit1_less40)
        series1.append('< 50', unit1_less50)
        series1.append('< 60', unit1_less60)

        sliceUnit1_1 = series1.slices()[0]
        sliceUnit1_1.setBrush(QtGui.QColor("#ff0000"))
        sliceUnit1_2 = series1.slices()[1]
        sliceUnit1_2.setBrush(QtGui.QColor("#0000ff"))
        sliceUnit1_3 = series1.slices()[2]
        sliceUnit1_3.setBrush(QtGui.QColor("#b6b600"))
        sliceUnit1_4 = series1.slices()[3]
        sliceUnit1_4.setBrush(QtGui.QColor("#00aa00"))
        sliceUnit1_5 = series1.slices()[4]
        sliceUnit1_5.setBrush(QtGui.QColor("#f44d00"))
        sliceUnit1_6 = series1.slices()[5]
        sliceUnit1_6.setBrush(QtGui.QColor("#aa00ff"))

        chart1 = QtChart.QChart()
        chart1.addSeries(series1)
        chart1.setAnimationOptions(QChart.SeriesAnimations)
        chart1.legend().hide()

        chartview1 = QtChart.QChartView(chart1)
        chartview1.setRenderHint(QPainter.Antialiasing)

        self.unit_test1_widget.setContentsMargins(0, 0, 0, 0)
        lay1 = QtWidgets.QHBoxLayout(self.unit_test1_widget)
        lay1.setContentsMargins(0, 0, 0, 0)
        lay1.addWidget(chartview1)

        series2 = QtChart.QPieSeries()
        series2.append('< 10', unit2_less10)
        series2.append('< 20', unit2_less20)
        series2.append('< 30', unit2_less30)
        series2.append('< 40', unit2_less40)
        series2.append('< 50', unit2_less50)
        series2.append('< 60', unit2_less60)

        sliceUnit2_1 = series2.slices()[0]
        sliceUnit2_1.setBrush(QtGui.QColor("#ff0000"))
        sliceUnit2_2 = series2.slices()[1]
        sliceUnit2_2.setBrush(QtGui.QColor("#0000ff"))
        sliceUnit2_3 = series2.slices()[2]
        sliceUnit2_3.setBrush(QtGui.QColor("#b6b600"))
        sliceUnit2_4 = series2.slices()[3]
        sliceUnit2_4.setBrush(QtGui.QColor("#00aa00"))
        sliceUnit2_5 = series2.slices()[4]
        sliceUnit2_5.setBrush(QtGui.QColor("#f44d00"))

        chart2 = QtChart.QChart()
        chart2.addSeries(series2)
        chart2.setAnimationOptions(QChart.SeriesAnimations)
        chart2.legend().hide()

        chartview2 = QtChart.QChartView(chart2)
        chartview2.setRenderHint(QPainter.Antialiasing)

        self.unit_test2_widget.setContentsMargins(0, 0, 0, 0)
        lay2 = QtWidgets.QHBoxLayout(self.unit_test2_widget)
        lay2.setContentsMargins(0, 0, 0, 0)
        lay2.addWidget(chartview2)

        series3 = QtChart.QPieSeries()
        series3.append('< 10', preAssess_less10)
        series3.append('< 20', preAssess_less20)
        series3.append('< 30', preAssess_less30)

        slicePreAssess_1 = series3.slices()[0]
        slicePreAssess_1.setBrush(QtGui.QColor("#ff0000"))
        slicePreAssess_2 = series3.slices()[1]
        slicePreAssess_2.setBrush(QtGui.QColor("#0000ff"))
        slicePreAssess_3 = series3.slices()[2]
        slicePreAssess_3.setBrush(QtGui.QColor("#b6b600"))

        chart3 = QtChart.QChart()
        chart3.addSeries(series3)
        chart3.setAnimationOptions(QChart.SeriesAnimations)
        chart3.legend().hide()

        chartview3 = QtChart.QChartView(chart3)
        chartview3.setRenderHint(QPainter.Antialiasing)

        self.pre_assess_widget.setContentsMargins(0, 0, 0, 0)
        lay3 = QtWidgets.QHBoxLayout(self.pre_assess_widget)
        lay3.setContentsMargins(0, 0, 0, 0)
        lay3.addWidget(chartview3)

        series4 = QtChart.QPieSeries()
        series4.append('< 10', postAssess_less10)
        series4.append('< 20', postAssess_less20)
        series4.append('< 30', postAssess_less30)

        slicePostAssess_1 = series4.slices()[0]
        slicePostAssess_1.setBrush(QtGui.QColor("#ff0000"))
        slicePostAssess_2 = series4.slices()[1]
        slicePostAssess_2.setBrush(QtGui.QColor("#0000ff"))
        slicePostAssess_3 = series4.slices()[2]
        slicePostAssess_3.setBrush(QtGui.QColor("#b6b600"))

        chart4 = QtChart.QChart()
        chart4.addSeries(series4)
        chart4.setAnimationOptions(QChart.SeriesAnimations)
        chart4.legend().hide()

        chartview4 = QtChart.QChartView(chart4)
        chartview4.setRenderHint(QPainter.Antialiasing)

        self.post_assess_widget.setContentsMargins(0, 0, 0, 0)
        lay4 = QtWidgets.QHBoxLayout(self.post_assess_widget)
        lay4.setContentsMargins(0, 0, 0, 0)
        lay4.addWidget(chartview4)

    def loadUnitTest1(self):
        row = 0
        rowCount = 0
        all_unitTest1_circle = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
        all_unitTest1_parabola = db.child("precal_questions").child("lesson1").child("parabolaQuestion").get()
        all_unitTest1_ellipse = db.child("precal_questions").child("lesson1").child("ellipseQuestion").get()
        all_unitTest1_hyperbola = db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").get()

        for student in all_unitTest1_circle.each():
            rowCount = rowCount + 1
        for student in all_unitTest1_parabola.each():
            rowCount = rowCount + 1
        for student in all_unitTest1_ellipse.each():
            rowCount = rowCount + 1
        for student in all_unitTest1_hyperbola.each():
            rowCount = rowCount + 1
        
        self.tableWidget_2.setRowCount(rowCount)

        for circle in all_unitTest1_circle.each():
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(circle.val()["questionId"])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(circle.val()["circle_1_question"])))
                row = row + 1 
        for parabola in all_unitTest1_parabola.each():
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(parabola.val()["questionId"])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(parabola.val()["parabola_question"])))
                row = row + 1
        for ellipse in all_unitTest1_ellipse.each():
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(ellipse.val()["questionId"])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(ellipse.val()["ellipse_question"])))
                row = row + 1
        for hyperbola in all_unitTest1_hyperbola.each():
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(hyperbola.val()["questionId"])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(hyperbola.val()["hyperbola_question"])))
                row = row + 1
    
    def loadUnitTest2(self):
        row = 0
        rowCount = 0
        all_unitTest2_substitution = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()
        all_unitTest2_elimination = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()
        
        for student in all_unitTest2_substitution.each():
            rowCount = rowCount + 1
        for student in all_unitTest2_elimination.each():
            rowCount = rowCount + 1
        
        self.tableWidget_3.setRowCount(rowCount)

        for substitution in all_unitTest2_substitution.each():
                self.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(substitution.val()["questionId"])))
                self.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(str(substitution.val()["substitution_question"])))
                row = row + 1 
        for elimination in all_unitTest2_elimination.each():
                self.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(elimination.val()["questionId"])))
                self.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(str(elimination.val()["elimination_question"])))
                row = row + 1

    def loadPreAssess(self):
        row = 0
        rowCount = 0
        all_preAssess_circle = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()
        all_preAssess_parabola = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()
        all_preAssess_ellipse = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()
        all_preAssess_hyperbola = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()
        all_preAssess_substitution = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()
        all_preAssess_elimination = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()
        
        for student in all_preAssess_circle.each():
            rowCount = rowCount + 1
        for student in all_preAssess_parabola.each():
            rowCount = rowCount + 1
        for student in all_preAssess_ellipse.each():
            rowCount = rowCount + 1
        for student in all_preAssess_hyperbola.each():
            rowCount = rowCount + 1
        for student in all_preAssess_substitution.each():
            rowCount = rowCount + 1
        for student in all_preAssess_elimination.each():
            rowCount = rowCount + 1

        self.tableWidget_4.setRowCount(rowCount)

        for circle in all_preAssess_circle.each():
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(circle.val()["questionId"])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(circle.val()["circle_1_question"])))
                row = row + 1 
        for parabola in all_preAssess_parabola.each():
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(parabola.val()["questionId"])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(parabola.val()["parabola_question"])))
                row = row + 1
        for ellipse in all_preAssess_ellipse.each():
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(ellipse.val()["questionId"])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(ellipse.val()["ellipse_question"])))
                row = row + 1
        for hyperbola in all_preAssess_hyperbola.each():
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(hyperbola.val()["questionId"])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(hyperbola.val()["hyperbola_question"])))
                row = row + 1
        for substitution in all_preAssess_substitution.each():
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(substitution.val()["questionId"])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(substitution.val()["substitution_question"])))
                row = row + 1 
        for elimination in all_preAssess_elimination.each():
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(elimination.val()["questionId"])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(elimination.val()["elimination_question"])))
                row = row + 1

    def loadPostAssess(self):
        row = 0
        rowCount = 0
        all_postAssess_circle = db.child("precal_questions").child("post-assess").child("circleQuestion").get()
        all_postAssess_parabola = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()
        all_postAssess_ellipse = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()
        all_postAssess_hyperbola = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()
        all_postAssess_substitution = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()
        all_postAssess_elimination = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()
        
        for student in all_postAssess_circle.each():
            rowCount = rowCount + 1
        for student in all_postAssess_parabola.each():
            rowCount = rowCount + 1
        for student in all_postAssess_ellipse.each():
            rowCount = rowCount + 1
        for student in all_postAssess_hyperbola.each():
            rowCount = rowCount + 1
        for student in all_postAssess_substitution.each():
            rowCount = rowCount + 1
        for student in all_postAssess_elimination.each(): 
            rowCount = rowCount + 1

        self.tableWidget_5.setRowCount(rowCount)

        for circle in all_postAssess_circle.each():
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(circle.val()["questionId"])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(circle.val()["circle_1_question"])))
                row = row + 1 
        for parabola in all_postAssess_parabola.each():
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(parabola.val()["questionId"])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(parabola.val()["parabola_question"])))
                row = row + 1
        for ellipse in all_postAssess_ellipse.each():
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(ellipse.val()["questionId"])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(ellipse.val()["ellipse_question"])))
                row = row + 1
        for hyperbola in all_postAssess_hyperbola.each():
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(hyperbola.val()["questionId"])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(hyperbola.val()["hyperbola_question"])))
                row = row + 1
        for substitution in all_postAssess_substitution.each():
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(substitution.val()["questionId"])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(substitution.val()["substitution_question"])))
                row = row + 1 
        for elimination in all_postAssess_elimination.each():
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(elimination.val()["questionId"])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(elimination.val()["elimination_question"])))
                row = row + 1

        # PROFILE BUTTON FUNCTIONS
    def updateProfile(self):
        if willLogout == 0:
            self.hide()
            self.toUpdateProf = toTeachUpdateProfile()
            self.toUpdateProf.show()
        else:
            pass
    def logoutProfile(self):
        if willLogout == 0:
            self.tologoutProf = toTeachLogout(self)
            self.tologoutProf.show()
        else:
            pass

    def hideWindow(self):
        if willLogout == 0:
            self.showMinimized()  
        else:
            pass
    def bigWindow(self):
        if willLogout == 0:
            if self.restoreWindow == 0:
                self.showMaximized()
                self.maxWindow = True
                self.restoreWindow = 1

            else:           
                self.showNormal()  
                self.maxWindow = False
                self.restoreWindow = 0
        else:
            pass

    def showProfile(self):
        if willLogout == 0:
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
        else:
            pass

    def showModule1(self):
        if willLogout == 0:
            self.moduleMenuPages.setCurrentIndex(0)
            self.lessonsContainer.setVisible(True)
        else:
            pass

    def showModule2(self):
        if willLogout == 0:
            self.moduleMenuPages.setCurrentIndex(1)
            self.lessonsContainer.setVisible(True)
        else:
            pass

    def showModule3(self):
        if willLogout == 0:
            self.moduleMenuPages.setCurrentIndex(2)
            self.lessonsContainer.setVisible(True)
        else:
            pass

    def showHome(self):
        if willLogout == 0:
            self.menuPages.setCurrentIndex(0)
        else:
            pass
    def showModules(self):
        if willLogout == 0:
            self.loadData()
            self.menuPages.setCurrentIndex(1)
        else:
            pass
    def showProgress(self):
        if willLogout == 0:
            self.loadUnitTest1()
            self.loadUnitTest2()
            self.loadPreAssess()
            self.loadPostAssess()
            self.menuPages.setCurrentIndex(2)
        else:
            pass
    
    def showInformation(self):
        if willLogout == 0:
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
        else:
            pass
        
    def showHelp(self):
        if willLogout == 0:
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
        else:
            pass

    def showLeftMenu(self):
        if willLogout == 0:
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
        else:
            pass

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
        if willLogout == 0:
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
        else:
            pass

    def hideRightMenu(self):
        if willLogout == 0:
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
        else:
            pass

class create_unit1Question(QMainWindow):
    def __init__(self):
        super(create_unit1Question, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(16)
        self.stackedWidget_5.setCurrentIndex(0)
        self.stackedWidget_6.setCurrentIndex(0)
        self.unitTest1_answerScore_widget.setVisible(False)
        self.unitTest1_solutionScore_widget.setVisible(False)

        self.unitTest1_questionId_error.setVisible(False)
        self.unitTest1_question_error.setVisible(False)
        self.unitTest1_solutionId_error.setVisible(False)
        self.unitTest1_solutionScore_error.setVisible(False)
        self.unitTest1_solution_error.setVisible(False)
        self.unitTest1_answerId_error.setVisible(False)
        self.unitTest1_answerScore_error.setVisible(False)
        self.unitTest1_answer_error.setVisible(False)
        self.unitTest_allError.setVisible(False)
        self.unitTest_allPass.setVisible(False)

        self.unitTest1Circle_Button.clicked.connect(self.questionCircle)
        self.unitTest1Parabola_Button.clicked.connect(self.questionParabola)
        self.unitTest1Ellipse_Button.clicked.connect(self.questionEllipse)
        self.unitTest1Hyperbola_Button.clicked.connect(self.questionHyperbola)

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
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def questionCircle(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.unitTest1_question_textEdit.toPlainText() 
        circle_1_answer1 = self.unitTest1_answer1_textEdit.text()
        circle_1_answer2 = self.unitTest1_answer2_textEdit.text()
        circle_1_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            data ={"questionId":questionId,"circle_1_question":circle_1_question,
        "circle_1_solution1": circle_1_solution1,"circle_1_solution2": circle_1_solution2,
        "circle_1_answer1":circle_1_answer1, "circle_1_answer2":circle_1_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("lesson1").child("circleQuestion").push(data)

    def questionParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.unitTest1_question_textEdit.toPlainText() 
        parabola_answer1 = self.unitTest1_answer1_textEdit.text()
        parabola_answer2 = self.unitTest1_answer2_textEdit.text()
        parabola_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        parabola_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            data ={"questionId":questionId,"parabola_question":parabola_question,
           "parabola_solution1": parabola_solution1,"parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,
           "parabola_answer2":parabola_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("lesson1").child("parabolaQuestion").push(data)

    def questionEllipse(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            ellipse_question = self.unitTest1_question_textEdit.toPlainText() 
            ellipse_answer1 = self.unitTest1_answer1_textEdit.text()
            ellipse_answer2 = self.unitTest1_answer2_textEdit.text()
            ellipse_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
            ellipse_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
            questionId = self.unitTest1_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.unitTest1_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.unitTest1_solutionId_textEdit.text()
            sol_num = "2"

            if ellipse_question == "":
                self.question_error = 1
                self.unitTest1_question_error.setVisible(True)
            if ellipse_answer1 == "" or ellipse_answer2 == "":
                self.answer_error = 1
                self.unitTest1_answer_error.setVisible(True)
            if ellipse_solution1 == "" or ellipse_solution2 == "":
                self.solution_error = 1
                self.unitTest1_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.unitTest1_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.unitTest1_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.unitTest1_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.unitTest_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.unitTest_allPass.setVisible(True)
                self.unitTest1_questionId_error.setVisible(False)
                self.unitTest1_question_error.setVisible(False)
                self.unitTest1_solutionId_error.setVisible(False)
                self.unitTest1_solutionScore_error.setVisible(False)
                self.unitTest1_solution_error.setVisible(False)
                self.unitTest1_answerId_error.setVisible(False)
                self.unitTest1_answerScore_error.setVisible(False)
                self.unitTest1_answer_error.setVisible(False)
                self.unitTest_allError.setVisible(False)

                self.unitTest1_question_textEdit.clear() 
                self.unitTest1_answer1_textEdit.clear()
                self.unitTest1_answer2_textEdit.clear()
                self.unitTest1_solution1_textEdit.clear()
                self.unitTest1_solution2_textEdit.clear()
                self.unitTest1_questionId_textEdit.clear() 
                self.unitTest1_answerId_textEdit.clear()
                self.unitTest1_solutionId_textEdit.clear()
                
                data ={"questionId":questionId,"ellipse_question":ellipse_question,
            "ellipse_solution1": ellipse_solution1,"ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,
            "ellipse_answer2":ellipse_answer2, "isActive":checkId, "answerId":answerId,
            "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("lesson1").child("ellipseQuestion").push(data)

    def questionHyperbola(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            hyperbola_question = self.unitTest1_question_textEdit.toPlainText() 
            hyperbola_answer1 = self.unitTest1_answer1_textEdit.text()
            hyperbola_answer2 = self.unitTest1_answer2_textEdit.text()
            hyperbola_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
            hyperbola_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
            questionId = self.unitTest1_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.unitTest1_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.unitTest1_solutionId_textEdit.text()
            sol_num = "2"

            if hyperbola_question == "":
                self.question_error = 1
                self.unitTest1_question_error.setVisible(True)
            if hyperbola_answer1 == "" or hyperbola_answer2 == "":
                self.answer_error = 1
                self.unitTest1_answer_error.setVisible(True)
            if hyperbola_solution1 == "" or hyperbola_solution2 == "":
                self.solution_error = 1
                self.unitTest1_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.unitTest1_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.unitTest1_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.unitTest1_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.unitTest_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.unitTest_allPass.setVisible(True)
                self.unitTest1_questionId_error.setVisible(False)
                self.unitTest1_question_error.setVisible(False)
                self.unitTest1_solutionId_error.setVisible(False)
                self.unitTest1_solutionScore_error.setVisible(False)
                self.unitTest1_solution_error.setVisible(False)
                self.unitTest1_answerId_error.setVisible(False)
                self.unitTest1_answerScore_error.setVisible(False)
                self.unitTest1_answer_error.setVisible(False)
                self.unitTest_allError.setVisible(False)

                self.unitTest1_question_textEdit.clear() 
                self.unitTest1_answer1_textEdit.clear()
                self.unitTest1_answer2_textEdit.clear()
                self.unitTest1_solution1_textEdit.clear()
                self.unitTest1_solution2_textEdit.clear()
                self.unitTest1_questionId_textEdit.clear() 
                self.unitTest1_answerId_textEdit.clear()
                self.unitTest1_solutionId_textEdit.clear()

                data ={"questionId":questionId,"hyperbola_question":hyperbola_question,
        "hyperbola_solution1": hyperbola_solution1,"hyperbola_solution2": hyperbola_solution2,
        "hyperbola_answer1":hyperbola_answer1, "hyperbola_answer2":hyperbola_answer2,
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
        "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").push(data)

class create_unit2Question(QMainWindow):
    def __init__(self):
        super(create_unit2Question, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(17)
        self.stackedWidget_7.setCurrentIndex(0)
        self.stackedWidget_8.setCurrentIndex(0)
        self.unitTest2_answerScore_widget.setVisible(False)
        self.unitTest2_solutionScore_widget.setVisible(False)

        self.unitTest2_questionId_error.setVisible(False)
        self.unitTest2_question_error.setVisible(False)
        self.unitTest2_solutionId_error.setVisible(False)
        self.unitTest2_solutionScore_error.setVisible(False)
        self.unitTest2_solution_error.setVisible(False)
        self.unitTest2_answerId_error.setVisible(False)
        self.unitTest2_answerScore_error.setVisible(False)
        self.unitTest2_answer_error.setVisible(False)
        self.unitTest2_allError.setVisible(False)
        self.unitTest2_allPass.setVisible(False)

        self.unitTest2Substitution_Button.clicked.connect(self.questionSubstitution)
        self.unitTest2Elimination_Button.clicked.connect(self.questionElimination)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def questionSubstitution(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        substitution_question = self.unitTest2_question_textEdit.toPlainText() 
        substitution_answer1 = self.unitTest2_answer1_textEdit.text()
        substitution_answer2 = self.unitTest2_answer2_textEdit.text()
        substitution_solution1 = self.unitTest2_solution1_textEdit.toPlainText()
        substitution_solution2 = self.unitTest2_solution2_textEdit.toPlainText()
        questionId = self.unitTest2_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest2_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest2_solutionId_textEdit.text()
        sol_num = "2"

        if substitution_question == "":
            self.question_error = 1
            self.unitTest2_question_error.setVisible(True)
        if substitution_answer1 == "" or substitution_answer2 == "":
            self.answer_error = 1
            self.unitTest2_answer_error.setVisible(True)
        if substitution_solution1 == "" or substitution_solution2 == "":
            self.solution_error = 1
            self.unitTest2_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest2_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest2_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest2_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest2_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest2_allPass.setVisible(True)
            self.unitTest2_questionId_error.setVisible(False)
            self.unitTest2_question_error.setVisible(False)
            self.unitTest2_solutionId_error.setVisible(False)
            self.unitTest2_solutionScore_error.setVisible(False)
            self.unitTest2_solution_error.setVisible(False)
            self.unitTest2_answerId_error.setVisible(False)
            self.unitTest2_answerScore_error.setVisible(False)
            self.unitTest2_answer_error.setVisible(False)
            self.unitTest2_allError.setVisible(False)

            self.unitTest2_question_textEdit.clear() 
            self.unitTest2_answer1_textEdit.clear()
            self.unitTest2_answer2_textEdit.clear()
            self.unitTest2_solution1_textEdit.clear()
            self.unitTest2_solution2_textEdit.clear()
            self.unitTest2_questionId_textEdit.clear() 
            self.unitTest2_answerId_textEdit.clear()
            self.unitTest2_solutionId_textEdit.clear()

            data ={"questionId":questionId,"substitution_question":substitution_question,
        "substitution_solution1": substitution_solution1,"substitution_solution2": substitution_solution2,
        "substitution_answer1":substitution_answer1, "substitution_answer2":substitution_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("lesson2").child("substitutionQuestion").push(data)

    def questionElimination(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        elimination_question = self.unitTest2_question_textEdit.toPlainText() 
        elimination_answer1 = self.unitTest2_answer1_textEdit.text()
        elimination_answer2 = self.unitTest2_answer2_textEdit.text()
        elimination_solution1 = self.unitTest2_solution1_textEdit.toPlainText()
        elimination_solution2 = self.unitTest2_solution2_textEdit.toPlainText()
        questionId = self.unitTest2_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest2_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest2_solutionId_textEdit.text()
        sol_num = "2"

        if elimination_question == "":
            self.question_error = 1
            self.unitTest2_question_error.setVisible(True)
        if elimination_answer1 == "" or elimination_answer2 == "":
            self.answer_error = 1
            self.unitTest2_answer_error.setVisible(True)
        if elimination_solution1 == "" or elimination_solution2 == "":
            self.solution_error = 1
            self.unitTest2_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest2_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest2_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest2_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest2_allError.setVisible(True)
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest2_allPass.setVisible(True)
            self.unitTest2_questionId_error.setVisible(False)
            self.unitTest2_question_error.setVisible(False)
            self.unitTest2_solutionId_error.setVisible(False)
            self.unitTest2_solutionScore_error.setVisible(False)
            self.unitTest2_solution_error.setVisible(False)
            self.unitTest2_answerId_error.setVisible(False)
            self.unitTest2_answerScore_error.setVisible(False)
            self.unitTest2_answer_error.setVisible(False)
            self.unitTest2_allError.setVisible(False)

            self.unitTest2_question_textEdit.clear() 
            self.unitTest2_answer1_textEdit.clear()
            self.unitTest2_answer2_textEdit.clear()
            self.unitTest2_solution1_textEdit.clear()
            self.unitTest2_solution2_textEdit.clear()
            self.unitTest2_questionId_textEdit.clear() 
            self.unitTest2_answerId_textEdit.clear()
            self.unitTest2_solutionId_textEdit.clear()

            data ={"questionId":questionId,"elimination_question":elimination_question,
           "elimination_solution1": elimination_solution1,"elimination_solution2": elimination_solution2,"elimination_answer1":elimination_answer1,
           "elimination_answer2":elimination_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("lesson2").child("eliminationQuestion").push(data)
class create_unit1Question(QMainWindow):
    def __init__(self):
        super(create_unit1Question, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(16)
        self.stackedWidget_5.setCurrentIndex(0)
        self.stackedWidget_6.setCurrentIndex(0)
        self.unitTest1_answerScore_widget.setVisible(False)
        self.unitTest1_solutionScore_widget.setVisible(False)

        self.unitTest1_questionId_error.setVisible(False)
        self.unitTest1_question_error.setVisible(False)
        self.unitTest1_solutionId_error.setVisible(False)
        self.unitTest1_solutionScore_error.setVisible(False)
        self.unitTest1_solution_error.setVisible(False)
        self.unitTest1_answerId_error.setVisible(False)
        self.unitTest1_answerScore_error.setVisible(False)
        self.unitTest1_answer_error.setVisible(False)
        self.unitTest_allError.setVisible(False)
        self.unitTest_allPass.setVisible(False)

        self.unitTest1Circle_Button.clicked.connect(self.questionCircle)
        self.unitTest1Parabola_Button.clicked.connect(self.questionParabola)
        self.unitTest1Ellipse_Button.clicked.connect(self.questionEllipse)
        self.unitTest1Hyperbola_Button.clicked.connect(self.questionHyperbola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def questionCircle(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.unitTest1_question_textEdit.toPlainText() 
        circle_1_answer1 = self.unitTest1_answer1_textEdit.text()
        circle_1_answer2 = self.unitTest1_answer2_textEdit.text()
        circle_1_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            data ={"questionId":questionId,"circle_1_question":circle_1_question,
        "circle_1_solution1": circle_1_solution1,"circle_1_solution2": circle_1_solution2,
        "circle_1_answer1":circle_1_answer1, "circle_1_answer2":circle_1_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("lesson1").child("circleQuestion").push(data)

    def questionParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.unitTest1_question_textEdit.toPlainText() 
        parabola_answer1 = self.unitTest1_answer1_textEdit.text()
        parabola_answer2 = self.unitTest1_answer2_textEdit.text()
        parabola_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        parabola_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            data ={"questionId":questionId,"parabola_question":parabola_question,
           "parabola_solution1": parabola_solution1,"parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,
           "parabola_answer2":parabola_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("lesson1").child("parabolaQuestion").push(data)

    def questionEllipse(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            ellipse_question = self.unitTest1_question_textEdit.toPlainText() 
            ellipse_answer1 = self.unitTest1_answer1_textEdit.text()
            ellipse_answer2 = self.unitTest1_answer2_textEdit.text()
            ellipse_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
            ellipse_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
            questionId = self.unitTest1_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.unitTest1_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.unitTest1_solutionId_textEdit.text()
            sol_num = "2"

            if ellipse_question == "":
                self.question_error = 1
                self.unitTest1_question_error.setVisible(True)
            if ellipse_answer1 == "" or ellipse_answer2 == "":
                self.answer_error = 1
                self.unitTest1_answer_error.setVisible(True)
            if ellipse_solution1 == "" or ellipse_solution2 == "":
                self.solution_error = 1
                self.unitTest1_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.unitTest1_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.unitTest1_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.unitTest1_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.unitTest_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.unitTest_allPass.setVisible(True)
                self.unitTest1_questionId_error.setVisible(False)
                self.unitTest1_question_error.setVisible(False)
                self.unitTest1_solutionId_error.setVisible(False)
                self.unitTest1_solutionScore_error.setVisible(False)
                self.unitTest1_solution_error.setVisible(False)
                self.unitTest1_answerId_error.setVisible(False)
                self.unitTest1_answerScore_error.setVisible(False)
                self.unitTest1_answer_error.setVisible(False)
                self.unitTest_allError.setVisible(False)

                self.unitTest1_question_textEdit.clear() 
                self.unitTest1_answer1_textEdit.clear()
                self.unitTest1_answer2_textEdit.clear()
                self.unitTest1_solution1_textEdit.clear()
                self.unitTest1_solution2_textEdit.clear()
                self.unitTest1_questionId_textEdit.clear() 
                self.unitTest1_answerId_textEdit.clear()
                self.unitTest1_solutionId_textEdit.clear()
                
                data ={"questionId":questionId,"ellipse_question":ellipse_question,
            "ellipse_solution1": ellipse_solution1,"ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,
            "ellipse_answer2":ellipse_answer2, "isActive":checkId, "answerId":answerId,
            "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("lesson1").child("ellipseQuestion").push(data)

    def questionHyperbola(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            hyperbola_question = self.unitTest1_question_textEdit.toPlainText() 
            hyperbola_answer1 = self.unitTest1_answer1_textEdit.text()
            hyperbola_answer2 = self.unitTest1_answer2_textEdit.text()
            hyperbola_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
            hyperbola_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
            questionId = self.unitTest1_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.unitTest1_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.unitTest1_solutionId_textEdit.text()
            sol_num = "2"

            if hyperbola_question == "":
                self.question_error = 1
                self.unitTest1_question_error.setVisible(True)
            if hyperbola_answer1 == "" or hyperbola_answer2 == "":
                self.answer_error = 1
                self.unitTest1_answer_error.setVisible(True)
            if hyperbola_solution1 == "" or hyperbola_solution2 == "":
                self.solution_error = 1
                self.unitTest1_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.unitTest1_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.unitTest1_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.unitTest1_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.unitTest_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.unitTest_allPass.setVisible(True)
                self.unitTest1_questionId_error.setVisible(False)
                self.unitTest1_question_error.setVisible(False)
                self.unitTest1_solutionId_error.setVisible(False)
                self.unitTest1_solutionScore_error.setVisible(False)
                self.unitTest1_solution_error.setVisible(False)
                self.unitTest1_answerId_error.setVisible(False)
                self.unitTest1_answerScore_error.setVisible(False)
                self.unitTest1_answer_error.setVisible(False)
                self.unitTest_allError.setVisible(False)

                self.unitTest1_question_textEdit.clear() 
                self.unitTest1_answer1_textEdit.clear()
                self.unitTest1_answer2_textEdit.clear()
                self.unitTest1_solution1_textEdit.clear()
                self.unitTest1_solution2_textEdit.clear()
                self.unitTest1_questionId_textEdit.clear() 
                self.unitTest1_answerId_textEdit.clear()
                self.unitTest1_solutionId_textEdit.clear()
                
                data ={"questionId":questionId,"hyperbola_question":hyperbola_question,
        "hyperbola_solution1": hyperbola_solution1,"hyperbola_solution2": hyperbola_solution2,
        "hyperbola_answer1":hyperbola_answer1, "hyperbola_answer2":hyperbola_answer2,
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
        "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").push(data)

class create_preQuestion(QMainWindow):
    def __init__(self):
        super(create_preQuestion, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(0)
        self.stackedWidget_12.setCurrentIndex(0)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)
        
        self.preCircle_Button.clicked.connect(self.questionCircle)
        self.preParabola_Button.clicked.connect(self.questionParabola)
        self.preEllipse_Button.clicked.connect(self.questionEllipse)
        self.preHyperbola_Button.clicked.connect(self.questionHyperbola)
        self.preSubstitution_Button.clicked.connect(self.questionSubstitution)
        self.preElimination_Button.clicked.connect(self.questionElimination)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
        
    def questionCircle(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.preAssess_question_textEdit.toPlainText() 
        circle_1_answer1 = self.preAssess_answer1_textEdit.text()
        circle_1_answer2 = self.preAssess_answer2_textEdit.text()
        circle_1_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"circle_1_question":circle_1_question,
        "circle_1_solution1": circle_1_solution1,"circle_1_solution2": circle_1_solution2,
        "circle_1_answer1":circle_1_answer1, "circle_1_answer2":circle_1_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("pre-assess").child("circleQuestion").push(data)

    def questionParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.preAssess_question_textEdit.toPlainText() 
        parabola_answer1 = self.preAssess_answer1_textEdit.text()
        parabola_answer2 = self.preAssess_answer2_textEdit.text()
        parabola_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        parabola_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"parabola_question":parabola_question,
           "parabola_solution1": parabola_solution1,"parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,
           "parabola_answer2":parabola_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("pre-assess").child("parabolaQuestion").push(data)

    def questionEllipse(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            ellipse_question = self.preAssess_question_textEdit.toPlainText() 
            ellipse_answer1 = self.preAssess_answer1_textEdit.text()
            ellipse_answer2 = self.preAssess_answer2_textEdit.text()
            ellipse_solution1 = self.preAssess_solution1_textEdit.toPlainText()
            ellipse_solution2 = self.preAssess_solution2_textEdit.toPlainText()
            questionId = self.preAssess_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.preAssess_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.preAssess_solutionId_textEdit.text()
            sol_num = "2"

            if ellipse_question == "":
                self.question_error = 1
                self.preAssess_question_error.setVisible(True)
            if ellipse_answer1 == "" or ellipse_answer2 == "":
                self.answer_error = 1
                self.preAssess_answer_error.setVisible(True)
            if ellipse_solution1 == "" or ellipse_solution2 == "":
                self.solution_error = 1
                self.preAssess_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.preAssess_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.preAssess_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.preAssess_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.preAssess_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.preAssess_allPass.setVisible(True)
                self.preAssess_questionId_error.setVisible(False)
                self.preAssess_question_error.setVisible(False)
                self.preAssess_solutionId_error.setVisible(False)
                self.preAssess_solutionScore_error.setVisible(False)
                self.preAssess_solution_error.setVisible(False)
                self.preAssess_answerId_error.setVisible(False)
                self.preAssess_answerScore_error.setVisible(False)
                self.preAssess_answer_error.setVisible(False)
                self.preAssess_allError.setVisible(False)

                self.preAssess_question_textEdit.clear() 
                self.preAssess_answer1_textEdit.clear()
                self.preAssess_answer2_textEdit.clear()
                self.preAssess_solution1_textEdit.clear()
                self.preAssess_solution2_textEdit.clear()
                self.preAssess_questionId_textEdit.clear() 
                self.preAssess_answerId_textEdit.clear()
                self.preAssess_solutionId_textEdit.clear()
                
                data ={"questionId":questionId,"ellipse_question":ellipse_question,
            "ellipse_solution1": ellipse_solution1,"ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,
            "ellipse_answer2":ellipse_answer2, "isActive":checkId, "answerId":answerId,
            "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("pre-assess").child("ellipseQuestion").push(data)

    def questionHyperbola(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            hyperbola_question = self.preAssess_question_textEdit.toPlainText() 
            hyperbola_answer1 = self.preAssess_answer1_textEdit.text()
            hyperbola_answer2 = self.preAssess_answer2_textEdit.text()
            hyperbola_solution1 = self.preAssess_solution1_textEdit.toPlainText()
            hyperbola_solution2 = self.preAssess_solution2_textEdit.toPlainText()
            questionId = self.preAssess_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.preAssess_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.preAssess_solutionId_textEdit.text()
            sol_num = "2"

            if hyperbola_question == "":
                self.question_error = 1
                self.preAssess_question_error.setVisible(True)
            if hyperbola_answer1 == "" or hyperbola_answer2 == "":
                self.answer_error = 1
                self.preAssess_answer_error.setVisible(True)
            if hyperbola_solution1 == "" or hyperbola_solution2 == "":
                self.solution_error = 1
                self.preAssess_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.preAssess_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.preAssess_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.preAssess_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.preAssess_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.preAssess_allPass.setVisible(True)
                self.preAssess_questionId_error.setVisible(False)
                self.preAssess_question_error.setVisible(False)
                self.preAssess_solutionId_error.setVisible(False)
                self.preAssess_solutionScore_error.setVisible(False)
                self.preAssess_solution_error.setVisible(False)
                self.preAssess_answerId_error.setVisible(False)
                self.preAssess_answerScore_error.setVisible(False)
                self.preAssess_answer_error.setVisible(False)
                self.preAssess_allError.setVisible(False)

                self.preAssess_question_textEdit.clear() 
                self.preAssess_answer1_textEdit.clear()
                self.preAssess_answer2_textEdit.clear()
                self.preAssess_solution1_textEdit.clear()
                self.preAssess_solution2_textEdit.clear()
                self.preAssess_questionId_textEdit.clear() 
                self.preAssess_answerId_textEdit.clear()
                self.preAssess_solutionId_textEdit.clear()

                data ={"questionId":questionId,"hyperbola_question":hyperbola_question,
        "hyperbola_solution1": hyperbola_solution1,"hyperbola_solution2": hyperbola_solution2,
        "hyperbola_answer1":hyperbola_answer1, "hyperbola_answer2":hyperbola_answer2,
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
        "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").push(data)

    
    def questionSubstitution(self):
        # .setText
        # self.unitTest2Q1Sol_textEdit.toPlainText() QTEXTEDIT malaki
        # self.unitTest2Q9_textEdit.text() QLINEEDIT maliit

        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        substitution_question = self.preAssess_question_textEdit.toPlainText() 
        substitution_answer1 = self.preAssess_answer1_textEdit.text()
        substitution_answer2 = self.preAssess_answer2_textEdit.text()
        substitution_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        substitution_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if substitution_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if substitution_answer1 == "" or substitution_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if substitution_solution1 == "" or substitution_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"substitution_question":substitution_question,
        "substitution_solution1": substitution_solution1,"substitution_solution2": substitution_solution2,
        "substitution_answer1":substitution_answer1, "substitution_answer2":substitution_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("pre-assess").child("substitutionQuestion").push(data)

    def questionElimination(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        elimination_question = self.preAssess_question_textEdit.toPlainText() 
        elimination_answer1 = self.preAssess_answer1_textEdit.text()
        elimination_answer2 = self.preAssess_answer2_textEdit.text()
        elimination_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        elimination_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if elimination_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if elimination_answer1 == "" or elimination_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if elimination_solution1 == "" or elimination_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"elimination_question":elimination_question,
           "elimination_solution1": elimination_solution1,"elimination_solution2": elimination_solution2,"elimination_answer1":elimination_answer1,
           "elimination_answer2":elimination_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("pre-assess").child("eliminationQuestion").push(data)
class create_postQuestion(QMainWindow):
    def __init__(self):
        super(create_postQuestion, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        self.topicPages.setCurrentIndex(15)
        self.stackedWidget_9.setCurrentIndex(0)
        self.stackedWidget_10.setCurrentIndex(0)
        self.postAssess_answerScore_widget.setVisible(False)
        self.postAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)
        
        self.postCircle_Button.clicked.connect(self.questionCircle)
        self.postParabola_Button.clicked.connect(self.questionParabola)
        self.postEllipse_Button.clicked.connect(self.questionEllipse)
        self.postHyperbola_Button.clicked.connect(self.questionHyperbola)
        self.postSubstitution_Button.clicked.connect(self.questionSubstitution)
        self.postElimination_Button.clicked.connect(self.questionElimination)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
        
    def questionCircle(self):
        # .setText
        # self.unitTest2Q1Sol_textEdit.toPlainText() QTEXTEDIT malaki
        # self.unitTest2Q9_textEdit.text() QLINEEDIT maliit

        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.postAssess_question_textEdit.toPlainText() 
        circle_1_answer1 = self.postAssess_answer1_textEdit.text()
        circle_1_answer2 = self.postAssess_answer2_textEdit.text()
        circle_1_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"circle_1_question":circle_1_question,
        "circle_1_solution1": circle_1_solution1,"circle_1_solution2": circle_1_solution2,
        "circle_1_answer1":circle_1_answer1, "circle_1_answer2":circle_1_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("post-assess").child("circleQuestion").push(data)

    def questionParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.postAssess_question_textEdit.toPlainText() 
        parabola_answer1 = self.postAssess_answer1_textEdit.text()
        parabola_answer2 = self.postAssess_answer2_textEdit.text()
        parabola_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        parabola_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"parabola_question":parabola_question,
           "parabola_solution1": parabola_solution1,"parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,
           "parabola_answer2":parabola_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("post-assess").child("parabolaQuestion").push(data)

    def questionEllipse(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            ellipse_question = self.postAssess_question_textEdit.toPlainText() 
            ellipse_answer1 = self.postAssess_answer1_textEdit.text()
            ellipse_answer2 = self.postAssess_answer2_textEdit.text()
            ellipse_solution1 = self.postAssess_solution1_textEdit.toPlainText()
            ellipse_solution2 = self.postAssess_solution2_textEdit.toPlainText()
            questionId = self.postAssess_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.postAssess_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.postAssess_solutionId_textEdit.text()
            sol_num = "2"

            if ellipse_question == "":
                self.question_error = 1
                self.postAssess_question_error.setVisible(True)
            if ellipse_answer1 == "" or ellipse_answer2 == "":
                self.answer_error = 1
                self.postAssess_answer_error.setVisible(True)
            if ellipse_solution1 == "" or ellipse_solution2 == "":
                self.solution_error = 1
                self.postAssess_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.postAssess_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.postAssess_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.postAssess_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.postAssess_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.postAssess_allPass.setVisible(True)
                self.postAssess_questionId_error.setVisible(False)
                self.postAssess_question_error.setVisible(False)
                self.postAssess_solutionId_error.setVisible(False)
                self.postAssess_solutionScore_error.setVisible(False)
                self.postAssess_solution_error.setVisible(False)
                self.postAssess_answerId_error.setVisible(False)
                self.postAssess_answerScore_error.setVisible(False)
                self.postAssess_answer_error.setVisible(False)
                self.postAssess_allError.setVisible(False)

                self.postAssess_question_textEdit.clear() 
                self.postAssess_answer1_textEdit.clear()
                self.postAssess_answer2_textEdit.clear()
                self.postAssess_solution1_textEdit.clear()
                self.postAssess_solution2_textEdit.clear()
                self.postAssess_questionId_textEdit.clear() 
                self.postAssess_answerId_textEdit.clear()
                self.postAssess_solutionId_textEdit.clear()
                
                data ={"questionId":questionId,"ellipse_question":ellipse_question,
            "ellipse_solution1": ellipse_solution1,"ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,
            "ellipse_answer2":ellipse_answer2, "isActive":checkId, "answerId":answerId,
            "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("post-assess").child("ellipseQuestion").push(data)

    def questionHyperbola(self):
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0

            hyperbola_question = self.postAssess_question_textEdit.toPlainText() 
            hyperbola_answer1 = self.postAssess_answer1_textEdit.text()
            hyperbola_answer2 = self.postAssess_answer2_textEdit.text()
            hyperbola_solution1 = self.postAssess_solution1_textEdit.toPlainText()
            hyperbola_solution2 = self.postAssess_solution2_textEdit.toPlainText()
            questionId = self.postAssess_questionId_textEdit.text() 
            checkId = "active"
            answerId = self.postAssess_answerId_textEdit.text()
            answer_num = "2"
            solutionId = self.postAssess_solutionId_textEdit.text()
            sol_num = "2"

            if hyperbola_question == "":
                self.question_error = 1
                self.postAssess_question_error.setVisible(True)
            if hyperbola_answer1 == "" or hyperbola_answer2 == "":
                self.answer_error = 1
                self.postAssess_answer_error.setVisible(True)
            if hyperbola_solution1 == "" or hyperbola_solution2 == "":
                self.solution_error = 1
                self.postAssess_solution_error.setVisible(True)
            if questionId == "":
                self.questionId_error = 1
                self.postAssess_questionId_error.setVisible(True)
            if answerId == "":
                self.answerId_error = 1
                self.postAssess_answerId_error.setVisible(True)
            if solutionId == "":
                self.solutionId_error
                self.postAssess_solutionId_error.setVisible(True)

            if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
                self.postAssess_allError.setVisible(True)

                self.questionId_error = 0
                self.question_error = 0
                self.solutionId_error = 0
                self.solution_error = 0
                self.answerId_error = 0
                self.answer_error = 0
            else:
                self.postAssess_allPass.setVisible(True)
                self.postAssess_questionId_error.setVisible(False)
                self.postAssess_question_error.setVisible(False)
                self.postAssess_solutionId_error.setVisible(False)
                self.postAssess_solutionScore_error.setVisible(False)
                self.postAssess_solution_error.setVisible(False)
                self.postAssess_answerId_error.setVisible(False)
                self.postAssess_answerScore_error.setVisible(False)
                self.postAssess_answer_error.setVisible(False)
                self.postAssess_allError.setVisible(False)

                self.postAssess_question_textEdit.clear() 
                self.postAssess_answer1_textEdit.clear()
                self.postAssess_answer2_textEdit.clear()
                self.postAssess_solution1_textEdit.clear()
                self.postAssess_solution2_textEdit.clear()
                self.postAssess_questionId_textEdit.clear() 
                self.postAssess_answerId_textEdit.clear()
                self.postAssess_solutionId_textEdit.clear()

                data ={"questionId":questionId,"hyperbola_question":hyperbola_question,
        "hyperbola_solution1": hyperbola_solution1,"hyperbola_solution2": hyperbola_solution2,
        "hyperbola_answer1":hyperbola_answer1, "hyperbola_answer2":hyperbola_answer2,
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, 
        "solutionId":solutionId, "sol_num":sol_num}
                db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").push(data)

    
    def questionSubstitution(self):
        # .setText
        # self.unitTest2Q1Sol_textEdit.toPlainText() QTEXTEDIT malaki
        # self.unitTest2Q9_textEdit.text() QLINEEDIT maliit

        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        substitution_question = self.postAssess_question_textEdit.toPlainText() 
        substitution_answer1 = self.postAssess_answer1_textEdit.text()
        substitution_answer2 = self.postAssess_answer2_textEdit.text()
        substitution_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        substitution_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if substitution_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if substitution_answer1 == "" or substitution_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if substitution_solution1 == "" or substitution_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"substitution_question":substitution_question,
        "substitution_solution1": substitution_solution1,"substitution_solution2": substitution_solution2,
        "substitution_answer1":substitution_answer1, "substitution_answer2":substitution_answer2, 
        "isActive":checkId, "answerId":answerId, "answer_num":answer_num, "solutionId":solutionId, 
        "sol_num":sol_num}
            db.child("precal_questions").child("post-assess").child("substitutionQuestion").push(data)

    def questionElimination(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        elimination_question = self.postAssess_question_textEdit.toPlainText() 
        elimination_answer1 = self.postAssess_answer1_textEdit.text()
        elimination_answer2 = self.postAssess_answer2_textEdit.text()
        elimination_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        elimination_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if elimination_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if elimination_answer1 == "" or elimination_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if elimination_solution1 == "" or elimination_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)
            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            data ={"questionId":questionId,"elimination_question":elimination_question,
           "elimination_solution1": elimination_solution1,"elimination_solution2": elimination_solution2,"elimination_answer1":elimination_answer1,
           "elimination_answer2":elimination_answer2, "isActive":checkId, "answerId":answerId,
           "answer_num":answer_num, "solutionId":solutionId, "sol_num":sol_num}
            db.child("precal_questions").child("post-assess").child("eliminationQuestion").push(data)

class update_unit1Circle(QMainWindow):
    def __init__(self):
        super(update_unit1Circle, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_circle = db.child("precal_questions").child("lesson1").child("circleQuestion").get()

        for circle in all_unitTest1_circle.each():
            if circle.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(circle.val()["circle_1_question"])
                data.scores.update_QuestionID = str(circle.val()["questionId"])
                data.scores.update_SolutionID = str(circle.val()["solutionId"])
                data.scores.update_Solution1 = str(circle.val()["circle_1_solution1"])
                data.scores.update_Solution2 = str(circle.val()["circle_1_solution2"])
                data.scores.update_AnswerId = str(circle.val()["answerId"])
                data.scores.update_Answer1 = str(circle.val()["circle_1_answer1"])
                data.scores.update_Answer2 = str(circle.val()["circle_1_answer2"])

        self.topicPages.setCurrentIndex(16)
        self.stackedWidget_5.setCurrentIndex(1)
        self.stackedWidget_6.setCurrentIndex(1)
        self.unitTest1_answerScore_widget.setVisible(False)
        self.unitTest1_solutionScore_widget.setVisible(False)

        self.unitTest1_questionId_error.setVisible(False)
        self.unitTest1_question_error.setVisible(False)
        self.unitTest1_solutionId_error.setVisible(False)
        self.unitTest1_solutionScore_error.setVisible(False)
        self.unitTest1_solution_error.setVisible(False)
        self.unitTest1_answerId_error.setVisible(False)
        self.unitTest1_answerScore_error.setVisible(False)
        self.unitTest1_answer_error.setVisible(False)
        self.unitTest_allError.setVisible(False)
        self.unitTest_allPass.setVisible(False)

        self.unitTest1_question_textEdit.setText(data.scores.update_Question) 
        self.unitTest1_answer1_textEdit.setText(data.scores.update_Answer1)
        self.unitTest1_answer2_textEdit.setText(data.scores.update_Answer2)
        self.unitTest1_solution1_textEdit.setText(data.scores.update_Solution1)
        self.unitTest1_solution2_textEdit.setText(data.scores.update_Solution2)
        self.unitTest1_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.unitTest1_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.unitTest1_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.unitTest1Circle_update_Button.clicked.connect(self.updateCircle)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateCircle(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.unitTest1_question_textEdit.toPlainText() 
        circle_1_answer1 = self.unitTest1_answer1_textEdit.text()
        circle_1_answer2 = self.unitTest1_answer2_textEdit.text()
        circle_1_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            all_unitTest1_circle = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
            for update_circle in all_unitTest1_circle.each():
                if update_circle.val()["questionId"] == questionId_save:
                    keyId = update_circle.key()
            db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).update({
                "questionId":questionId,"circle_1_question":circle_1_question,"circle_1_solution1": circle_1_solution1,
                "circle_1_solution2": circle_1_solution2,"circle_1_answer1":circle_1_answer1,"circle_1_answer2":circle_1_answer2,
                "answerId":answerId,"solutionId":solutionId})

class update_unit1Parabola(QMainWindow):
    def __init__(self):
        super(update_unit1Parabola, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_parabola = db.child("precal_questions").child("lesson1").child("parabolaQuestion").get()

        for parabola in all_unitTest1_parabola.each():
            if parabola.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(parabola.val()["parabola_question"])
                data.scores.update_QuestionID = str(parabola.val()["questionId"])
                data.scores.update_SolutionID = str(parabola.val()["solutionId"])
                data.scores.update_Solution1 = str(parabola.val()["parabola_solution1"])
                data.scores.update_Solution2 = str(parabola.val()["parabola_solution2"])
                data.scores.update_AnswerId = str(parabola.val()["answerId"])
                data.scores.update_Answer1 = str(parabola.val()["parabola_answer1"])
                data.scores.update_Answer2 = str(parabola.val()["parabola_answer2"])

        self.topicPages.setCurrentIndex(16)
        self.stackedWidget_5.setCurrentIndex(1)
        self.stackedWidget_6.setCurrentIndex(2)
        self.unitTest1_answerScore_widget.setVisible(False)
        self.unitTest1_solutionScore_widget.setVisible(False)

        self.unitTest1_questionId_error.setVisible(False)
        self.unitTest1_question_error.setVisible(False)
        self.unitTest1_solutionId_error.setVisible(False)
        self.unitTest1_solutionScore_error.setVisible(False)
        self.unitTest1_solution_error.setVisible(False)
        self.unitTest1_answerId_error.setVisible(False)
        self.unitTest1_answerScore_error.setVisible(False)
        self.unitTest1_answer_error.setVisible(False)
        self.unitTest_allError.setVisible(False)
        self.unitTest_allPass.setVisible(False)

        self.unitTest1_question_textEdit.setText(data.scores.update_Question) 
        self.unitTest1_answer1_textEdit.setText(data.scores.update_Answer1)
        self.unitTest1_answer2_textEdit.setText(data.scores.update_Answer2)
        self.unitTest1_solution1_textEdit.setText(data.scores.update_Solution1)
        self.unitTest1_solution2_textEdit.setText(data.scores.update_Solution2)
        self.unitTest1_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.unitTest1_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.unitTest1_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.unitTest1Parabola_update_Button.clicked.connect(self.updateParabola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.unitTest1_question_textEdit.toPlainText() 
        parabola_answer1 = self.unitTest1_answer1_textEdit.text()
        parabola_answer2 = self.unitTest1_answer2_textEdit.text()
        parabola_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        parabola_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            all_unitTest1_circle = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
            for update_circle in all_unitTest1_circle.each():
                if update_circle.val()["questionId"] == questionId_save:
                    keyId = update_circle.key()
            db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).update({
                "questionId":questionId,"parabola_question":parabola_question,
           "parabola_solution1": parabola_solution1,"parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,
           "parabola_answer2":parabola_answer2, "answerId":answerId,
           "solutionId":solutionId})

class update_unit1Ellipse(QMainWindow):
    def __init__(self):
        super(update_unit1Ellipse, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_ellipse = db.child("precal_questions").child("lesson1").child("ellipseQuestion").get()

        for ellipse in all_unitTest1_ellipse.each():
            if ellipse.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(ellipse.val()["ellipse_question"])
                data.scores.update_QuestionID = str(ellipse.val()["questionId"])
                data.scores.update_SolutionID = str(ellipse.val()["solutionId"])
                data.scores.update_Solution1 = str(ellipse.val()["ellipse_solution1"])
                data.scores.update_Solution2 = str(ellipse.val()["ellipse_solution2"])
                data.scores.update_AnswerId = str(ellipse.val()["answerId"])
                data.scores.update_Answer1 = str(ellipse.val()["ellipse_answer1"])
                data.scores.update_Answer2 = str(ellipse.val()["ellipse_answer2"])

        self.topicPages.setCurrentIndex(16)
        self.stackedWidget_5.setCurrentIndex(1)
        self.stackedWidget_6.setCurrentIndex(3)
        self.unitTest1_answerScore_widget.setVisible(False)
        self.unitTest1_solutionScore_widget.setVisible(False)

        self.unitTest1_questionId_error.setVisible(False)
        self.unitTest1_question_error.setVisible(False)
        self.unitTest1_solutionId_error.setVisible(False)
        self.unitTest1_solutionScore_error.setVisible(False)
        self.unitTest1_solution_error.setVisible(False)
        self.unitTest1_answerId_error.setVisible(False)
        self.unitTest1_answerScore_error.setVisible(False)
        self.unitTest1_answer_error.setVisible(False)
        self.unitTest_allError.setVisible(False)
        self.unitTest_allPass.setVisible(False)

        self.unitTest1_question_textEdit.setText(data.scores.update_Question) 
        self.unitTest1_answer1_textEdit.setText(data.scores.update_Answer1)
        self.unitTest1_answer2_textEdit.setText(data.scores.update_Answer2)
        self.unitTest1_solution1_textEdit.setText(data.scores.update_Solution1)
        self.unitTest1_solution2_textEdit.setText(data.scores.update_Solution2)
        self.unitTest1_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.unitTest1_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.unitTest1_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.unitTest1Ellipse_update_Button.clicked.connect(self.updateEllipse)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateEllipse(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        ellipse_question = self.unitTest1_question_textEdit.toPlainText() 
        ellipse_answer1 = self.unitTest1_answer1_textEdit.text()
        ellipse_answer2 = self.unitTest1_answer2_textEdit.text()
        ellipse_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        ellipse_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if ellipse_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if ellipse_answer1 == "" or ellipse_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if ellipse_solution1 == "" or ellipse_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            all_unitTest1_circle = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
            for update_circle in all_unitTest1_circle.each():
                if update_circle.val()["questionId"] == questionId_save:
                    keyId = update_circle.key()
            db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).update({
                "questionId":questionId,"ellipse_question":ellipse_question,
           "ellipse_solution1": ellipse_solution1,"ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,
           "ellipse_answer2":ellipse_answer2, "answerId":answerId,"solutionId":solutionId})

class update_unit1Hyperbola(QMainWindow):
    def __init__(self):
        super(update_unit1Hyperbola, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_hyperbola = db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").get()

        for hyperbola in all_unitTest1_hyperbola.each():
            if hyperbola.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(hyperbola.val()["hyperbola_question"])
                data.scores.update_QuestionID = str(hyperbola.val()["questionId"])
                data.scores.update_SolutionID = str(hyperbola.val()["solutionId"])
                data.scores.update_Solution1 = str(hyperbola.val()["hyperbola_solution1"])
                data.scores.update_Solution2 = str(hyperbola.val()["hyperbola_solution2"])
                data.scores.update_AnswerId = str(hyperbola.val()["answerId"])
                data.scores.update_Answer1 = str(hyperbola.val()["hyperbola_answer1"])
                data.scores.update_Answer2 = str(hyperbola.val()["hyperbola_answer2"])

        self.topicPages.setCurrentIndex(16)
        self.stackedWidget_5.setCurrentIndex(1)
        self.stackedWidget_6.setCurrentIndex(2)
        self.unitTest1_answerScore_widget.setVisible(False)
        self.unitTest1_solutionScore_widget.setVisible(False)

        self.unitTest1_questionId_error.setVisible(False)
        self.unitTest1_question_error.setVisible(False)
        self.unitTest1_solutionId_error.setVisible(False)
        self.unitTest1_solutionScore_error.setVisible(False)
        self.unitTest1_solution_error.setVisible(False)
        self.unitTest1_answerId_error.setVisible(False)
        self.unitTest1_answerScore_error.setVisible(False)
        self.unitTest1_answer_error.setVisible(False)
        self.unitTest_allError.setVisible(False)
        self.unitTest_allPass.setVisible(False)

        self.unitTest1_question_textEdit.setText(data.scores.update_Question) 
        self.unitTest1_answer1_textEdit.setText(data.scores.update_Answer1)
        self.unitTest1_answer2_textEdit.setText(data.scores.update_Answer2)
        self.unitTest1_solution1_textEdit.setText(data.scores.update_Solution1)
        self.unitTest1_solution2_textEdit.setText(data.scores.update_Solution2)
        self.unitTest1_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.unitTest1_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.unitTest1_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.unitTest1Parabola_update_Button.clicked.connect(self.updatehyperbola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updatehyperbola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        hyperbola_question = self.unitTest1_question_textEdit.toPlainText() 
        hyperbola_answer1 = self.unitTest1_answer1_textEdit.text()
        hyperbola_answer2 = self.unitTest1_answer2_textEdit.text()
        hyperbola_solution1 = self.unitTest1_solution1_textEdit.toPlainText()
        hyperbola_solution2 = self.unitTest1_solution2_textEdit.toPlainText()
        questionId = self.unitTest1_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest1_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest1_solutionId_textEdit.text()
        sol_num = "2"

        if hyperbola_question == "":
            self.question_error = 1
            self.unitTest1_question_error.setVisible(True)
        if hyperbola_answer1 == "" or hyperbola_answer2 == "":
            self.answer_error = 1
            self.unitTest1_answer_error.setVisible(True)
        if hyperbola_solution1 == "" or hyperbola_solution2 == "":
            self.solution_error = 1
            self.unitTest1_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest1_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest1_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest1_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest_allPass.setVisible(True)
            self.unitTest1_questionId_error.setVisible(False)
            self.unitTest1_question_error.setVisible(False)
            self.unitTest1_solutionId_error.setVisible(False)
            self.unitTest1_solutionScore_error.setVisible(False)
            self.unitTest1_solution_error.setVisible(False)
            self.unitTest1_answerId_error.setVisible(False)
            self.unitTest1_answerScore_error.setVisible(False)
            self.unitTest1_answer_error.setVisible(False)
            self.unitTest_allError.setVisible(False)

            self.unitTest1_question_textEdit.clear() 
            self.unitTest1_answer1_textEdit.clear()
            self.unitTest1_answer2_textEdit.clear()
            self.unitTest1_solution1_textEdit.clear()
            self.unitTest1_solution2_textEdit.clear()
            self.unitTest1_questionId_textEdit.clear() 
            self.unitTest1_answerId_textEdit.clear()
            self.unitTest1_solutionId_textEdit.clear()

            all_unitTest1_circle = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
            for update_circle in all_unitTest1_circle.each():
                if update_circle.val()["questionId"] == questionId_save:
                    keyId = update_circle.key()
            db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).update({
                "questionId":questionId,"hyperbola_question":hyperbola_question,
       "hyperbola_solution1": hyperbola_solution1,"hyperbola_solution2": hyperbola_solution2,
       "hyperbola_answer1":hyperbola_answer1, "hyperbola_answer2":hyperbola_answer2,"answerId":answerId, 
       "solutionId":solutionId})

class update_unit2Substitution(QMainWindow):
    def __init__(self):
        super(update_unit2Substitution, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest2_substitution = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()

        for substitution in all_unitTest2_substitution.each():
            if substitution.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(substitution.val()["substitution_question"])
                data.scores.update_QuestionID = str(substitution.val()["questionId"])
                data.scores.update_SolutionID = str(substitution.val()["solutionId"])
                data.scores.update_Solution1 = str(substitution.val()["substitution_solution1"])
                data.scores.update_Solution2 = str(substitution.val()["substitution_solution2"])
                data.scores.update_AnswerId = str(substitution.val()["answerId"])
                data.scores.update_Answer1 = str(substitution.val()["substitution_answer1"])
                data.scores.update_Answer2 = str(substitution.val()["substitution_answer2"])

        self.topicPages.setCurrentIndex(17)
        self.stackedWidget_7.setCurrentIndex(1)
        self.stackedWidget_8.setCurrentIndex(1)
        self.unitTest2_answerScore_widget.setVisible(False)
        self.unitTest2_solutionScore_widget.setVisible(False)

        self.unitTest2_questionId_error.setVisible(False)
        self.unitTest2_question_error.setVisible(False)
        self.unitTest2_solutionId_error.setVisible(False)
        self.unitTest2_solutionScore_error.setVisible(False)
        self.unitTest2_solution_error.setVisible(False)
        self.unitTest2_answerId_error.setVisible(False)
        self.unitTest2_answerScore_error.setVisible(False)
        self.unitTest2_answer_error.setVisible(False)
        self.unitTest2_allError.setVisible(False)
        self.unitTest2_allPass.setVisible(False)

        self.unitTest2_question_textEdit.setText(data.scores.update_Question) 
        self.unitTest2_answer1_textEdit.setText(data.scores.update_Answer1)
        self.unitTest2_answer2_textEdit.setText(data.scores.update_Answer2)
        self.unitTest2_solution1_textEdit.setText(data.scores.update_Solution1)
        self.unitTest2_solution2_textEdit.setText(data.scores.update_Solution2)
        self.unitTest2_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.unitTest2_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.unitTest2_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.unitTest2Substitution_update_Button.clicked.connect(self.updateSubstitution)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateSubstitution(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        substitution_question = self.unitTest2_question_textEdit.toPlainText() 
        substitution_answer1 = self.unitTest2_answer1_textEdit.text()
        substitution_answer2 = self.unitTest2_answer2_textEdit.text()
        substitution_solution1 = self.unitTest2_solution1_textEdit.toPlainText()
        substitution_solution2 = self.unitTest2_solution2_textEdit.toPlainText()
        questionId = self.unitTest2_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest2_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest2_solutionId_textEdit.text()
        sol_num = "2"

        if substitution_question == "":
            self.question_error = 1
            self.unitTest2_question_error.setVisible(True)
        if substitution_answer1 == "" or substitution_answer2 == "":
            self.answer_error = 1
            self.unitTest2_answer_error.setVisible(True)
        if substitution_solution1 == "" or substitution_solution2 == "":
            self.solution_error = 1
            self.unitTest2_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest2_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest2_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest2_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest2_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest2_allPass.setVisible(True)
            self.unitTest2_questionId_error.setVisible(False)
            self.unitTest2_question_error.setVisible(False)
            self.unitTest2_solutionId_error.setVisible(False)
            self.unitTest2_solutionScore_error.setVisible(False)
            self.unitTest2_solution_error.setVisible(False)
            self.unitTest2_answerId_error.setVisible(False)
            self.unitTest2_answerScore_error.setVisible(False)
            self.unitTest2_answer_error.setVisible(False)
            self.unitTest2_allError.setVisible(False)

            self.unitTest2_question_textEdit.clear() 
            self.unitTest2_answer1_textEdit.clear()
            self.unitTest2_answer2_textEdit.clear()
            self.unitTest2_solution1_textEdit.clear()
            self.unitTest2_solution2_textEdit.clear()
            self.unitTest2_questionId_textEdit.clear() 
            self.unitTest2_answerId_textEdit.clear()
            self.unitTest2_solutionId_textEdit.clear()

            all_unitTest2_substitute = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()
            for update_subs in all_unitTest2_substitute.each():
                if update_subs.val()["questionId"] == questionId_save:
                    keyId = update_subs.key()
            db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).update({
                "questionId":questionId,"substitution_question":substitution_question,
       "substitution_solution1": substitution_solution1,"substitution_solution2": substitution_solution2,
       "substitution_answer1":substitution_answer1, "substitution_answer2":substitution_answer2,"answerId":answerId, 
       "solutionId":solutionId})
            
class update_unit2Elimination(QMainWindow):
    def __init__(self):
        super(update_unit2Elimination, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest2_elimination = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()

        for elimination in all_unitTest2_elimination.each():
            if elimination.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(elimination.val()["elimination_question"])
                data.scores.update_QuestionID = str(elimination.val()["questionId"])
                data.scores.update_SolutionID = str(elimination.val()["solutionId"])
                data.scores.update_Solution1 = str(elimination.val()["elimination_solution1"])
                data.scores.update_Solution2 = str(elimination.val()["elimination_solution2"])
                data.scores.update_AnswerId = str(elimination.val()["answerId"])
                data.scores.update_Answer1 = str(elimination.val()["elimination_answer1"])
                data.scores.update_Answer2 = str(elimination.val()["elimination_answer2"])

        self.topicPages.setCurrentIndex(17)
        self.stackedWidget_5.setCurrentIndex(1)
        self.stackedWidget_6.setCurrentIndex(2)
        self.unitTest2_answerScore_widget.setVisible(False)
        self.unitTest2_solutionScore_widget.setVisible(False)

        self.unitTest2_questionId_error.setVisible(False)
        self.unitTest2_question_error.setVisible(False)
        self.unitTest2_solutionId_error.setVisible(False)
        self.unitTest2_solutionScore_error.setVisible(False)
        self.unitTest2_solution_error.setVisible(False)
        self.unitTest2_answerId_error.setVisible(False)
        self.unitTest2_answerScore_error.setVisible(False)
        self.unitTest2_answer_error.setVisible(False)
        self.unitTest2_allError.setVisible(False)
        self.unitTest2_allPass.setVisible(False)

        self.unitTest2_question_textEdit.setText(data.scores.update_Question) 
        self.unitTest2_answer1_textEdit.setText(data.scores.update_Answer1)
        self.unitTest2_answer2_textEdit.setText(data.scores.update_Answer2)
        self.unitTest2_solution1_textEdit.setText(data.scores.update_Solution1)
        self.unitTest2_solution2_textEdit.setText(data.scores.update_Solution2)
        self.unitTest2_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.unitTest2_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.unitTest2_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.unitTest2Elimination_update_Button.clicked.connect(self.updateElimination)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateElimination(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        elimination_question = self.unitTest2_question_textEdit.toPlainText() 
        elimination_answer1 = self.unitTest2_answer1_textEdit.text()
        elimination_answer2 = self.unitTest2_answer2_textEdit.text()
        elimination_solution1 = self.unitTest2_solution1_textEdit.toPlainText()
        elimination_solution2 = self.unitTest2_solution2_textEdit.toPlainText()
        questionId = self.unitTest2_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.unitTest2_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.unitTest2_solutionId_textEdit.text()
        sol_num = "2"

        if elimination_question == "":
            self.question_error = 1
            self.unitTest2_question_error.setVisible(True)
        if elimination_answer1 == "" or elimination_answer2 == "":
            self.answer_error = 1
            self.unitTest2_answer_error.setVisible(True)
        if elimination_solution1 == "" or elimination_solution2 == "":
            self.solution_error = 1
            self.unitTest2_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.unitTest2_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.unitTest2_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.unitTest2_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.unitTest2_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.unitTest2_allPass.setVisible(True)
            self.unitTest2_questionId_error.setVisible(False)
            self.unitTest2_question_error.setVisible(False)
            self.unitTest2_solutionId_error.setVisible(False)
            self.unitTest2_solutionScore_error.setVisible(False)
            self.unitTest2_solution_error.setVisible(False)
            self.unitTest2_answerId_error.setVisible(False)
            self.unitTest2_answerScore_error.setVisible(False)
            self.unitTest2_answer_error.setVisible(False)
            self.unitTest2_allError.setVisible(False)

            self.unitTest2_question_textEdit.clear() 
            self.unitTest2_answer1_textEdit.clear()
            self.unitTest2_answer2_textEdit.clear()
            self.unitTest2_solution1_textEdit.clear()
            self.unitTest2_solution2_textEdit.clear()
            self.unitTest2_questionId_textEdit.clear() 
            self.unitTest2_answerId_textEdit.clear()
            self.unitTest2_solutionId_textEdit.clear()

            all_unitTest2_substitute = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()
            for update_subs in all_unitTest2_substitute.each():
                if update_subs.val()["questionId"] == questionId_save:
                    keyId = update_subs.key()
            db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).update({
                "questionId":questionId,"elimination_question":elimination_question,
       "elimination_solution1": elimination_solution1,"elimination_solution2": elimination_solution2,
       "elimination_answer1":elimination_answer1, "elimination_answer2":elimination_answer2,"answerId":answerId, 
       "solutionId":solutionId})

class update_preCircle(QMainWindow):
    def __init__(self):
        super(update_preCircle, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_circle = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()

        for circle in all_unitTest1_circle.each():
            if circle.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(circle.val()["circle_1_question"])
                data.scores.update_QuestionID = str(circle.val()["questionId"])
                data.scores.update_SolutionID = str(circle.val()["solutionId"])
                data.scores.update_Solution1 = str(circle.val()["circle_1_solution1"])
                data.scores.update_Solution2 = str(circle.val()["circle_1_solution2"])
                data.scores.update_AnswerId = str(circle.val()["answerId"])
                data.scores.update_Answer1 = str(circle.val()["circle_1_answer1"])
                data.scores.update_Answer2 = str(circle.val()["circle_1_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(1)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)

        self.preAssess_question_textEdit.setText(data.scores.update_Question) 
        self.preAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.preAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.preAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.preAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.preAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.preAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.preAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.preCircle_update_Button.clicked.connect(self.updateCircle)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateCircle(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.preAssess_question_textEdit.toPlainText() 
        circle_1_answer1 = self.preAssess_answer1_textEdit.text()
        circle_1_answer2 = self.preAssess_answer2_textEdit.text()
        circle_1_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            self.preAssess_question_textEdit.setReadOnly(True)
            self.preAssess_answer1_textEdit.setReadOnly(True)
            self.preAssess_answer2_textEdit.setReadOnly(True)
            self.preAssess_solution1_textEdit.setReadOnly(True)
            self.preAssess_solution2_textEdit.setReadOnly(True)
            self.preAssess_questionId_textEdit.setReadOnly(True)
            self.preAssess_answerId_textEdit.setReadOnly(True)
            self.preAssess_solutionId_textEdit.setReadOnly(True)

            all_unitTest1_circle = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()
            for update_circle in all_unitTest1_circle.each():
                if update_circle.val()["questionId"] == questionId_save:
                    keyId = update_circle.key()
            db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).update({
                "questionId":questionId,"circle_1_question":circle_1_question,"circle_1_solution1": circle_1_solution1,
                "circle_1_solution2": circle_1_solution2,"circle_1_answer1":circle_1_answer1,"circle_1_answer2":circle_1_answer2,
                "answerId":answerId,"solutionId":solutionId})

class update_preParabola(QMainWindow):
    def __init__(self):
        super(update_preParabola, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_parabola = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()

        for parabola in all_unitTest1_parabola.each():
            if parabola.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(parabola.val()["parabola_question"])
                data.scores.update_QuestionID = str(parabola.val()["questionId"])
                data.scores.update_SolutionID = str(parabola.val()["solutionId"])
                data.scores.update_Solution1 = str(parabola.val()["parabola_solution1"])
                data.scores.update_Solution2 = str(parabola.val()["parabola_solution2"])
                data.scores.update_AnswerId = str(parabola.val()["answerId"])
                data.scores.update_Answer1 = str(parabola.val()["parabola_answer1"])
                data.scores.update_Answer2 = str(parabola.val()["parabola_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(2)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)

        self.preAssess_question_textEdit.setText(data.scores.update_Question) 
        self.preAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.preAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.preAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.preAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.preAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.preAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.preAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.preParabola_update_Button.clicked.connect(self.updateParabola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.preAssess_question_textEdit.toPlainText() 
        parabola_answer1 = self.preAssess_answer1_textEdit.text()
        parabola_answer2 = self.preAssess_answer2_textEdit.text()
        parabola_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        parabola_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            all_unitTest1_parabola = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()
            for update_parabola in all_unitTest1_parabola.each():
                if update_parabola.val()["questionId"] == questionId_save:
                    keyId = update_parabola.key()
            db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).update({
                "questionId":questionId,"parabola_question":parabola_question,"parabola_solution1": parabola_solution1,
                "parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,"parabola_answer2":parabola_answer2,
                "answerId":answerId,"solutionId":solutionId})

class update_preEllipse(QMainWindow):
    def __init__(self):
        super(update_preEllipse, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_ellipse = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()

        for ellipse in all_unitTest1_ellipse.each():
            if ellipse.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(ellipse.val()["ellipse_question"])
                data.scores.update_QuestionID = str(ellipse.val()["questionId"])
                data.scores.update_SolutionID = str(ellipse.val()["solutionId"])
                data.scores.update_Solution1 = str(ellipse.val()["ellipse_solution1"])
                data.scores.update_Solution2 = str(ellipse.val()["ellipse_solution2"])
                data.scores.update_AnswerId = str(ellipse.val()["answerId"])
                data.scores.update_Answer1 = str(ellipse.val()["ellipse_answer1"])
                data.scores.update_Answer2 = str(ellipse.val()["ellipse_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(3)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)

        self.preAssess_question_textEdit.setText(data.scores.update_Question) 
        self.preAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.preAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.preAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.preAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.preAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.preAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.preAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.preEllipse_update_Button.clicked.connect(self.updateEllipse)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateEllipse(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        ellipse_question = self.preAssess_question_textEdit.toPlainText() 
        ellipse_answer1 = self.preAssess_answer1_textEdit.text()
        ellipse_answer2 = self.preAssess_answer2_textEdit.text()
        ellipse_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        ellipse_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if ellipse_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if ellipse_answer1 == "" or ellipse_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if ellipse_solution1 == "" or ellipse_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            all_unitTest1_ellipse = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()
            for update_ellipse in all_unitTest1_ellipse.each():
                if update_ellipse.val()["questionId"] == questionId_save:
                    keyId = update_ellipse.key()
            db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).update({
                "questionId":questionId,"ellipse_question":ellipse_question,"ellipse_solution1": ellipse_solution1,
                "ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,"ellipse_answer2":ellipse_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_preHyperbola(QMainWindow):
    def __init__(self):
        super(update_preHyperbola, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_hyperbola = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()

        for hyperbola in all_unitTest1_hyperbola.each():
            if hyperbola.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(hyperbola.val()["hyperbola_question"])
                data.scores.update_QuestionID = str(hyperbola.val()["questionId"])
                data.scores.update_SolutionID = str(hyperbola.val()["solutionId"])
                data.scores.update_Solution1 = str(hyperbola.val()["hyperbola_solution1"])
                data.scores.update_Solution2 = str(hyperbola.val()["hyperbola_solution2"])
                data.scores.update_AnswerId = str(hyperbola.val()["answerId"])
                data.scores.update_Answer1 = str(hyperbola.val()["hyperbola_answer1"])
                data.scores.update_Answer2 = str(hyperbola.val()["hyperbola_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(4)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)

        self.preAssess_question_textEdit.setText(data.scores.update_Question) 
        self.preAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.preAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.preAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.preAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.preAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.preAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.preAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.preHyperbola_update_Button.clicked.connect(self.updateHyperbola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateHyperbola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        hyperbola_question = self.preAssess_question_textEdit.toPlainText() 
        hyperbola_answer1 = self.preAssess_answer1_textEdit.text()
        hyperbola_answer2 = self.preAssess_answer2_textEdit.text()
        hyperbola_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        hyperbola_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if hyperbola_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if hyperbola_answer1 == "" or hyperbola_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if hyperbola_solution1 == "" or hyperbola_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            all_unitTest1_hyperbola = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()
            for update_hyperbola in all_unitTest1_hyperbola.each():
                if update_hyperbola.val()["questionId"] == questionId_save:
                    keyId = update_hyperbola.key()
            db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).update({
                "questionId":questionId,"hyperbola_question":hyperbola_question,"hyperbola_solution1": hyperbola_solution1,
                "hyperbola_solution2": hyperbola_solution2,"hyperbola_answer1":hyperbola_answer1,"hyperbola_answer2":hyperbola_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_preSubstitution(QMainWindow):
    def __init__(self):
        super(update_postSubstitution, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_substitution = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()

        for substitution in all_unitTest1_substitution.each():
            if substitution.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(substitution.val()["substitution_question"])
                data.scores.update_QuestionID = str(substitution.val()["questionId"])
                data.scores.update_SolutionID = str(substitution.val()["solutionId"])
                data.scores.update_Solution1 = str(substitution.val()["substitution_solution1"])
                data.scores.update_Solution2 = str(substitution.val()["substitution_solution2"])
                data.scores.update_AnswerId = str(substitution.val()["answerId"])
                data.scores.update_Answer1 = str(substitution.val()["substitution_answer1"])
                data.scores.update_Answer2 = str(substitution.val()["substitution_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(5)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)

        self.preAssess_question_textEdit.setText(data.scores.update_Question) 
        self.preAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.preAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.preAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.preAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.preAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.preAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.preAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.preSubstitution_update_Button.clicked.connect(self.updateSubstitution)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateSubstitution(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        substitution_question = self.preAssess_question_textEdit.toPlainText() 
        substitution_answer1 = self.preAssess_answer1_textEdit.text()
        substitution_answer2 = self.preAssess_answer2_textEdit.text()
        substitution_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        substitution_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if substitution_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if substitution_answer1 == "" or substitution_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if substitution_solution1 == "" or substitution_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            all_unitTest1_substitution = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()
            for update_substitution in all_unitTest1_substitution.each():
                if update_substitution.val()["questionId"] == questionId_save:
                    keyId = update_substitution.key()
            db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).update({
                "questionId":questionId,"substitution_question":substitution_question,"substitution_solution1": substitution_solution1,
                "substitution_solution2": substitution_solution2,"substitution_answer1":substitution_answer1,"substitution_answer2":substitution_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_preElimination(QMainWindow):
    def __init__(self):
        super(update_preElimination, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_elimination = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()

        for elimination in all_unitTest1_elimination.each():
            if elimination.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(elimination.val()["elimination_question"])
                data.scores.update_QuestionID = str(elimination.val()["questionId"])
                data.scores.update_SolutionID = str(elimination.val()["solutionId"])
                data.scores.update_Solution1 = str(elimination.val()["elimination_solution1"])
                data.scores.update_Solution2 = str(elimination.val()["elimination_solution2"])
                data.scores.update_AnswerId = str(elimination.val()["answerId"])
                data.scores.update_Answer1 = str(elimination.val()["elimination_answer1"])
                data.scores.update_Answer2 = str(elimination.val()["elimination_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(6)
        self.preAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.preAssess_questionId_error.setVisible(False)
        self.preAssess_question_error.setVisible(False)
        self.preAssess_solutionId_error.setVisible(False)
        self.preAssess_solutionScore_error.setVisible(False)
        self.preAssess_solution_error.setVisible(False)
        self.preAssess_answerId_error.setVisible(False)
        self.preAssess_answerScore_error.setVisible(False)
        self.preAssess_answer_error.setVisible(False)
        self.preAssess_allError.setVisible(False)
        self.preAssess_allPass.setVisible(False)

        self.preAssess_question_textEdit.setText(data.scores.update_Question) 
        self.preAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.preAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.preAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.preAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.preAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.preAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.preAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.preElimination_update_Button.clicked.connect(self.updateElimination)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateElimination(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        elimination_question = self.preAssess_question_textEdit.toPlainText() 
        elimination_answer1 = self.preAssess_answer1_textEdit.text()
        elimination_answer2 = self.preAssess_answer2_textEdit.text()
        elimination_solution1 = self.preAssess_solution1_textEdit.toPlainText()
        elimination_solution2 = self.preAssess_solution2_textEdit.toPlainText()
        questionId = self.preAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.preAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.preAssess_solutionId_textEdit.text()
        sol_num = "2"

        if elimination_question == "":
            self.question_error = 1
            self.preAssess_question_error.setVisible(True)
        if elimination_answer1 == "" or elimination_answer2 == "":
            self.answer_error = 1
            self.preAssess_answer_error.setVisible(True)
        if elimination_solution1 == "" or elimination_solution2 == "":
            self.solution_error = 1
            self.preAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.preAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.preAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.preAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.preAssess_allPass.setVisible(True)
            self.preAssess_questionId_error.setVisible(False)
            self.preAssess_question_error.setVisible(False)
            self.preAssess_solutionId_error.setVisible(False)
            self.preAssess_solutionScore_error.setVisible(False)
            self.preAssess_solution_error.setVisible(False)
            self.preAssess_answerId_error.setVisible(False)
            self.preAssess_answerScore_error.setVisible(False)
            self.preAssess_answer_error.setVisible(False)
            self.preAssess_allError.setVisible(False)

            self.preAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.preAssess_solution1_textEdit.clear()
            self.preAssess_solution2_textEdit.clear()
            self.preAssess_questionId_textEdit.clear() 
            self.preAssess_answerId_textEdit.clear()
            self.preAssess_solutionId_textEdit.clear()

            all_unitTest1_elimination = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()
            for update_elimination in all_unitTest1_elimination.each():
                if update_elimination.val()["questionId"] == questionId_save:
                    keyId = update_elimination.key()
            db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).update({
                "questionId":questionId,"elimination_question":elimination_question,"elimination_solution1": elimination_solution1,
                "elimination_solution2": elimination_solution2,"elimination_answer1":elimination_answer1,"elimination_answer2":elimination_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_postCircle(QMainWindow):
    def __init__(self):
        super(update_postCircle, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_circle = db.child("precal_questions").child("post-assess").child("circleQuestion").get()

        for circle in all_unitTest1_circle.each():
            if circle.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(circle.val()["circle_1_question"])
                data.scores.update_QuestionID = str(circle.val()["questionId"])
                data.scores.update_SolutionID = str(circle.val()["solutionId"])
                data.scores.update_Solution1 = str(circle.val()["circle_1_solution1"])
                data.scores.update_Solution2 = str(circle.val()["circle_1_solution2"])
                data.scores.update_AnswerId = str(circle.val()["answerId"])
                data.scores.update_Answer1 = str(circle.val()["circle_1_answer1"])
                data.scores.update_Answer2 = str(circle.val()["circle_1_answer2"])

        self.topicPages.setCurrentIndex(14)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(1)
        self.postAssess_answerScore_widget.setVisible(False)
        self.preAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)

        self.postAssess_question_textEdit.setText(data.scores.update_Question) 
        self.postAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.postAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.postAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.postAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.postAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.postAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.postAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.postCircle_update_Button.clicked.connect(self.updateCircle)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateCircle(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        circle_1_question = self.postAssess_question_textEdit.toPlainText() 
        circle_1_answer1 = self.postAssess_answer1_textEdit.text()
        circle_1_answer2 = self.postAssess_answer2_textEdit.text()
        circle_1_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        circle_1_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if circle_1_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if circle_1_answer1 == "" or circle_1_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if circle_1_solution1 == "" or circle_1_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            all_unitTest1_circle = db.child("precal_questions").child("post-assess").child("circleQuestion").get()
            for update_circle in all_unitTest1_circle.each():
                if update_circle.val()["questionId"] == questionId_save:
                    keyId = update_circle.key()
            db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).update({
                "questionId":questionId,"circle_1_question":circle_1_question,"circle_1_solution1": circle_1_solution1,
                "circle_1_solution2": circle_1_solution2,"circle_1_answer1":circle_1_answer1,"circle_1_answer2":circle_1_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_postParabola(QMainWindow):
    def __init__(self):
        super(update_postParabola, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_parabola = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()

        for parabola in all_unitTest1_parabola.each():
            if parabola.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(parabola.val()["parabola_question"])
                data.scores.update_QuestionID = str(parabola.val()["questionId"])
                data.scores.update_SolutionID = str(parabola.val()["solutionId"])
                data.scores.update_Solution1 = str(parabola.val()["parabola_solution1"])
                data.scores.update_Solution2 = str(parabola.val()["parabola_solution2"])
                data.scores.update_AnswerId = str(parabola.val()["answerId"])
                data.scores.update_Answer1 = str(parabola.val()["parabola_answer1"])
                data.scores.update_Answer2 = str(parabola.val()["parabola_answer2"])

        self.topicPages.setCurrentIndex(15)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(2)
        self.postAssess_answerScore_widget.setVisible(False)
        self.postAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)

        self.postAssess_question_textEdit.setText(data.scores.update_Question) 
        self.postAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.postAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.postAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.postAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.postAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.postAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.postAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.postParabola_update_Button.clicked.connect(self.updateParabola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateParabola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        parabola_question = self.postAssess_question_textEdit.toPlainText() 
        parabola_answer1 = self.postAssess_answer1_textEdit.text()
        parabola_answer2 = self.postAssess_answer2_textEdit.text()
        parabola_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        parabola_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if parabola_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if parabola_answer1 == "" or parabola_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if parabola_solution1 == "" or parabola_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.preAssess_answer1_textEdit.clear()
            self.preAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            all_unitTest1_parabola = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()
            for update_parabola in all_unitTest1_parabola.each():
                if update_parabola.val()["questionId"] == questionId_save:
                    keyId = update_parabola.key()
            db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).update({
                "questionId":questionId,"parabola_question":parabola_question,"parabola_solution1": parabola_solution1,
                "parabola_solution2": parabola_solution2,"parabola_answer1":parabola_answer1,"parabola_answer2":parabola_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_postEllipse(QMainWindow):
    def __init__(self):
        super(update_postEllipse, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_ellipse = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()

        for ellipse in all_unitTest1_ellipse.each():
            if ellipse.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(ellipse.val()["ellipse_question"])
                data.scores.update_QuestionID = str(ellipse.val()["questionId"])
                data.scores.update_SolutionID = str(ellipse.val()["solutionId"])
                data.scores.update_Solution1 = str(ellipse.val()["ellipse_solution1"])
                data.scores.update_Solution2 = str(ellipse.val()["ellipse_solution2"])
                data.scores.update_AnswerId = str(ellipse.val()["answerId"])
                data.scores.update_Answer1 = str(ellipse.val()["ellipse_answer1"])
                data.scores.update_Answer2 = str(ellipse.val()["ellipse_answer2"])

        self.topicPages.setCurrentIndex(15)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(3)
        self.postAssess_answerScore_widget.setVisible(False)
        self.postAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)

        self.postAssess_question_textEdit.setText(data.scores.update_Question) 
        self.postAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.postAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.postAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.postAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.postAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.postAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.postAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.postEllipse_update_Button.clicked.connect(self.updateEllipse)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateEllipse(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        ellipse_question = self.postAssess_question_textEdit.toPlainText() 
        ellipse_answer1 = self.postAssess_answer1_textEdit.text()
        ellipse_answer2 = self.postAssess_answer2_textEdit.text()
        ellipse_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        ellipse_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if ellipse_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if ellipse_answer1 == "" or ellipse_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if ellipse_solution1 == "" or ellipse_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            all_unitTest1_ellipse = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()
            for update_ellipse in all_unitTest1_ellipse.each():
                if update_ellipse.val()["questionId"] == questionId_save:
                    keyId = update_ellipse.key()
            db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).update({
                "questionId":questionId,"ellipse_question":ellipse_question,"ellipse_solution1": ellipse_solution1,
                "ellipse_solution2": ellipse_solution2,"ellipse_answer1":ellipse_answer1,"ellipse_answer2":ellipse_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_postHyperbola(QMainWindow):
    def __init__(self):
        super(update_postHyperbola, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_hyperbola = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()

        for hyperbola in all_unitTest1_hyperbola.each():
            if hyperbola.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(hyperbola.val()["hyperbola_question"])
                data.scores.update_QuestionID = str(hyperbola.val()["questionId"])
                data.scores.update_SolutionID = str(hyperbola.val()["solutionId"])
                data.scores.update_Solution1 = str(hyperbola.val()["hyperbola_solution1"])
                data.scores.update_Solution2 = str(hyperbola.val()["hyperbola_solution2"])
                data.scores.update_AnswerId = str(hyperbola.val()["answerId"])
                data.scores.update_Answer1 = str(hyperbola.val()["hyperbola_answer1"])
                data.scores.update_Answer2 = str(hyperbola.val()["hyperbola_answer2"])

        self.topicPages.setCurrentIndex(15)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(4)
        self.postAssess_answerScore_widget.setVisible(False)
        self.postAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)

        self.postAssess_question_textEdit.setText(data.scores.update_Question) 
        self.postAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.postAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.postAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.postAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.postAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.postAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.postAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.postHyperbola_update_Button.clicked.connect(self.updateHyperbola)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateHyperbola(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        hyperbola_question = self.postAssess_question_textEdit.toPlainText() 
        hyperbola_answer1 = self.postAssess_answer1_textEdit.text()
        hyperbola_answer2 = self.postAssess_answer2_textEdit.text()
        hyperbola_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        hyperbola_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if hyperbola_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if hyperbola_answer1 == "" or hyperbola_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if hyperbola_solution1 == "" or hyperbola_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            all_unitTest1_hyperbola = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()
            for update_hyperbola in all_unitTest1_hyperbola.each():
                if update_hyperbola.val()["questionId"] == questionId_save:
                    keyId = update_hyperbola.key()
            db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).update({
                "questionId":questionId,"hyperbola_question":hyperbola_question,"hyperbola_solution1": hyperbola_solution1,
                "hyperbola_solution2": hyperbola_solution2,"hyperbola_answer1":hyperbola_answer1,"hyperbola_answer2":hyperbola_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_postSubstitution(QMainWindow):
    def __init__(self):
        super(update_postSubstitution, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_substitution = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()

        for substitution in all_unitTest1_substitution.each():
            if substitution.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(substitution.val()["substitution_question"])
                data.scores.update_QuestionID = str(substitution.val()["questionId"])
                data.scores.update_SolutionID = str(substitution.val()["solutionId"])
                data.scores.update_Solution1 = str(substitution.val()["substitution_solution1"])
                data.scores.update_Solution2 = str(substitution.val()["substitution_solution2"])
                data.scores.update_AnswerId = str(substitution.val()["answerId"])
                data.scores.update_Answer1 = str(substitution.val()["substitution_answer1"])
                data.scores.update_Answer2 = str(substitution.val()["substitution_answer2"])

        self.topicPages.setCurrentIndex(15)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(5)
        self.postAssess_answerScore_widget.setVisible(False)
        self.postAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)

        self.postAssess_question_textEdit.setText(data.scores.update_Question) 
        self.postAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.postAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.postAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.postAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.postAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.postAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.postAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.postSubstitution_update_Button.clicked.connect(self.updateSubstitution)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateSubstitution(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        substitution_question = self.postAssess_question_textEdit.toPlainText() 
        substitution_answer1 = self.postAssess_answer1_textEdit.text()
        substitution_answer2 = self.postAssess_answer2_textEdit.text()
        substitution_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        substitution_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if substitution_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if substitution_answer1 == "" or substitution_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if substitution_solution1 == "" or substitution_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.preAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            all_unitTest1_substitution = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()
            for update_substitution in all_unitTest1_substitution.each():
                if update_substitution.val()["questionId"] == questionId_save:
                    keyId = update_substitution.key()
            db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).update({
                "questionId":questionId,"substitution_question":substitution_question,"substitution_solution1": substitution_solution1,
                "substitution_solution2": substitution_solution2,"substitution_answer1":substitution_answer1,"substitution_answer2":substitution_answer2,
                "answerId":answerId,"solutionId":solutionId})
class update_postElimination(QMainWindow):
    def __init__(self):
        super(update_postElimination, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/lessonDashboard.ui",self)
        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro"
        self.setWindowTitle(title)

        all_unitTest1_elimination = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()

        for elimination in all_unitTest1_elimination.each():
            if elimination.val()["questionId"] == questionId_save:
                data.scores.update_Question = str(elimination.val()["elimination_question"])
                data.scores.update_QuestionID = str(elimination.val()["questionId"])
                data.scores.update_SolutionID = str(elimination.val()["solutionId"])
                data.scores.update_Solution1 = str(elimination.val()["elimination_solution1"])
                data.scores.update_Solution2 = str(elimination.val()["elimination_solution2"])
                data.scores.update_AnswerId = str(elimination.val()["answerId"])
                data.scores.update_Answer1 = str(elimination.val()["elimination_answer1"])
                data.scores.update_Answer2 = str(elimination.val()["elimination_answer2"])

        self.topicPages.setCurrentIndex(15)
        self.stackedWidget_11.setCurrentIndex(1)
        self.stackedWidget_12.setCurrentIndex(6)
        self.postAssess_answerScore_widget.setVisible(False)
        self.postAssess_solutionScore_widget.setVisible(False)

        self.postAssess_questionId_error.setVisible(False)
        self.postAssess_question_error.setVisible(False)
        self.postAssess_solutionId_error.setVisible(False)
        self.postAssess_solutionScore_error.setVisible(False)
        self.postAssess_solution_error.setVisible(False)
        self.postAssess_answerId_error.setVisible(False)
        self.postAssess_answerScore_error.setVisible(False)
        self.postAssess_answer_error.setVisible(False)
        self.postAssess_allError.setVisible(False)
        self.postAssess_allPass.setVisible(False)

        self.postAssess_question_textEdit.setText(data.scores.update_Question) 
        self.postAssess_answer1_textEdit.setText(data.scores.update_Answer1)
        self.postAssess_answer2_textEdit.setText(data.scores.update_Answer2)
        self.postAssess_solution1_textEdit.setText(data.scores.update_Solution1)
        self.postAssess_solution2_textEdit.setText(data.scores.update_Solution2)
        self.postAssess_questionId_textEdit.setText(data.scores.update_QuestionID) 
        self.postAssess_answerId_textEdit.setText(data.scores.update_AnswerId)
        self.postAssess_solutionId_textEdit.setText(data.scores.update_SolutionID)

        self.postElimination_update_Button.clicked.connect(self.updateElimination)

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
        global fromQuestion
        fromQuestion = 1
        self.back = toDashboardTeach()
        self.back.show()

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
    
    def updateElimination(self):
        self.questionId_error = 0
        self.question_error = 0
        self.solutionId_error = 0
        self.solution_error = 0
        self.answerId_error = 0
        self.answer_error = 0

        elimination_question = self.postAssess_question_textEdit.toPlainText() 
        elimination_answer1 = self.postAssess_answer1_textEdit.text()
        elimination_answer2 = self.postAssess_answer2_textEdit.text()
        elimination_solution1 = self.postAssess_solution1_textEdit.toPlainText()
        elimination_solution2 = self.postAssess_solution2_textEdit.toPlainText()
        questionId = self.postAssess_questionId_textEdit.text() 
        checkId = "active"
        answerId = self.postAssess_answerId_textEdit.text()
        answer_num = "2"
        solutionId = self.postAssess_solutionId_textEdit.text()
        sol_num = "2"

        if elimination_question == "":
            self.question_error = 1
            self.postAssess_question_error.setVisible(True)
        if elimination_answer1 == "" or elimination_answer2 == "":
            self.answer_error = 1
            self.postAssess_answer_error.setVisible(True)
        if elimination_solution1 == "" or elimination_solution2 == "":
            self.solution_error = 1
            self.postAssess_solution_error.setVisible(True)
        if questionId == "":
            self.questionId_error = 1
            self.postAssess_questionId_error.setVisible(True)
        if answerId == "":
            self.answerId_error = 1
            self.postAssess_answerId_error.setVisible(True)
        if solutionId == "":
            self.solutionId_error
            self.postAssess_solutionId_error.setVisible(True)

        if self.question_error == 1 or self.answer_error == 1 or self.solution_error == 1 or self.questionId_error == 1 or self.solutionId_error == 1 or self.answerId_error == 1:
            self.postAssess_allError.setVisible(True)

            self.questionId_error = 0
            self.question_error = 0
            self.solutionId_error = 0
            self.solution_error = 0
            self.answerId_error = 0
            self.answer_error = 0
        else:
            self.postAssess_allPass.setVisible(True)
            self.postAssess_questionId_error.setVisible(False)
            self.postAssess_question_error.setVisible(False)
            self.postAssess_solutionId_error.setVisible(False)
            self.postAssess_solutionScore_error.setVisible(False)
            self.postAssess_solution_error.setVisible(False)
            self.postAssess_answerId_error.setVisible(False)
            self.postAssess_answerScore_error.setVisible(False)
            self.postAssess_answer_error.setVisible(False)
            self.postAssess_allError.setVisible(False)

            self.postAssess_question_textEdit.clear() 
            self.postAssess_answer1_textEdit.clear()
            self.postAssess_answer2_textEdit.clear()
            self.postAssess_solution1_textEdit.clear()
            self.postAssess_solution2_textEdit.clear()
            self.postAssess_questionId_textEdit.clear() 
            self.postAssess_answerId_textEdit.clear()
            self.postAssess_solutionId_textEdit.clear()

            all_unitTest1_elimination = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()
            for update_elimination in all_unitTest1_elimination.each():
                if update_elimination.val()["questionId"] == questionId_save:
                    keyId = update_elimination.key()
            db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).update({
                "questionId":questionId,"elimination_question":elimination_question,"elimination_solution1": elimination_solution1,
                "elimination_solution2": elimination_solution2,"elimination_answer1":elimination_answer1,"elimination_answer2":elimination_answer2,
                "answerId":answerId,"solutionId":solutionId})

class update_unit1Question(QDialog):
    def __init__(self, parent):
        super(update_unit1Question, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(0)
        self.unitTest1_error_widget.setVisible(False)

        self.unitTest1_check_pushButton.clicked.connect(self.checkFunction)
        self.unitTest1_cancel_pushButton.clicked.connect(self.cancelFunction)

    def checkFunction(self):
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking
        circle_questions = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("lesson1").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("lesson1").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").get()
        
        global willLogout
        
        for circle in circle_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toCirc = update_unit1Circle()
                self.toCirc.show()
            else:
                pass
        for parabola in parabola_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toPara = update_unit1Parabola()
                self.toPara.show()
            else:
                pass
        for ellipse in ellipse_questions.each():
            if ellipse.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toEllip = update_unit1Ellipse()
                self.toEllip.show()
            else:
                pass
        for hyperbola in hyperbola_questions.each():
            if hyperbola.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toHyper = update_unit1Hyperbola()
                self.toHyper.show()
            else:
                pass
        self.stackedWidget.setCurrentIndex(0)
        self.unitTest1_error_widget.setVisible(True)
    
    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()

class update_unit2Question(QDialog):
    def __init__(self, parent):
        super(update_unit2Question, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(0)
        self.unitTest1_error_widget.setVisible(False)

        self.unitTest1_check_pushButton.clicked.connect(self.checkFunction)
        self.unitTest1_cancel_pushButton.clicked.connect(self.cancelFunction)

    def checkFunction(self):
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking
        substitution_questions = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()

        global willLogout
        
        for substitute in substitution_questions.each():
            if substitute.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toSubs = update_unit2Substitution()
                self.toSubs.show()
            else:
                pass
        for eliminate in elimination_questions.each():
            if eliminate.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toElim = update_unit2Elimination()
                self.toElim.show()
            else:
                pass
        self.stackedWidget.setCurrentIndex(1)
        self.unitTest1_error_widget.setVisible(True)
    
    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()

class update_preQuestion(QDialog):
    def __init__(self, parent):
        super(update_preQuestion, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(0)
        self.unitTest1_error_widget.setVisible(False)

        self.unitTest1_check_pushButton.clicked.connect(self.checkFunction)
        self.unitTest1_cancel_pushButton.clicked.connect(self.cancelFunction)

    def checkFunction(self):
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking
        circle_questions = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()
        substitution_questions = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()

        global willLogout

        for circle in circle_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toCirc = update_preCircle()
                self.toCirc.show()
            else:
                pass
        for parabola in parabola_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toPara = update_preParabola()
                self.toPara.show()
            else:
                pass
        for ellipse in ellipse_questions.each():
            if ellipse.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toEllip = update_preEllipse()
                self.toEllip.show()
            else:
                pass
        for hyperbola in hyperbola_questions.each():
            if hyperbola.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toHyper = update_preHyperbola()
                self.toHyper.show()
            else:
                pass        
        for substitute in substitution_questions.each():
            if substitute.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toSubs = update_preSubstitution()
                self.toSubs.show()
            else:
                pass
        for eliminate in elimination_questions.each():
            if eliminate.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toElim = update_preElimination()
                self.toElim.show()
            else:
                pass
        self.stackedWidget.setCurrentIndex(1)
        self.unitTest1_error_widget.setVisible(True)
    
    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()

class update_postQuestion(QDialog):
    def __init__(self, parent):
        super(update_postQuestion, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(0)
        self.unitTest1_error_widget.setVisible(False)

        self.unitTest1_check_pushButton.clicked.connect(self.checkFunction)
        self.unitTest1_cancel_pushButton.clicked.connect(self.cancelFunction)

    def checkFunction(self):
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking
        circle_questions = db.child("precal_questions").child("post-assess").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()
        substitution_questions = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()

        global willLogout

        for circle in circle_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toCirc = update_postCircle()
                self.toCirc.show()
            else:
                pass
        for parabola in parabola_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toPara = update_postParabola()
                self.toPara.show()
            else:
                pass
        for ellipse in ellipse_questions.each():
            if ellipse.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toEllip = update_postEllipse()
                self.toEllip.show()
            else:
                pass
        for hyperbola in hyperbola_questions.each():
            if hyperbola.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toHyper = update_postHyperbola()
                self.toHyper.show()
            else:
                pass        
        for substitute in substitution_questions.each():
            if substitute.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toSubs = update_postSubstitution()
                self.toSubs.show()
            else:
                pass
        for eliminate in elimination_questions.each():
            if eliminate.val()["questionId"] == checking:
                willLogout = 0
                self.parent().hide()
                self.toElim = update_postElimination()
                self.toElim.show()
            else:
                pass
        self.stackedWidget.setCurrentIndex(1)
        self.unitTest1_error_widget.setVisible(True)
    
    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()

class delete_unit1Question(QDialog):
    def __init__(self, parent):
        super(delete_unit1Question, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)

        self.unitTest1_delete_pushButton.clicked.connect(self.deleteFunction)
        self.unitTest1_cancel1_pushButton.clicked.connect(self.cancelFunction)

    def deleteFunction(self):
        self.isCheck = 0
        self.isCorrect = 1
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking

        circle_questions = db.child("precal_questions").child("lesson1").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("lesson1").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("lesson1").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").get()
        
        global willLogout       
        for circle in circle_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_circle in circle_questions.each():
                    if delete_circle.val()["questionId"] == questionId_save:
                        keyId = delete_circle.key()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("circle_1_question").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("circle_1_solution1").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("circle_1_solution2").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("circle_1_answer1").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("circle_1_answer2").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("lesson1").child("circleQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for parabola in parabola_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_parabola in parabola_questions.each():
                    if delete_parabola.val()["questionId"] == questionId_save:
                        keyId = delete_parabola.key()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("parabola_question").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("parabola_solution1").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("parabola_solution2").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("parabola_answer1").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("parabola_answer2").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for ellipse in ellipse_questions.each():
            if ellipse.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_ellipse in ellipse_questions.each():
                    if delete_ellipse.val()["questionId"] == questionId_save:
                        keyId = delete_ellipse.key()
                        db.child("precal_questions").child("lesson1").child("parabolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("ellipse_question").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("ellipse_solution1").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("ellipse_solution2").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("ellipse_answer1").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("ellipse_answer2").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("lesson1").child("ellipseQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for hyperbola in hyperbola_questions.each():
            if hyperbola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_hyperbola in hyperbola_questions.each():
                    if delete_hyperbola.val()["questionId"] == questionId_save:
                        keyId = delete_hyperbola.key()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("hyperbola_question").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("hyperbola_solution1").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("hyperbola_solution2").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("hyperbola_answer1").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("hyperbola_answer2").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("lesson1").child("hyperbolaQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        if self.isCheck == 0:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
        else:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
            else:
                self.stackedWidget.setCurrentIndex(1)

    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()

class delete_unit2Question(QDialog):
    def __init__(self, parent):
        super(delete_unit2Question, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)

        self.unitTest1_delete_pushButton.clicked.connect(self.deleteFunction)
        self.unitTest1_cancel1_pushButton.clicked.connect(self.cancelFunction)

    def deleteFunction(self):
        self.isCheck = 0
        self.isCorrect = 1
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking

        substitution_questions = db.child("precal_questions").child("lesson2").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("lesson2").child("eliminationQuestion").get()

        global willLogout       
        for circle in substitution_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_substitution in substitution_questions.each():
                    if delete_substitution.val()["questionId"] == questionId_save:
                        keyId = delete_substitution.key()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("substitution_question").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("substitution_solution1").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("substitution_solution2").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("substitution_answer1").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("substitution_answer2").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("lesson2").child("substitutionQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for parabola in elimination_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_elimination in elimination_questions.each():
                    if delete_elimination.val()["questionId"] == questionId_save:
                        keyId = delete_elimination.key()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("elimination_question").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("elimination_solution1").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("elimination_solution2").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("elimination_answer1").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("elimination_answer2").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("lesson2").child("eliminationQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1

        if self.isCheck == 0:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
        else:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
            else:
                self.stackedWidget.setCurrentIndex(1)

    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()

class delete_preQuestion(QDialog):
    def __init__(self, parent):
        super(delete_preQuestion, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)

        self.unitTest1_delete_pushButton.clicked.connect(self.deleteFunction)
        self.unitTest1_cancel1_pushButton.clicked.connect(self.cancelFunction)

    def deleteFunction(self):
        self.isCheck = 0
        self.isCorrect = 1
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking

        circle_questions = db.child("precal_questions").child("pre-assess").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("pre-assess").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("pre-assess").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").get()
        substitution_questions = db.child("precal_questions").child("pre-assess").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("pre-assess").child("eliminationQuestion").get()

        global willLogout       
        for circle in circle_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_circle in circle_questions.each():
                    if delete_circle.val()["questionId"] == questionId_save:
                        keyId = delete_circle.key()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("circle_1_question").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("circle_1_solution1").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("circle_1_solution2").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("circle_1_answer1").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("circle_1_answer2").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("pre-assess").child("circleQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for parabola in parabola_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_parabola in parabola_questions.each():
                    if delete_parabola.val()["questionId"] == questionId_save:
                        keyId = delete_parabola.key()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("parabola_question").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("parabola_solution1").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("parabola_solution2").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("parabola_answer1").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("parabola_answer2").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("pre-assess").child("parabolaQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for ellipse in ellipse_questions.each():
            if ellipse.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_ellipse in ellipse_questions.each():
                    if delete_ellipse.val()["questionId"] == questionId_save:
                        keyId = delete_ellipse.key()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("ellipse_question").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("ellipse_solution1").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("ellipse_solution2").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("ellipse_answer1").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("ellipse_answer2").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("pre-assess").child("ellipseQuestion").child(keyId).child("sol_num").remove()  
            else:
                self.isCheck=1
        for hyperbola in hyperbola_questions.each():
            if hyperbola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_hyperbola in hyperbola_questions.each():
                    if delete_hyperbola.val()["questionId"] == questionId_save:
                        keyId = delete_hyperbola.key()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_question").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_solution1").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_solution2").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_answer1").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_answer2").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("pre-assess").child("hyperbolaQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for substitution in substitution_questions.each():
            if substitution.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_substitution in substitution_questions.each():
                    if delete_substitution.val()["questionId"] == questionId_save:
                        keyId = delete_substitution.key()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("substitution_question").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("substitution_solution1").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("substitution_solution2").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("substitution_answer1").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("substitution_answer2").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("pre-assess").child("substitutionQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for elimination in elimination_questions.each():
            if elimination.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_elimination in elimination_questions.each():
                    if delete_elimination.val()["questionId"] == questionId_save:
                        keyId = delete_elimination.key()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("elimination_question").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("elimination_solution1").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("elimination_solution2").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("elimination_answer1").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("elimination_answer2").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("pre-assess").child("eliminationQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1

        if self.isCheck == 0:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
        else:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
            else:
                self.stackedWidget.setCurrentIndex(1)

    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()
class delete_postQuestion(QDialog):
    def __init__(self, parent):
        super(delete_postQuestion, self).__init__(parent)
        self.ui = Ui_logoutDialog()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("data/warningToLogout.ui",self)

        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Teacher"
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        global willLogout
        willLogout = 1
        self.logoutUpdatePages.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)

        self.unitTest1_delete_pushButton.clicked.connect(self.deleteFunction)
        self.unitTest1_cancel1_pushButton.clicked.connect(self.cancelFunction)

    def deleteFunction(self):
        self.isCheck = 0
        self.isCorrect = 1
        checking = self.unitTest1_textEdit.toPlainText()
        global questionId_save
        questionId_save = checking

        circle_questions = db.child("precal_questions").child("post-assess").child("circleQuestion").get()
        parabola_questions = db.child("precal_questions").child("post-assess").child("parabolaQuestion").get()
        ellipse_questions = db.child("precal_questions").child("post-assess").child("ellipseQuestion").get()
        hyperbola_questions = db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").get()
        substitution_questions = db.child("precal_questions").child("post-assess").child("substitutionQuestion").get()
        elimination_questions = db.child("precal_questions").child("post-assess").child("eliminationQuestion").get()

        global willLogout       
        for circle in circle_questions.each():
            if circle.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_circle in circle_questions.each():
                    if delete_circle.val()["questionId"] == questionId_save:
                        keyId = delete_circle.key()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("circle_1_question").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("circle_1_solution1").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("circle_1_solution2").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("circle_1_answer1").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("circle_1_answer2").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("post-assess").child("circleQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for parabola in parabola_questions.each():
            if parabola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_parabola in parabola_questions.each():
                    if delete_parabola.val()["questionId"] == questionId_save:
                        keyId = delete_parabola.key()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("parabola_question").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("parabola_solution1").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("parabola_solution2").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("parabola_answer1").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("parabola_answer2").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("post-assess").child("parabolaQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for ellipse in ellipse_questions.each():
            if ellipse.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_ellipse in ellipse_questions.each():
                    if delete_ellipse.val()["questionId"] == questionId_save:
                        keyId = delete_ellipse.key()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("ellipse_question").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("ellipse_solution1").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("ellipse_solution2").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("ellipse_answer1").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("ellipse_answer2").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("post-assess").child("ellipseQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for hyperbola in hyperbola_questions.each():
            if hyperbola.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_hyperbola in hyperbola_questions.each():
                    if delete_hyperbola.val()["questionId"] == questionId_save:
                        keyId = delete_hyperbola.key()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_question").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_solution1").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_solution2").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_answer1").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("hyperbola_answer2").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("post-assess").child("hyperbolaQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for substitution in substitution_questions.each():
            if substitution.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_substitution in substitution_questions.each():
                    if delete_substitution.val()["questionId"] == questionId_save:
                        keyId = delete_substitution.key()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("substitution_question").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("substitution_solution1").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("substitution_solution2").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("substitution_answer1").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("substitution_answer2").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("post-assess").child("substitutionQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1
        for elimination in elimination_questions.each():
            if elimination.val()["questionId"] == checking:
                willLogout = 0
                self.isCheck = 0
                self.isCorrect = 0
                for delete_elimination in elimination_questions.each():
                    if delete_elimination.val()["questionId"] == questionId_save:
                        keyId = delete_elimination.key()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("questionId").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("elimination_question").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("elimination_solution1").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("elimination_solution2").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("elimination_answer1").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("elimination_answer2").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("answerId").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("solutionId").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("isActive").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("answer_num").remove()
                        db.child("precal_questions").child("post-assess").child("eliminationQuestion").child(keyId).child("sol_num").remove()
            else:
                self.isCheck=1

        if self.isCheck == 0:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
        else:
            if self.isCorrect == 0:
                self.stackedWidget.setCurrentIndex(2)
            else:
                self.stackedWidget.setCurrentIndex(1)

    def cancelFunction(self):
        global willLogout
        willLogout = 0
        self.hide()
 
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
        
        self.logoutUpdatePages.setCurrentIndex(1)
        global willLogout 
        willLogout = 1
        self.yes_pushButton_2.clicked.connect(self.yesFunction)
        self.no_pushButton_2.clicked.connect(self.noFunction)

    def yesFunction(self):
        
        self.hide()
        self.parent().hide()
        self.toGoBack = toStudTeach()
        self.toGoBack.show()
    
    def noFunction(self):
        global willLogout 
        willLogout =0
        self.hide()
        
               
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
        
        self.next = toDashboardTeach()
        self.next.show()
##################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)   
    w = toStudTeach()
    w.show()
    sys.exit(app.exec_())

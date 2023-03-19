import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.uic import loadUi
from PyQt5.QtSvg import QSvgWidget
from graph import *
from io import BytesIO

import matplotlib.pyplot as plt

from studTeach import Ui_studTeachWindow
from studLogin import Ui_studLoginWindow
from studRegister import Ui_studRegisterWindow
from teachLogin import Ui_teachLoginWindow
from teachRegister import Ui_teachRegisterWindow
from dashboard import Ui_dashboardWindow
from dashboardTeach import Ui_dashboardTeachWindow
from forgotPassBoth import Ui_forgotPassBothWindow
from updateInfo import Ui_updateInfoDialog
from lessonDashboard import Ui_topicLessonMainWindow
from warningToLogout import Ui_logoutDialog
from graph import * 
from training import *
import time

import pyrebase
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

idKey = ""
assess_score = 0
unit1_score = 0
unit2_score = 0

#stud87313
#dummyemail@gmail.com
#thisispass

#560498750
#dummybot@gmail.com
#passisthis

#stud87343
#steveHernandez@gmail.com
#Stevie8912

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
                    # keyID = keyAccess.key()
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
                    self.toLogin = function()
                    self.toLogin.loading()

                else:
                    self.warning_Widget.setVisible(True)
                    self.warningPages.setCurrentIndex(0)
                    print("Invalid email or password.")

        except:
            # self.rightMenuContainer.setVisible(False)
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

        loadUi("forgotPassBoth.ui",self)
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
                    # print(student.key())
                    # print(student.val())
                    # studFname = (student.val()["fname"])
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

        loadUi("studRegister.ui",self)

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
       ,"isActive":isActive}
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

        loadUi("teachLogin.ui",self)

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
                    # keyID = keyAccess.key()
                    print("yes")

                    login= auth.sign_in_with_email_and_password(email,password)
                    login = auth.refresh(login['refreshToken'])
                    # now we have a fresh token
                    login['idToken']
                    print("Login Successfully")
                    print(auth.get_account_info(login['idToken']))

                    print(email)
                    print(password)
                    
                    self.hide()
                    self.toLogin = functionTeach()
                    self.toLogin.loading()
                else:
                    self.warning_Widget.setVisible(True)
                    print("Invalid email or password.")
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


class toTeachForgotPass(QMainWindow):
    def __init__(self):
        super(toTeachForgotPass, self).__init__()
        self.ui = Ui_forgotPassBothWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("forgotPassBoth.ui",self)
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
                    # print(student.key())
                    # print(student.val())
                    # studFname = (student.val()["fname"])
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

        loadUi("updateInfo.ui",self)
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

        loadUi("dashboard.ui",self)


        self.setWindowIcon(QIcon(":/images/logo.png"))
        title = "Mathguro Student"
        self.setWindowTitle(title)

        print(idKey)
        

        all_students = db.child("student").get()
        for student in all_students.each():
            if student.val()["studentSchoolID"] == idKey:
                # print(student.key())
                # print(student.val())
                studFname = (student.val()["fname"])
                studMname = (student.val()["mname"])
                studLname = (student.val()["lname"])
                studCourse = (student.val()["course"])
                studYear = (student.val()["year"])
                studSection = (student.val()["section"])
                studSchool = (student.val()["school"])

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
        self.lesson3_1Container.setVisible(False)
        self.lesson3_2Container.setVisible(False)
        self.lesson3_3Container.setVisible(False)

        self.lessonInfo1Container.setVisible(False)
        self.lessonInfo2Container.setVisible(False)
        self.lessonInfo3Container.setVisible(False)

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
        self.settings_pushButton.clicked.connect(self.showSettings)
        self.information_pushButton.clicked.connect(self.showInformation)
        self.help_pushButton.clicked.connect(self.showHelp)

        # MODULES BUTTONS
        self.module1_pushButton.clicked.connect(self.showModule1)
        self.module2_pushButton.clicked.connect(self.showModule2)
        # self.module4_pushButton.clicked.connect(self.showParabolaModules)

        # TOP SIDE BUTTONS
        self.profileMenu_pushButton.clicked.connect(self.showProfile)
        self.moreMenu_pushButton.clicked.connect(self.showMore)
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
        self.hide()
        self.unitTestConics = unitTest_1()
        self.unitTestConics.show()
    def unitTest2(self):
        self.hide()
        self.unitTestSys = unitTest_2()
        self.unitTestSys.show()

# PROFILE BUTTON FUNCTIONS
    def updateProfile(self):
        self.hide()
        self.toUpdateProf = toStudUpdateProfile()
        self.toUpdateProf.show()
    def logoutProfile(self):
        self.toLogoutStud = toStudLogout()
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

            with open("precalc_keywords.txt", "r", encoding='utf-8') as f:
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
    def showMore(self):
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
        self.rightMenuPages.setCurrentIndex(1)

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

    def showSettings(self):
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
        self.centerMenuPages.setCurrentIndex(0)
    
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
    def __init__(self):
        super(toStudLogout, self).__init__()
        self.ui = Ui_logoutDialog()
        
        # self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("warningToLogout.ui",self)

        self.setWindowModality(Qt.ApplicationModal)

        self.yes_pushButton.clicked.connect(self.yesFunction)
        self.no_pushButton.clicked.connect(self.noFunction)

    def yesFunction(self):
        print("YES PRESSED")
        sys.exit()
    
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

class topicLesson1(QMainWindow):
    def __init__(self):
        super(topicLesson1, self).__init__()
        self.ui = Ui_topicLessonMainWindow()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("lessonDashboard.ui",self)
        self.topicPages.setCurrentIndex(0)
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

        loadUi("lessonDashboard.ui",self)
        self.topicPages.setCurrentIndex(2)

        self.parabolaEx1PlotButton.clicked.connect(self.parabolaGraph1)
        self.parabolaEx2PlotButton.clicked.connect(self.parabolaGraph2)
        self.ellipseEx1PlotButton.clicked.connect(self.ellipseGraph1)
        self.ellipseEx2PlotButton.clicked.connect(self.ellipseGraph2)

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

        loadUi("lessonDashboard.ui",self)
        self.topicPages.setCurrentIndex(3)

        self.parabolaEx1PlotButton.clicked.connect(self.parabolaGraph1)
        self.parabolaEx2PlotButton.clicked.connect(self.parabolaGraph2)
        self.ellipseEx1PlotButton.clicked.connect(self.ellipseGraph1)
        self.ellipseEx2PlotButton.clicked.connect(self.ellipseGraph2)

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

        loadUi("lessonDashboard.ui",self)
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

        loadUi("lessonDashboard.ui",self)
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

        loadUi("lessonDashboard.ui",self)
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

        loadUi("lessonDashboard.ui",self)
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

        loadUi("lessonDashboard.ui",self)
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
        global assess_score
        assess_score = 0
        # Question 1, solution and answer
        question = "question_21_Solution"
        check_assess_q1_sol = chat(question, assess_sol_Q1)
        question = "question_21_Answer"
        check_assess_q1_ans = chat(question, assess_ans_Q1)
                
        if check_assess_q1_sol == "correct":
            assess_score = assess_score + 2
        if check_assess_q1_ans == "correct":
            assess_score = assess_score + 1

        # Question 2, solution and answer
        question = "question_22_Solution"
        check_assess_q2_sol = chat(question, assess_sol_Q2)
        question = "question_22_Answer"
        check_assess_q2_ans = chat(question, assess_ans_Q2)

        if check_assess_q2_sol == "correct":
            assess_score = assess_score + 2
        if check_assess_q2_ans == "correct":
            assess_score = assess_score + 1

        # Question 3, solution and answer
        question = "question_23_Solution"
        check_assess_q3_sol = chat(question, assess_sol_Q3)
        question = "question_23_Answer"
        check_assess_q3_ans = chat(question, assess_ans_Q3)

        if check_assess_q3_sol == "correct":
            assess_score = assess_score + 2
        if check_assess_q3_ans == "correct":
            assess_score = assess_score + 1

        # Question 4, solution and answer
        question = "question_24_Solution"
        check_assess_q4_sol = chat(question, assess_sol_Q4)
        question = "question_24_Answer"
        check_assess_q4_ans = chat(question, assess_ans_Q4)

        if check_assess_q4_sol == "correct":
            assess_score = assess_score + 2
        if check_assess_q4_ans == "correct":
            assess_score = assess_score + 1

        # Question 5, solution and answer
        question = "question_25_Solution"
        check_assess_q5_sol = chat(question, assess_sol_Q5)
        question = "question_25_Answer"
        check_assess_q5_ans = chat(question, assess_ans_Q5)

        if check_assess_q5_sol == "correct":
            assess_score = assess_score + 2
        if check_assess_q5_ans == "correct":
            assess_score = assess_score + 1
        
        print(assess_score)

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

        loadUi("lessonDashboard.ui",self)
        self.topicPages.setCurrentIndex(5)

        self.submitTest_Button.clicked.connect(self.submitTest)

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

    def submitTest(self):
        # Question 1 , answer and solution
        solution_Unit1_Q1 = self.unitTestQ1Sol_textEdit.toPlainText()
        answer1_Unit1_Q1 = self.unitTestQ1Center_textEdit.text()
        # Question 2 , answer and solution
        solution_Unit1_Q2 = self.unitTestQ2Sol_textEdit.toPlainText()
        answer1_Unit1_Q2 = self.unitTestQ2Center_textEdit.text()
        answer2_Unit1_Q2 = self.unitTestQ2Radius_textEdit.text()
        # Question 3 , answer and solution
        solution_Unit1_Q3 = self.unitTestQ3Sol_textEdit.toPlainText()
        answer1_Unit1_Q3 = self.unitTestQ3Vertex_textEdit.text()
        answer2_Unit1_Q3 = self.unitTestQ3Focus_textEdit.text()
        # Question 4 , answer and solution
        solution_Unit1_Q4 = self.unitTestQ4Sol_textEdit.toPlainText()
        answer1_Unit1_Q4 = self.unitTestQ4Vertex_textEdit.text()
        answer2_Unit1_Q4 = self.unitTestQ4Focus_textEdit.text()
        # Question 5 , answer and solution
        solution_Unit1_Q5 = self.unitTestQ5Sol_textEdit.toPlainText()
        answer1_Unit1_Q5 = self.unitTestQ5Center_textEdit.text()
        # Question 6 , answer and solution
        solution_Unit1_Q6 = self.unitTestQ6Sol_textEdit.toPlainText()
        answer1_Unit1_Q6 = self.unitTestQ6Foci1_textEdit.text()
        answer2_Unit1_Q6 = self.unitTestQ6Foci2_textEdit.text()
        # Question 7 , answer and solution
        solution_Unit1_Q7 = self.unitTestQ7Sol_textEdit.toPlainText()
        answer1_Unit1_Q7 = self.unitTestQ7Vertex1_textEdit.text()
        answer2_Unit1_Q7 = self.unitTestQ7Vertex2_textEdit.text()
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
        global unit1_score
        unit1_score = 0
        # Question 1, solution and answer
        question = "question_1_Solution"
        check_unit1_q1_sol = chat(question, solution_Unit1_Q1)
        question = "question_1_Answer"
        check_unit1_q1_ans = chat(question, answer1_Unit1_Q1)

        if check_unit1_q1_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q1_ans == "correct":
            unit1_score = unit1_score + 1  

        # Question 2, solution and answer
        question = "question_2_Solution"
        check_unit1_q2_sol = chat(question, solution_Unit1_Q2)
        question = "question_2_Center_Answer"
        check_unit1_q2_center_ans = chat(question, answer1_Unit1_Q2)
        question = "question_2_Radius_Answer"
        check_unit1_q2_radius_ans = chat(question, answer2_Unit1_Q2)

        if check_unit1_q2_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q2_center_ans == "correct":
            unit1_score = unit1_score + 1
        if check_unit1_q2_radius_ans == "correct":
            unit1_score = unit1_score + 1    

        # Question 3, solution and answer
        question = "question_3_Solution"
        check_unit1_q3_sol = chat(question, solution_Unit1_Q3)
        question = "question_3_Vertex"
        check_unit1_q3_vertex_ans = chat(question, answer1_Unit1_Q3)
        question = "question_3_Focus"
        check_unit1_q3_focus_ans = chat(question, answer2_Unit1_Q3)

        if check_unit1_q3_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q3_vertex_ans == "correct":
            unit1_score = unit1_score + 1
        if check_unit1_q3_focus_ans == "correct":
            unit1_score = unit1_score + 1    

        # Question 4, solution and answer
        question = "question_4_Solution"
        check_unit1_q4_sol = chat(question, solution_Unit1_Q4)
        question = "question_4_Vertex"
        check_unit1_q4_vertex_ans = chat(question, answer1_Unit1_Q4)
        question = "question_4_Focus"
        check_unit1_q4_focus_ans = chat(question, answer2_Unit1_Q4)

        if check_unit1_q4_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q4_vertex_ans == "correct":
            unit1_score = unit1_score + 1
        if check_unit1_q4_focus_ans == "correct":
            unit1_score = unit1_score + 1    

        # Question 5, solution and answer
        question = "question_5_Solution"
        check_unit1_q5_sol = chat(question, solution_Unit1_Q5)
        question = "question_5_Center"
        check_unit1_q5_vertex_ans = chat(question, answer1_Unit1_Q5)
        
        if check_unit1_q5_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q5_vertex_ans == "correct":
            unit1_score = unit1_score + 1

        # Question 6, solution and answer
        question = "question_6_Solution"
        check_unit1_q6_sol = chat(question, solution_Unit1_Q6)
        question = "question_6_Foci1"
        check_unit1_q6_foci1_ans = chat(question, answer1_Unit1_Q6)
        question = "question_6_Foci2"
        check_unit1_q6_foci2_ans = chat(question, answer2_Unit1_Q6)

        if check_unit1_q6_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q6_foci1_ans == "correct":
            unit1_score = unit1_score + 1
        if check_unit1_q6_foci2_ans == "correct":
            unit1_score = unit1_score + 1    

        # Question 7, solution and answer
        question = "question_7_Solution"
        check_unit1_q7_sol = chat(question, solution_Unit1_Q7)
        question = "question_7_Vertex1"
        check_unit1_q7_vertex1_ans = chat(question, answer1_Unit1_Q7)
        question = "question_7_Vertex2"
        check_unit1_q7_vertex2_ans = chat(question, answer2_Unit1_Q7)

        if check_unit1_q7_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q7_vertex1_ans == "correct":
            unit1_score = unit1_score + 1
        if check_unit1_q7_vertex2_ans == "correct":
            unit1_score = unit1_score + 1            

        # Question 8, solution and answer
        question = "question_8_Solution"
        check_unit1_q8_sol = chat(question, solution_Unit1_Q8)
        question = "question_8_Center"
        check_unit1_q8_center_ans = chat(question, answer1_Unit1_Q8)

        if check_unit1_q8_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q8_center_ans == "correct":
            unit1_score = unit1_score + 1

        # Question 9, solution and answer
        question = "question_9_Solution"
        check_unit1_q9_sol = chat(question, solution_Unit1_Q9)
        question = "question_9_MinorAxis"
        check_unit1_q9_minorAxis_ans = chat(question, answer1_Unit1_Q9)

        if check_unit1_q9_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q9_minorAxis_ans == "correct":
            unit1_score = unit1_score + 1

        # Question 10, solution and answer
        question = "question_10_Solution"
        check_unit1_q10_sol = chat(question, solution_Unit1_Q10)
        question = "question_10_Foci1"
        check_unit1_q10_standEquat_ans = chat(question, answer1_Unit1_Q10)

        if check_unit1_q10_sol == "correct":
            unit1_score = unit1_score + 2
        if check_unit1_q10_standEquat_ans == "correct":
            unit1_score = unit1_score + 1
        
        print(unit1_score)

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

        loadUi("lessonDashboard.ui",self)
        self.topicPages.setCurrentIndex(11)

        self.submitTest2_Button.clicked.connect(self.submitTest2)

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
        global unit2_score
        unit2_score = 0
        # Question 1, solution and answer
        question = "question_11_Solution"
        check_unit2_q1_sol = chat(question, solution_Unit2_Q1)
        question = "question_11_Answer"
        check_unit2_q1_ans = chat(question, answer1_Unit2_Q1)

        if check_unit2_q1_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q1_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 2, solution and answer
        question = "question_12_Solution"
        check_unit2_q2_sol = chat(question, solution_Unit2_Q2)
        question = "question_12_Answer"
        check_unit2_q2_ans = chat(question, answer1_Unit2_Q2)

        if check_unit2_q2_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q2_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 3, solution and answer
        question = "question_13_Solution"
        check_unit2_q3_sol = chat(question, solution_Unit2_Q3)
        question = "question_13_Answer"
        check_unit2_q3_ans = chat(question, answer1_Unit2_Q3)

        if check_unit2_q3_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q3_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 4, solution and answer
        question = "question_14_Solution"
        check_unit2_q4_sol = chat(question, solution_Unit2_Q4)
        question = "question_14_Answer"
        check_unit2_q4_ans = chat(question, answer1_Unit2_Q4)

        if check_unit2_q4_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q4_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 5, solution and answer
        question = "question_15_Solution"
        check_unit2_q5_sol = chat(question, solution_Unit2_Q5)
        question = "question_15_Answer"
        check_unit2_q5_ans = chat(question, answer1_Unit2_Q5)

        if check_unit2_q5_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q5_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 6, solution and answer
        question = "question_16_Solution"
        check_unit2_q6_sol = chat(question, solution_Unit2_Q6)
        question = "question_16_Answer"
        check_unit2_q6_ans = chat(question, answer1_Unit2_Q6)

        if check_unit2_q6_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q6_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 7, solution and answer
        question = "question_17_Solution"
        check_unit2_q7_sol = chat(question, solution_Unit2_Q7)
        question = "question_17_Answer"
        check_unit2_q7_ans = chat(question, answer1_Unit2_Q7)

        if check_unit2_q7_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q7_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 8, solution and answer
        question = "question_18_Solution"
        check_unit2_q8_sol = chat(question, solution_Unit2_Q8)
        question = "question_18_Answer"
        check_unit2_q8_ans = chat(question, answer1_Unit2_Q8)

        if check_unit2_q8_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q8_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 9, solution and answer
        question = "question_19_Solution"
        check_unit2_q9_sol = chat(question, solution_Unit2_Q9)
        question = "question_19_Answer"
        check_unit2_q9_ans = chat(question, answer1_Unit2_Q9)

        if check_unit2_q9_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q9_ans == "correct":
            unit2_score = unit2_score + 1  

        # Question 10, solution and answer
        question = "question_20_Solution"
        check_unit2_q10_sol = chat(question, solution_Unit2_Q10)
        question = "question_20_Answer"
        check_unit2_q10_ans = chat(question, answer1_Unit2_Q10)

        if check_unit2_q10_sol == "correct":
            unit2_score = unit2_score + 2
        if check_unit2_q10_ans == "correct":
            unit2_score = unit2_score + 1  

        print(unit2_score)

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

class splashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("loadingScreen.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        pixmap = QPixmap("load1.jpg")
        self.setPixmap(pixmap)
    def mousePressEvent(self, event):
        pass

    
class toTeachUpdateProfile(QDialog):
    def __init__(self):
        super(toTeachUpdateProfile, self).__init__()
        self.ui = Ui_updateInfoDialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("updateInfo.ui",self)
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

        loadUi("dashboardTeach.ui",self)

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
        self.settings_pushButton.clicked.connect(self.showSettings)
        self.information_pushButton.clicked.connect(self.showInformation)
        self.help_pushButton.clicked.connect(self.showHelp)

        # TOP SIDE BUTTONS
        self.profileMenu_pushButton.clicked.connect(self.showProfile)
        self.moreMenu_pushButton.clicked.connect(self.showMore)
        self.closeRightMenu_pushButton.clicked.connect(self.hideRightMenu)
        
        # PROFILE BUTTON FUNCTIONS 
        self.updateAcc_pushButton.clicked.connect(self.updateProfile)
        self.logoutAcc_pushButton.clicked.connect(self.logoutProfile)

        QSizeGrip(self.sizeGrip)

        # PROFILE BUTTON FUNCTIONS
    def updateProfile(self):
        self.hide()
        self.toUpdateProf = toTeachUpdateProfile()
        self.toUpdateProf.show()
    def logoutProfile(self):
        self.tologoutProf = toTeachLogout()
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
    def showMore(self):
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
        self.rightMenuPages.setCurrentIndex(1)

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
        # self.lessonsContainer.setVisible(False)

    def showSettings(self):
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
        self.centerMenuPages.setCurrentIndex(0)
    
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
    def __init__(self):
        super(toTeachLogout, self).__init__()
        self.ui = Ui_logoutDialog()
        
        # self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.offset = None

        loadUi("warningToLogout.ui",self)

        self.setWindowModality(Qt.ApplicationModal)

        self.yes_pushButton.clicked.connect(self.yesFunction)
        self.no_pushButton.clicked.connect(self.noFunction)

    def yesFunction(self):
        print("YES PRESSED")
        sys.exit()
    
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

class functionTeach:
    def loading(self):
        self.screen = toSplashScreen()
        self.screen.show()
        for i in range(100):
            self.screen.progressBar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.1)
        self.screen.close()
        print("yes")
        self.next = toDashboardTeach()
        self.next.show()

class toSplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("loadingScreen.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        pixmap = QPixmap("load1.jpg")
        self.setPixmap(pixmap)
    def mousePressEvent(self, event):
        pass
##################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # # Show message box then Exit App if no system tray was detected
    # if not QSystemTrayIcon.isSystemTrayAvailable():
    #     QMessageBox.critical(None, "System Tray", "System tray was not detected!")
    #     sys.exit(1)

    # # Do not completely exit the app when the last window is closed
    # # Change value to true if you want to full exit the app
    # app.setQuitOnLastWindowClosed(False)

    # # Create System Tray
    # tray = QSystemTrayIcon(QIcon(u":/images/logo.png"), app)
    # # Create Tray Action Menu
    # menu = QMenu()
    # # Add Action to Tray
    # # Show message box action
    # # action_message_box = QAction("Show a message box")
    # # menu.addAction(action_message_box)

    # # Hide Window Action
    # action_hide = QAction("Hide Window")
    # menu.addAction(action_hide)

    # # Show Window Action
    # action_show = QAction("Show Window")
    # menu.addAction(action_show)

    # # Exit App Action
    # action_exit = QAction("Exit")
    # action_exit.triggered.connect(app.exit)
    # menu.addAction(action_exit)

    # # Add Context menu to Tray
    # tray.setContextMenu(menu)
    # # Show tray
    # tray.show()

    w = toStudTeach()
    # w = toDashboard()
    # w = toStudLogout()
    w.show()
    sys.exit(app.exec_())








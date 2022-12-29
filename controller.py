import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

from studTeachButton import Ui_studTeachWindow
from studLogin import Ui_studLoginWindow
from studRegister import Ui_studRegisterWindow
from teachLogin import Ui_teachLoginWindow
from teachRegister import Ui_teachRegisterWindow

class studTeach(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_studTeachWindow()
        self.ui.setupUi(self)
    
    def toStudLogin(self):
        self.toStud = studLogin()
        self.toStud.show()
        self.hide()
    
    def toTeachLogin(self):
        self.toStud = teachLogin()
        self.toStud.show()
        self.hide()
        
    def toExitProg(self):
        sys.exit()

class studLogin(QMainWindow):
    # DISPLAY
    def __init__(self):
        super().__init__()
        self.ui = Ui_studLoginWindow()
        self.ui.setupUi(self)
    
    # TO REGISTER
    def toRegister(self):
        self.toRegis = studRegister()
        self.toRegis.show()
        self.hide()

    # FORGOT ACCOUNT
    def forgetAcc(self):
        print("STUDENT FORGOT ACCOUNT")

    # LOG IN ACCOUNT
    def toLogToApp(self):
        print("STUDENT LOG IN TO APP")

    # GO TO MAIN
    def goBack(self):
        self.toStudTeach = studTeach()
        self.toStudTeach.show()
        self.hide()

    # TERMINATE APP
    def toExitProg(self):
        sys.exit()

class studRegister(QMainWindow):
    # DISPLAY
    def __init__(self):
        super().__init__()
        self.ui = Ui_studRegisterWindow()
        self.ui.setupUi(self)

    # REGISTER TO DB
    def toRegisterDb(self):
        # self.toRegis = teachLogin()
        # self.toRegis.show()
        # self.hide()
        print ("STUDENT REGISTER ACCOUNT")

    # GO TO LOGIN SCREEN
    def goBack(self):
        self.toLogin = studLogin()
        self.toLogin.show()
        self.hide()

    # GO BACK
    def toExitProg(self):
        sys.exit()

class teachLogin(QMainWindow):
    # DISPLAY
    def __init__(self):
        super().__init__()
        self.ui = Ui_teachLoginWindow()
        self.ui.setupUi(self)
    
    # TO REGISTER ACCOUNT
    def toRegister(self):
        self.toRegis = teachRegister()
        self.toRegis.show()
        self.hide()

    # FORGOT ACCOUNT
    def forgetAcc(self):
        print("TEACHER FORGET ACCOUNT")

    # LOG IN ACCOUNT
    def toLogToApp(self):
        print("TEACHER LOG IN TO APP")

    # GO TO MAIN
    def goBack(self):
        self.toStudTeach = studTeach()
        self.toStudTeach.show()
        self.hide()

    # TO TERMINATE APP
    def toExitProg(self):
        sys.exit()

class teachRegister(QMainWindow):
    # DISPLAY
    def __init__(self):
        super().__init__()
        self.ui = Ui_teachRegisterWindow()
        self.ui.setupUi(self)

    # REGISTER TO DB
    def toRegisterDb(self):
        # self.toRegis = teachLogin()
        # self.toRegis.show()
        # self.hide()
        print("TEACHER REGISTER ACCOUNT")

    # GO TO LOGIN SCREEN
    def goBack(self):
        self.toLogin = teachLogin()
        self.toLogin.show()
        self.hide()

    # GO BACK
    def toExitProg(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = studTeach()
    w.show()
    sys.exit(app.exec_())



















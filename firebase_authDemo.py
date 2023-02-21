import pyrebase

#dummyemail@gmail.com
#thisispass

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

    ######################### login signup ########################
# def signup():
#     print("Signup...")
#     email=input("Enter email: ")
#     password=input("Enter password: ")
#     try:
#         user= auth.create_user_with_email_and_password(email, password)
#         print("Signup Successfully")
#     except:
#         print("Email already exists!")

# def login():
#     print("Log in...")
#     email = input("Enter email: ")
#     password = input("Enter password: ")
#     try:
#         login= auth.sign_in_with_email_and_password(email,password)
#         print("Login Successfully")
#         print(auth.get_account_info(login['idToken']))
#     except:
#         print("Invalid email or password.")
# ans = input("Are you a new user?[y/n]")
# if ans=='y':
#     signup()
# elif ans == 'n':
#     login()


######################## ADD DATA #######################
# Teacher
#   STEM
#     fname,mname,lname,course,teachSchoolID,school,email,isActive
#   ABM
#   HUMSS
#   GAS

# fname= "juan"
# mname = "A."
# lname = "gallardo"
# course = "STEM"
# teachSchoolID = "560498750"
# school = "Delpa" 
# email = "dummybot@gmail.com"
# isActive = "1"

# data ={"fname":fname,"mname":mname,"lname":lname, "course":course
#        ,"teachSchoolID":teachSchoolID,"school":school,"email":email
#        ,"isActive":isActive}
# db.child("teacher").push(data)

# Student
#   STEM
#     11 = fname,mname,lname,course,yr,section,school,email,
#     12
#   ABM
#     11
#     12
#   HUMSS
#     11
#     12
#   GAS
#     11
#     12

# fname= "patrick"
# mname = "A."
# lname = "gallardo"
# course = "STEM"
# year = "11"
# section = "A"
# studentSchoolID = "stud87313"
# school = "Delpa" 
# email = "dummyemail@gmail.com"
# isActive = "1"

# data ={"fname":fname,"mname":mname,"lname":lname, "course":course
#        ,"year":year,"section":section,"studentSchoolID":studentSchoolID,"school":school,"email":email
#        ,"isActive":isActive}
# db.child("student").push(data)
############################## ADD #####################################

######################### UPDATE #####################################
# course = "ABM"
# teachKey = db.child("teacher").get()
# for keyAccess in teachKey.each():
#     if keyAccess.val()["teachSchoolID"] == teachSchoolID:
#         keyID = keyAccess.key()
# db.child("teacher").child(keyID).update({"course":course})

#     if(keyAccess().val["teachSchoolID"]=="560498750"):
#       keyID = keyAccess.key()
#      # keyVal = keyAccess.val() 
# db.child("teacher").child(keyID).update("course")
######################## UPDATE ########################################

################################## DELETE ####################################
# teachKey = db.child("teacher").get()
# for keyAccess in teachKey.each():
    # if(keyAccess.val()["teachSchoolID"]=="560498750"):
#       keyID = keyAccess.key()
#      # keyVal = keyAccess.val()
# db.child("teacher").child(keyID).remove("course")

# course = "ABM"
# teachKey = db.child("teacher").get()
# for keyAccess in teachKey.each():
#     if keyAccess.val()["teachSchoolID"] == teachSchoolID:
#         keyID = keyAccess.key()

# db.child("teacher").child(keyID).remove("course")

################################## DELETE ####################################

##################################  RETRIEVE #############################################
# teachData = db.child("teacher").get()
# for teachCount in teachData.each():
#     print(teachCount.val())
#   if(teachCount()["teachSchoolID"]=="560498750"):
#     print("yes")
  #   keyID = teachCount.key()
  #   print(keyID)

################################ COMPARE ######################

# teachKey = db.child("teacher").get()
# for keyAccess in teachKey.each():
#     if keyAccess.val()["teachSchoolID"] == teachSchoolID:
#         keyID = keyAccess.key()
#         print("yes")

##################################  RETRIEVE #############################################

# all_teachers = db.child("teacher").get()
# for teacher in all_teachers.each():
#   # print(teacher.key())
#   # print(teacher.val())
#   teachID = (teacher.val()["teachSchoolID"])
# print(teachID)

# class yellow:
#   def studIDSave(self):
#     return("stud87343")

# saveID = yellow()
# studentIDSave = saveID.studIDSave()
# print(studentIDSave)

# saveID = toStudLogin()
# studentIDSave = saveID.studIDSave()


# all_students = db.child("student").get()
# for student in all_students.each():
#   if student.val()["studentSchoolID"] == teachSchoolID:
#     # print(student.key())
#     print(student.val())
#     # studID = (student.val()["studentSchoolID"])
# # print(studID)


##################################  RETRIEVE #############################################

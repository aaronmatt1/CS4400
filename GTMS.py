##GTMS UI

from tkinter import *
from tkinter import messagebox as mbox
import base64
import pymysql

class GTMS:
    def __init__(self, win):

        self.connect()

    # def loginPage(self):
    #
    #     topFrame = Frame(LogWin)
    #     topFrame.grid(row=0, colum=0)
    #     topFrame.configure(background='#c1a82f')
    #     bottomFrame = Fram(LogWin)
    #     bottomFrame.grid(row=1, column=0)
    #
    #     Label(text="Georgia Tech Medical Center System", font=('Arial', 20)).pack

    #def newPatientPage(self):

    def connect(self):

        try:
            self.db = pymysql.connect(host="academic-mysql.cc.gatech.edu", #connecting to the database
                                passwd='KDKR2YQY', user='cs4400_Group_65',
                                db='cs4400_Group_65')
            self.c = self.db.cursor()



        except:

            mbox.showerror(title='Connection Error', message='Check your internet connection')
            return NONE

        query = 'INSERT INTO USER(Username, Password) VALUES("FlorianF", "12345")'
        self.c.execute(query)

        query = 'INSERT INTO PATIENT(Name,HomePhone,Username,DOB,Gender,Address,WorkPhone,Height,Weight)' \
                'VALUES("Florian Foerester","706-595-1000", "FF123", "1986-04-01", "M", "1423 Burgamy Ln.", "706-222-9373", "62", "180")'
        self.c.execute(query)
        self.db.close()

LogWin = Tk()
LogWin.title('GTMS Login')
obj = GTMS(LogWin)
LogWin.mainloop()


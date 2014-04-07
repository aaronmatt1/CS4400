##GTMS UI

from tkinter import *
from tkinter import messagebox as mbox
import base64
import pymysql

class GTMS:
    def __init__(self, win):

        self.connect()

        self.patientProfile()

    # def loginPage(self):
    #
    #     topFrame = Frame(LogWin)
    #     topFrame.grid(row=0, colum=0)
    #     topFrame.configure(background='#c1a82f')
    #     bottomFrame = Frame(LogWin)
    #     bottomFrame.grid(row=1, column=0)
    #
    #     Label(text="Georgia Tech Medical Center System", font=('Arial', 20)).pack

    def patientProfile(self):
        #very rough, dont have the top dow quite yet. It looks pretty poopish, but the rest is pretty good
        self.patientWin = Toplevel(LogWin)
        self.patientWin.title('Patient Profile')
        self.patientWin.configure(background='#cfb53b')

        topFrame = Frame(self.patientWin, bd=10)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        bottomFrame = Frame(self.patientWin)
        bottomFrame.grid(row=1, column=0)
        bottomFrame.configure(background='#cfb53b')

        pageName = Label(topFrame, text="Patient Profile", font=("Arial", 25))
        pageName.grid(row=0, column=0)
        pageName.configure(background='#cfb53b')

        logo = PhotoImage(file='gatech_logo.gif')
        imageLabel = Label(topFrame, image=logo)
        imageLabel.image = logo
        imageLabel.grid(row=0, column=1)
        imageLabel.configure(background='#cfb53b')

        #creating labels and entry boxes to be added to window in loop
        attributes = {
            'nameLabel': ['Patient Name: ', 'self.nameEntry'],
            'dobLabel': ['Date of Birth: ', 'self.dobEntry'],
            'addressLabel': ['Address: ', 'self.addressEntry'],
            'homePhoneLabel': ['Home Phone: ', 'self.homePhoneEntry'],
            'workPhoneLabel': ['Work Phone: ', 'self.workPhoneEntry'],
            'weightLabel': ['Weight: ', 'self.weightEntry'],
            'heightLabel': ['Height: ', 'self.heightEntry'],
            'allergiesLabel': ['Allergies: ', 'self.allergiesEntry']
        }

        #setting up pulldowns for gender and income
        self.gender = StringVar()
        self.gender.set(NONE)

        self.annualIncome = StringVar()
        self.annualIncome.set(NONE)

        #going to change the dict to a list. dicts arent ordered, so labels come out in random order
        rows = 0
        for x in attributes.keys():

            labelname = x
            entryname = attributes[x][1]
            labelname = Label(bottomFrame, text=attributes[x][0])
            labelname.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
            labelname.configure(background='#cfb53b')
            entryname = Entry(bottomFrame, width=30)
            entryname.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")

            rows += 1

            #little bit of hardcoding
            if rows == 2:
                genderLabel = Label(bottomFrame, text="Gender: ")
                genderLabel.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
                genderLabel.configure(background='#cfb53b')
                self.genderPulldown = OptionMenu(bottomFrame, self.gender, 'Male', 'Female')
                self.genderPulldown.config(width=20)
                self.genderPulldown.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")
                self.genderPulldown.configure(background='#999')
                rows += 1
            elif rows == 8:
                incomeLabel = Label(bottomFrame, text="Annual Income: ")
                incomeLabel.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
                incomeLabel.configure(background='#cfb53b')
                self.incomePulldown = OptionMenu(bottomFrame,
                                                 self.annualIncome,
                                                 '0-15000', '15000-30000', '30000-50000', '50000-75000', '75000-100000',
                                                 '100000+')
                self.incomePulldown.config(width=20)
                self.incomePulldown.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")
                self.incomePulldown.configure(background='#999')
                rows += 1

        addAllergies = Button(bottomFrame, text='+', height=1)
        addAllergies.grid(row=9, column=2)

        submit = Button(bottomFrame, text='Submit')
        submit.grid(row=11, column=3)







    def connect(self):

        try:
            self.db = pymysql.connect(host="academic-mysql.cc.gatech.edu", #connecting to the database
                                passwd='KDKR2YQY', user='cs4400_Group_65',
                                db='cs4400_Group_65')
            self.c = self.db.cursor()



        except:

            mbox.showerror(title='Connection Error', message='Check your internet connection')
            return NONE



LogWin = Tk()
LogWin.title('GTMS Login')
obj = GTMS(LogWin)
LogWin.mainloop()


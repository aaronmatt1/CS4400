##GTMRS UI

from tkinter import *
from tkinter import messagebox as mbox
import urllib.request
import base64
import pymysql

class GTMRS:
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
    
    def LoginPage(self, LogWin):
        #Yellow Jacket Logo
        url = 'http://comparch.gatech.edu/buzz.gif'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        pic = response.read()
        b64_data = base64.encodebytes(pic)
        self.photo = PhotoImage(data=b64_data)

        #Top Banner         
        banner = Label(LogWin, bg=color, width=450, height=50, text='Login', padx=10, font=('Berlin Sans FB', 18), 
                        image=self.photo, compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=4)
        
        #Main Body
        username_label = Label(LogWin, text='Username: ',  bg=color)
        username_label.grid(row=1, column=1, sticky=E, pady=20)

        self.username_entry = Entry(LogWin)
        self.username_entry.grid(row=1, column=2, sticky=W)

        password_label = Label(LogWin, text='Password: ',  bg=color)
        password_label.grid(row=2, column=1, sticky=E, pady=10)

        self.password_entry = Entry(LogWin, show='*')
        self.password_entry.grid(row=2,column=2, sticky=W)

        login = Button(LogWin, text='Login', width=10, cursor='hand2')
        login.grid(row=3,column=2,sticky=E)

        register = Button(LogWin, text='Register', width=10, cursor='hand2', command=self.Register)
        register.grid(row=3,column=3,sticky=W)
        
    def Register(self):
        LogWin.iconify()
        self.reg = Toplevel()
        reg = self.reg
        reg.title('GTMRS New User Registration')
        reg.config(bg=color)
        
        #Top Banner
        banner = Label(reg, bg=color, width=450, height=50, text='New User Registration', padx=10, 
                        font=('Berlin Sans FB', 18), image=self.photo, compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=4)
        
        #Main Body
        username_label = Label(reg, text='Username: ', bg=color, padx=10, pady=10)
        username_label.grid(row=1, column=1, sticky=W)

        self.username_entry = Entry(reg, width=30)
        self.username_entry.grid(row=1, column=2)
        
        password_label = Label(reg, text='Password: ', bg=color, padx=10)
        password_label.grid(row=2, column=1, sticky=W)

        self.password_entry = Entry(reg, width=30, show='*')
        self.password_entry.grid(row=2, column=2)

        confirm_label = Label(reg, text='Confirm Password: ', bg=color, padx=10, pady=10)
        confirm_label.grid(row=3, column=1, sticky=W)
        
        self.confirm_entry = Entry(reg, width=30, show='*')
        self.confirm_entry.grid(row=3, column=2)

        user_type_label = Label(reg, text='Type of User: ', bg=color, padx=10)
        user_type_label.grid(row=4,column=1, sticky=W)
        
        #User Type Pulldown Menu
        self.userType = StringVar()
        self.userType.set('Select User Type')
        types = ['Doctor', 'Patient', 'Administrative Personnel']
        userTypeMenu = OptionMenu(reg, self.userType, *types)
        userTypeMenu.grid(row=4,column=2, sticky=N)
        
        #Register Button
        register = Button(reg, text='Register', command=self.RegisterNew, cursor='hand2')
        register.grid(row=5, column=2, sticky=E, pady=10)
        
        #Cancel Button: Return To Login
        cancel = Button(reg, text='Cancel', command=self.BackToLogin(reg), cursor='hand2')
        cancel.grid(row=5, column=3, sticky=W, pady=10)

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
        attributes = [
            ['nameLabel', 'Patient Name: ', 'self.nameEntry'],
            ['dobLabel', 'Date of Birth: ', 'self.dobEntry'],
            ['addressLabel', 'Address: ', 'self.addressEntry'],
            ['homePhoneLabel', 'Home Phone: ', 'self.homePhoneEntry'],
            ['workPhoneLabel', 'Work Phone: ', 'self.workPhoneEntry'],
            ['weightLabel', 'Weight: ', 'self.weightEntry'],
            ['heightLabel', 'Height: ', 'self.heightEntry'],
            ['allergiesLabel', 'Allergies: ', 'self.allergiesEntry']
        ]

        #setting up pulldowns for gender and income
        self.gender = StringVar()
        self.gender.set(NONE)

        self.annualIncome = StringVar()
        self.annualIncome.set(NONE)

        #changed from dict to list, hopefullythis still works
        rows = 0
        for x in range(len(attributes)):

            labelname = attributes[x][0]
            entryname = attributes[x][2]
            labelname = Label(bottomFrame, text=attributes[x][1])
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
    
    #Function Handle to return to Login Window
    def BackToLogin(self, currentWin):
        currentWin.iconify()
        LogWin.deiconify()

LogWin = Tk()
color='#FFFF99'
LogWin.title('GTMRS Login')
obj = GTMRS(LogWin)
LogWin.mainloop()


##GTMS UI

from tkinter import *
from tkinter import messagebox as mbox
from tkinter import ttk
import urllib.request
import base64
import pymysql

class GTMS:
    def __init__(self, win):

        self.connect()
        self.db.close() #get rid of this before trying to write to/read from DB

        url = 'http://comparch.gatech.edu/buzz.gif'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        pic = response.read()
        b64_data = base64.encodebytes(pic)
        self.photo = PhotoImage(data=b64_data)

        self.LoginPage(LogWin)

        self.patientProfile()
        self.patientWin.withdraw()

        self.Register()
        self.reg.withdraw()

        self.doctorProfile()
        self.doctorWin.withdraw()

        self.appoinmentPage()

        self.homePage()
        self.hpWin.withdraw()

    def LoginPage(self, LogWin):

        #Top Banner
        banner = Label(LogWin, bg='#cfb53b', width=450, height=50, text='GTMS Login', padx=10, font=('Berlin Sans FB', 18),
                   image=self.photo, compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=4)

        #Main Body
        username_label = Label(LogWin, text='Username:      ',  bg='#cfb53b')
        username_label.grid(row=1, column=1, sticky=E, pady=20)

        self.username_entry = ttk.Entry(LogWin, width=35)
        self.username_entry.grid(row=1, column=2, sticky=W)

        password_label = Label(LogWin, text='Password:      ',  bg='#cfb53b')
        password_label.grid(row=2, column=1, sticky=E, pady=10)

        self.password_entry = ttk.Entry(LogWin, show='*', width=35)
        self.password_entry.grid(row=2, column=2, sticky=W)

        login = ttk.Button(LogWin, text='Login', width=5, cursor='hand2')
        login.grid(row=3, column=3, sticky=EW, padx=5, pady=5)

        register = ttk.Button(LogWin, text='Register', width=10, cursor='hand2')
        register.grid(row=4, column=3, sticky=EW, padx=5, pady=5)

    def Register(self):

        self.reg = Toplevel(LogWin)
        self.reg = self.reg
        self.reg.title('GTMRS New User Registration')
        self.reg.config(bg='#cfb53b')

        #Top Banner
        banner = Label(self.reg, bg='#cfb53b', width=450, height=50, text='New User Registration', padx=10,
                   font=('Berlin Sans FB', 18), image=self.photo, compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=6)

        #Main Body
        username_label = Label(self.reg, text='Username: ', bg='#cfb53b', padx=10, pady=10)
        username_label.grid(row=1, column=1, sticky=W)

        self.username_entry = Entry(self.reg, width=30)
        self.username_entry.grid(row=1, column=2, columnspan=3, sticky=EW)

        password_label = Label(self.reg, text='Password: ', bg='#cfb53b', padx=10)
        password_label.grid(row=2, column=1, sticky=W)

        self.password_entry = Entry(self.reg, width=30, show='*')
        self.password_entry.grid(row=2, column=2, columnspan=3, sticky=EW)

        confirm_label = Label(self.reg, text='Confirm Password: ', bg='#cfb53b', padx=10, pady=10)
        confirm_label.grid(row=3, column=1, sticky=W)

        self.confirm_entry = Entry(self.reg, width=30, show='*')
        self.confirm_entry.grid(row=3, column=2, columnspan=3, sticky=EW)

        user_type_label = Label(self.reg, text='Type of User: ', bg='#cfb53b', padx=10)
        user_type_label.grid(row=4,column=1, sticky=W)

        self.usertype = StringVar()
        #User Type Pulldown Menu
        self.userType = StringVar()
        self.userType.set('Select User Type')
        types = ['Doctor', 'Patient', 'Administrative Personnel']
        userTypeMenu = ttk.Combobox(self.reg, textvariable=self.userType, values=types)
        userTypeMenu.grid(row=4, column=2, columnspan=3, sticky='NEW')

        #Register Button
        register = ttk.Button(self.reg, text='Register')#, command=self.RegisterNew, cursor='hand2')
        register.grid(row=5, column=2, sticky=EW, pady=10, padx=5)
        #Cancel Button: Return To Login
        cancel = ttk.Button(self.reg, text='Cancel')#, command=self.BackToLogin(reg), cursor='hand2')
        cancel.grid(row=5, column=3, sticky=EW, pady=10, padx=5)

    def patientProfile(self):

        self.patientWin = Toplevel(LogWin)
        self.patientWin.title('Patient Profile')
        self.patientWin.configure(background='#cfb53b')

        topFrame = Frame(self.patientWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.patientWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.patientWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Patient Profile", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #creating labels and entry boxes to be added to window in loop
        attributes = [
            '          Patient Name: ',
            '          Date of Birth: ',
            '          Address: ',
            '          Home Phone: ',
            '          Work Phone: ',
            '          Weight: ',
            '          Height(in inches): ',
            '          Allergies: '
        ]


        #setting up pulldowns for gender and income
        self.gender = StringVar()
        self.gender.set('--Select Your Gender--')

        self.annualIncome = StringVar()
        self.annualIncome.set('--Select Your Annual Income--')

        #its working, but label names are not coming out in any specific order. Any ideas?
        rows = 0
        for x in range(len(attributes)):

            labelname = Label(bottomFrame, text=attributes[x])
            labelname.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
            labelname.configure(background='#cfb53b')
            rows += 1

            #little bit of hardcoding
            if rows == 2:
                genderLabel = Label(bottomFrame, text="          Gender: ")
                genderLabel.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
                genderLabel.configure(background='#cfb53b')
                self.genderPulldown = ttk.Combobox(bottomFrame, textvariable=self.gender, values=['Male','Female'])
                self.genderPulldown.config(width=20)
                self.genderPulldown.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")
                self.genderPulldown.configure(background='#999')
                self.genderPulldown.config(state='readonly')
                rows += 1
            elif rows == 8:
                incomeLabel = Label(bottomFrame, text="          Annual Income: ")
                incomeLabel.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
                incomeLabel.configure(background='#cfb53b')
                incomes = ['0-15000', '15000-30000', '30000-50000', '50000-75000', '75000-100000', '100000+']
                self.incomePulldown = ttk.Combobox(bottomFrame, textvariable=self.annualIncome, values=incomes)
                self.incomePulldown.config(width=20)
                self.incomePulldown.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")
                self.incomePulldown.configure(background='#999')
                self.incomePulldown.config(state='readonly')
                rows += 1

        self.nameEntry = ttk.Entry(bottomFrame, width=30)
        self.nameEntry.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        self.dobEntry = ttk.Entry(bottomFrame, width=30)
        self.dobEntry.grid(row=1, column=1, padx=10, pady=10, sticky="NSEW")

        self.addressEntry = ttk.Entry(bottomFrame, width=30)
        self.addressEntry.grid(row=3, column=1, padx=10, pady=10, sticky="NSEW")

        self.homePhoneEntry = ttk.Entry(bottomFrame, width=30)
        self.homePhoneEntry.grid(row=4, column=1, padx=10, pady=10, sticky="NSEW")

        self.workPhoneEntry = ttk.Entry(bottomFrame, width=30)
        self.workPhoneEntry.grid(row=5, column=1, padx=10, pady=10, sticky="NSEW")

        self.weightEntry = ttk.Entry(bottomFrame, width=30)
        self.weightEntry.grid(row=6, column=1, padx=10, pady=10, sticky="NSEW")

        self.heightEntry = ttk.Entry(bottomFrame, width=30)
        self.heightEntry.grid(row=7, column=1, padx=10, pady=10, sticky="NSEW")

        self.allergiesEntry = ttk.Entry(bottomFrame, width=30)
        self.allergiesEntry.grid(row=9, column=1, padx=10, pady=10, sticky="NSEW")

        addAllergies = ttk.Button(bottomFrame, text='+', width=5)
        addAllergies.grid(row=9, column=2)

        submit = ttk.Button(bottomFrame, text='Submit', command=self.submitForm)
        submit.grid(row=11, column=3, pady=10, padx=20)

    def doctorProfile(self):

        self.doctorWin = Toplevel(LogWin)
        self.doctorWin.title('Doctor Profile')
        self.doctorWin.configure(background='#cfb53b')

        topFrame = Frame(self.doctorWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.doctorWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.doctorWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Doctor Profile", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #creating labels and entry boxes to be added to window in loop
        attributes = [
            '     License Number: ',
            '     First Name: ',
            '     Date of Birth: ',
            '     Work Phone: ',
            '     Room Number: ',
            '     Home Address: ',
        ]

        rows = 0

        self.specialty = StringVar()
        self.specialty.set('--Select Your Specialty--')
        self.specialties = ['General Physician',
                       'Heart Specialist',
                       'Eye Physician',
                       'Orthopedics',
                       'Psychiatry',
                       'Gynecologist']

        self.days = StringVar()
        self.days.set('Monday')
        days = ['Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday']

        self.fromTime = StringVar()
        self.fromTime.set('----')
        fromTimes = ['8:00am', '8:30am', '9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am',
                     '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm', '3:00pm', '3:30pm',
                     '4:00pm', '4:30pm', '5:00pm', '5:30pm']

        self.toTime = StringVar()
        self.toTime.set('----')
        toTimes = ['8:30am', '9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am',
                   '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm', '3:00pm', '3:30pm',
                   '4:00pm', '4:30pm', '5:00pm', '5:30pm', '6:00pm']

        for x in range(len(attributes)):

            if rows == 5:
                specialtyLabel = Label(bottomFrame, text="     Specialty: ")
                specialtyLabel.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
                specialtyLabel.configure(background='#cfb53b')

                self.specialtyPulldown = ttk.Combobox(bottomFrame, textvariable=self.specialty, values=self.specialties)
                self.specialtyPulldown.config(width=20)
                self.specialtyPulldown.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")
                self.specialtyPulldown.configure(background='#999')
                self.specialtyPulldown.config(state='readonly')
                rows += 1

            labelname = Label(bottomFrame, text=attributes[x])
            labelname.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
            labelname.configure(background='#cfb53b')
            rows += 1

        self.licenseEntry = ttk.Entry(bottomFrame, width=30)
        self.licenseEntry.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        self.fNameEntry = ttk.Entry(bottomFrame, width=30)
        self.fNameEntry.grid(row=1, column=1, padx=10, pady=10, sticky="NSEW")

        self.lNameEntry = ttk.Entry(bottomFrame, width=30)
        self.lNameEntry.grid(row=2, column=1, padx=10, pady=10, sticky="NSEW")

        self.DdobEntry = ttk.Entry(bottomFrame, width=30)
        self.DdobEntry.grid(row=3, column=1, padx=10, pady=10, sticky="NSEW")

        self.DworkPhoneEntry = ttk.Entry(bottomFrame, width=30)
        self.DworkPhoneEntry.grid(row=4, column=1, padx=10, pady=10, sticky="NSEW")

        self.roomEntry = ttk.Entry(bottomFrame, width=30)
        self.roomEntry.grid(row=6, column=1, padx=10, pady=10, sticky="NSEW")

        self.DaddressEntry = ttk.Entry(bottomFrame, width=30)
        self.DaddressEntry.grid(row=7, column=1, padx=10, pady=10, sticky="NSEW")

        #Creating Availability Pulldown Row
        availableFrame = Frame(bottomFrame)
        availableFrame.grid(row=rows, column=0, pady=10, columnspan=2)
        availableFrame.configure(background='#cfb53b')

        availableLabel = Label(availableFrame, text='     Availability: ')
        availableLabel.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        availableLabel.configure(background='#cfb53b')

        self.availableEntry = ttk.Combobox(availableFrame, textvariable=self.days, values=days, width=11)
        self.availableEntry.grid(row=0, column=1, padx=10, sticky="W")
        self.availableEntry.config(state='readonly')

        fromLabel = Label(availableFrame, text='From: ')
        fromLabel.grid(row=0, column=2)
        fromLabel.configure(background='#cfb53b')

        self.fromEntry = ttk.Combobox(availableFrame, textvariable=self.fromTime, values=fromTimes, width=8)
        self.fromEntry.grid(row=0, column=3, padx=5, sticky="W")
        self.fromEntry.config(state='readonly')

        toLabel = Label(availableFrame, text='To: ')
        toLabel.grid(row=0, column=4)
        toLabel.configure(background='#cfb53b')

        self.toEntry = ttk.Combobox(availableFrame, textvariable=self.toTime, values=toTimes, width=8)
        self.toEntry.grid(row=0, column=5, padx=5, sticky="W")
        self.toEntry.config(state='readonly')

        plusButton = ttk.Button(availableFrame, text='+', width=2.5)
        plusButton.grid(row=0, column=6, padx=5)

        #Putting Buttons at the Bottom
        buttonFrame = Frame(bottomFrame)
        buttonFrame.grid(row=9, column=0, columnspan=2)
        buttonFrame.configure(background='#cfb53b')

        createButton = ttk.Button(buttonFrame, text='Create Profile')
        createButton.pack(side=RIGHT, padx=5, pady=10)

        editProfButton = ttk.Button(buttonFrame, text='Edit Profile')
        editProfButton.pack(side=RIGHT, padx=5, pady=10)

    def homePage(self):

        self.hpWin = Toplevel(LogWin)
        self.hpWin.title('Home Page')
        self.hpWin.configure(background='#cfb53b')

        topFrame = Frame(self.hpWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.doctorWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.hpWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Home Page", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

    def appoinmentPage(self):

        self.apptWin = Toplevel(LogWin)
        self.apptWin.title('Appointments')
        self.apptWin.configure(background='#cfb53b')

        topFrame = Frame(self.apptWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.apptWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.apptWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Appointments", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        self.specialtySearch = StringVar()
        self.specialtySearch.set('--Select a Specialty--')
        specialtyFrame = Frame(bottomFrame, bd=1, background='#cfb53b')

        specialtyFrame.grid(row=0, column=0)
        specialtyLabel = Label(specialtyFrame, text='     Specialty: ', background='#cfb53b')
        specialtyLabel.grid(row=0, column=0, pady=15)

        self.specialtyPulldown = ttk.Combobox(specialtyFrame, textvariable=self.specialty, values=self.specialties)
        self.specialtyPulldown.grid(row=0, column=1, padx=5, pady=15)
        self.specialtyPulldown.config(state='readonly')

        searchButton = ttk.Button(specialtyFrame, text='Search', command=self.updateAppts)
        searchButton.grid(row=0, column=2, padx=50, pady=15)

        self.apptFrame = Frame(bottomFrame, background='#cfb53b')
        self.apptFrame.grid(row=1, column=0)

        colNames = ['     Doctor Name     ', '     Phone Number     ', '     Room Number     ', '     Availability     ',
                    '     Ratings     ']

        for x in range(len(colNames)):
            tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
            tableFrame.grid(row=0, column=x, sticky='EW')
            label = Label(tableFrame, text=colNames[x], background='#cfb53b')
            label.pack(fill=BOTH)

    def updateAppts(self):
        doctorsInfo = {
            'A': ['Phone', 'Room', ['Available1','Available2','Available3'], '******'],
            'B': ['Phone', 'Room', ['Available1','Available2','Available3'], '******'],
            'C': ['Phone', 'Room', ['Available1','Available2','Available3'], '******'],
            'D': ['Phone', 'Room', ['Available1','Available2','Available3'], '******'],
        }
        rows = 1
        for x in doctorsInfo.keys():
            tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
            tableFrame.grid(row=rows, column=0, sticky='EW')
            label = Label(tableFrame, text=x, background='#cfb53b')
            label.pack(fill=BOTH)
            for y in range(len(doctorsInfo[x])):
                if isinstance(doctorsInfo[x][y], list):
                    for z in range(len(doctorsInfo[x][y])):
                        tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
                        tableFrame.grid(row=rows, column=y+1, sticky='EW')
                        label = Label(tableFrame, text=doctorsInfo[x][y][z], background='#cfb53b')
                        label.pack(fill=BOTH)
                        rows += 1
                tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
                tableFrame.grid(row=rows, column=y+1, sticky='EW')
                label = Label(tableFrame, text=doctorsInfo[x][y], background='#cfb53b')
                label.pack(fill=BOTH)

            rows += 1

    def submitForm(self):

        #todo: error checking
        PName = self.nameEntry.get()
        DOB = self.dobEntry.get()
        Gender = self.gender.get()
        Address = self.addressEntry.get()
        HomePhone = self.homePhoneEntry.get()
        WorkPhone = self.workPhoneEntry.get()
        Weight = self.weightEntry.get()
        Height = self.heightEntry.get()
        AnnualIncome = self.annualIncome.get()
        Allergies = self.allergiesEntry.get()

        self.connect()

        query = '''INSERT INTO PATIENT(Name,HomePhone,Username,DOB,Gender,Address,WorkPhone,Height,Weight,AnnualIncome)
                VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''\
                .format(PName, HomePhone, self.Username, DOB, Gender, Address, WorkPhone, Height, Weight, AnnualIncome)

        self.c.execute(query)

    def connect(self):

        try:
            self.db = pymysql.connect(host="academic-mysql.cc.gatech.edu", #connecting to the database
                                passwd='KDKR2YQY', user='cs4400_Group_65',
                                db='cs4400_Group_65')
            self.c = self.db.cursor()



        except:

            mbox.showerror(title='Connection Error', message='Check your internet connection')
            return NONE

LogWin = Tk() #This will be where the login page goes.
LogWin.title('GTMS Login')
LogWin.configure(background='#cfb53b')
obj = GTMS(LogWin)
LogWin.mainloop()



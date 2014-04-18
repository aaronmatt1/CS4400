##GTMS UI

from tkinter import *
from tkinter import messagebox as mbox
from tkinter import ttk
from re import *
import urllib.request
import base64
import pymysql

class GTMS:
    def __init__(self, win):

        self.connect()
        #self.db.close() #get rid of this before trying to write to/read from DB

        url = 'http://comparch.gatech.edu/buzz.gif'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        pic = response.read()
        b64_data = base64.encodebytes(pic)
        self.photo = PhotoImage(data=b64_data)

        self.LoginPage(LogWin)

        self.patientProfile()

        self.Register()

        self.doctorProfile()

        self.appoinmentPage()

        self.patientHomePage()

        self.doctorHomePage()

        self.VisitHistory()

        self.OrderMeds()

        self.PaymentInfo()

        self.RateDoctor()

        self.sendMessage()

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

        login = ttk.Button(LogWin, text='Login', width=5, cursor='hand2', command=self.LoginCheck)
        login.grid(row=3, column=3, sticky=EW, padx=5, pady=5)

        register = ttk.Button(LogWin, text='Register', width=10, cursor='hand2', command=self.Register)
        register.grid(row=4, column=3, sticky=EW, padx=5, pady=5)
        
    def LoginCheck(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM USER WHERE Username= %s AND Password= %s", (username, password))
        result = cursor.fetchall()
        #If user account exists
        if result != ():
            show = mbox.showinfo("Login Complete", "Login successful.")
            cursor.execute("SELECT COUNT(*) FROM PATIENT WHERE Username= %s", (username))
            result = cursor.fetchall()
            #If user is patient
            if result[0][0] == 1:
                LogWin.iconify()
                self.patientHomepage()
            else:
                cursor.execute("SELECT COUNT(*) FROM DOCTOR WHERE Username= %s", (username))
                result = cursor.fetchall()
                #If user is doctor
                if result[0][0]  == 1:
                    LogWin.iconify()
                    self.doctorHomepage()
                #User must be Admin
                else:
                    LogWin.iconify()
                    self.adminHomepage()
        else:
            error = mbox.showerror("Login Error", "Login information incorrect. Please try again or register as new user.")
            return

    def Register(self):
        
        color = '#cfb53b'
        LogWin.iconify()
        self.newRegWin = Toplevel(LogWin)
        self.newRegWin.title('New User Register')
        self.newRegWin.configure(background='#cfb53b')

        topFrame = Frame(self.newRegWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.newRegWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.newRegWin)
        bottomFrame.grid(row=2, column=0, padx=10)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Register", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Main Body
        username_label = Label(bottomFrame, text='Username: ', bg='#cfb53b', padx=10, pady=10)
        username_label.grid(row=1, column=1, sticky=W)

        self.username_entry = Entry(bottomFrame, width=30)
        self.username_entry.grid(row=1, column=2, columnspan=3, sticky=EW, padx=5)

        password_label = Label(bottomFrame, text='Password: ', bg='#cfb53b', padx=10)
        password_label.grid(row=2, column=1, sticky=W)

        self.password_entry = Entry(bottomFrame, width=30, show='*')
        self.password_entry.grid(row=2, column=2, columnspan=3, sticky=EW, padx=5)

        confirm_label = Label(bottomFrame, text='Confirm Password: ', bg='#cfb53b', padx=10, pady=10)
        confirm_label.grid(row=3, column=1, sticky=W)

        self.confirm_entry = Entry(bottomFrame, width=30, show='*')
        self.confirm_entry.grid(row=3, column=2, columnspan=3, sticky=EW, padx=5)

        user_type_label = Label(bottomFrame, text='Type of User: ', bg='#cfb53b', padx=10)
        user_type_label.grid(row=4, column=1, sticky=W, padx=5)

        #User Type Pulldown Menu
        self.userType = StringVar()
        self.userType.set('Select User Type')
        types = ['Doctor', 'Patient', 'Administrative Personnel']
        userTypeMenu = ttk.Combobox(bottomFrame, textvariable=self.userType, values=types)
        userTypeMenu.config(state='readonly')
        userTypeMenu.grid(row=4, column=2, columnspan=3, sticky='NEW')

        #Register Button
        register = ttk.Button(bottomFrame, text='Register', command=self.RegisterNew, cursor='hand2')
        register.grid(row=5, column=2, sticky=EW, pady=10, padx=5)
        #Cancel Button: Return To Login
        cancel = ttk.Button(bottomFrame, text='Cancel')#, command=self.BackToLogin(reg), cursor='hand2')
        cancel.grid(row=5, column=3, sticky=EW, pady=10, padx=5)
        
    def RegisterNew(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            confirm = self.confirm_entry.get()
            #If username and password entries are not empty
            if username != '' and password != '':
                #If password and confirm match
                if password.split() == confirm.split():
                    #If username and password are less than 15 chars
                    if len(password) < 15 or len(username) < 15:
                        num = findall("\d+", password)
                        letters = findall("[a-zA-Z]", password)
                        #If password contains both letters and numbers
                        if num != [] and letters != []:
                            db = self.connect()
                            cursor = db.cursor()
                            cursor.execute("SELECT * FROM USER WHERE Username= %s", (username))
                            data = []
                            for i in cursor:
                                data.append(i)
                            #If username is not taken
                            if data == []:
                                cursor.execute("INSERT INTO USER (Username, Password) VALUES (%s, %s)", (username, password))
                                mbox.showinfo("Registration Complete", "User is now registered into GTMRS database")
                                db.commit()
                                #If user is patient
                                if self.user_type.get() == 'Patient':
                                    self.reg.iconify()
                                    self.patientProfile()
                                #If user is doctor
                                elif self.user_type.get() == 'Doctor':
                                    self.reg.iconify()
                                    self.doctorProfile()
                            else:
                                error = mbox.showerror("Registration Error", "Username is already in use.")
                                return
                        else:
                            error = mbox.showerror("Registration Error", "Please verify that password contains both letters and numbers.")
                            return
                    else:
                        error = mbox.showerror("Registration Error", "Please enter shorter password and/or username.")
                else:
                    error = mbox.showerror("Registration Error", "Please check that password is entered correctly.")
                    return
            else:
                error = mbox.showerror("Registration Error", "Please enter valid username and/or password.")
                return                
        except:
            error = mbox.showerror("Registration Error", "Please try again.")
            return

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

        submit = ttk.Button(bottomFrame, text='Submit', command=self.PsubmitForm)
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
                       'Gynecologist',
                       'Cardiologist']

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
        availableFrame.grid(row=rows, column=0, pady=10, columnspan=5)
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
        buttonFrame.grid(row=9, column=0, columnspan=5)
        buttonFrame.configure(background='#cfb53b')

        createButton = ttk.Button(buttonFrame, text='Create Profile')
        createButton.pack(side=RIGHT, padx=5, pady=10)

        editProfButton = ttk.Button(buttonFrame, text='Edit Profile')
        editProfButton.pack(side=RIGHT, padx=5, pady=10)

    def patientHomePage(self):

        self.patHPWin = Toplevel(LogWin)
        self.patHPWin.title('Home Page')
        self.patHPWin.configure(background='#cfb53b')

        topFrame = Frame(self.patHPWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.patHPWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.patHPWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Patient Home Page", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        makeAppointButton = Button(bottomFrame, text='Make Appointments', relief=FLAT, command=self.MakeAppt)
        makeAppointButton.grid(row=0, column=0, padx=20, pady=10, sticky='W')
        makeAppointButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        viewVisitButton = Button(bottomFrame, text='View Visit History', relief=FLAT, command=self.VisitHistory)
        viewVisitButton.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        viewVisitButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        orderMedButton = Button(bottomFrame, text='Order Medication', relief=FLAT, command=self.OrderMeds)
        orderMedButton.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        orderMedButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        communicateButton = Button(bottomFrame, text='Communicate', relief=FLAT, command=self.Communicator)
        communicateButton.grid(row=3, column=0, padx=20, pady=10, sticky='W')
        communicateButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        rateDocButton = Button(bottomFrame, text='Rate a Doctor', relief=FLAT, command=self.RateDoctor)
        rateDocButton.grid(row=4, column=0, padx=20, pady=10, sticky='W')
        rateDocButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        editProfile = Button(bottomFrame, text='Edit Profile', relief=FLAT, command=self.EditProfile)
        editProfile.grid(row=5, column=0, padx=20, pady=10, sticky='W')
        editProfile.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        hardCodedSpaceLabel = Label(bottomFrame, text='                                          ')
        hardCodedSpaceLabel.grid(row=0, column=1)
        hardCodedSpaceLabel.configure(background='#cfb53b')

        messageText = 'You have {info from DB} unread messages'
        unreadMsgButton = Button(bottomFrame, text=messageText, relief=FLAT)
        unreadMsgButton.grid(row=0, column=2, padx=10, pady=10)
        unreadMsgButton.configure(font=('Arial', 8),
                                  foreground='blue',
                                  background='#cfb53b')

    def doctorHomePage(self):

        self.docHPWin = Toplevel(LogWin)
        self.docHPWin.title('Doctor Home Page')
        self.docHPWin.configure(background='#cfb53b')

        topFrame = Frame(self.docHPWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.docHPWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.docHPWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Home Page", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        makeAppointButton = Button(bottomFrame, text='View Appointments \n Calendar', relief=FLAT)
        makeAppointButton.grid(row=0, column=0, padx=20, pady=10, sticky='W')
        makeAppointButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        viewPrescripButton = Button(bottomFrame, text='Prescriptions', relief=FLAT)
        viewPrescripButton.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        viewPrescripButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        orderMedButton = Button(bottomFrame, text='Create Surgery \n Records', relief=FLAT)
        orderMedButton.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        orderMedButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        communicateButton = Button(bottomFrame, text='Communicate', relief=FLAT)
        communicateButton.grid(row=3, column=0, padx=20, pady=10, sticky='W')
        communicateButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        rateDocButton = Button(bottomFrame, text='Edit Profile', relief=FLAT)
        rateDocButton.grid(row=4, column=0, padx=20, pady=10, sticky='W')
        rateDocButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        hardCodedSpaceLabel = Label(bottomFrame, text='                                          ')
        hardCodedSpaceLabel.grid(row=0, column=1)
        hardCodedSpaceLabel.configure(background='#cfb53b')

        messageText = 'You have {info from DB} unread messages'
        unreadMsgButton = Button(bottomFrame, text=messageText, relief=FLAT)
        unreadMsgButton.grid(row=0, column=2, padx=10, pady=10)
        unreadMsgButton.configure(font=('Arial', 8),
                                  foreground='blue',
                                  background='#cfb53b')
                                  
    def VisitHistory(self):

        color = '#cfb53b'
        self.patHPWin.iconify()
        self.visitHistWin = Toplevel(LogWin)
        visitHistWin = self.visitHistWin
        visitHistWin.title('Visit History')
        visitHistWin.configure(background='#cfb53b')

        topFrame = Frame(visitHistWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(visitHistWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(visitHistWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Visit History", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Main Body
        date_visits_frame = Frame(bottomFrame, bg=color)
        date_visits_frame.grid(row=1, column=0, rowspan=5)
        
        dateVisitsLabel = Label(date_visits_frame, text='Dates of Visits', bg=color)
        dateVisitsLabel.grid(row=0, column=0, sticky=N)

        #Date Visits Listbox
        username = self.username_entry.get()
        self.connect()

        self.c.execute("SELECT DateVisit FROM VISIT WHERE PUsername='%s'" % (username))
        result = self.c.fetchall()
        date_visits = ()
        for date in result:
            date_visits += (date[0],)
        
        self.dateVisits = StringVar(value=date_visits)

        date_visits_lbox = Listbox(date_visits_frame, listvariable=self.dateVisits, width=12, height=5)
        date_visits_lbox.grid(row=1, column=0, padx=3, sticky=N)

        #Vertical Separator
        separator = ttk.Separator(bottomFrame, orient=VERTICAL)
        separator.grid(row=1, column=1, sticky='NSW', rowspan=4)

        #Visit History Frame
        attributes = ['Consulting Doctor: ', 'Blood Pressure: ', 'Diagnosis: ', 'Medications Prescribed: ']
        count = 1
        for attribute in attributes:
            attribute_label = Label(bottomFrame, text=attribute, bg=color)
            attribute_label.grid(row=count, column=1, padx=10, pady=10, sticky=W)
            count += 1

        consul_doc = Entry(bottomFrame, width=20)
        consul_doc.grid(row=1, column=2, sticky=W)

        bloodFrame = Frame(bottomFrame, background=color)
        bloodFrame.grid(row=2, column=2, sticky=W)

        systolic_lbl = Label(bloodFrame, text='Systolic: ', bg=color)
        systolic_lbl.grid(row=0, column=0)

        systolic_entry = Entry(bloodFrame, width=5)
        systolic_entry.grid(row=0, column=1, padx=5)

        diastolic_lbl = Label(bloodFrame, text='Diastolic: ', bg=color)
        diastolic_lbl.grid(row=0, column=2, sticky=N)

        diastolic_entry = Entry(bloodFrame, width=5)
        diastolic_entry.grid(row=0, column=3, padx=5)

        diagnosis = Canvas(bottomFrame, bg='white', width=100, height=50)
        diagnosis.grid(row=3, column=2, sticky=W)

    def visitReport(self):
        
        self.docHPWin = Toplevel(LogWin)
        self.docHPWin.title('Doctor Home Page')
        self.docHPWin.configure(background='#cfb53b')

        topFrame = Frame(self.docHPWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.docHPWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.docHPWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Home Page", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

    def RateDoctor(self):

        color = '#cfb53b'
        self.patHPWin.iconify()
        self.rateWin = Toplevel(LogWin)
        self.rateWin.title('Rate a Doctor')
        self.rateWin.configure(background='#cfb53b')

        topFrame = Frame(self.rateWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.rateWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.rateWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Rate a Doctor", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Main Body
        select_doc = Label(bottomFrame, text='Select Doctors: ', bg=color)
        select_doc.grid(row=1, column=0, padx=20, sticky=W, pady=10)

        cursor = self.connect()

        cursor.execute("SELECT FName, LName FROM DOCTOR")
        result = self.c.fetchall()
        doctors = []
        for doctor in result:
            doctors.append('Dr. ' + doctor[0] + ' ' + doctor[1])
        self.doctor = StringVar()
        self.doctor.set('Select Doctor')
        doctors_pulldown = ttk.Combobox(bottomFrame, textvariable=self.doctor, values=doctors)
        doctors_pulldown.grid(row=1, column=1, sticky=W, pady=10)
        doctors_pulldown.config(state='readonly')

        rating_label = Label(bottomFrame, text='Rating: ', bg=color)
        rating_label.grid(row=2, column=0, padx=20, sticky=W, pady=5)

        ratings = list(range(1, 6))
        self.rating = StringVar()
        self.rating.set('----')

        rating_pulldown = ttk.Combobox(bottomFrame, textvariable=self.rating, values=ratings)
        rating_pulldown.config(width=10, state='readonly')
        rating_pulldown.grid(row=2, column=1, sticky=W, pady=5)

        submit = ttk.Button(bottomFrame, text='Submit Rating', command=self.SubmitRating)
        submit.grid(row=3, column=2, padx=10, pady=10, sticky=W)

    def SubmitRating(self):

        try:
            rating = int(self.rating.get())

            #cursor = self.connect()
            #self.db.close()
            #cursor.execute("INSERT INTO RATES(PUsername, DUsername, Rating) VALUES('{0}', '{1}', {2})".format(

        except:
            mbox.showerror(title='ERROR', message='Please Select a Rating')

    def OrderMeds(self):

        color = '#cfb53b'
        self.patHPWin.iconify()
        self.orderWin = Toplevel(LogWin)
        self.orderWin.title('Order Medication')
        self.orderWin.configure(background='#cfb53b')

        topFrame = Frame(self.orderWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.orderWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.orderWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Order Medication", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Main Body
        attributes = ["Medicine Name: ", 'Dosage: ',
                      'Duration: ', 'Consulting Doctor: ', 'Date of Prescription: ']
        count = 1
        for attribute in attributes:
            attribute_label = Label(bottomFrame, text=attribute, bg=color)
            attribute_label.grid(row=count, column=0, padx=10, pady=10, sticky=W)
            count += 1

        self.meds_name = Entry(bottomFrame, width=30)
        self.meds_name.grid(row=1, column=1, columnspan=3, sticky=W)

        dosage_frame = Frame(bottomFrame)
        dosage_frame.grid(row=2, column=1, sticky=W)
        
        self.dosage_amount = Entry(dosage_frame, width=5)
        self.dosage_amount.grid(row=0, column=0, sticky=W)

        per = Label(dosage_frame, text='every day', bg=color)
        per.grid(row=0, column=1, sticky=W)

        duration_frame = Frame(bottomFrame)
        duration_frame.grid(row=3, column=1, sticky=W)

        self.duration_months = Entry(duration_frame, width=5)
        self.duration_months.grid(row=0, column=0, sticky=W)

        months = Label(duration_frame, text='months', bg=color)
        months.grid(row=0, column=1, sticky=W)

        self.duration_days = Entry(duration_frame, width=5)
        self.duration_days.grid(row=0, column=2, sticky=W)

        days = Label(duration_frame, text='days', bg=color)
        days.grid(row=0, column=3, sticky=W)

        self.consulting_doctor = Entry(bottomFrame, width=20)
        self.consulting_doctor.grid(row=4, column=1, columnspan=4, sticky=W)

        date_prescription_frame = Frame(bottomFrame)
        date_prescription_frame.grid(row=5, column=1, sticky=W)

        years = list(range(1910, 2015))
        months = list(range(1, 13))
        days = list(range(1, 32))
        
        self.prescrip_year = StringVar()
        self.prescrip_year.set('Year')

        prescrip_year = ttk.Combobox(date_prescription_frame, textvariable=self.prescrip_year, values=years)
        prescrip_year.config(width=5, state='readonly')
        prescrip_year.grid(row=0, column=0, sticky=W)

        self.prescrip_month = StringVar()
        self.prescrip_month.set('Month')

        prescrip_month = ttk.Combobox(date_prescription_frame, textvariable=self.prescrip_month, values=months)
        prescrip_month.config(width=7, state='readonly')
        prescrip_month.grid(row=0, column=1, sticky=W)

        self.prescrip_day = StringVar()
        self.prescrip_day.set('Day')

        prescrip_day = ttk.Combobox(date_prescription_frame, textvariable=self.prescrip_day, values=days)
        prescrip_day.config(width=5, state='readonly')
        prescrip_day.grid(row=0, column=2, sticky=W)
        
        checkout = ttk.Button(bottomFrame, text='Checkout', cursor='hand2', command=self.PaymentInfo)
        checkout.grid(row=6, column=2, padx=10, pady=10)

    def sendMessage(self):
        self.patHPWin.iconify()
        self.messageWin= Toplevel(LogWin)
        self.messageWin.title('Communicator')
        self.messageWin.configure(background='#cfb53b')

        topFrame = Frame(self.messageWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.messageWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.messageWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Communicator", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        sendTo = StringVar()
        sendTo.set('------')
        contacts = ['A', 'B', 'C']

        toFrame = Frame(bottomFrame, background='#cfb53b')
        toFrame.pack(pady=15)
        Label(toFrame, text='Select Name:   ', background='#cfb53b').grid(row=0, column=0)
        contactPulldown = ttk.Combobox(toFrame, textvariable=sendTo, values=contacts)
        contactPulldown.grid(row=0, column=1, sticky='w')

        messageFrame = Frame(bottomFrame, background='#cfb53b')
        messageFrame.pack(padx=10, pady=20)

        text = """""".strip()

        scroll = Scrollbar(messageFrame)
        scroll.grid(row=0, column=1, sticky='NS')

        self.box = Text(messageFrame, wrap='word', font='Arial 12 italic', relief=GROOVE)

        scroll.config()

        self.box.config(height=10, width=40)
        self.box.config()
        self.box.insert(1.0, text)
        self.box.grid(row=0, column=0, sticky='EW')

        scroll.config(command=self.box.yview)
        self.box.config(yscrollcommand=scroll.set)

        Button(bottomFrame, text='Send Message', command=self.getMessage).pack(pady=5, anchor=CENTER)

    def getMessage(self):

        message = self.box.get("1.0", 'end')

    def PaymentInfo(self):

        color = '#cfb53b'
        self.patHPWin.iconify()
        self.payWin = Toplevel(LogWin)
        self.payWin.title('Payment Information')
        self.payWin.configure(background='#cfb53b')

        topFrame = Frame(self.payWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.payWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.payWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Payment Information", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Main Body
        attributes = ["Cardholder's Name: ", 'Card Number: ',
                      'Type of Card: ', 'CVV: ', 'Date of Expiry: ']
        count = 1
        for attribute in attributes:
            attribute_label = Label(bottomFrame, text=attribute, bg=color)
            attribute_label.grid(row=count, column=0, padx=10, pady=10, sticky=W)
            count += 1

        self.cardholder_name = Entry(bottomFrame, width=30)
        self.cardholder_name.grid(row=1, column=1, sticky=W)

        self.card_number = Entry(bottomFrame, width=30)
        self.card_number.grid(row=2, column=1, sticky=W)

        self.card_type = StringVar()
        self.card_type.set('Select Card Type')

        types = ['Visa', 'Mastercard', 'Discover', 'American Express']

        paymentPulldown = ttk.Combobox(bottomFrame, textvariable=self.card_type, values=types)
        paymentPulldown.config(width=25, state='readonly')
        paymentPulldown.grid(row=3, column=1, sticky=W)

        self.cvv = Entry(bottomFrame, width=30)
        self.cvv.grid(row=4, column=1, sticky=W)

        date_expiry_frame = Frame(bottomFrame, background=color)
        date_expiry_frame.grid(row=5, column=1, sticky=W)

        years = list(range(1910, 2014))
        months = list(range(1, 13))
        days = list(range(1, 32))
        
        self.expiry_year = StringVar()
        self.expiry_year.set('Year')

        expiry_year = ttk.Combobox(date_expiry_frame, textvariable=self.expiry_year, values=years)
        expiry_year.config(width=5)
        expiry_year.config(state='readonly')
        expiry_year.grid(row=0, column=0, sticky=W, padx=2)

        self.expiry_month = StringVar()
        self.expiry_month.set('Month')

        expiry_month = ttk.Combobox(date_expiry_frame, textvariable=self.expiry_month, values=months)
        expiry_month.config(width=7, state='readonly')
        expiry_month.grid(row=0, column=1, sticky=W, padx=2)

        self.expiry_day = StringVar()
        self.expiry_day.set('Day')

        expiry_day = ttk.Combobox(date_expiry_frame, textvariable=self.expiry_day, values=days)
        expiry_day.config(width=5, state='readonly')
        expiry_day.grid(row=0, column=2, sticky=W, padx=5)

        order = ttk.Button(bottomFrame, text='Order', cursor='hand2', command=self.PayMeds)
        order.grid(row=6, column=2, padx=5, pady=5)

    def appoinmentPage(self):
        self.patHPWin.iconify()
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

    def updateAppts(self):

        self.cursor = self.connect()

        query = "SELECT Username,FName,LName,AvgRating FROM `DOCTOR` WHERE Specialty = '{}'".format(self.specialty.get())
        self.cursor.execute(query)
        specialists = list(self.c.fetchall())

        doctorsList = []
        self.docRatingDict = {}
        for specialist in specialists:
            doctorsList.append(specialist[1]+' '+specialist[2])
            self.docRatingDict[specialist[0]] = specialist[3]

        self.docSelected = StringVar()

        self.docSelected.set('--Select A Specialist--')

        self.selectionFrame = Frame(self.apptWin, background='#cfb53b')
        self.selectionFrame.grid(row=3, column=0, pady=10)
        self.specialistPulldown = ttk.Combobox(self.selectionFrame, textvariable=self.docSelected, values=doctorsList)
        self.specialistPulldown.config(state='readonly')
        self.specialistPulldown.config(width=30)

        Label(self.selectionFrame, text='Specialist:   ', background='#cfb53b').grid(row=0, column=0, padx=5, pady=10)

        self.specialistPulldown.grid(row=0, column=1, padx=5, pady=10)
        self.rateLabel = Label(self.selectionFrame, text='Avg Rating: ')
        self.rateLabel.grid(row=0, column=2, padx=5, pady=10, sticky='W')
        self.rateLabel.configure(background='#cfb53b')

        self.specialistPulldown.bind("<<ComboboxSelected>>", self.specialistSelected)

    def specialistSelected(self, event=NONE):

        docName = self.docSelected.get().split()

        userNameQuery = 'SELECT Username FROM DOCTOR WHERE FName = "{}" AND LName = "{}"'.format(docName[0], docName[1])
        self.cursor.execute(userNameQuery)
        username = self.cursor.fetchone()[0]

        self.rateLabel.config(text='Avg Rating: {}'.format(self.docRatingDict[username]))

        timeQuery = '''SELECT Day_Date,From_Time,To_Time
                        FROM AVAILABILITY
                        NATURAL JOIN DOCTOR
                        WHERE DOCTOR.Username = AVAILABILITY.Username
                        AND DOCTOR.Username = "{}"'''.format(username)
        self.cursor.execute(timeQuery)
        times = list(self.c.fetchall())
        timesList = []
        for timeSlot in times:
            timesList.append(str(timeSlot[0])[0:3]+':  '+str(timeSlot[1])+' - '+str(timeSlot[2]))

        self.db.close()

        try:
            self.timePulldown.destroy()
        except:
            pass

        self.timeSelected = StringVar()
        self.timeSelected.set('--Select A Time--')

        Label(self.selectionFrame, text='Time Slot:   ', background='#cfb53b').grid(row=1, column=0, padx=5, pady=5)

        self.timePulldown = ttk.Combobox(self.selectionFrame, textvariable=self.timeSelected,
                                             values=timesList)
        self.timePulldown.config(state='readonly')
        self.timePulldown.config(width=30)
        self.timePulldown.grid(row=1, column=1, padx=5, pady=5)
        self.requestButton = ttk.Button(self.selectionFrame, text='Request Appointment')
        self.requestButton.grid(row=2, column=0, columnspan=3, pady=5, sticky='EW')

    def PsubmitForm(self):

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
        if PName != []:
            if HomePhone != []:
                if DOB != []:
                    if Address != []:
                        if AnnualIncome != []:

                            self.connect()
                    
                            query = '''INSERT INTO PATIENT(Name,HomePhone,Username,DOB,Gender,Address,WorkPhone,Height,Weight,AnnualIncome)
                                    VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''\
                                    .format(PName, HomePhone, self.username, DOB, Gender, Address, WorkPhone, Height, Weight, AnnualIncome)
                            
                            self.c.execute(query)
                        else:
                            error = mbox.showerror("Patient Form", "Please enter a valid annual income.")
                            return
                    else:
                        error = mbox.showerror("Patient Form", "Please enter a valid address.")
                        return
                else:
                    error = mbox.showerror("Patient Form", "Please enter a valid date of birth.")
                    return
            else:
                error = mbox.showerror("Patient Form", "Please enter a valid home phone number.")
                return
        else:
            error = mbox.showerror("Patient Form", "Please enter a valid name.")
            return

    def PayMeds(self):
        pass

    def connect(self):

        try:
            self.db = pymysql.connect(host="academic-mysql.cc.gatech.edu", #connecting to the database
                                passwd='KDKR2YQY', user='cs4400_Group_65',
                                db='cs4400_Group_65')
            self.c = self.db.cursor()
            return self.c

        except:
            mbox.showerror(title='Connection Error', message='Check your internet connection')
            return NONE

        self.db.close()

LogWin = Tk() #This will be where the login page goes.
LogWin.title('GTMS Login')
LogWin.configure(background='#cfb53b')
obj = GTMS(LogWin)
LogWin.mainloop()




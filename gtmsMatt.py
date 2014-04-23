from tkinter import *
from tkinter import messagebox as mbox
from tkinter import ttk
from re import *
import urllib.request
import base64
import pymysql

class GTMS:

    def __init__(self, win):

        url = 'http://comparch.gatech.edu/buzz.gif'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        pic = response.read()
        b64_data = base64.encodebytes(pic)
        self.photo = PhotoImage(data=b64_data)

        self.LoginPage(LogWin)

    def LoginPage(self, LogWin):
        #Top Banner
        banner = Label(LogWin, bg='#cfb53b', width=450, height=50, text='GTMS Login', padx=10, font=('Berlin Sans FB', 18),
                   image=self.photo, compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=4)

        #Main Body
        username_label = Label(LogWin, text='Username:      ',  bg='#cfb53b')
        username_label.grid(row=1, column=1, sticky=E, pady=20)

        self.User = StringVar()
        self.Pass = StringVar()
        self.User.set('NONE')
        self.Pass.set('NONE')

        self.username_entry = ttk.Entry(LogWin, textvariable=self.User, width=35)
        self.username_entry.grid(row=1, column=2, sticky=W)
        self.username_entry.delete(0, END)

        password_label = Label(LogWin, text='Password:      ',  bg='#cfb53b')
        password_label.grid(row=2, column=1, sticky=E, pady=10)

        self.password_entry = ttk.Entry(LogWin, textvariable=self.Pass, show='*', width=35)
        self.password_entry.grid(row=2, column=2, sticky=W)
        self.password_entry.delete(0, END)

        login = ttk.Button(LogWin, text='Login', width=5, cursor='hand2', command=self.LoginCheck)
        login.grid(row=3, column=3, sticky=EW, padx=5, pady=5)

        register = ttk.Button(LogWin, text='Register', width=10, cursor='hand2', command=self.Register)
        register.grid(row=4, column=3, sticky=EW, padx=5, pady=5)
        
    def LoginCheck(self):

        self.Registering = FALSE
        self.username = self.User.get()
        password = self.Pass.get()
        self.cursor = self.connect()
        query = 'SELECT * FROM USER WHERE Username= "{}" AND Password= "{}"'.format(self.username, password)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        #If user account exists
        if result:
            show = mbox.showinfo("Login Complete", "Login successful.")
            self.cursor.execute('SELECT COUNT(*) FROM PATIENT WHERE Username= "{}"'.format(self.username))
            result = self.cursor.fetchall()
            #If user is patient
            if result[0][0] == 1:
                self.userType = 'patient'
                LogWin.iconify()
                self.db.close()
                self.patientScreens()

            else:
                self.cursor.execute('SELECT COUNT(*) FROM DOCTOR WHERE Username= "{}"'.format(self.username))
                result = self.cursor.fetchall()
                #If user is doctor
                if result[0][0] == 1:
                    self.userType = 'doctor'
                    LogWin.iconify()
                    self.db.close()
                    self.doctorScreens()

                #User must be Admin
                else:
                    self.userType = 'admin'
                    LogWin.iconify()
                    self.db.close()
                    self.adminScreens()

        else:
            error = mbox.showerror("Login Error", "Login information incorrect. Please try again or register as new user.")
            return

    def Register(self):

        color = '#cfb53b'

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
        
        note = Label(bottomFrame, text='Note: Choose a password that contains both letters and numbers and is between 6 - 15 characters long.',
                     font=('Arial', 8), bg='#cfb53b', wraplength=175, justify=LEFT)
        note.grid(row=2, column=5, sticky=W)

        confirm_label = Label(bottomFrame, text='Confirm Password: ', bg='#cfb53b', padx=10, pady=10)
        confirm_label.grid(row=3, column=1, sticky=W)

        self.confirm_entry = Entry(bottomFrame, width=30, show='*')
        self.confirm_entry.grid(row=3, column=2, columnspan=3, sticky=EW, padx=5)

        user_type_label = Label(bottomFrame, text='Type of User: ', bg='#cfb53b', padx=10)
        user_type_label.grid(row=4, column=1, sticky=W, padx=5)

        #User Type Pulldown Menu
        self.Type = StringVar()
        self.Type.set('Select User Type')
        types = ['Doctor', 'Patient', 'Administrative Personnel']
        userTypeMenu = ttk.Combobox(bottomFrame, textvariable=self.Type, values=types)
        userTypeMenu.config(state='readonly')
        userTypeMenu.grid(row=4, column=2, columnspan=3, sticky='NEW')

        #Register Button
        register = ttk.Button(bottomFrame, text='Register', command=self.RegisterNew, cursor='hand2')
        register.grid(row=5, column=2, sticky=EW, pady=10, padx=5)
        #Cancel Button: Return To Login
        cancel = ttk.Button(bottomFrame, text='Cancel', command=lambda: self.newRegWin.destroy(), cursor='hand2')
        cancel.grid(row=5, column=3, sticky=EW, pady=10, padx=5)
        
    def RegisterNew(self):
        #try:
        self.Registering = TRUE
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        #If username,  password , and confirm password entries are not empty
        if self.username != '' and password != '' and confirm != '':
            #If password and confirm match
            if password.split() == confirm.split():
                #If username and password are less than 15 chars
                if len(password) < 15 or len(username) < 15:
                    num = findall("\d+", password)
                    letters = findall("[a-zA-Z]", password)
                    #If password contains both letters and numbers
                    if num != [] and letters != []:
                        cursor = self.connect()
                        
                        cursor.execute('SELECT * FROM USER WHERE Username= "{}"'.format(self.username))
                        data = []
                        for i in cursor:
                            data.append(i)
                        #If username is not taken
                        if data == []:
                            cursor.execute('INSERT INTO USER (Username, Password) VALUES ("{}", "{}")'.format(self.username, password))
                            mbox.showinfo("Registration Complete", "User is now registered into GTMRS database")
                            self.db.commit()
                            #If user is patient
                            if self.Type.get() == 'Patient':
                                self.userType = 'patient'
                                self.newRegWin.withdraw()
                                self.patientProfile()
                            #If user is doctor
                            elif self.Type.get() == 'Doctor':
                                self.userType = 'doctor'
                                self.newRegWin.withdraw()
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
        #except:
            #error = mbox.showerror("Registration Error", "Please try again.")
            #return

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

        addAllergies = ttk.Button(bottomFrame, text='+', width=5, command=self.AddAllergies)#create code with SQL to put entry into DB under patient, then clear entry
        addAllergies.grid(row=9, column=2)
        
        #This block of code is intended for when the patient edits his profile.
        #In this case, the patient's current information will be pulled from
        #the database and inserted into the appropriate entry. The patient
        #can then edit the necessary info.
        cursor = self.connect()
        cursor.execute('SELECT COUNT(*) FROM PATIENT WHERE Username = "{}"'.format(self.username))
        result = self.c.fetchall()
        #PATIENT(Name, HomePhone, Username, DOB, Gender, Address, WorkPhone, Height, Weight, AnnualIncome)
        result = result[0]
        #If the patient info is in the PATIENT table, insert the current info
        #into the corresponding entries
        if result[0] != 0:
            cursor.execute('SELECT * FROM PATIENT WHERE Username = "{}"'.format(self.username))
            result = self.c.fetchall()
            result = list(result[0])
            for x in range(len(result)):
                if not result[x]:
                    result[x] = ''
            self.nameEntry.insert(END, result[0])
            self.dobEntry.insert(END, result[3])
            self.gender.set(result[4])
            self.addressEntry.insert(END, result[5])
            self.homePhoneEntry.insert(END, result[1])
            self.workPhoneEntry.insert(END, result[6])
            self.weightEntry.insert(END, result[8])
            self.heightEntry.insert(END, result[7])
            self.annualIncome.set(result[9])

        submit = ttk.Button(bottomFrame, text='Submit', command=self.PsubmitForm)
        submit.grid(row=11, column=3, pady=10, padx=20)

        self.patientWin.protocol("WM_DELETE_WINDOW", self.EditToHP)
        
    def AddAllergies(self):

        allergies = self.allergiesEntry.get()
        cursor = self.connect()
        self.c.execute("INSERT INTO ALLERGIES(Username, Allergy) VALUES('%s', '%s')" % (self.username, allergies))
        self.db.commit()

        self.allergiesEntry.delete(0, END)

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
            '     Last Name: ',
            '     Date of Birth: ',
            '     Work Phone: ',
            '     Specialty: ',
            '     Room Number: ',
            '     Home Address: ',
        ]


        self.specialty = StringVar()
        self.specialty.set('--Select Your Specialty--')
        self.specialties = ['General Physician',
                       'Heart Specialist',
                       'Eye Physician',
                       'Orthopedics',
                       'Psychiatry',
                       'Gynecologist']

        self.day = StringVar()
        self.day.set("---")
        days = list(range(1,31))

        self.month = StringVar()
        self.month.set("---")
        months = list(range(1,13))

        self.year = StringVar()
        self.year.set("---")
        years = list(range(2014,2050,1))

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

        rows = 0

        for x in range(len(attributes)):

            if x == 5:
                specialtyLabel = Label(bottomFrame, text=attributes[rows])
                specialtyLabel.grid(row=rows, column=0, padx=10, pady=10, sticky="W")
                specialtyLabel.configure(background='#cfb53b')

                self.specialtyPulldown = ttk.Combobox(bottomFrame, textvariable=self.specialty, values=self.specialties)
                self.specialtyPulldown.config(width=20)
                self.specialtyPulldown.grid(row=rows, column=1, padx=10, pady=10, sticky="NSEW")
                self.specialtyPulldown.configure(background='#999')
                self.specialtyPulldown.config(state='readonly')
                rows += 1
            else:

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
        availableFrame.grid(row=rows+1, column=0, pady=10, columnspan=5)
        availableFrame.configure(background='#cfb53b')

        date_available = Frame(availableFrame)
        date_available.grid(row=0, column=1, sticky='NSEW')
        date_available.configure(background=color)

        availableLabel = Label(date_available, text='     Availability: ')
        availableLabel.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        availableLabel.configure(background='#cfb53b')

        self.availableYearEntry = ttk.Combobox(date_available, textvariable=self.year, values=years, width=8)
        self.availableYearEntry.grid(row=0, column=1, padx=2, sticky="W")
        self.availableYearEntry.config(state='readonly')

        self.availableMonthEntry = ttk.Combobox(date_available, textvariable=self.month, values=months, width=4)
        self.availableMonthEntry.grid(row=0, column=2, padx=2, sticky="W")
        self.availableMonthEntry.config(state='readonly')

        self.availableDayEntry = ttk.Combobox(date_available, textvariable=self.day, values=days, width=6)
        self.availableDayEntry.grid(row=0, column=3, padx=2, sticky="W")
        self.availableDayEntry.config(state='readonly')

        fromLabel = Label(date_available, text='From: ')
        fromLabel.grid(row=0, column=4)
        fromLabel.configure(background='#cfb53b')

        self.fromEntry = ttk.Combobox(date_available, textvariable=self.fromTime, values=fromTimes, width=8)
        self.fromEntry.grid(row=0, column=5, padx=5, sticky="W")
        self.fromEntry.config(state='readonly')

        toLabel = Label(date_available, text='To: ')
        toLabel.grid(row=0, column=6)
        toLabel.configure(background='#cfb53b')

        self.toEntry = ttk.Combobox(date_available, textvariable=self.toTime, values=toTimes, width=8)
        self.toEntry.grid(row=0, column=7, padx=5, sticky="W")
        self.toEntry.config(state='readonly')

        #This block of code is intended for when the doctor edits his profile.
        #In this case, the doctors's current information will be pulled from
        #the database and inserted into the appropriate entry. The patient
        #can then edit the necessary info.
        cursor = self.connect()
        cursor.execute('SELECT COUNT(*) FROM DOCTOR WHERE Username = "{}"'.format(self.username))
        result = cursor.fetchall()
        #PATIENT(Name, HomePhone, Username, DOB, Gender, Address, WorkPhone, Height, Weight, AnnualIncome)
        result = result[0]
        #If the patient info is in the PATIENT table, insert the current info
        #into the corresponding entries
        if result[0] != 0:
            cursor.execute('SELECT * FROM DOCTOR WHERE Username = "{}"'.format(self.username))
            result = cursor.fetchall()
            result = result[0]
            self.licenseEntry.insert(END, result[1])
            self.fNameEntry.insert(END, result[2])
            self.lNameEntry.insert(END, result[3])
            self.DdobEntry.insert(END, result[4])
            self.DworkPhoneEntry.insert(END, result[5])
            self.specialty.set(result[6])
            self.roomEntry.insert(END, result[7])
            self.DaddressEntry.insert(END, result[8])
        self.db.close()
            

        def addTimes():

            timePattern = '\d*:\d\d'
            
            day = self.day.get()
            month = self.month.get()
            year = self.year.get()
            date= year+'-'+month+'-'+day
            fromTime = re.findall(timePattern, self.fromEntry.get())[0]+':00'
            toTime = re.findall(timePattern, self.toEntry.get())[0]+':00'
            try:
                query = 'INSERT INTO AVAILABILITY (Username,Day_Date,From_Time,To_Time) VALUES ("{}","{}","{}","{}")'.format(self.username,date,fromTime,toTime)
                cursor = self.connect()
                cursor.execute(query)
                self.db.close()
                mbox.showinfo("Time Added","You have added an availability on {} from {} to {}".format(date, self.fromEntry.get(), self.toEntry.get()))
                return
            except:
                mbox.showerror("ERROR", "You have already added this availability.")
                return

        def createProfile():

            ##If a user that has already created a profile tries to hit create again, a SQL primary key error will be thrown and this will show the user a message
            try:
                LicenseNo = int(self.licenseEntry.get())
                First = self.fNameEntry.get()
                Last = self.lNameEntry.get()
                DOB = self.DdobEntry.get()
                specialty = self.specialty.get()
                workPhone = self.DworkPhoneEntry.get()
                roomNo = int(self.roomEntry.get())
                address = self.DaddressEntry.get()
                query = 'INSERT INTO DOCTOR VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(self.username,LicenseNo,First,Last,DOB,workPhone,specialty,roomNo,address)
                cursor = self.connect()
                cursor.execute(query)
                self.db.close()
                mbox.showinfo("Success", "Profile Created! Welcome Doctor!")
            except:
                mbox.showerror("Error", "User already created in Database!")
                self.createButton.config(state=DISABLED)
            
        def editProfile():

            LicenseNo = int(self.licenseEntry.get())
            First = self.fNameEntry.get()
            Last = self.lNameEntry.get()
            DOB = self.DdobEntry.get()
            specialty = self.specialty.get()
            workPhone = self.DworkPhoneEntry.get()
            roomNo = int(self.roomEntry.get())
            address = self.DaddressEntry.get()
            query = 'UPDATE DOCTOR SET LicenseNo="{}", FName="{}", LName="{}", DOB="{}", WorkPhone="{}", Specialty="{}", RoomNo="{}", WorkAddress="{}" WHERE Username="{}"'\
                    .format(LicenseNo,First,Last,DOB,workPhone,specialty,roomNo,address,self.username)
            cursor = self.connect()
            cursor.execute(query)
            self.db.close()
            self.profToDHP()
            mbox.showinfo("Success", "Profile Edited")
            return
            
        plusButton = ttk.Button(availableFrame, text='+', width=2.5, command=addTimes)
        plusButton.grid(row=0, column=6, padx=5)

        #Putting Buttons at the Bottom
        buttonFrame = Frame(bottomFrame)
        buttonFrame.grid(row=10, column=0, columnspan=5)
        buttonFrame.configure(background='#cfb53b')

        self.createButton = ttk.Button(buttonFrame, text='Create Profile', command=createProfile)
        self.createButton.pack(side=RIGHT, padx=5, pady=10)

        self.editProfButton = ttk.Button(buttonFrame, text='Edit Profile', command=editProfile)
        self.editProfButton.pack(side=RIGHT, padx=5, pady=10)






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

        makeAppointButton = Button(bottomFrame, text='Make Appointments', relief=FLAT, command=self.appointmentPage)
        makeAppointButton.grid(row=0, column=0, padx=20, pady=10, sticky='W')
        makeAppointButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        viewVisitButton = Button(bottomFrame, text='View Visit History', relief=FLAT, command=self.patHPToVisitHist)
        viewVisitButton.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        viewVisitButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        orderMedButton = Button(bottomFrame, text='Order Medication', relief=FLAT, command=self.patHPToOrderMeds)
        orderMedButton.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        orderMedButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        communicateButton = Button(bottomFrame, text='Communicate', relief=FLAT, command=self.patHPToComm)
        communicateButton.grid(row=3, column=0, padx=20, pady=10, sticky='W')
        communicateButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        rateDocButton = Button(bottomFrame, text='Rate a Doctor', relief=FLAT, command=self.patHpToRate)
        rateDocButton.grid(row=4, column=0, padx=20, pady=10, sticky='W')
        rateDocButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        editProfile = Button(bottomFrame, text='Edit Profile', relief=FLAT, command=self.patHPToEdit)
        editProfile.grid(row=5, column=0, padx=20, pady=10, sticky='W')
        editProfile.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        hardCodedSpaceLabel = Label(bottomFrame, text='                                          ')
        hardCodedSpaceLabel.grid(row=0, column=1)
        hardCodedSpaceLabel.configure(background='#cfb53b')
        

        cursor = self.connect()
        query = 'SELECT COUNT(*) FROM DOCTOR_TO_PATIENT WHERE Recipient = "{}" and Status = "Unread"'\
                .format(self.username)
        cursor.execute(query)
        messages = list(cursor.fetchall())[0][0]


        messageText = 'You have {} unread messages'.format(messages)
        self.unreadMsgButton = Button(bottomFrame, text=messageText, relief=FLAT, command=self.messagesPage)
        self.unreadMsgButton.grid(row=0, column=2, padx=10, pady=10)
        self.unreadMsgButton.configure(font=('Arial', 8),
                                       foreground='blue',
                                       background='#cfb53b')

        if messages == 0:
            self.unreadMsgButton.config(state=DISABLED)

        self.patHPWin.protocol("WM_DELETE_WINDOW", self.endProgram)

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

        viewAppointButton = Button(bottomFrame, text='View Appointments Calendar', relief=FLAT, command=self.searchAppt)
        viewAppointButton.grid(row=0, column=0, padx=20, pady=10, sticky='W')
        viewAppointButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        patientVisitsButton = Button(bottomFrame, text='Patient Visits', relief=FLAT, command=self.recordVisit)
        patientVisitsButton.grid(row=1, column=0, padx=20, pady=10, sticky='W')
        patientVisitsButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        recordSurgeryButton = Button(bottomFrame, text='Record Surgery', relief=FLAT)
        recordSurgeryButton.grid(row=2, column=0, padx=20, pady=10, sticky='W')
        recordSurgeryButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        communicateButton = Button(bottomFrame, text='Communicate', relief=FLAT)
        communicateButton.grid(row=3, column=0, padx=20, pady=10, sticky='W')
        communicateButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        editProfileButton = Button(bottomFrame, text='Edit Profile', relief=FLAT, command=self.docHPToProfile)
        editProfileButton.grid(row=4, column=0, padx=20, pady=10, sticky='W')
        editProfileButton.configure(font='Arial',
                                    foreground='blue',
                                    background='#cfb53b')

        hardCodedSpaceLabel = Label(bottomFrame, text='                                          ')
        hardCodedSpaceLabel.grid(row=0, column=1)
        hardCodedSpaceLabel.configure(background='#cfb53b')

        cursor = self.connect()
        query = 'SELECT COUNT(*) FROM PATIENT_TO_DOCTOR WHERE Recipient = "{}" and Status = "Unread"'\
                .format(self.username)
        cursor.execute(query)
        messages1 = list(cursor.fetchall())[0][0]
        query = 'SELECT COUNT(*) FROM DOCTOR_TO_DOCTOR WHERE Recipient = "{}" and Status = "Unread"'\
                .format(self.username)
        cursor.execute(query)
        messages2 = list(cursor.fetchall())[0][0]
        messages = messages1 + messages2
        self.db.close()


        messageText = 'You have {} unread messages'.format(messages)
        if messages == 0:
            messageText = 'You have no unread messages'
        self.unreadMsgButton = Button(bottomFrame, text=messageText, relief=FLAT, command=self.messagesPage)
        self.unreadMsgButton.grid(row=0, column=2, padx=10, pady=10)
        self.unreadMsgButton.configure(font=('Arial', 8),
                                  foreground='blue',
                                  background='#cfb53b')

        apptReqButton = Button(bottomFrame, text='Appointment Requests', relief=FLAT, command=self.apptRequests)
        apptReqButton.grid(row=1, column=2, padx=10)
        apptReqButton.configure(font=('Arial', 8),
                                  foreground='blue',
                                  background='#cfb53b')

        if messages == 0:
            self.unreadMsgButton.config(state=DISABLED)


        self.docHPWin.protocol("WM_DELETE_WINDOW", self.endProgram)

    def recordVisit(self):
        
        color = '#cfb53b'

        self.recordWin = Toplevel(LogWin)
        self.recordWin.title('Record/Prescribe')
        self.recordWin.configure(background='#cfb53b')

        topFrame = Frame(self.recordWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.recordWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.recordWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Record a Visit", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Visit History Frame
        attributes = ['Date of Visit: ', 'Patient Name: ', 'Blood Pressure: ', 'Diagnosis: ']
        count = 0
        for attribute in attributes:
            attribute_label = Label(bottomFrame, text=attribute, bg=color)
            attribute_label.grid(row=count, column=0, padx=5, pady=10, sticky=W)
            count += 1

        dateVisitEntry = Entry(bottomFrame,width=25)
        dateVisitEntry.grid(row=0,column=1, columnspan=5, sticky='W')

        patientNameEntry = Entry(bottomFrame, width=25)
        patientNameEntry.grid(row=1,column=1, columnspan=5, sticky='W')

        systolic_lbl = Label(bottomFrame, text='Systolic: ', bg=color)
        systolic_lbl.grid(row=2, column=1, sticky='W')

        systolic_entry = Entry(bottomFrame, width=5)
        systolic_entry.grid(row=2, column=2, padx=2)

        diastolic_lbl = Label(bottomFrame, text='Diastolic: ', bg=color)
        diastolic_lbl.grid(row=2, column=3, padx=2)

        diastolic_entry = Entry(bottomFrame, width=5)
        diastolic_entry.grid(row=2, column=4, padx=5)

        diagnosisText = Text(bottomFrame, width=22, height=4)
        diagnosisText.grid(row=3,column=1,columnspan=5, padx=10, pady=10, sticky='EW')

        def submitVisit():

            bill = 50

            visitDate = dateVisitEntry.get()
            patientName = patientNameEntry.get()
            SBP = systolic_entry.get()
            DBP = diastolic_entry.get()
            diagnosis = diagnosisText.get("1.0", END)

            query = 'SELECT Username FROM PATIENT WHERE Name="{}"'.format(patientName)
            cursor = self.connect()
            cursor.execute(query)
            patient = cursor.fetchone()[0]

            query = 'INSERT INTO VISIT VALUES ("{}", "{}", "{}", {}, {}, {})'.format(visitDate,self.username,patient,bill,SBP,DBP)
            cursor.execute(query)

            query = 'INSERT INTO DIAGNOSIS VALUES ("{}","{}","{}","{}")'.format(patient,visitDate,self.username,diagnosis)
            cursor.execute(query)

            query = 'INSERT INTO RECORDS VALUES ("{}","{}","{}")'.format(patient,self.username,visitDate)
            cursor.execute(query)

            self.db.commit()
            cursor.close()
            self.db.close()

        ##################This is where it splits to prescription#################

        separateFrame = Frame(self.recordWin, bd=1, background='black')
        separateFrame.grid(row=4, column=0, sticky='EW')

        prescriptionFrame = Frame(self.recordWin)
        prescriptionFrame.grid(row=5, column=0)
        prescriptionFrame.configure(background='#cfb53b')

        nameFrame = Frame(prescriptionFrame, background=color)
        nameFrame.grid(row=0, column=0, columnspan=6)

        prescribeName = Label(nameFrame, text="Prescribe", font=("Arial", 25))
        prescribeName.pack()
        prescribeName.configure(background='#cfb53b')

        attributes = ['Drug Name: ', 'Usage: ', 'Duration: ', 'Notes: ']
        count = 1
        for attribute in attributes:
            attribute_label = Label(prescriptionFrame, text=attribute, bg=color)
            attribute_label.grid(row=count, column=0, padx=5, pady=10, sticky=W)
            count += 1

        drugEntry = Entry(prescriptionFrame,width=25)
        drugEntry.grid(row=1,column=1, columnspan=5, sticky='W')

        usageEntry = Entry(prescriptionFrame, width=25)
        usageEntry.grid(row=2,column=1, sticky='W')
        Label(prescriptionFrame, text='mg/day', background=color).grid(row=2,column=2, columnspan=5, sticky='W')

        durationEntry = Entry(prescriptionFrame, width=5)
        durationEntry.grid(row=3, column=1, padx=2)
        Label(prescriptionFrame, text='days', background=color).grid(row=3, column=2, columnspan=5, padx=2)

        notes = Text(prescriptionFrame, width=22, height=4)
        notes.grid(row=4,column=1,columnspan=5, padx=10, pady=10, sticky='EW')

        def addPrescrip():
            print('Prescription Added')

        submitFrame = Frame(prescriptionFrame, background=color)
        submitFrame.grid(row=5, column=0, columnspan=6, pady=10, sticky='EW')

        ttk.Button(submitFrame, text='Add Prescription', command=addPrescrip).pack(fill=BOTH,pady=5)

        ttk.Button(submitFrame, text='Submit', command=submitVisit).pack(fill=BOTH, pady=5)
        
        formattingFrame = Frame(self.recordWin, background=color)
        formattingFrame.grid(row=6, column=0)
        spaceFormat = Label(formattingFrame, 
                            text='                                                                                                                                  ',
                            background=color).pack()

    def searchAppt(self):

        self.searchApptWin = Toplevel(LogWin)
        self.searchApptWin.title('Search Appointments')
        self.searchApptWin.config(bg=color)
        
        topFrame = Frame(self.searchApptWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.searchApptWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.searchApptWin)
        bottomFrame.grid(row=2, column=0, pady=15)
        bottomFrame.configure(background='#cfb53b')

        logo = ttk.Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = ttk.Label(topFrame, text="Search Appointments", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        dateLabel = Label(bottomFrame, text="Date: ", background=color)
        dateLabel.grid(row=0, column=0, padx=5, sticky='W')

        days = list(range(1,31))

        months = list(range(1,13))

        years = list(range(2014,2050,1))

        year = StringVar()
        year.set('----')
        month = StringVar()
        month.set('----')
        day = StringVar()
        day.set('----')

        self.apptYearEntry = ttk.Combobox(bottomFrame, textvariable=year, values=years, width=8)
        self.apptYearEntry.grid(row=0, column=1, padx=2, sticky="W")
        self.apptYearEntry.config(state='readonly')

        self.apptMonthEntry = ttk.Combobox(bottomFrame, textvariable=month, values=months, width=4)
        self.apptMonthEntry.grid(row=0, column=2, padx=2, sticky="W")
        self.apptMonthEntry.config(state='readonly')

        self.apptDayEntry = ttk.Combobox(bottomFrame, textvariable=day, values=days, width=6)
        self.apptDayEntry.grid(row=0, column=3, padx=2, sticky="W")
        self.apptDayEntry.config(state='readonly')

        def searchApptClick():

            year = self.apptYearEntry.get()
            month = self.apptMonthEntry.get()
            if len(month)<2:
                month = '0'+ month
            day = self.apptDayEntry.get()
            if len(day)<2:
                day = '0'+ day

            date = year+'-'+month+'-'+day
            query = '''SELECT P.Name,RA.ScheduledTime FROM REQUEST_APPOINTMENT AS RA
                    INNER JOIN PATIENT AS P 
                    ON P.Username = RA.PUsername
                    WHERE RA.DUsername="{}" AND RA.Status="Accepted" AND RA.Date="{}"'''.format(self.username, date)

            cursor = self.connect()
            cursor.execute(query)
            appts = list(cursor.fetchall())
            apptList = []
            for appt in appts:
                apptList.append([appt[0], appt[1]])

            apptFrame = Frame(bottomFrame, background=color)
            apptFrame.grid(row=1, column=0, padx=25, pady=20, sticky="EW", columnspan=6)

            headers = ['                 Patient                ',
                   '            Scheduled Time              ']

            for x in range(len(headers)):
                tableFrame = Frame(apptFrame, borderwidth=1, background='black')
                tableFrame.grid(row=0, column=x, sticky='EW', padx=1)
                label = Label(tableFrame, text=headers[x], background=color)
                label.pack(fill=BOTH)

            rows = 1
            for x in apptList:
                for y in range(len(x)):
                    tableFrame = Frame(apptFrame, borderwidth=1, background='black')
                    tableFrame.grid(row=rows, column=y, sticky='EW', padx=1, pady=1)
                    label = Label(tableFrame, text=x[y], background='white')
                    label.pack(fill=BOTH)
                rows+=1


        searchButton = ttk.Button(bottomFrame, text="View Appointments", command=searchApptClick)
        searchButton.grid(row=0, column=4, padx=5)

    def adminHomePage(self):

        self.adminHPWin = Toplevel(LogWin)
        self.adminHPWin.title('Administrator HomePage')
        self.adminHPWin.config(bg=color)
        
        topFrame = Frame(self.adminHPWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.adminHPWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.adminHPWin)
        bottomFrame.grid(row=2, column=0, pady=15)
        bottomFrame.configure(background='#cfb53b')

        logo = ttk.Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = ttk.Label(topFrame, text="Administrator HomePage", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')
        
        billing = Button(bottomFrame, text='Billing', relief=FLAT, fg='blue', command=self.Billing, background=color)
        billing.pack(anchor=CENTER, padx=10, pady=5)
        
        docReport = Button(bottomFrame, text='Doctor Performance Report', relief=FLAT, fg='blue', command=self.DocReport, background=color)
        docReport.pack(anchor=CENTER, padx=10, pady=5)
        
        surgeryReport = Button(bottomFrame, text='Surgery Report', relief=FLAT, fg='blue', command=self.SurgeryReport, background=color)
        surgeryReport.pack(anchor=CENTER, padx=10, pady=5)
        
        patientReport = Button(bottomFrame, text='Patient Visit Report', relief=FLAT, fg='blue', command=self.PatientReport, background=color)
        patientReport.pack(anchor=CENTER, padx=10, pady=5)

    def DocReport(self):

        self.adminHPWin.withdraw()

        self.DocReportWin = Toplevel(LogWin)
        self.DocReportWin.title('Doctor Performance Report')
        self.DocReportWin.config(bg=color)
        
        topFrame = Frame(self.DocReportWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.DocReportWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.DocReportWin)
        bottomFrame.grid(row=2, column=0, pady=15)
        bottomFrame.configure(background='#cfb53b')

        logo = ttk.Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = ttk.Label(topFrame, text="Doctor Performance Report", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        headers = ['       Specialty       ',
                   '    Number of Surgeries Performed  ',
                   '       Average Rating       ']

        for x in range(len(headers)):
            tableFrame = Frame(bottomFrame, borderwidth=1, background='black')
            tableFrame.grid(row=0, column=x, sticky='EW', padx=1)
            label = Label(tableFrame, text=headers[x], background=color)
            label.pack(fill=BOTH)


        query = '''SELECT Specialty, COUNT(DISTINCT P.CPT)AS Surgeries, AVG(R.Rating)AS AvgRating FROM DOCTOR AS D
                LEFT JOIN RATES AS R 
                ON R.DUsername = D.Username
                LEFT JOIN PERFORMS_SURGERY AS P
                ON D.Username = P.DUsername
                GROUP BY D.Specialty  '''

        cursor = self.connect()
        cursor.execute(query)

        info = list(cursor.fetchall())
        rows = 1
        for x in info:
            x = list(x)
            x[2] = str(x[2])[0:4]
            for y in range(len(x)):
                tableFrame = Frame(bottomFrame, borderwidth=1, background='black')
                tableFrame.grid(row=rows, column=y, sticky='EW', padx=1, pady=1)
                label = Label(tableFrame, text=x[y], background='white')
                label.pack(fill=BOTH)
            rows+=1

        cursor.close()

        self.DocReportWin.protocol("WM_DELETE_WINDOW", self.DocReportToAdminWin)


    def SurgeryReport(self):
        pass

    def PatientReport(self):
        pass

        # SELECT D.FName,LName, COUNT(V.PUsername) AS "No. of Patients", COUNT(P.MedName),SUM(V.BillingAmt) FROM DOCTOR AS D 
        # LEFT JOIN PRESCRIPTION AS P ON D.Username = P.DUsername
        # INNER JOIN VISIT AS V ON D.Username = V.DUsername
        # GROUP BY D.Username

    def Billing(self):
        pass

                                  
    def VisitHistory(self):

        color = '#cfb53b'

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

        logo = ttk.Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = ttk.Label(topFrame, text="Visit History", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        #Main Body
        date_visits_frame = Frame(bottomFrame, bg=color)
        date_visits_frame.grid(row=1, column=0, rowspan=5, sticky=N)
        
        dateVisitsLabel = Label(date_visits_frame, text='Dates of Visits', background=color)
        dateVisitsLabel.grid(row=0, column=0, sticky=N)

        #Date Visits Listbox
        username = self.username_entry.get()
        cursor = self.connect()

        cursor.execute("SELECT DateVisit FROM VISIT WHERE PUsername='%s'" % (username))
        result = cursor.fetchall()
        date_visits = ()
        for date in result:
            date_visits += (date[0],)
        
        self.dateVisits = StringVar(value=date_visits)

        date_visits_lbox = Listbox(date_visits_frame, listvariable=self.dateVisits, width=12, height=5)
        date_visits_lbox.grid(row=1, column=0, padx=10, sticky=N)

        #Vertical Separator
        separator = ttk.Separator(bottomFrame, orient=VERTICAL)
        separator.grid(row=1, column=1, pady=5, sticky='NSW', rowspan=4)

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

        diagnosis = Text(bottomFrame, width=22, height=4)
        diagnosis.grid(row=3, column=2, padx=10, sticky=W)
        
        meds_frame = Frame(bottomFrame, bg='black')
        meds_frame.grid(row=4, column=2, sticky=W)

        col_names = ['Medicine Name', 'Dosage', 'Duration', 'Notes']

        for i in range(len(col_names)):
            label = Label(meds_frame, text=col_names[i], bg='white')
            label.grid(row=0, column=i, padx=1, pady=1, sticky=NSEW)

        self.visitHistWin.protocol("WM_DELETE_WINDOW", self.visitHistToHP)

    def visitReport(self):
        
        self.docHPWin = Toplevel(LogWin)
        self.docHPWin.title('Visit Report')
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
        pageName = Label(topFrame, text="Patient Visit Report", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

    def RateDoctor(self):

        color = '#cfb53b'

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
        result = cursor.fetchall()
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

        self.rateWin.protocol("WM_DELETE_WINDOW", self.rateToHP)

    def SubmitRating(self):

        try:
            rating = int(self.rating.get())
        except:
            mbox.showerror("ERROR", "Select a Rating")
            return
        patient_username = self.username
        doc_name = self.doctor.get()
        doc_name = doc_name[4:]
        doc_name = doc_name.split()
        fname = doc_name[0]
        lname = doc_name[1]
        query = "SELECT Username FROM DOCTOR WHERE FName='%s' AND LName='%s'" % (fname, lname)

        cursor = self.connect()

        cursor.execute(query)
        result = cursor.fetchall()
        doc_username = result[0][0]

        try:
            cursor.execute("INSERT INTO RATES(PUsername, DUsername, Rating) VALUES('{0}', '{1}', {2})".format(patient_username, doc_username, rating))
        except:
            mbox.showerror("ERROR", "You have already rated this doctor!")
            return

        self.rateWin.protocol("WM_DELETE_WINDOW", self.rateToHP)

        info = mbox.showinfo("Rating Doctor", "Rating submitted!")
        self.doctor.set('--Select a Specialist--')
        self.rating.set('----')
        self.rateToHP()
        return

    def OrderMeds(self):

        color = '#cfb53b'

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

        per = Label(dosage_frame, text='mg/day', bg=color)
        per.grid(row=0, column=1, sticky=W)

        duration_frame = Frame(bottomFrame)
        duration_frame.grid(row=3, column=1, sticky=W)

        self.duration_days = Entry(duration_frame, width=5)
        self.duration_days.grid(row=0, column=0, sticky=W)

        days = Label(duration_frame, text='days', bg=color)
        days.grid(row=0, column=1, sticky=W)

        self.consulting_doctor = Entry(bottomFrame, width=30)
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
        
        add = Button(bottomFrame, text='Add medication to basket', relief=FLAT, fg='blue', bg=color, command=self.AddMeds)
        add.grid(row=6, column=1, padx=10, pady=10)
        
        checkout = ttk.Button(bottomFrame, text='Checkout', cursor='hand2', command=self.PaymentInfo)
        checkout.grid(row=6, column=2, padx=10, pady=10)

        self.orderWin.protocol("WM_DELETE_WINDOW", self.orderToHP)
        
    def AddMeds(self):

        meds_name = self.meds_name.get()
        dosage = self.dosage_amount.get()
        duration_days = self.duration_days.get()
        docFname, docLname = self.consulting_doctor.get().split()
        
        cursor = self.connect()
        query = 'SELECT Username FROM DOCTOR WHERE FName="{}" AND LName="{}"'.format(docFname,docLname)
        cursor.execute(query)
        consulting_doc = cursor.fetchone()
        date_prescription = self.prescrip_year.get() + '-' + self.prescrip_month.get() + '-' + self.prescrip_day.get()

        query = 'SELECT COUNT(*) FROM PRESCRIPTION WHERE MedName="{}" AND Dosage="{}" AND Duration="{}" AND DUsername="{}" AND DateVisit="{}" AND PUsername="{}" AND Ordered="N"'\
                .format(meds_name, dosage, duration_days, consulting_doc[0], date_prescription, self.username)
        cursor.execute(query)
        if cursor.fetchone()[0] != 0:
            mbox.showinfo("Medicine Added", "Your prescription has been added to the cart")
            query = 'UPDATE PRESCRIPTION SET Ordered="Y" WHERE PUsername="{}"'.format(self.username)
            cursor.execute(query)
            self.db.commit()
            return
        else:
            mbox.showerror("ERROR", "You have not been prescribed this medication")
            return

        
    def sendMessage(self):

        self.messageWin = Toplevel(LogWin)
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

        cursor = self.connect()
        if self.userType == 'patient':

            query = 'SELECT FName,LName FROM DOCTOR'
            cursor.execute(query)
            doctorsList = list(cursor.fetchall())
            recipNames = []
            for doctor in doctorsList:
                recipNames.append(doctor[0]+' '+doctor[1])

        if self.userType == 'doctor':

            query = 'SELECT FName,LName FROM DOCTOR'
            cursor.execute(query)
            doctorsList = list(cursor.fetchall())
            query = 'SELECT FName,LName FROM PATIENT'
            cursor.execute(query)
            patientList = list(cursor.fetchall())
            doctorsList.extend(patientList)
            recipients = doctorsList

            recipNames = []
            for recipient in recipients:
                recipNames.append(recipient[0]+' '+recipient[1])

        cursor.close()
        self.db.close()

        self.sendTo = StringVar()
        self.sendTo.set('------')


        toFrame = Frame(bottomFrame, background='#cfb53b')
        toFrame.pack(pady=15)
        Label(toFrame, text='Select Name:   ', background='#cfb53b').grid(row=0, column=0)
        contactPulldown = ttk.Combobox(toFrame, textvariable=self.sendTo, values=recipNames)
        contactPulldown.grid(row=0, column=1, sticky='w')

        messageFrame = Frame(bottomFrame, background='#cfb53b')
        messageFrame.pack(padx=10, pady=20)

        text = """""".strip()

        scroll = Scrollbar(messageFrame)
        scroll.grid(row=0, column=1, sticky='NS')

        self.box = Text(messageFrame, wrap='word', font='Arial 12', relief=GROOVE)

        scroll.config()

        self.box.config(height=10, width=40)
        self.box.config()
        self.box.insert(1.0, text)
        self.box.grid(row=0, column=0, sticky='EW')

        scroll.config(command=self.box.yview)
        self.box.config(yscrollcommand=scroll.set)

        Button(bottomFrame, text='Send Message', command=self.getMessage).pack(pady=5, anchor=CENTER)

        self.messageWin.protocol("WM_DELETE_WINDOW", self.CommToPatHP)

    def getMessage(self):

        message = self.box.get("1.0", 'end')
        recipient = self.sendTo.get()
        cursor = self.connect()

        name = recipient.split()
        query = 'SELECT * FROM DOCTOR WHERE FName="{}" AND LName="{}"'.format(name[0], name[1])
        cursor.execute(query)
        recipUsername = cursor.fetchone()
        if recipUsername[0]:
            self.recipientType = 'doctor'
        else:
            self.recipientType = 'patient'
            query = 'SELECT Username FROM PATIENT WHERE FName="{}" AND LName="{}"'.format(name[0], name[1])
            cursor.execute(query)
            recipUsername = cursor.fetchone()
            recipUsername = recipUsername[0]


        if self.userType == 'patient':
            query = '''INSERT INTO PATIENT_TO_DOCTOR (Sender,Recipient,Content,DateTime,Status) VALUES ("{}","{}","{}",CURRENT_TIMESTAMP,"{}")'''.format(self.username, recipient, message, "Unread")
            cursor.execute(query)
            mbox.showinfo(title='Message Sent', message='Message Sent!')
            self.box.delete("1.0", END)
            self.CommToPatHP()


        elif self.userType == 'doctor':

            if self.recipientType == 'doctor':
                query = '''INSERT INTO DOCTOR_TO_DOCTOR Sender,Recipient,Content,DateTime,Status
                        VALUES ("{}","{}","{}",CURRENT_TIMESTAMP,"{}")'''\
                        .format(self.username, recipUsername[0], message, "Unread")
                cursor.execute(query)
                mbox.showinfo(title='Message Sent', message='Message Sent!')
                self.box.delete("1.0", END)
                self.sendTo.set('----')
                self.CommToPatHP()


            elif self.recipientType == 'patient':
                query = '''INSERT INTO DOCTOR_TO_PATIENT Sender,Recipient,Content,DateTime,Status
                        VALUES ("{}","{}","{}",CURRENT_TIMESTAMP,"{}")'''\
                        .format(self.username, recipUsername, message, "Unread")
                cursor.execute(query)
                mbox.showinfo(title='Message Sent', message='Message Sent!')
                self.box.delete("1.0", END)
                self.sendTo.set('----')
                self.CommToPatHP()


        cursor.close()
        self.db.close()

    def apptRequests(self):

        self.requestWin = Toplevel(LogWin)
        self.requestWin.title('Appointment Requests')
        self.requestWin.configure(background='#cfb53b')

        topFrame = Frame(self.requestWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.requestWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.requestWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Appointment Requests", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        cursor = self.connect()
        query = 'SELECT Name,Date,ScheduledTime FROM REQUEST_APPOINTMENT LEFT JOIN PATIENT ON PUsername = Username WHERE DUsername = "{}" AND Status = "Pending"'\
                .format(self.username)
        cursor.execute(query)
        requests = list(cursor.fetchall())

        requestList = []
        
        for request in requests:
            requestList.append([request[0], request[1], request[2]])

        headers = ['       Name      ',
                   '       Date       ',
                   '        Scheduled Time       ']

        acceptDict = {}
        declineDict = {}
        frameDict = {}

        for x in range(len(requestList)):
            acceptDict[x] = requestList[x]
            declineDict[x] = requestList[x]
            frameDict[x] = requestList[x]

        def AcceptAppt( e):
            for x in range(len(acceptDict)):
                if e.widget == acceptDict[x]:

                    
                    Pname = requestList[x][0]

                    cursor = self.connect()
                    query = 'SELECT Username FROM PATIENT WHERE Name = "{}"'.format(Pname)
                    cursor.execute(query)
                    patient = cursor.fetchone()

                    query = 'SELECT FName, LName FROM DOCTOR WHERE Username = "{}"'.format(self.username)
                    cursor.execute(query)
                    dName = cursor.fetchone()
                    doctor = 'Dr. '+dName[0] + ' ' + dName[1]

                    message = 'Appointment Accepted \n\n'+ 'Day: '+ requestList[x][1] +'\n'+ 'Time: ' + requestList[x][2] + '\n' + 'Specialist: ' + doctor

                    query = 'INSERT INTO DOCTOR_TO_PATIENT (Sender,Recipient,Content,Status,DateTime) VALUES ("{}","{}","{}","Unread",CURRENT_TIMESTAMP)'.format(self.username,patient[0],message)

                    cursor.execute(query)

                    query = 'UPDATE REQUEST_APPOINTMENT SET Status="Accepted" WHERE DUsername="{}" AND PUsername="{}"'.format(self.username,patient[0])
                    cursor.execute(query)
                    cursor.close()
                    self.db.commit()
                    self.db.close()


        def DeclineAppt( e):
            for x in range(len(declineDict)):
                if e.widget == declineDict[x]:
                    doc_username = self.username
                    cursor = self.connect()
                    query = "SELECT PUsername FROM REQUEST_APPOINTMENT LEFT JOIN PATIENT ON PUsername = Username WHERE Name='{}' AND Date='{}' AND ScheduledTime='{}'"\
                            .format(requestList[x][0], requestList[x][1], requestList[x][2])
                    cursor.execute(query)
                    result = cursor.fetchall()
                    patient_username = result[0][0]

                    query = "DELETE FROM REQUEST_APPOINTMENT WHERE PUsername='{}' AND DUsername='{}' AND Date='{}' AND ScheduledTime='{}'".format(patient_username, doc_username, requestList[x][1], requestList[x][2])
                    cursor.execute(query)
                    frameDict[x].destroy()

        requestFrame = Frame(bottomFrame, bg=color)
        requestFrame.grid(row=0, column=0, sticky='NSEW', padx=15, pady=15)

        for x in range(len(headers)):
            tableFrame = Frame(requestFrame, borderwidth=1, background='black')
            tableFrame.grid(row=0, column=x, sticky='EW', padx=1)
            label = Label(tableFrame, text=headers[x], background=color)
            label.pack(fill=BOTH)

        for x in range(len(requestList)):
            for y in range(len(requestList[x])):
                tableFrame = Frame(requestFrame, borderwidth=1, background=color)
                tableFrame.grid(row=x+1, column=y, sticky='NSEW', padx=1, pady=5)
                label = Label(tableFrame, text=requestList[x][y], background='white')
                label.pack(fill=BOTH)

            acceptDict[x] = ttk.Button(requestFrame, width=8, text='Accept')
            acceptDict[x].bind("<ButtonRelease-1>", AcceptAppt)
            acceptDict[x].grid(row=x+1, column=3, padx=5)
            
            declineDict[x] = ttk.Button(requestFrame, width=8, text='Decline')
            declineDict[x].bind("<ButtonRelease-1>", DeclineAppt)
            declineDict[x].grid(row=x+1, column=4, padx=5)

        self.requestWin.protocol("WM_DELETE_WINDOW", self.requestsToDocHP)

    def messagesPage(self):

        cursor = self.connect()

        self.readMessageWin= Toplevel(LogWin)
        self.readMessageWin.title('Messages')
        self.readMessageWin.configure(background='#cfb53b')

        topFrame = Frame(self.readMessageWin)
        topFrame.grid(row=0, column=0)
        topFrame.configure(background='#cfb53b')
        midFrame = Frame(self.readMessageWin, bd=1, background='black')
        midFrame.grid(row=1, column=0, sticky='EW')
        bottomFrame = Frame(self.readMessageWin)
        bottomFrame.grid(row=2, column=0)
        bottomFrame.configure(background='#cfb53b')

        logo = Label(topFrame, image=self.photo)
        logo.grid(row=0, column=1)
        logo.configure(background='#cfb53b')
        pageName = Label(topFrame, text="Messages", font=("Arial", 25))
        pageName.grid(row=0, column=0, sticky='EW')
        pageName.configure(background='#cfb53b')

        messageFrame = Frame(bottomFrame, bg=color)
        messageFrame.grid(row=0, column=0, sticky='NSEW', padx=15, pady=15)

        headers = ['       Sender       ',
                   '       Status       ',
                   '        Content       ',
                   '       Time       ']

        for x in range(len(headers)):
            tableFrame = Frame(messageFrame, borderwidth=1, background='black')
            tableFrame.grid(row=0, column=x, sticky='EW', padx=1)
            label = Label(tableFrame, text=headers[x], background=color)
            label.pack(fill=BOTH)

        if self.userType == 'patient':
            tableName = 'DOCTOR_TO_PATIENT'
            query = '''SELECT Sender, Content, Status, DateTime
                    FROM '''+tableName+''' WHERE Status = "Unread" AND Recipient = "{}"'''.format(self.username)
            cursor.execute(query)
            unreadMessages = list(cursor.fetchall())

            unreadMessagesList = []
            for mssg in unreadMessages:
                unreadMessagesList.append([mssg[0], mssg[2], mssg[1], mssg[3]])

        elif self.userType == 'doctor':
            tableName = ['DOCTOR_TO_DOCTOR', 'PATIENT_TO_DOCTOR']
            query = '''SELECT Sender, Content, Status, DateTime
                    FROM '''+tableName[0]+''' WHERE Status = "Unread" AND Recipient = "{}"'''.format(self.username)

            cursor.execute(query)
            unreadMessages = list(cursor.fetchall())

            query = '''SELECT Sender, Content, Status, DateTime
                    FROM '''+tableName[1]+''' WHERE Status = "Unread" AND Recipient = "{}"'''.format(self.username)

            cursor.execute(query)
            unreadMessages2 = list(cursor.fetchall())


            unreadMessages.extend(unreadMessages2)

        unreadMessagesList = []
        for mssg in unreadMessages:
            unreadMessagesList.append([mssg[0], mssg[2], mssg[1], mssg[3]])

        for x in range(len(unreadMessagesList)):
            for y in range(len(unreadMessagesList[x])):
                tableFrame = Frame(messageFrame, borderwidth=1, background=color)
                tableFrame.grid(row=x+1, column=y, sticky='NSEW', padx=1, pady=5)
                label = Label(tableFrame, text=unreadMessagesList[x][y], background='white')
                label.pack(fill=BOTH)

        if self.userType == 'patient':
            tableName = 'DOCTOR_TO_PATIENT'
            query = 'UPDATE '+tableName+' SET Status = "Read" WHERE Status = "Unread" AND Recipient = "{}"'.format(self.username)
            cursor.execute(query)
            self.db.commit()
            self.unreadMsgButton.config(text="You have no new messages", state=DISABLED)

        elif self.userType == 'doctor':
            tableName = ['DOCTOR_TO_DOCTOR', 'PATIENT_TO_DOCTOR']
            query = '''UPDATE '''+tableName[0]+''' SET Status="Read" WHERE Recipient = "{}"'''.format(self.username)
            cursor.execute(query)
            query = '''UPDATE '''+tableName[1]+''' SET Status="Read" WHERE Recipient = "{}"'''.format(self.username)
            cursor.execute(query)
            self.db.commit()
            self.unreadMsgButton.config(text="You have no new messages", state=DISABLED)

        self.db.close()

        if self.userType == 'patient':
            self.readMessageWin.protocol("WM_DELETE_WINDOW", self.MssgToHP)
        elif self.userType =='doctor':
            self.readMessageWin.protocol("WM_DELETE_WINDOW", self.MssgToDocHP)

    def PaymentInfo(self):

        color = '#cfb53b'

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

        years = list(range(14, 99))
        months = list(range(1, 13))
        
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

        order = ttk.Button(bottomFrame, text='Order', cursor='hand2', command=self.PayMeds)
        order.grid(row=6, column=2, padx=5, pady=5)

    def appointmentPage(self):

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

        self.apptWin.protocol("WM_DELETE_WINDOW", self.ApptToPatHP)

    def updateAppts(self):

        try:
            self.specialistPulldown.destroy()
            self.rateLabel.destroy()
            self.timeSlot.destroy()
            self.timePulldown.destroy()
            self.requestButton.destroy()
        except:
            pass

        cursor = self.connect()

        query = "SELECT Username,FName,LName FROM `DOCTOR` WHERE Specialty = '{}'".format(self.specialty.get())
        cursor.execute(query)
        specialists = list(cursor.fetchall())

        self.db.close()

        doctorsList = []
        for specialist in specialists:
            doctorsList.append(specialist[1]+' '+specialist[2])

        self.docSelected = StringVar()

        self.docSelected.set('--Select A Specialist--')

        self.selectionFrame = Frame(self.apptWin, background='#cfb53b')
        self.selectionFrame.grid(row=3, column=0, pady=10)
        self.specialistPulldown = ttk.Combobox(self.selectionFrame, textvariable=self.docSelected, values=doctorsList)
        self.specialistPulldown.config(state='readonly')
        self.specialistPulldown.config(width=30)

        Label(self.selectionFrame, text='Specialist:   ', background='#cfb53b').grid(row=0, column=0, padx=5, pady=10, sticky='W')

        self.specialistPulldown.grid(row=0, column=1, padx=5, pady=10, sticky='EW')
        self.rateLabel = Label(self.selectionFrame, text='Avg Rating: ')
        self.rateLabel.grid(row=0, column=2, padx=5, pady=10, sticky='W')
        self.rateLabel.configure(background='#cfb53b')

        self.specialistPulldown.bind("<<ComboboxSelected>>", self.specialistSelected)

    def specialistSelected(self, event=NONE):

        try:
            self.apptDateY.destroy()
            self.apptDateD.destroy()
            self.apptDateM.destroy()
            self.timeSlot.destroy()
            self.timePulldown.destroy()
        except:
            pass

        cursor = self.connect()

        docName = self.docSelected.get().split()

        userNameQuery = 'SELECT Username FROM DOCTOR WHERE FName = "{}" AND LName = "{}"'.format(docName[0], docName[1])
        cursor.execute(userNameQuery)
        username = cursor.fetchone()[0]

        avgRatingQ = 'SELECT AVG(Rating) FROM RATES WHERE DUsername="{}"'.format(username)
        cursor.execute(avgRatingQ)

        try:
            avgRating = float(self.cursor.fetchone()[0])
            self.rateLabel.config(text='Avg Rating: %0.2f'%(avgRating))
        except:
            self.rateLabel.config(text='No Ratings')

        timeQuery = '''SELECT Day_Date
                        FROM AVAILABILITY
                        NATURAL JOIN DOCTOR
                        WHERE DOCTOR.Username = AVAILABILITY.Username
                        AND DOCTOR.Username = "{}"'''.format(username)

        cursor.execute(timeQuery)
        times = list(self.c.fetchall())
        timesList = []
        ##Year Day Month
        years = []
        days =[]
        months = []
        for timeSlot in times:
            Y,M,D = str(timeSlot[0]).split('-')
            if Y not in years:
                years.append(Y)
            if D not in days:
                days.append(D)
            if M not in months:
                months.append(M)
        years.sort()
        days.sort()
        months.sort()
        
        self.apptYear = StringVar()
        self.apptYear.set('----')
        self.apptDay = StringVar()
        self.apptDay.set('----')
        self.apptMonth = StringVar()
        self.apptMonth.set('----')

        timeFrame = Frame(self.selectionFrame)
        timeFrame.grid(row=1,column=0,columnspan=3)
        timeFrame.configure(background=color)

        apptDateLabel = Label(timeFrame, text='Date:   ', background='#cfb53b')
        apptDateLabel.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        self.apptDateY = ttk.Combobox(timeFrame, textvariable=self.apptYear, values=years)
        self.apptDateY.config(state='readonly')
        self.apptDateY.config(width=8)
        self.apptDateY.grid(row=0, column=1, padx=2, pady=5, sticky='W')

        self.apptDateM = ttk.Combobox(timeFrame, textvariable=self.apptMonth, values=months)
        self.apptDateM.config(state='readonly')
        self.apptDateM.config(width=6)
        self.apptDateM.grid(row=0, column=2, padx=2, pady=5, sticky='W')

        self.apptDateD = ttk.Combobox(timeFrame, textvariable=self.apptDay, values=days)
        self.apptDateD.config(state='readonly')
        self.apptDateD.config(width=4)
        self.apptDateD.grid(row=0, column=3, padx=2, pady=5, sticky='W')

        self.disableRequest = FALSE

        cursor.close()

        def dateSelected():

            try:
                self.timeSlot.destroy()
                self.timePulldown.destroy()
            except:
                pass

            cursor = self.connect()

            self.timeSelected = StringVar()
            self.timeSelected.set('--Select A Time--')

            self.apptDate = self.apptDateY.get() + '-' + self.apptDateM.get() + '-' + self.apptDateD.get()

            query = '''SELECT From_Time,To_Time
                        FROM AVAILABILITY
                        NATURAL JOIN DOCTOR
                        WHERE DOCTOR.Username = AVAILABILITY.Username
                        AND DOCTOR.Username = "{}" AND AVAILABILITY.Day_Date = "{}"'''.format(username,self.apptDate)

            cursor.execute(query)
            apptTimes = list(cursor.fetchall())
            apptTimesList = []
            for time in apptTimes:
                apptTimesList.append(str(time[0])+' - '+str(time[1]))

            self.timeSlot = Label(timeFrame, text='Time Slot:   ', background='#cfb53b')
            self.timeSlot.grid(row=1, column=0, padx=5, pady=5, sticky='W')

            self.timePulldown = ttk.Combobox(timeFrame, textvariable=self.timeSelected, values=apptTimesList)
            self.timePulldown.config(state='readonly')
            self.timePulldown.config(width=15)
            self.timePulldown.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='W')

            if not apptTimesList:
                self.timePulldown.config(values=['No Available Times'], state=DISABLED)
                self.disableRequest = TRUE

            cursor.close()

        searchDateButton = Button(timeFrame, text='Search For Times', command=dateSelected)
        searchDateButton.grid(row=0, column=4, padx=5)

        def RequestAppt():

            cursor = self.connect()

            patient_username = self.username
            doc_username = username
            cursor.execute("SELECT COUNT(*) FROM REQUEST_APPOINTMENT WHERE PUsername='%s'" % (patient_username))
            result=self.c.fetchall()
            #If user is visiting for first time
            if result[0][0] == 0:
                scheduled_appt = self.timeSelected.get()
                pattern = '(\d+:\d+:00 - \d+:\d+:00)'
                scheduled_time = findall(pattern, scheduled_appt)[0]
                cursor.execute("INSERT INTO REQUEST_APPOINTMENT(PUsername, DUsername, Date, ScheduledTime, Status) VALUES('%s', '%s', '%s', '%s', 'Pending')" % (patient_username, doc_username, self.apptDate, scheduled_time))
                self.db.commit()
                info = mbox.showinfo("Appointment Requests", "Appointment requests complete.")
                self.apptWin.destroy()
            #Wait for request to be accepted
            else:
                scheduled_appt = self.timeSelected.get()
                pattern = '(\d+:\d+:00 - \d+:\d+:00)'
                scheduled_time = findall(pattern, scheduled_appt)[0]
                cursor.execute("INSERT INTO REQUEST_APPOINTMENT(PUsername, DUsername, Date, ScheduledTime, Status) VALUES('%s', '%s', '%s', '%s', 'Accepted')" % (patient_username, doc_username, self.apptDate, scheduled_time))
                self.db.commit()
                info = mbox.showinfo("Appintment Requests Status", "Your appointment request has been sent to the specified doctors.")                
                self.apptWin.destroy()
            cursor.close()        
        self.requestButton = ttk.Button(self.selectionFrame, text='Request Appointment', command=RequestAppt)
        self.requestButton.grid(row=2, column=0, columnspan=3, pady=5, sticky='EW')
        
        if self.disableRequest:
            self.requestButton.config(state=DISABLED)

        self.db.close()

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

                            ##If patient is registering, insert. If updating, Update
                            if self.Registering:
                                query = '''INSERT INTO PATIENT(Name,HomePhone,Username,DOB,Gender,Address,WorkPhone,Height,Weight,AnnualIncome)
                                        VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''\
                                        .format(PName, HomePhone, self.username_entry.get(), DOB, Gender, Address, WorkPhone, Height, Weight, AnnualIncome)
                            else:
                                query = 'UPDATE PATIENT SET Name="{}", HomePhone="{}", Username="{}", DOB="{}", Gender="{}", Address="{}", WorkPhone="{}", Height="{}", Weight="{}", AnnualIncome="{}" WHERE Username="{}"'\
                                        .format(PName, HomePhone, self.username, DOB, Gender, Address, WorkPhone, Height, Weight, AnnualIncome,self.username)
                            self.c.execute(query)
                            
                            self.patientWin.destroy()
                            self.patientScreens()

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

        name = self.cardholder_name.get()
        number = self.card_number.get()
        cardType = self.card_type.get()
        expiryY = self.expiry_year.get()
        expiryM = self.expiry_month.get()
        if len(expiryM)<2:
            expiryM = '0'+ expiryM
        expiry = expiryM +'/'+ expiryY
        CVV = self.cvv.get()

        cursor = self.connect()

        query = 'UPDATE PATIENT SET CreditCardNo="{}" WHERE Username="{}"'.format(number,self.username)
        cursor.execute(query)

        query = 'INSERT INTO PAYMENT_INFO (CardNo,CardHolderName,CardType,Expiry,CVV) VALUES({},"{}","{}","{}",{})'.format(number,name,cardType,expiry,CVV)

        cursor.execute(query)
        self.db.commit()

        mbox.showinfo("Order Complete", "Your medication has been ordered")
    
    def EditProfile(self):
        self.Registering = FALSE
        username = self.username_entry.get()
        self.c.execute("SELECT COUNT(*) FROM PATIENT WHERE Username= %s", (username))
        result = self.c.fetchall()
        if result[0][0] == 1:
            self.patientProfile()
        else:
            self.c.execute("SELECT COUNT(*) FROM DOCTOR WHERE Username= %s", (username))
            result = self.c.fetchall()
            if result[0][0]  == 1:
                self.doctorProfile()
                

    def patHPToAppts(self):

        self.patHPWin.withdraw()
        self.apptWin.deiconify()

    def patHPToVisitHist(self):

        self.patHPWin.withdraw()
        self.visitHistWin.deiconify()

    def patHPToOrderMeds(self):

        self.patHPWin.withdraw()
        self.orderWin.deiconify()

    def patHPToComm(self):

        self.patHPWin.withdraw()
        self.messageWin.deiconify()

    def patHpToRate(self):

        self.patHPWin.withdraw()
        self.rateWin.deiconify()

    def patHPToEdit(self):

        self.patHPWin.withdraw()
        self.patientWin.deiconify()

    def patHPToMessages(self):

        self.patHPWin.withdraw()
        self.readMessageWin.deiconify()

    def EditToHP(self):

        self.patientWin.withdraw()
        self.patHPWin.deiconify()

    def visitHistToHP(self):

        self.visitHistWin.withdraw()
        self.patHPWin.deiconify()

    def orderToHP(self):

        self.orderWin.withdraw()
        self.patHPWin.deiconify()

    def orderToPay(self):

        self.orderWin.withdraw()
        self.payWin.deiconify()

    def rateToHP(self):

        self.rateWin.withdraw()
        self.patHPWin.deiconify()

    def MssgToHP(self):

        self.readMessageWin.withdraw()
        self.patHPWin.deiconify()

    def ApptToPatHP(self):

        self.apptWin.destroy()
        self.patHPWin.deiconify()

    def CommToPatHP(self):

        self.messageWin.withdraw()
        self.patHPWin.deiconify()

    def docHPToRequests(self):

        self.docHPWin.withdraw()
        self.requestWin.deiconify()

    def docHPToProfile(self):

        self.docHPWin.withdraw()
        self.doctorWin.deiconify()

    def profToDHP(self):

        self.doctorWin.withdraw()
        self.docHPWin.deiconify()

    def requestsToDocHP(self):

        self.requestWin.withdraw()
        self.docHPWin.deiconify()

    def MssgToDocHP(self):

        self.readMessageWin.withdraw()
        self.docHPWin.deiconify()

    def DocReportToAdminWin(self):

        self.DocReportWin.destroy()
        self.adminHPWin.deiconify()

    def patientScreens(self):

        self.patientHomePage()

        self.doctorProfile()
        self.doctorWin.withdraw()

        self.Register()
        self.newRegWin.withdraw()

        self.patientProfile()
        self.patientWin.withdraw()

        self.VisitHistory()
        self.visitHistWin.withdraw()

        self.OrderMeds()
        self.orderWin.withdraw()

        self.PaymentInfo()
        self.payWin.withdraw()

        self.RateDoctor()
        self.rateWin.withdraw()

        self.sendMessage()
        self.messageWin.withdraw()

    def doctorScreens(self):

        self.doctorHomePage()

        self.doctorProfile()
        self.doctorWin.withdraw()

    def adminScreens(self):
        
        self.adminHomePage()

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

    def endProgram(self, event=NONE):
        #If DB is already closed, just destroy the main window to end the program
        try:
            self.db.close()
            LogWin.destroy()
        except:
            LogWin.destroy()



color = '#cfb53b'
LogWin = Tk() #This will be where the login page goes.
LogWin.title('GTMS Login')
LogWin.configure(background='#cfb53b')
obj = GTMS(LogWin)
LogWin.mainloop()

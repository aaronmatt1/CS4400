#Use patient: Juan Borjas and DateVisit: 2014-04-02

def PatientVisits(self):
        self.patientVisitsWin = Toplevel()
        pvw = self.patientVisitsWin
        pvw.config(bg=color)
        pvw.title('Patient Visit History')
        
        #Top Banner
        banner = Label(pvw, bg=color, width=450, height=50, text='Patient Visit History', padx=10,
                       font=('Berlin Sans FB', 18), image=self.photo,
                       compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=4)

        #Main Body
        name = Label(pvw, text='Name: ', bg=color)
        name.grid(row=1, column=0, sticky=E)

        name = Entry(pvw, width=20)
        name.grid(row=1, column=1, pady=5, sticky=W)

        phone = Label(pvw, text='Phone: ', bg=color)
        phone.grid(row=1, column=2, sticky=E)

        home_phone = Entry(pvw, width=15)
        home_phone.grid(row=1, column=3, sticky=W)

        patient_frame = Frame(pvw, bg='black')
        patient_frame.grid(row=2, column=0, columnspan=3, sticky=W)

        

        def ViewHistory():
            visit_frame = Frame(pvw, bg=color)
            visit_frame.grid(row=3, columnspan=4, padx=2, pady=2)
            
            date_visits_label = Label(visit_frame, text='Dates of Visit', bg=color)
            date_visits_label.grid(row=0, column=0, sticky=NW)
            
            #Date Visits Listbox
            username = self.username.get()
            db = self.Connect()
            cursor = db.cursor()
            cursor.execute("SELECT V.DateVisit FROM VISIT AS V LEFT JOIN PATIENT AS P ON PUsername=P.Username WHERE P.Name='{}' OR P.HomePhone='{}'".format(name.get(), home_phone.get()))
            result = cursor.fetchall()
            date_visits=()
            for date in result:
                date_visits += (date[0],)
            
            self.dateVisits = StringVar(value=date_visits)

            def UpdateViewHistory(e):
                index = date_visits_lbox.curselection()[0]
                date_selected = date_visits_lbox.get(index, index)[0]
                query = "SELECT Username FROM PATIENT WHERE Name='{}' AND HomePhone='{}'".format(self.patient_name, self.patient_home_phone)
                cursor.execute(query)
                patient_username=cursor.fetchall()[0][0]

                query = "SELECT SystolicBP, DiastolicBP FROM (VISIT AS V JOIN PATIENT AS P ON PUsername=P.Username) WHERE P.Username='{}' AND V.DateVisit='{}'".format(patient_username, date_selected)
                cursor.execute(query)
                result=cursor.fetchall()[0]
                
                date_visit.delete(0, END)
                date_visit.insert(0, date_selected)

                systolic_entry.delete(0, END)
                systolic_entry.insert(0, result[0])

                diastolic_entry.delete(0, END)
                diastolic_entry.insert(0, result[1])

                query = "SELECT Diagnosis FROM DIAGNOSIS WHERE PUsername = '{}' AND DateVisit = '{}' AND DUsername = '{}'".format(patient_username, date_selected, self.username.get())
                cursor.execute(query)
                diagnosis=cursor.fetchall()[0][0]

                diagnosis_entry.delete(1.0, END)
                diagnosis_entry.insert(END,  diagnosis)

                query = "SELECT MedName, Dosage, Duration, Notes FROM PRESCRIPTION WHERE DateVisit = '{}' AND DUsername = '{}' AND PUsername = '{}'".format(date_selected, self.username.get(), patient_username)
                cursor.execute(query)
                result = list(cursor.fetchall())

                for i in range(len(result)):
                    for j in range(len(result[i])):
                        label = Label(meds_frame, text=result[i][j], bg='white', bd=4)
                        label.grid(row=i+1, column=j, padx=1, pady=1, sticky=NSEW)

            date_visits_lbox = Listbox(visit_frame, listvariable=self.dateVisits, width=12, height=5)
            date_visits_lbox.grid(row=1, column=0, padx=3, sticky=NW)
            date_visits_lbox.bind("<Double-1>", UpdateViewHistory)

            #Vertical Separator
            separator = ttk.Separator(visit_frame, orient=VERTICAL)
            separator.grid(row=0, column=1, sticky=N+S+W, rowspan=4)

            #Visit History Frame
            attributes = ['Date of Visit: ', 'Blood Pressure: ', 'Diagnosis: ', 'Medications Prescribed: ']
            count = 0
            for attribute in attributes:
                attribute_label = Label(visit_frame, text=attribute, bg=color)
                attribute_label.grid(row=count, column=1, padx=10, pady=10, sticky=NW)
                count += 1

            date_visit = Entry(visit_frame, width=15)
            date_visit.grid(row=0, column=2, sticky=W)

            bloodFrame = Frame(visit_frame)
            bloodFrame.grid(row=1, column=2, sticky=W)

            systolic_lbl = Label(bloodFrame, text='Systolic: ', bg=color)
            systolic_lbl.grid(row=0, column=0)

            systolic_entry = Entry(bloodFrame, width=5)
            systolic_entry.grid(row=0, column=1)

            diastolic_lbl = Label(bloodFrame, text='Diastolic: ', bg=color)
            diastolic_lbl.grid(row=0, column=2, sticky=N)

            diastolic_entry = Entry(bloodFrame, width=5)
            diastolic_entry.grid(row=0, column=3)

            diagnosis_entry = Text(visit_frame, width=30, height=4)
            diagnosis_entry.grid(row=2, column=2, sticky=W)

            meds_frame = Frame(visit_frame, bg='black')
            meds_frame.grid(row=3, column=2)

            meds_col_names = ['Medicine Name', 'Dosage', 'Duration', 'Notes']

            for col in range(len(meds_col_names)):
                label = Label(meds_frame, text=meds_col_names[col], bg='white', bd=4)
                label.grid(row=0, column=col, padx=1, pady=1, sticky=NSEW)

            query = "SELECT MedName, Dosage, Duration, Notes FROM PRESCRIPTION WHERE PUsername='{}' AND DUsername='{}' AND DateVisit='{}'"

        def SearchPatient():
            col_names = ['Patient Name', 'Phone Number']

            for col in range(len(col_names)):
                label = Label(patient_frame, text=col_names[col], bg='white', bd=4)
                label.grid(row=0, column=col, padx=1, pady=1, sticky=NSEW)

                space = Label(patient_frame, text=' ', bg='white', bd=4)
                space.grid(row=0, column=3, columnspan=2, padx=1, pady=1, sticky=NSEW)
                
            db = self.Connect()
            cursor = db.cursor()
            cursor.execute("SELECT Name, HomePhone FROM PATIENT WHERE Name=%s OR HomePhone=%s", (name.get(), home_phone.get()))
            result = list(cursor.fetchall())
            self.patient_name = result[0][0]
            self.patient_home_phone = result[0][1]
            
            for i in range(len(result)):
                for j in range(len(result[i])):
                    label = Label(patient_frame, text=result[i][j], bg='white', bd=4)
                    label.grid(row=i+1, column=j, padx=1, pady=1, sticky=NSEW)

                    button_frame = Frame(patient_frame, bg='white', bd=4)
                    button_frame.grid(row=i+1, column=3, padx=1, pady=1, sticky=NSEW)

                    view = ttk.Button(button_frame, text='View History', command=ViewHistory)
                    view.grid(row=0, column=0, padx=5)

                    record = ttk.Button(button_frame, text='Record Visit', command=self.RecordVisit)
                    record.grid(row=0, column=1, padx=5)
                                
        search = ttk.Button(pvw, text='Search', command=SearchPatient)
        search.grid(row=1, column=4, padx=5, pady=5)
        
def RecordVisit(self):
     pass

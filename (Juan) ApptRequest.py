def apptRequests(self):
        self.apptRequestWin = Toplevel()
        apptRequestWin = self.apptRequestWin
        apptRequestWin.title('Appointment Requests Page')
        apptRequestWin.config(bg=color)
        
        #Top Banner
        banner = Label(apptRequestWin, bg=color, width=450, height=50, text='Doctor Homepage', padx=10,
                       font=('Berlin Sans FB', 18), image=self.photo,
                       compound=RIGHT, anchor=N)
        banner.grid(row=0, columnspan=4)

        doc_username = self.username.get()
        query = "SELECT Name,Date,ScheduledTime FROM REQUEST_APPOINTMENT LEFT JOIN PATIENT ON PUsername = Username WHERE DUsername = '{}' AND Status='Pending'".format(doc_username)
        db = self.Connect()
        cursor = db.cursor()
        cursor.execute(query)
        requests = list(cursor.fetchall())

        requestList = []
        
        for request in requests:
            requestList.append([request[0], request[1], request[2]])

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
                    patient_name = requestList[x][0]
                    doc_username = self.username.get()

                    db = self.Connect()
                    cursor = db.cursor()
                    query = 'SELECT Username FROM PATIENT WHERE Name = "{}"'.format(patient_name)
                    cursor.execute(query)
                    patient_username = cursor.fetchone()

                    query = 'SELECT FName, LName FROM DOCTOR WHERE Username = "{}"'.format(doc_username)
                    cursor.execute(query)
                    dName = cursor.fetchone()
                    doctor = 'Dr. '+dName[0] + ' ' + dName[1]

                    message = 'Appointment Accepted \n\n'+ 'Day: '+ str(requestList[x][1]) +'\n'+ 'Time: ' + requestList[x][2] + '\n' + 'Specialist: ' + doctor

                    query = 'INSERT INTO DOCTOR_TO_PATIENT (Sender,Recipient,Content,Status,DateTime) VALUES ("{}","{}","{}","Unread",CURRENT_TIMESTAMP)'.format(doc_username,patient_username[0],message)
                    cursor.execute(query)

                    query = 'UPDATE REQUEST_APPOINTMENT SET Status="Accepted" WHERE DUsername="{}" AND PUsername="{}" AND Date="{}"'.format(doc_username,patient_username[0], str(requestList[x][1]))
                    cursor.execute(query)

                    frameDict[x].destroy()

                    db.commit()                   

        def DeclineAppt( e):
            for x in range(len(declineDict)):
                if e.widget == declineDict[x]:
                    doc_username = self.username.get()
                    db = self.Connect()
                    cursor = db.cursor()
                    query = "SELECT PUsername FROM REQUEST_APPOINTMENT LEFT JOIN PATIENT ON PUsername = Username WHERE Name='{}' AND Date='{}' AND ScheduledTime='{}'"\
                            .format(requestList[x][0], requestList[x][1], requestList[x][2])
                    cursor.execute(query)
                    result = cursor.fetchall()
                    patient_username = result[0][0]

                    query = "DELETE FROM REQUEST_APPOINTMENT WHERE PUsername='{}' AND DUsername='{}' AND Date='{}' AND ScheduledTime='{}'".format(patient_username, doc_username, requestList[x][1], requestList[x][2])
                    cursor.execute(query)
                    frameDict[x].destroy()

        appt_frame = Frame(apptRequestWin, bg='black')
        appt_frame.grid(row=1, column=0, padx=10, pady=10)

        col_names = ['Name', 'Date', 'Scheduled Time']

        for i in range(len(col_names)):
            col_name = Label(appt_frame, text=col_names[i], bg='white')
            col_name.grid(row=0, column=i, padx=1, pady=1, sticky=NSEW)

        for i in range(len(requestList)):
            frameDict[i] = Frame(appt_frame, bg='black')
            frameDict[i].grid(row=i+1, column=0, columnspan=5, sticky='NSEW')
            for j in range(len(requestList[i])):
                
                label = Label(frameDict[i], text=requestList[i][j], bg='white', bd=4)
                label.grid(row=i+1, column=j, padx=1, pady=1, sticky=NSEW)

            acceptDict[i] = ttk.Button(frameDict[i], width=8, text='Accept')
            acceptDict[i].bind("<ButtonRelease-1>", AcceptAppt)
            acceptDict[i].grid(row=i+1, column=3, padx=5)
            
            declineDict[i] = ttk.Button(frameDict[i], width=8, text='Decline')
            declineDict[i].bind("<ButtonRelease-1>", DeclineAppt)
            declineDict[i].grid(row=i+1, column=4, padx=5)

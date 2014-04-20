Original Appointment Window
    #     self.apptWin = Toplevel(LogWin)
    #     self.apptWin.title('Appointments')
    #     self.apptWin.configure(background='#cfb53b')
    #
    #     topFrame = Frame(self.apptWin)
    #     topFrame.grid(row=0, column=0)
    #     topFrame.configure(background='#cfb53b')
    #     midFrame = Frame(self.apptWin, bd=1, background='black')
    #     midFrame.grid(row=1, column=0, sticky='EW')
    #     bottomFrame = Frame(self.apptWin)
    #     bottomFrame.grid(row=2, column=0)
    #     bottomFrame.configure(background='#cfb53b')
    #
    #     logo = Label(topFrame, image=self.photo)
    #     logo.grid(row=0, column=1)
    #     logo.configure(background='#cfb53b')
    #     pageName = Label(topFrame, text="Appointments", font=("Arial", 25))
    #     pageName.grid(row=0, column=0, sticky='EW')
    #     pageName.configure(background='#cfb53b')
    #
    #     self.specialtySearch = StringVar()
    #     self.specialtySearch.set('--Select a Specialty--')
    #     specialtyFrame = Frame(bottomFrame, bd=1, background='#cfb53b')
    #
    #     specialtyFrame.grid(row=0, column=0)
    #     specialtyLabel = Label(specialtyFrame, text='     Specialty: ', background='#cfb53b')
    #     specialtyLabel.grid(row=0, column=0, pady=15)
    #
    #     self.specialtyPulldown = ttk.Combobox(specialtyFrame, textvariable=self.specialty, values=self.specialties)
    #     self.specialtyPulldown.grid(row=0, column=1, padx=5, pady=15)
    #     self.specialtyPulldown.config(state='readonly')
    #
    #     searchButton = ttk.Button(specialtyFrame, text='Search', command=self.updateAppts)
    #     searchButton.grid(row=0, column=2, padx=50, pady=15)
    #
    #     self.apptFrame = Frame(bottomFrame, background='#cfb53b')
    #     self.apptFrame.grid(row=1, column=0)
    #
    #     colNames = ['     Doctor Name     ', '     Phone Number     ', '     Room Number     ', '     Availability     ',
    #                 '     Ratings     ']
    #
    #     for x in range(len(colNames)):
    #         tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
    #         tableFrame.grid(row=0, column=x, sticky='EW')
    #         label = Label(tableFrame, text=colNames[x], background='white')
    #         label.pack(fill=BOTH)


Original Update Appt Win

# self.doctorsInfo = {
#             'A': ['Phone', 'Room', ['Available4'], '******'],
#             'B': ['Phone', 'Room', ['Available1',  'Available3', 'Available4'], '***'],
#             'C': ['Phone', 'Room', ['Available3', 'Available4'], '****'],
#             'D': ['Phone', 'Room', ['Available1', 'Available2', 'Available3', 'Available4'], '**'],
#             'E': ['Phone', 'Room', ['Available1', 'Available2', 'Available3', 'Available4'], '**'],
#             'F': ['Phone', 'Room', ['Available1', 'Available2',  'Available4'], '**']
#         }
#
#         doctorsList = []
#         for doctor in self.doctorsInfo.keys():
#             doctorsList.append(doctor)
#
#         rows = 1
#         for x in self.doctorsInfo.keys():
#             for y in range(len(self.doctorsInfo[x])):
#                 if rows <= (len(doctorsList)*len(self.doctorsInfo[x][2])):
#                     tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
#                     tableFrame.grid(row=rows, column=0, sticky='EW')
#                     label = Label(tableFrame, text=x, background='white')
#                     label.pack(fill=BOTH)
#                 if isinstance(self.doctorsInfo[x][y], list):
#                     zrow = rows
#                     for z in range(len(self.doctorsInfo[x][y])):
#                         tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
#                         tableFrame.grid(row=zrow, column=y+1, sticky='EW')
#                         label = Label(tableFrame, text=self.doctorsInfo[x][y][z], background='white')
#                         label.pack(fill=BOTH)
#                         zrow += 1
#                         if zrow <= (len(doctorsList)*len(self.doctorsInfo[x][2])):
#                             for a in range(len(self.doctorsInfo[x])+1):
#                                 tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
#                                 tableFrame.grid(row=zrow, column=a, sticky='EW')
#                                 label = Label(tableFrame, text='  ', background='white')
#                                 label.pack(fill=BOTH)
#
#                     y += 1
#
#                 if rows <= (len(doctorsList)*len(self.doctorsInfo[x][2])):
#                     tableFrame = Frame(self.apptFrame, borderwidth=1, background='black')
#                     tableFrame.grid(row=rows, column=y+1, sticky='EW')
#                     label = Label(tableFrame, text=self.doctorsInfo[x][y], background='white')
#                     label.pack(fill=BOTH)
#
#                 try:
#                     rows = zrow
#                 except:
#                     pass
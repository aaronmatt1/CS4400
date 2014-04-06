##GTMS UI

import base64

class GTMS:
    def __init__(self, win):

        LoginPage()

    def loginPage(self):

        topFrame = Frame(LogWin)
        topFrame.grid(row=0, colum=0)
        topFrame.configure(background='#c1a82f')
        bottomFrame = Fram(LogWin)
        bottomFrame.grid(row=1, column=0)

        Label(text="Georgia Tech Medical Center System", font=('Arial', 20)).pack



LogWin = Tk()
LogWin.title('GTMS Login')
obj = GTMS(LogWin)
LogWin.mainloop()


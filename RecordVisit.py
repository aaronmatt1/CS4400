__author__ = 'jsuit'


class RecordVisit(object):

        #incomeCutoff is the cutoff to receive a discount
        #initialFee is the initial Fee for a doctor
        #discount is the amount of discount that poor people receive
        #e_cost is the cost if you are not poor.
        def recordNewVisit(self, pusername, dusername, date, bpsystolic, sysbp, db, incomeCutoff, initialFee, discount, e_cost):
                date = date.replace("/", "-")
                q = """SELECT COUNT(*) FROM VISIT WHERE
                DUsername = %s AND PUsername = %s AND DateVisit = %s""" % dusername, pusername,date
                c = db.cursor()
                if c.execute(q) != 0:
                        return "ERROR"
                else:
                        q = "SELECT AnnualIncome FROM PATIENT WHERE Username=%s" % pusername
                        income = c.execute(q)
                        discountReceived = False
                        if income < incomeCutoff:
                                discountReceived = True
                        #first time visiting doctor?
                        q = "SELECT COUNT(*) FROM VISIT WHERE DUsername = $username AND PUsername = $p_username"
                        firstTime = 0
                        if c.execute(q) == 0:
                              #first time visiting doctor
                              firstTime  = 1

                        b_amt = float(e_cost)
                        if discountReceived:
                                cost = discount* b_amt
                        else:
                                cost = b_amt
                        amountOwed = firstTime * initialFee+ cost

                        q = """INSERT INTO VISIT (DateVisit, DUsername, PUsername,BillingAmt, DiastolicBP, SystolicBP,
                        VALUES (%s, %s, %s, %f, %s, %s)""" %date,dusername,pusername,amountOwed,bpsystolic,sysbp
                        c.execute(q)
                        c.close()

        def setDiagnosis(self, diagnosis, pusername, dusername, date, db):
                c = db.cursor()
                q = """SELECT COUNT(*) FROM DIAGNOSIS WHERE PUsername = %s AND DUsername = %s AND DateVisit =%s
                        AND DIAGNOSIS = %s""" % pusername, dusername,date, diagnosis
                num = c.execute(q)
                if num == 0:
                        q = """ INSERT INTO DIAGNOSIS (PUsername, DateVisit, DUsername, Diagnosis)
                        VALUES (%s, %s,%s,%s)""" % pusername,date, dusername,diagnosis
                else:
                        q = """UPDATE DIAGNOSIS set Diagnosis = %s WHERE PUsername = %s AND DUsername = %s
                                AND DateVisit = %s""" % diagnosis, pusername,dusername,date
                c.execute(q)
                c.close()

        #todo prescribeMeds
        def prescribeMeds(self, drugname, dosage, duration, notes, db):
                c = db.cursor()
                """ dp stuff"""

                c.close()




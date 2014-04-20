__author__ = 'jsuit'

import VisitHistory

class VisitHistoryPatient(VisitHistory):

        def isinDatabase(self, username,db):
              pass

        """ Returns  SELECT MedName, Dosage, Duration, Notes FROM PRESCRIPTION
	            WHERE DateVisit = %s AND DUsername = %s AND PUsername =
                %s % date, dusername, pusername"""
        def getMeds(self, pusername, dusername, date, db):
                c = db.cursor()
                q = """SELECT MedName, Dosage, Duration, Notes FROM PRESCRIPTION
	            WHERE DateVisit = %s AND DUsername = %s AND PUsername =
                %s""" % date, dusername, pusername
                return c.execute(q)

        """RETURNS q = SELECT Diagnosis FROM DIAGNOSIS WHERE PUsername = %s AND DateVisit = %s
                AND DUsername = %s % pusername, date, dusername"""
        def getDiagnosis(self, pusername, dusername, date,db):
                q = """SELECT Diagnosis FROM DIAGNOSIS WHERE PUsername = %s AND DateVisit = %s
                AND DUsername = %s""" % pusername, date, dusername
                c = db.cursor()
                return c.execute(q)
        """SELECT DiastolicBP, SystolicBP FROM VISIT WHERE DUsername = %s AND PUsername =%s Date = %s"""
        def getBP(self,db, dusername, pusername, date):
                c = db.cursor()
                q = """SELECT DiastolicBP, SystolicBP FROM VISIT WHERE DUsername = %s AND PUsername =%s Date = %s""" %\
                    dusername, pusername,date
                return c.execute(q)

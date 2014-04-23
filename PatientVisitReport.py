__author__ = 'jsuit'


class PatientVisitReport(object):
        #use these two functions to calcuate total billing
        def getPoorPatientsReport(self,db, poorCutoff):
               q = """SELECT PS.PUsername,t1.Type, t1.CPT t2.TotalBilling
                        FROM PERFORMS SURGERY AS PS
                        INNER JOIN
                        (SELECT AnnualIncome FROM PATIENT WHERE AnnualIncome <=
                        %f)
                        INNER JOIN
                        (SELECT SUM(t1.Cost*.5) as “TotalBilling”, PUsername
                        FROM PERFORMS_SURGERY AS PS
		                INNER JOIN
		                        (SELECT Cost, Type From SURGERY) t1
		                        ON t1.CPT = PS.CPT
                        GROUP BY t1.Type) t2
	                    ON PS.PUsername = t2.PUsername;
                """%poorCutoff
               c = db.cursor()
               data = c.execute(q)
               c.close()
               return data

        def getNonPoorPatientsReport(self, db, poorCutoff):
                q = """SELECT PS.PUsername,t1.Type, t1.CPT t2.TotalBilling2 FROM PERFORMS SURGERY
                        AS PS
	                    INNER JOIN
                                (SELECT AnnualIncome FROM PATIENT WHERE AnnualIncome >
                                %f)
                        INNER JOIN
                        (SELECT SUM(t1.Cost) as “TotalBilling2”, PUsername
                        FROM PERFORMS_SURGERY AS PS
		                INNER JOIN
		                        (SELECT Cost From SURGERY) t1
		                ON t1.CPT = PS.CPT
                        GROUP BY t1.Type) t2
	                    ON PS.PUsername = t2.PUsername""" % poorCutoff
                c = db.cursor()
                data = c.execute(q)
                c.close()
                return data
        def getNoProcedures(self,db):
                #This counts number of distinct doctors doing a procedure
                q = """SELECT COUNT(DUsernames) IN PERFORMS_SURGERY AS PS
	            INNER JOIN
	            (SURGERY
	            GROUP BY Type)
	            ON SURGERY.CPT = PS.CPT
	            GROUP BY PS.DUsernames"""
                c = db.cursor()
                data = c.execute(q)
                c.close()
                return data

        def getNumPatientsByDoctor(self, db, month, year):
                q= """SELECT (FName + LName) as Name, t3.Visits, t2.Prescriptions
FROM DOCTOR as D
			INNER JOIN(
				SELECT DUsername, COUNT(DateVisit) AS Prescriptions
				FROM PRESCRIPTION
				WHERE MONTH(DateVisit) = $month
				AND YEAR(DateVisit)=$year
				GROUP BY PRESCRIPTION.DUsername
			)t2 ON D.username = t2.DUsername
			INNER JOIN(
				SELECT COUNT(DATEVISIT), DUsername
				FROM VISIT as V
				WHERE MONTH(DateVisit) = %s
				AND YEAR(DateVisit)=%s
				GROUP BY DUSername
			) t2 ON t2.DUsername=D.Username""" % month, year
                c = db.cursor()
                d = c.execute(q)
                c.close()
                return d;

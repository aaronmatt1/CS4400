__author__ = 'jsuit'


class AdminDoctorPerformance(object):

        def isAdmin(self,db, username):
                c = db.cursor()
                q = """SELECT COUNT(*) FROM ADMINISTRATIVE_PERSONNEL WHERE Username = %s""" % username
                num = c.execute(q)
                found  = False
                if num == 1:
                        found = True
                c.close()
                return found;

        def getDoctorPerformance(self, username, db):
                c = db.cursor()
                q = """SELECT D.specialty,AVG(t1.Rates) as Rating, Count(t0.CPT) as "Number of Surgeries Performed" FROM DOCTOR as D
	                    INNER JOIN(
		                        SELECT CPT, specialty
		                        FROM PERFORM_SURGERY AS P
		                        )t0 ON t0.DUsername=D.Username
	                            INNER JOIN(
		                        SELECT Rates
		                        FROM RATES
	                            ) t1 ON D.Username=t1.DUsername
	                            GROUP BY D.specialty"""
                return c.execute(q)
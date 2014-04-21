__author__ = 'jsuit'

import VisitHistory
class VisitHistoryDoc(VisitHistory):

       def isInDatabase(self,username,db):
               c = db.cursor()
               query = """SELECT COUNT(*) FROM DOCTOR WHERE Username = %s """ % username
               if c.execute(query) == 1:
                       return True
               else: return False
        
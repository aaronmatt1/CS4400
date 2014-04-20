__author__ = 'jsuit'

import VisitHistory
class VisitHistoryPatient(VisitHistory):
    """ return true or false ... i think
    """
    def isInDatabase(self,username,db):
        c= db.cursor()
        q = "SELECT * FROM PATIENT WHERE PUsername = %s" %username
        num = c.execute(q)
        if num ==1:
                return True
        else: return False

    """Everything else is in parent class"""


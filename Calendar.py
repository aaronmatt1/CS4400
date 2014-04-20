__author__ = 'jsuit'

import pymysql

class ViewAppts(object):

    def isADoct(self, userName,db):
        cursor = db.cursor()
        num = cursor.execute("Count * FROM Doctors WHERE Username = %s " % userName)
        if num == 1:
            return True
        else: return False

    """View appts method
    username is doctor's username
    day,month, year is the date
    db is the database"""

    def ViewAppts(self, username, day, month, year,db ):
        c = db.cursor()
        if  month is not None or year is not None and day is None:
            query = """SELECT COUNT(PUsername) FROM REQUEST_APPOINTMENT RA WHERE DUsername = %s GROUP BY RA.Year, RA.month
            , RA.day""" % username
            dates = c.execute(query)
            return dates
        elif month is None or year is None and day is not None:
            print("Not enough info given")
            return None
        else:
            query = """SELECT P.Name, V.ScheduledTime FROM REQUEST_APPOINTMENT AS RA
                    JOIN
                    PATIENT AS P
                    ON RA.PUsername = P.Username
                    WHERE RA.Day = %s AND RA.Month = %s AND RA.year = %s
                    ORDER BY V.ScheduledTime""" % day, month, year
            Name, scheduleTime = c.execute(query)
            if (Name is None or scheduleTime is None):
                return (None, None)
            return Name,scheduleTime



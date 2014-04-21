__author__ = 'jsuit'

class SearchPatients(object):

        """ View all patients with name and phone"""
        """ should return a username, name and phone"""
        """ testing is required"""

        def search(self, name, phone, dusername,db):
                c = db.cursor()
                if name is not None and name != '' and phone!= '' and phone is not None:
                        q = """SELECT Username as p_username, Name, HomePhone FROM PATIENT AS P
                                INNER JOIN
                                VISIT AS V
                                ON P.Username = V.PUsername
                                WHERE Name = %s AND WorkPhone = %s AND V.DUsername = %s"""  %name, phone,dusername


                elif name is not None and name != '' and (phone == '' or phone is None):
                       q= """SELECT Username as p_username, Name, HomePhone FROM PATIENT AS P
                                INNER JOIN
                                VISIT AS V
                                ON P.Username = V.PUsername
                                WHERE Name = %s AND V.DUsername = %s"""  %name, phone,dusername
                elif not(phone == '' or phone is None):
                       q= """SELECT Username as p_username, Name, HomePhone FROM PATIENT AS P
                                INNER JOIN
                                VISIT AS V
                                ON P.Username = V.PUsername
                                WHERE WorkPhone = %s AND V.DUsername = %s"""  %phone,dusername
                if q is not None:
                        data = c.execute(q)
                        c.close()
                        return data
                else:
                        return None

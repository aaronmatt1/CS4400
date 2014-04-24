
import pymysql

def connect():

    db = pymysql.connect(host="academic-mysql.cc.gatech.edu", #connecting to the database
                        passwd='KDKR2YQY', user='cs4400_Group_65',
                        db='cs4400_Group_65')
    c = db.cursor()
    return c

fromTimes = ['8:00am', '8:30am', '9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am', '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm', '3:00pm', '3:30pm', '4:00pm', '4:30pm', '5:00pm', '5:30pm']

toTimes = ['8:30am', '9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am', '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm','3:00pm','3:30pm', '4:00pm', '4:30pm', '5:00pm', '5:30pm', '6:00pm']

cursor = connect()
cursor.execute('SELECT Username FROM DOCTOR')
doctorList = list(cursor.fetchall())
docs =[]
for doctor in doctorList:
	docs.append(doctor[0])

dateList = ['2014-04-01','2014-04-02','2014-04-03','2014-04-04','2014-04-05']

for doctor in docs:
	for date in dateList:
		for x in range(len(fromTimes)):
			query = 'INSERT INTO AVAILABILITY (Username,Day_Date,From_Time,To_Time) VALUES ("{}","{}","{}","{}")'.format(doctor,date,fromTimes[x],toTimes[x])
			cursor.execute(query)
			if x%3 == 0:
				try:
					query = 'INSERT INTO AVAILABILITY (Username,Day_Date,From_Time,To_Time) VALUES ("{}","{}","{}","{}")'.format(doctor,date,fromTimes[x],toTimes[x+2])
					x+=3
					cursor.execute(query)
				except:
					pass

db.commit()
db.close()


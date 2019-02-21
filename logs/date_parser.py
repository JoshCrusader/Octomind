from datetime import datetime  
from datetime import timedelta  
import MySQLdb
#Add 1 day  
#print datetime.now() + timedelta(days=1)  
  
#Subtract 60 seconds  
#print datetime.now() - timedelta(seconds=60)  
  
#Add 2 years  
#print datetime.now() + timedelta(days=730)  
  
#Other Parameters you can pass in to timedelta:  
# days, seconds, microseconds,   
# milliseconds, minutes, hours, weeks    
#Pass multiple parameters (1 day and 5 minutes)

with open('cleaned_logs.txt', 'r') as f:       
    for line in f:
        log = line.split(',')
       
        conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="sensorDB")
        x = conn.cursor()
        try:
            x.execute("INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);",
                     (log[0],str(datetime.strptime(log[1], '%Y-%m-%d %H:%M:%S')), str(log[2])))
            conn.commit()
        except Exception as e:
            print (e)
            print("wats")
            conn.rollback()
        conn.close()
        pass
        


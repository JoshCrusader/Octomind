from datetime import datetime  
from datetime import timedelta  
  
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

with open('octomind-2-14.txt', 'r') as f:
    with open('octomind_log_new_2_14.txt', 'w') as log_file:        
        for line in f:
            log = line.split(',')
            data = str(log[0])+','+str(datetime.strptime(log[1], '%Y-%m-%d %H:%M:%S') + timedelta(days=0, hours=16,minutes=0))+','+str(log[2])
            log_file.write(data)
            print(data)
        
        


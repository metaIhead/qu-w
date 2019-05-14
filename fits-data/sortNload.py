import urllib.request
from datetime import datetime
import time
import os

data=open('name_fit.txt', 'r')
path=str(os.getcwd())
scroll=len(os.listdir(path=path))-2

date = datetime.now()
time_b=time.monotonic()
print("-----start-----: ",date)

for line in data:
    filename=line[0:-1]
    ext=filename[-3:]
    try:
        scroll=len(os.listdir(path=path))-2
        if (ext=="fit"):
            print(filename,"loaded", scroll)
            url='http://10.2.1.16/SRH/'+filename
            urllib.request.urlretrieve(url,filename)
    except:
        continue


time_e = time.monotonic()
date = datetime.now()
print("-----done-----: ",date)
print("time:  ",time_e-time_b)

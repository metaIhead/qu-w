from time import sleep
import urllib
from ftplib import FTP, error_perm

ftp = FTP("ssw.iszf.irk.ru", "anonymous", "anonymous")

ftp.cwd("RAO/srh48/2017/")
months=ftp.nlst()

#filemane='mf_20170101_020541.fit'



for month in months:
    ftp.cwd(month)
    days=ftp.nlst()
    for day in days:
        print("month: "+month+" -- "+"day: "+day)
        ftp.cwd(day)
        fits=ftp.nlst()
        print(ftp.pwd())
        for fit in fits:
            path=ftp.pwd()
            #print(path)

            ftp.cwd(path)
            ftp.retrbinary("RETR " + fit, open(fit, 'wb').write)

            # handle = open(path.rstrip("/") + "/" + fit.lstrip("/"), 'wb')
            # ftp.retrbinary('RETR %s' % fit, handle.write)
            #path="/home/ivan/"
            print("loaded",fit)
            ftp.cwd("..")
            sleep(5)

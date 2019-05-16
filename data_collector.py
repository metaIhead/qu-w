from time import sleep
from ftplib import FTP, error_perm

ftp = FTP("ssw.iszf.irk.ru", "anonymous", "anonymous")

ftp.cwd("RAO/srh48/2017/")
months=ftp.nlst()

for month in months:
    ftp.cwd(month)
    days=ftp.nlst()
    for day in days:
        print("month: "+month+" -- "+"day: "+day)
        ftp.cwd(day)
        fits=ftp.nlst()
        print(ftp.pwd())
        for fit in fits:
            path=str('ftp://ssw.iszf.irk.ru/RAO/srh48/2017/01/01/mf_20170101_020541.fit')
            #print(path)


            # handle = open(path.rstrip("/") + "/" + fit.lstrip("/"), 'wb')
            # ftp.retrbinary('RETR %s' % fit, handle.write)
            #path="/home/ivan/"
            ftp.retrbinary("STOR " + fit ,open(path, 'rb').write)

            print("loaded")
            ftp.cwd("..")
            sleep(5)



    # for day in list(range(1.2)):
    #     pass

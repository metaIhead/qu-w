from ftplib import FTP, error_perm

def walk(cd='/'):
    ftp.cwd(cd)
    print(cd)
    print(ftp.retrlines('LIST'))
    for i in ftp.nlst():
        try:
            walk(cd + i + '/')
        except error_perm:
            print(i)

ftp = FTP('mirror.yandex.ru')
ftp.login()
walk()
ftp.quit()

import pymysql.cursors
import urllib.request
from datetime import datetime


# Подключиться к базе данных.
connection = pymysql.connect(host='10.1.1.69',
                             user='kolomin',
                             password='kmsOvx74Q',
                             db='datacollector')

previous_name="none"

with connection.cursor() as cursor:
    while True:
        now = datetime.now()
        # SQL
        sql = "SELECT MAX(id), filename FROM files;"
        #sql = "SELECT id FROM files;  "
        #sql = "DESCRIBE files; "

        # Выполнить команду запроса (Execute Query).
        cursor.execute(sql)

        for row in cursor:
            name=row[1]


        if (previous_name==name):
            pass
        else:
            url='http://10.2.1.16/SRH/'+name
            urllib.request.urlretrieve(url,name)
            previous_name=name
            print(name,"   ",now)




# while True:
#     now = datetime.now()
#     try:
#         with connection.cursor() as cursor:
#
#             # SQL
#             sql = "SELECT MAX(id), filename FROM files;"
#             #sql = "SELECT id FROM files;  "
#             #sql = "DESCRIBE files; "
#
#             # Выполнить команду запроса (Execute Query).
#             cursor.execute(sql)
#
#             #print (cursor[1])
#
#             # for row in cursor:
#             #     print(row)
#
#     except:
#         # Закрыть соединение (Close connection).
#         #connection.close()
#         print("except")

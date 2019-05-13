import pymysql.cursors
import urllib.request
from datetime import datetime
import time


# Подключиться к базе данных.
connection = pymysql.connect(host='10.1.1.69',
                             user='kolomin',
                             password='kmsOvx74Q',
                             db='datacollector')

print("open file")
f = open('name_fit.txt', 'a')
with connection.cursor() as cursor:
    date = datetime.now()
    time_b=time.monotonic()
    print("-----start-----: ",date)

    # SQL
    #sql = "SELECT MAX(id), filename FROM files;"
    sql = "SELECT filename FROM files;"
    #sql = "DESCRIBE files; " #колонки в таблице

    # Выполнить команду запроса (Execute Query).
    print("sending SQL")
    cursor.execute(sql)

    print("writing data to file")
    for row in cursor:
        f.write(row[0] + '\n')

    time_e = time.monotonic()
    date = datetime.now()
    print("-----done-----: ",date)
    print("time:  ",time_e-time_b)


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

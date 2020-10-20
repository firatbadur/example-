from db import select_rows
from datetime import *


modbus_1 = (0, 0, time_iso, 0, 1,0, time_iso, 0, 2,0, time_iso, 0, 4, 0, time_iso, 0, 6, 0, time_iso, 0, 7, 0, time_iso, 0, None, None,None, None, None, None, None, None)
analog_1 = (0, 71.53, -64.59, 17.45, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 1, 31,
                                                                                          tzinfo=psycopg2.tz.FixedOffsetTimezone(
                                                                                              offset=180, name=None)),
                    1)

"""

İstek atılan zaman aralığını son-zaman<ilk-zaman olacak şekilde dögüye sokulacak. 


"""
import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Firat1212b."
DB_HOST = "localhost"
DB_PORT = "5432"
connect = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
cursor = connect.cursor()
zaman_2 = datetime.strptime('2020-05-16T21:13:00','%Y-%m-%dT%H:%M:%S')
zaman_3 = datetime.strptime('2020-05-16T21:22:00','%Y-%m-%dT%H:%M:%S')

k = 0


while(zaman_2<=zaman_3):


    sorgu_1 = """SELECT * FROM reads_ao WHERE time_iso BETWEEN %s AND %s"""
    cursor.execute(sorgu_1, (zaman_2, zaman_2+ timedelta(minutes=1)))
    value_modbus = cursor.fetchone()
    print(value_modbus)
    zaman_2 = zaman_2 + timedelta(minutes=1)














"""


"EN SON MODBUS IN GERÇEK LİSTESİNİ DÖNGÜYE SOKACAKTIM. ANALOGLARI HALLETTİM."

all_list = []
i = 0
while(i<len(modbus_1)):

    a = {"channelId": modbus_1[i],"value": modbus_1[i+1],"status": modbus_1[i+3]}
    all_list.append(a)
    i+=4


j = 0
while(j<len(analog_1)):
    debi = {"channelId": 3, "value": analog_1[j][1], "status": analog_1[10]}

    kab_sicaklik = {"channelId": 8, "value": analog_1[j][2], "status": analog_1[10]}

    kab_nem = {"channelId": 9, "value": analog_1[j][3], "status": analog_1[10]}

    akis = {"channelId": 5, "value": analog_1[j][4], "status": analog_1[10]}

    all_list.append(debi)
    all_list.append(kab_sicaklik)
    all_list.append(kab_nem)
    all_list.append(akis)

    j+=1
"""
















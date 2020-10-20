import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Firat1212b."
DB_HOST = "localhost"
DB_PORT = "5432"
connect = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
cursor = connect.cursor()

def station_info():
    sorgu = "SELECT * FROM station_info"

    cursor.execute(sorgu)
    station_info = cursor.fetchone()
    connect.commit()
    return station_info

def device_modbus():
    sorgu = "SELECT * FROM device_info"

    cursor.execute(sorgu)
    device_info = cursor.fetchall()
    connect.commit()
    return device_info

def device_ascii():
    sorgu = "SELECT * FROM device_ascii"

    cursor.execute(sorgu)
    device_ascii = cursor.fetchall()
    connect.commit()
    return device_ascii

def writes_dio(return_list):

    sorgu = """INSERT INTO reads_dio (id,di_0,di_1,di_2,di_3,di_4,di_5,di_6,di_7,
    do_0,do_1,do_2,do_3,do_4,do_5,do_6,do_7,time_iso,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    ,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sorgu, (return_list[0],return_list[1][0],return_list[1][1],return_list[1][2],return_list[1][3],return_list[1][4],
                           return_list[1][5],return_list[1][6],return_list[1][7],return_list[2][0],return_list[2][1],
                           return_list[2][2],return_list[2][3],return_list[2][4],return_list[2][5],return_list[2][6],
                           return_list[2][7],return_list[3],return_list[4]))
    connect.commit()

def writes_ao(return_list):
    #[[0, [66.69, -65.23, 10.6, -0.4, 0.0, 0.0, 0.0, 0.0], '2020-09-08T01:06:02', 1, 'Analog']]
    cursor = connect.cursor()
    sorgu = """INSERT INTO reads_ao (id,ao_0,ao_1,ao_2,ao_3,
    ao_4,ao_5,ao_6,ao_7,time_iso,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sorgu, (return_list[0][0],return_list[0][1][0],return_list[0][1][1],return_list[0][1][2],return_list[0][1][3],return_list[0][1][4],
                           return_list[0][1][5],return_list[0][1][6],return_list[0][1][7],return_list[0][2],return_list[0][3]))

    connect.commit()
    """[2, [8.008, 5.763, 4.892, 13.915, 9.004, 4.505, 2.312, 1.203], '2020-08-30T19:42:50', 1]"""
def writes_modbus(return_list):

    #a = [[0, 5.934, 1, '2020-08-27T21:54:32'], [2, 4.445, 1, '2020-08-27T21:54:32'], [1, 1503.568, 1, '2020-08-27T21:54:32'], [7, 14.725, 1, '2020-08-27T21:54:32']]
    # [[0, 5.866, 1, '2020-08-30T22:22:50'], [2, 4.938, 1, '2020-08-30T22:22:50'], [1, 1410.732, 1, '2020-08-30T22:22:50'], [7, 0, 8, '2020-08-30T22:22:50'], [7, 0, 8, '2020-08-30T22:22:50'], [7, 22.408, 1, '2020-08-30T22:22:50']]
    if(len(return_list) == 1):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1) VALUES (%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2]))
        connect.commit()

    elif(len(return_list) == 2):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2],
                               return_list[1][0], return_list[1][1], return_list[1][3], return_list[1][2]))
        connect.commit()

    elif(len(return_list)==3):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
            id_3,value_3,time_iso_3,status_3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2],
                               return_list[1][0], return_list[1][1], return_list[1][3], return_list[1][2],
                               return_list[2][0], return_list[2][1], return_list[2][3], return_list[2][2]))
        connect.commit()
    elif(len(return_list)==4):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
    id_3,value_3,time_iso_3,status_3,id_4,value_4,time_iso_4,status_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    ,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0],return_list[0][1],return_list[0][3],return_list[0][2],
                               return_list[1][0],return_list[1][1],return_list[1][3],return_list[1][2],
                               return_list[2][0],return_list[2][1],return_list[2][3],return_list[2][2],
                               return_list[3][0],return_list[3][1],return_list[3][3],return_list[3][2]))
        connect.commit()
    elif(len(return_list)==5):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
            id_3,value_3,time_iso_3,status_3,id_4,value_4,time_iso_4,status_4,id_5,value_5,time_iso_5,status_5) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            ,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2],
                               return_list[1][0], return_list[1][1], return_list[1][3], return_list[1][2],
                               return_list[2][0], return_list[2][1], return_list[2][3], return_list[2][2],
                               return_list[3][0], return_list[3][1], return_list[3][3], return_list[3][2],
                               return_list[4][0], return_list[4][1], return_list[4][3], return_list[4][2]))
        connect.commit()
    elif (len(return_list) == 6):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
                    id_3,value_3,time_iso_3,status_3,id_4,value_4,time_iso_4,status_4,id_5,value_5,time_iso_5,status_5,id_6,value_6,time_iso_6,status_6) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                    ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2],
                               return_list[1][0], return_list[1][1], return_list[1][3], return_list[1][2],
                               return_list[2][0], return_list[2][1], return_list[2][3], return_list[2][2],
                               return_list[3][0], return_list[3][1], return_list[3][3], return_list[3][2],
                               return_list[4][0], return_list[4][1], return_list[4][3], return_list[4][2],
                               return_list[5][0], return_list[5][1], return_list[5][3], return_list[5][2]))
        connect.commit()
    elif (len(return_list) == 7):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
                            id_3,value_3,time_iso_3,status_3,id_4,value_4,time_iso_4,status_4,id_5,value_5,time_iso_5,status_5
                            ,id_6,value_6,time_iso_6,status_6,id_7,value_7,time_iso_7,status_7) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                            ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2],
                               return_list[1][0], return_list[1][1], return_list[1][3], return_list[1][2],
                               return_list[2][0], return_list[2][1], return_list[2][3], return_list[2][2],
                               return_list[3][0], return_list[3][1], return_list[3][3], return_list[3][2],
                               return_list[4][0], return_list[4][1], return_list[4][3], return_list[4][2],
                               return_list[5][0], return_list[5][1], return_list[5][3], return_list[5][2],
                               return_list[6][0], return_list[6][1], return_list[6][3], return_list[6][2]))
        connect.commit()
    elif (len(return_list) == 8):
        sorgu = """INSERT INTO reads_modbus (id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
                                    id_3,value_3,time_iso_3,status_3,id_4,value_4,time_iso_4,status_4,id_5,value_5,time_iso_5,status_5
                                    ,id_6,value_6,time_iso_6,status_6,id_7,value_7,time_iso_7,status_7,id_8,value_8,time_iso_8,status_8) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                                    ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(sorgu, (return_list[0][0], return_list[0][1], return_list[0][3], return_list[0][2],
                               return_list[1][0], return_list[1][1], return_list[1][3], return_list[1][2],
                               return_list[2][0], return_list[2][1], return_list[2][3], return_list[2][2],
                               return_list[3][0], return_list[3][1], return_list[3][3], return_list[3][2],
                               return_list[4][0], return_list[4][1], return_list[4][3], return_list[4][2],
                               return_list[5][0], return_list[5][1], return_list[5][3], return_list[5][2],
                               return_list[6][0], return_list[6][1], return_list[6][3], return_list[6][2],
                               return_list[7][0], return_list[7][1], return_list[7][3], return_list[7][2]))
        connect.commit()

    else:
        error = open("C:/Logs/device_alert.txt", "a")
        error.write("Modbus parametre okuma hatası.\n")
        error.close()

def update_rows(row_list):
    try:
        sorgu = """UPDATE channel_rows SET debi = %s, kab_sicaklik=%s , kab_nem = %s, akis_hizi = %s, empty_ch1 = %s,empty_ch2 = %s,
                    empty_ch3 = %s,empty_ch4 = %s WHERE id=0"""
        cursor.execute(sorgu, (
        row_list[0], row_list[1], row_list[2], row_list[3], row_list[4], row_list[5], row_list[6], row_list[7]))

        connect.commit()
    except:pass

def select_rows():
    sorgu = "SELECT * FROM channel_rows"
    cursor.execute(sorgu)
    channel_rows = cursor.fetchone()
    connect.commit()

    #Örnek return (0, 1, 2, 3, 4, 5, 6, 7, 0)
    return channel_rows

def select_data(time_first,time_last,type):

    if(type == "Modbus"):

        try:
            sorgu_1 = """SELECT * FROM reads_modbus WHERE time_iso_1 BETWEEN %s AND %s"""
            cursor.execute(sorgu_1, (time_first, time_last))
            value_modbus = cursor.fetchone()
            connect.commit()
            return value_modbus

        except:
            "KOİ Cihazı ayrı olduğu için analizörlerdn herhangi biri arızalı olduğunda koi bilgisi yollamak için bu parametre var."
            sorgu_1 = """SELECT * FROM reads_modbus WHERE time_iso_5 BETWEEN %s AND %s"""
            cursor.execute(sorgu_1, (time_first, time_last))
            value_modbus = cursor.fetchone()
            connect.commit()
            return value_modbus
        finally:connect.commit()


    elif(type == "Ascii-A"):
        sorgu_2 = """SELECT * FROM reads_ao WHERE time_iso BETWEEN %s AND %s"""
        cursor.execute(sorgu_2, (time_first, time_last))
        value_ao = cursor.fetchone()
        connect.commit()
        return value_ao

    elif(type == 'Ascii-D'):
        sorgu_2 = """SELECT * FROM reads_dio WHERE time_iso BETWEEN %s AND %s"""
        cursor.execute(sorgu_2, (time_first, time_last))
        value_dio = cursor.fetchone()
        connect.commit()
        print(value_dio)
        return value_dio


def select_last_data(type):
    if (type == "Modbus"):
        sorgu = """SELECT id_1,value_1,time_iso_1,status_1,id_2,value_2,time_iso_2,status_2,
                                    id_3,value_3,time_iso_3,status_3,id_4,value_4,time_iso_4,status_4,id_5,value_5,time_iso_5,status_5
                                    ,id_6,value_6,time_iso_6,status_6,id_7,value_7,time_iso_7,status_7,id_8,value_8,time_iso_8,status_8
                                     FROM reads_modbus WHERE status_1 IN(1) ORDER BY time_iso_1 DESC LIMIT 1"""
        cursor.execute(sorgu)
        last_data = cursor.fetchone()
        return last_data

    elif (type == "Ascii-A"):
        sorgu = """SELECT id,ao_0,ao_1,ao_2,ao_3,ao_4,ao_5,ao_6,ao_7,time_iso,status
                                     FROM reads_ao WHERE status IN(1) ORDER BY time_iso DESC LIMIT 1"""
        cursor.execute(sorgu)
        last_data = cursor.fetchone()
        return last_data
    else:
        pass  # ASCİİ DİJİTAL VERİLER BURADA DÖNDÜRÜLECEK



"""
a = [(0, 9.274, datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2284.07, datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 1.316, datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 8.603, datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.274, datetime.datetime(2020, 9, 8, 21, 2, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2278.16, datetime.datetime(2020, 9, 8, 21, 2, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.446, datetime.datetime(2020, 9, 8, 21, 2, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 2, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 2, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 2, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.27, datetime.datetime(2020, 9, 8, 21, 3, 37, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2274.03, datetime.datetime(2020, 9, 8, 21, 3, 37, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.516, datetime.datetime(2020, 9, 8, 21, 3, 37, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 3, 37, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 3, 37, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 3, 37, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.271, datetime.datetime(2020, 9, 8, 21, 4, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2285.99, datetime.datetime(2020, 9, 8, 21, 4, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.532, datetime.datetime(2020, 9, 8, 21, 4, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 4, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 4, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 7.323, datetime.datetime(2020, 9, 8, 21, 4, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.273, datetime.datetime(2020, 9, 8, 21, 5, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2270.06, datetime.datetime(2020, 9, 8, 21, 5, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.443, datetime.datetime(2020, 9, 8, 21, 5, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 5, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 5, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 8.603, datetime.datetime(2020, 9, 8, 21, 5, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.268, datetime.datetime(2020, 9, 8, 21, 6, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2287.75, datetime.datetime(2020, 9, 8, 21, 6, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.62, datetime.datetime(2020, 9, 8, 21, 6, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 6, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 6, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 8.603, datetime.datetime(2020, 9, 8, 21, 6, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.268, datetime.datetime(2020, 9, 8, 21, 7, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2301.31, datetime.datetime(2020, 9, 8, 21, 7, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.463, datetime.datetime(2020, 9, 8, 21, 7, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 7, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 7, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 7, 22, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.268, datetime.datetime(2020, 9, 8, 21, 8, 12, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2306.83, datetime.datetime(2020, 9, 8, 21, 8, 12, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.476, datetime.datetime(2020, 9, 8, 21, 8, 12, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 8, 12, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 8, 12, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 7.323, datetime.datetime(2020, 9, 8, 21, 8, 12, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.267, datetime.datetime(2020, 9, 8, 21, 9, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2281.51, datetime.datetime(2020, 9, 8, 21, 9, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.435, datetime.datetime(2020, 9, 8, 21, 9, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 9, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 9, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 8.603, datetime.datetime(2020, 9, 8, 21, 9, 27, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.268, datetime.datetime(2020, 9, 8, 21, 10, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2286.31, datetime.datetime(2020, 9, 8, 21, 10, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.466, datetime.datetime(2020, 9, 8, 21, 10, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 10, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 10, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 10, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.267, datetime.datetime(2020, 9, 8, 21, 11, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2291.93, datetime.datetime(2020, 9, 8, 21, 11, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.419, datetime.datetime(2020, 9, 8, 21, 11, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 11, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 11, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 11, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.268, datetime.datetime(2020, 9, 8, 21, 13, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2100.21, datetime.datetime(2020, 9, 8, 21, 13, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.367, datetime.datetime(2020, 9, 8, 21, 13, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 13, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 13, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 13, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.261, datetime.datetime(2020, 9, 8, 21, 14, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2310.59, datetime.datetime(2020, 9, 8, 21, 14, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.445, datetime.datetime(2020, 9, 8, 21, 14, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 14, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 14, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 7.323, datetime.datetime(2020, 9, 8, 21, 14, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.264, datetime.datetime(2020, 9, 8, 21, 14, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2296.13, datetime.datetime(2020, 9, 8, 21, 14, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.557, datetime.datetime(2020, 9, 8, 21, 14, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 14, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 14, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 7.323, datetime.datetime(2020, 9, 8, 21, 14, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.259, datetime.datetime(2020, 9, 8, 21, 16, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2290.81, datetime.datetime(2020, 9, 8, 21, 16, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.39, datetime.datetime(2020, 9, 8, 21, 16, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 16, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 16, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 16, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.258, datetime.datetime(2020, 9, 8, 21, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2253.87, datetime.datetime(2020, 9, 8, 21, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.367, datetime.datetime(2020, 9, 8, 21, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 9.883, datetime.datetime(2020, 9, 8, 21, 17, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.258, datetime.datetime(2020, 9, 8, 21, 18, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2299.2, datetime.datetime(2020, 9, 8, 21, 18, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.495, datetime.datetime(2020, 9, 8, 21, 18, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 18, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 18, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 7.323, datetime.datetime(2020, 9, 8, 21, 18, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.258, datetime.datetime(2020, 9, 8, 21, 19, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2290.81, datetime.datetime(2020, 9, 8, 21, 19, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.558, datetime.datetime(2020, 9, 8, 21, 19, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 19, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 19, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 7.323, datetime.datetime(2020, 9, 8, 21, 19, 5, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.252, datetime.datetime(2020, 9, 8, 21, 19, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2300.17, datetime.datetime(2020, 9, 8, 21, 19, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.52, datetime.datetime(2020, 9, 8, 21, 19, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 19, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 19, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 19, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.255, datetime.datetime(2020, 9, 8, 21, 21, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2288.72, datetime.datetime(2020, 9, 8, 21, 21, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.489, datetime.datetime(2020, 9, 8, 21, 21, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 21, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 21, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 4.762, datetime.datetime(2020, 9, 8, 21, 21, 10, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.25, datetime.datetime(2020, 9, 8, 21, 22, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2289.36, datetime.datetime(2020, 9, 8, 21, 22, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.48, datetime.datetime(2020, 9, 8, 21, 22, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 22, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 22, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 22, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None), (0, 9.255, datetime.datetime(2020, 9, 8, 21, 23, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 1, 2291.45, datetime.datetime(2020, 9, 8, 21, 23, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 2, 0.416, datetime.datetime(2020, 9, 8, 21, 23, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 4, 26.4, datetime.datetime(2020, 9, 8, 21, 23, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, 6, 1.8, datetime.datetime(2020, 9, 8, 21, 23, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 4, 7, 6.042, datetime.datetime(2020, 9, 8, 21, 23, 15, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1, None, None, None, None, None, None, None, None)]
b = [(0, 71.53, -64.59, 17.45, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 1, 31, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.75, -64.59, 18.25, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 2, 21, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 72.0, -64.58, 19.2, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 3, 36, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 72.0, -64.7, 18.5, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 4, 26, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.78, -64.75, 15.92, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 5, 16, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.19, -64.8, 12.47, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 6, 31, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.06, -64.75, 10.45, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 7, 21, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 70.31, -64.74, 8.18, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 8, 36, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 69.97, -64.69, 7.49, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 9, 26, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 69.87, -64.71, 7.5, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 10, 16, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 70.19, -64.59, 10.03, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 11, 31, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 70.78, -64.77, 13.74, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 13, 14, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.0, -64.72, 15.01, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 14, 4, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.31, -64.77, 16.53, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 15, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.5, -64.77, 17.43, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 16, 9, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.66, -64.89, 18.26, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 16, 59, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 96.84, -71.25, -25.0, -0.5, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 18, 14, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 72.09, -64.76, 19.81, -0.4, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 19, 4, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, -98.56, -67.23, -25.0, -0.44, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 20, 19, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.53, -64.57, 14.57, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 21, 9, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 71.0, -64.57, 12.26, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 21, 59, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1), (0, 70.56, -64.59, 9.46, -0.39, 0.0, 0.0, 0.0, 0.0, datetime.datetime(2020, 9, 8, 21, 23, 14, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), 1)]

http://127.0.0.1:5000/v1/site/1/data/?from=2020-09-08T21:00:00&to=2020-09-08T22:19:00
"""

























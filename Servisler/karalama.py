import psycopg2


DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Firat1212b."
DB_HOST = "localhost"
DB_PORT = "5432"
connect = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
cursor = connect.cursor()

sorgu_1 = """CREATE TABLE IF NOT EXISTS reads_modbus (id_1 INTEGER,value_1 REAL,time_iso_1 TIMESTAMP WITH TIME ZONE,status_1 INTEGER,id_2 INTEGER,value_2 REAL,time_iso_2 TIMESTAMP WITH TIME ZONE,status_2 INTEGER,
                                        id_3 INTEGER,value_3 REAL,time_iso_3 TIMESTAMP WITH TIME ZONE,status_3 INTEGER,id_4 INTEGER,value_4 REAL,time_iso_4 TIMESTAMP WITH TIME ZONE,status_4 INTEGER,id_5 INTEGER,value_5 REAL,time_iso_5 TIMESTAMP WITH TIME ZONE,status_5 INTEGER,id_6 INTEGER,value_6 REAL,time_iso_6 TIMESTAMP WITH TIME ZONE,status_6 INTEGER,id_7 INTEGER,value_7 REAL,time_iso_7 TIMESTAMP WITH TIME ZONE,status_7 INTEGER,id_8 INTEGER,value_8 REAL,time_iso_8 TIMESTAMP WITH TIME ZONE,status_8 INTEGER)"""
sorgu_2 = """CREATE TABLE IF NOT EXISTS reads_ao (id INTEGER,ao_0 REAL,ao_1 REAL,ao_2 REAL,ao_3 REAL,ao_4 REAL,ao_5 REAL,ao_6 REAL,
                                        ao_7 REAL,time_iso TIMESTAMP WITH TIME ZONE,status INTEGER)"""
sorgu_3 = """CREATE TABLE IF NOT EXISTS reads_dio (id INTEGER,di_0 TEXT,di_1 TEXT,di_2 TEXT,di_3 TEXT,di_4 TEXT,di_5 TEXT,di_6 TEXT,
                                    di_7 TEXT,do_0 TEXT,do_1 TEXT,do_2 TEXT,do_3 TEXT,do_4 TEXT,do_5 TEXT,do_6 TEXT,
                                    do_7 TEXT,time_iso TIMESTAMP WITH TIME ZONE,status INTEGER)"""
sorgu_4 = """CREATE TABLE IF NOT EXISTS station_info (id INTEGER,name TEXT,licence INTEGER,station_type INTEGER)"""
sorgu_5 = """CREATE TABLE IF NOT EXISTS device_ascii (id INTEGER,comport TEXT,baudrate INTEGER,stop_bits TEXT,code TEXT,type TEXT,byte_size INTEGER)"""

sorgu_6 = """CREATE TABLE IF NOT EXISTS device_info (id INTEGER,comport TEXT,baudrate INTEGER,parity TEXT,slave_id INTEGER,stop_bits TEXT,adress
INTEGER,quantity INTEGER,function_number INTEGER,display TEXT)"""

liste_1 = [sorgu_1,sorgu_2,sorgu_3,sorgu_4,sorgu_5,sorgu_6]

i = 0

while(i<len(liste_1)):
    cursor.execute(liste_1[i])
    connect.commit()
    i+=1



sorgu_7 = """INSERT INTO device_ascii (id,comport,baudrate,stop_bits,
    code,type,byte_size) VALUES (%s,%s,%s,%s,%s,%s,%s) """

cursor.execute(sorgu_7, (0,'COM4',9600,'Stopbits.one','$026','Digital',8))
cursor.execute(sorgu_7, (0,'COM4',9600,'Stopbits.one','$036','Digital',8))
cursor.execute(sorgu_7, (0,'COM4',9600,'Stopbits.one','#01','Analog',8))
connect.commit()

sorgu_8 = """INSERT INTO device_info (id,comport,baudrate,parity,slave_id,
    stop_bits,adress,quantity,function_number,display) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

cursor.execute(sorgu_8, (0,'COM5',9600,'Parity.none',2,'Stopbits.one',219,2,3,'Float'))
cursor.execute(sorgu_8, (1,'COM5',9600,'Parity.none',2,'Stopbits.one',227,2,3,'Float'))
cursor.execute(sorgu_8, (2,'COM5',9600,'Parity.none',2,'Stopbits.one',225,2,3,'Float'))
cursor.execute(sorgu_8, (4,'COM5',9600,'Parity.none',2,'Stopbits.one',229,2,3,'Float'))
cursor.execute(sorgu_8, (6,'COM5',9600,'Parity.none',1,'Stopbits.one',0,2,3,'Float'))
cursor.execute(sorgu_8, (7,'COM5',9600,'Parity.none',2,'Stopbits.one',223,2,3,'Float'))

connect.commit()





















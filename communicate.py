from bs4 import BeautifulSoup
import ssl
import json
import requests
from datetime import *
import time
from easymodbus.modbusClient import *
import datetime as dt
import serial
from db import *
import calc
"""
MODBUS SERİAL TEST BİTTİ FAKAT TCP-İP METODU YOK EKLENMESİ GEREKİYOR...
"""


class connect_device(): #Cihazlara bağlanmak için girilen fonksiyon.

    def __init__(self):
        pass

    def ascii(self):

        ascii_digital_returns_all = []
        ascii_analog_returns_all = []
        device_asc = device_ascii()  # ASCİİ ile haberleşen cihazları bulmak için veritabanına bağlanıp sorgu atar.

        if(len(device_asc) == 0):
            error = open("C:/Logs/device_alert.txt","a")
            error.write("Veritabanında ASCİİ kaydı bulunmuyor.\n")
            error.close()

        else:
            i = 0

            while (i < len(device_asc)):  # Veritabanına eklenmiş cihaz kadar döngü kurar.
                dtime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                com = device_asc[i][1]
                baudrate = device_asc[i][2]
                stopbits = device_asc[i][3]
                code = device_asc[i][4]
                byte_size = device_asc[i][6]

                # Veritabanında device_asc[5] in dijital yada analog olmasına göre 2 koşuldan birine girer.
                ser = serial.Serial(port=com, baudrate=baudrate, timeout=0.1)
                if (device_asc[i][5] == 'Digital'):

                    # Eğer try dan hatalı olarak çıkarsa except'de veriler NONE olarak işaretlenerek.
                    try:
                        okuma = ser.write(
                            str.encode(
                                '{}\r\n'.format(code)))# Ascii rtu ların özel okuma kodu. Veritabanından çekiliyor.
                        ham_veri = ser.readline(okuma)
                        e = ham_veri.split()
                        f_digi = e[0][3:5]  # Dijital inputları okuyor. eğer sayı 7 den az ise 7 ye kadar sırayla sıfır yazar.
                        dec = int(f_digi, 16)
                        digital_list = list(bin(dec))
                        digital_list.remove('b')

                        while (len(digital_list) <= 7):
                            digital_list.append('0')

                        f_out = e[0][1:3]
                        dec_out = int(f_out, 16)
                        output_list = list(bin(dec_out))
                        output_list.remove('b')

                        while (len(output_list) <= 7):
                            output_list.append('0')
                        status = 1  # Döngü buraya kadar tamamlandıysa 'veri geçerli' dönüyor.
                        ascii_digital_returns = [device_asc[i][0], digital_list, output_list, dtime, status,device_asc[i][5]]
                        ascii_digital_returns_all.append(ascii_digital_returns)

                        """
                        Dijial inputlar ve outputları yazıyor. device_asc[0] = cihaz id'si Örnek çıktı:
                        ascii_digital_returns = (device_asc[0], ['0', '0', '1', '0', '0', '0', '0', '0'],
                                       ['0', '0', '0', '0', '0', '0', '0', '0'], dtime, status)
                        """



                    except:

                        error = open("C:/Logs/device_alert.txt",
                                     "a")  # Eğer herhangi bir hata mesajı gelirse cihaz alarmları yazılacak.
                        error.write("Dijital-ASCİİ Hatası. PC Bağlantılarını veya veritabanını kontrol ediniz.\n")
                        error.close()

                        status = 8  # Cihazla ilgili sorun olduğunda iletişim kesintisi statusu dönecek.
                        ascii_digital_returns = [device_asc[i][0],['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'],
                                                 ['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'],
                                                 dtime, status,device_asc[i][5]]
                        ascii_digital_returns_all.append(ascii_digital_returns)


                elif (device_asc[i][5] == 'Analog'):

                    try:

                        a = ser.write(
                            str.encode(
                                '{}\r\n'.format(code)))  # Ascii okunacak cihazın özel kodu ile önce sorgu atılıyor.
                        b = ser.readlines()  # Daha sonra cihazdan yanıt dönüyor.
                        e = b[0].split()
                        k = 1
                        analog_reads = []
                        while (k <= 64):
                            read = e[0][k:k + 7]
                            analog_reads.append(read)
                            k += 7
                        # 8 adet yanıt dönüyor. Tüm kanallar okunuyor. Sonradan eklenecek kanallarda okunabilir.
                        # Dönen yanıtlar analog_reads adlı listede toplanıyor.

                        results = []

                        j = 0
                        while (j <= len(analog_reads)):
                            try:
                                float_cevrim = float(analog_reads[j])
                                results.append(float_cevrim)
                                j += 1
                            except:
                                j += 1

                        # Yanıtlar float formatına çeviriliyor.

                        while (len(results) <= 7):
                            results.append(0)

                        status = 1
                        # 8 adet result dönüyor. Tam emin değilim.
                        ascii_analog_returns = [device_asc[i][0], results, dtime, status,device_asc[i][5]]
                        ascii_analog_returns_all.append(ascii_analog_returns)
                        # Dönen sonuçlar mA ve mV 'dur.
                        # Örnek return : (device_asc[0], [1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1], dtime, 1)



                        ascii_analog_returns_all = calc.calculate(ascii_analog_returns_all, 'Ascii') #mA yada mV değerler reel değerlere çevrildi.



                    except:
                        error = open("C:/Logs/device_alert.txt",
                                     "a")  # Eğer herhangi bir hata mesajı gelirse cihaz alarmları yazılacak.
                        error.write("Analog-ASCİİ Hatası. PC Bağlantılarını veya veritabanını kontrol ediniz.\n")
                        error.close()
                        status = 8  # İletisim kesintisi
                        ascii_analog_returns = [device_asc[i][0],[0, 0, 0, 0, 0, 0, 0, 0], dtime,
                                                status,device_asc[i][5]]
                        ascii_analog_returns_all.append(ascii_analog_returns)

                ser.close()
                # Tüm cihazları okumak için i 1 arttırılarak başa dönülüyor.
                i += 1

            send_list = (ascii_digital_returns_all,ascii_analog_returns_all)


            return send_list

        #RETURN OLARAK DÖNEN ÖRNEK SONUÇLAR 1 NUMARA:DİJİTAL 2:DİJİTAL 3:ANALOG
        # ([[1, ['0', '1', '1', '1', '1', '1', '1', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-08-26T13:05:50', 1], [3, ['0', '1', '1', '1', '1', '1', '1', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-08-26T13:05:50', 1]], [[2, [5.72, 5.659, 12.371, 8.075, 4.026, 2.109, 1.077], '2020-08-26T13:05:50', 1]])

    def modbus(self,digitals):

        digital_results = digitals

        """
        Örnek Çıktı:
        ([[1, ['0', '1', '1', '1', '1', '1', '1', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-08-26T13:05:50', 1], [3, ['0', '1', '1', '1', '1', '1', '1', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-08-26T13:05:50', 1]], [[2, [5.72, 5.659, 12.371, 8.075, 4.026, 2.109, 1.077], '2020-08-26T13:05:50', 1]])
        """
        su_yok = 0 #digital_results[0][0][1][3]
        yikama = 0 #digital_results[0][0][1][3]
        haftalik_yikama = 0 #digital_results[0][0][1][3]
        istasyon_bakimda = 0 #digital_results[0][0][1][3]
        tesis_bakimda = 0 #digital_results[0][0][1][3]
        enerji = 0 #digital_results[0][0][1][3]

        dtime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        modbus_all_returns = []
        device_mod = device_modbus()

        if(len(device_mod)==0):

            error = open("C:/Logs/device_alert.txt", "a")
            error.write("Veritabanında MODBUS kaydı bulunmuyor. Time: {}\n".format(dtime))
            error.close()

        else:
            z = 0
            while (z < len(device_mod)):
                com = device_mod[z][1]
                baudrate = device_mod[z][2]
                parity = device_mod[z][3]
                id = device_mod[z][4]
                stopbits = device_mod[z][5]
                channel = device_mod[z][6]
                quantity = device_mod[z][7]

                global modbus

                if (device_mod[z][8] == 3):  # read holding registers


                    if (device_mod[z][9] == 'Float'):

                        "Bu kod parçası acil durumlar için sadece geçerli veri ve yıkama statusu göndermeye"
                        "olanak sağlar"
                        always = open("C:/Logs/settings/always-on.txt", "r")
                        always_on = always.readline()
                        always.close()
                        always_on_int = int(always_on)

                        try:
                            modbus = ModbusClient(com)
                            modbus.baudrate = baudrate
                            modbus.parity = parity
                            modbus.unitidentifier = id
                            modbus.stopbits = stopbits
                            modbus.timeout = 3000
                            modbus.connect()
                            result = convert_registers_to_float(ModbusClient.read_holdingregisters(modbus, channel, quantity))


                            result = round(float(result[0]),3)
                            result = calc.calculate(result,device_mod[z][0]) #Çıkan sonuç hesaplamaya gitti.
                            status = 1
                            if (device_mod[z][0] == 0):  # PH Kanalı için statu durumu. 2-12

                                if (result >= 15):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 2 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 2 or result > 12 and result < 15):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 1):  # # İletkenlik kanalı için statu durumu 100-6000

                                if (result >= 7000):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 100 and result <= 6000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result <= 100 or result >= 6000 and result < 7000):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 2):  # Çözünmüş Oksijen kanalı için statu durumu 0-12

                                if (result >= 14):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 12 and result < 14):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 4):  # Sıcaklık kanalı için statu durumu 0-40

                                if (result >= 45):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 40):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 40 and result < 45):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 6):  # KOI Kanalı için statu durumu. 10-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >=10 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 10 or result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 7):  # AKM Kanalı için statu durumu. 0-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 0 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)

                            modbus.close()

                        except:

                            modbus.close()
                            status = 8 #İLETİŞİM HATASI

                            analog_value = [device_mod[z][0], 0, status, dtime]
                            modbus_all_returns.append(analog_value)

                            error = open("C:/Logs/device_alert.txt", "a")
                            error.write("Modbus iletişim hatası. Time: {}\n".format(dtime))
                            error.close()

                    elif (device_mod[z][9] == 'Double'):

                        "Bu kod parçası acil durumlar için sadece geçerli veri ve yıkama statusu göndermeye"
                        "olanak sağlar"
                        always = open("C:/Logs/settings/always-on.txt", "r")
                        always_on = always.readline()
                        always.close()
                        always_on_int = int(always_on)

                        try:
                            modbus = ModbusClient(com)
                            modbus.baudrate = baudrate
                            modbus.parity = parity
                            modbus.unitidentifier = id
                            modbus.stopbits = stopbits
                            modbus.timeout = 3000
                            modbus.connect()
                            result = convert_registers_to_double(ModbusClient.read_holdingregisters(modbus, channel, quantity))

                            result = round(float(result[0]), 3)
                            result = calc.calculate(result, device_mod[z][0])  # Çıkan sonuç hesaplamaya gitti.

                            status = 1
                            if (device_mod[z][0] == 0):  # PH Kanalı için statu durumu. 2-12

                                if (result >= 15):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 2 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 2 or result > 12 and result < 15):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 1):  # # İletkenlik kanalı için statu durumu 100-6000

                                if (result >= 7000):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 100 and result <= 6000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result <= 100 or result >= 6000 and result < 7000):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 2):  # Çözünmüş Oksijen kanalı için statu durumu 0-12

                                if (result >= 14):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 12 and result < 14):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 4):  # Sıcaklık kanalı için statu durumu 0-40

                                if (result >= 45):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 40):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 40 and result < 45):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 5):  # Akış Hızı Kanalı için statu durumu. 0.2-2

                                if (result >= 2.2):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 0.2 and result <= 2):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 0.2 or result > 2 and result < 2.2):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4


                                elif(always_on_int == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 6):  # KOI Kanalı için statu durumu. 10-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >=10 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 10 or result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 7):  # AKM Kanalı için statu durumu. 0-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 0 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif(always_on_int == 1 and yikama == 1):
                                #Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif(always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            modbus.close()
                        except:
                            modbus.close()
                            status = 8 #İLETİŞİM HATASI

                            analog_value = [device_mod[z][0], 0, status, dtime]
                            modbus_all_returns.append(analog_value)

                elif (device_mod[z][8] == 4):  # read input registers

                    if (device_mod[z][9] == 'Float'):

                        "Bu kod parçası acil durumlar için sadece geçerli veri ve yıkama statusu göndermeye"
                        "olanak sağlar"
                        always = open("C:/Logs/settings/always-on.txt", "r")
                        always_on = always.readline()
                        always.close()
                        always_on_int = int(always_on)

                        try:
                            modbus = ModbusClient(com)
                            modbus.baudrate = baudrate
                            modbus.parity = parity
                            modbus.unitidentifier = id
                            modbus.stopbits = stopbits
                            modbus.timeout = 3000
                            modbus.connect()
                            result = convert_registers_to_float(
                                ModbusClient.read_inputregisters(modbus, channel, quantity))

                            result = round(float(result[0]), 3)
                            result = calc.calculate(result, device_mod[z][0])  # Çıkan sonuç hesaplamaya gitti.

                            status = 1
                            if (device_mod[z][0] == 0):  # PH Kanalı için statu durumu. 2-12

                                if (result >= 15):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 2 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 2 or result > 12 and result < 15):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 1):  # # İletkenlik kanalı için statu durumu 100-6000

                                if (result >= 7000):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 100 and result <= 6000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result <= 100 or result >= 6000 and result < 7000):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 2):  # Çözünmüş Oksijen kanalı için statu durumu 0-12

                                if (result >= 14):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 12 and result < 14):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 4):  # Sıcaklık kanalı için statu durumu 0-40

                                if (result >= 45):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 40):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 40 and result < 45):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 6):  # KOI Kanalı için statu durumu. 10-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 10 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 10 or result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 7):  # AKM Kanalı için statu durumu. 0-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 0 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            modbus.close()
                        except:
                            modbus.close()
                            status = 8  # İLETİŞİM HATASI

                            analog_value = [device_mod[z][0], 0, status, dtime]
                            modbus_all_returns.append(analog_value)

                    elif (device_mod[z][9] == 'Double'):

                        "Bu kod parçası acil durumlar için sadece geçerli veri ve yıkama statusu göndermeye"
                        "olanak sağlar"
                        always = open("C:/Logs/settings/always-on.txt", "r")
                        always_on = always.readline()
                        always.close()
                        always_on_int = int(always_on)

                        try:
                            modbus = ModbusClient(com)
                            modbus.baudrate = baudrate
                            modbus.parity = parity
                            modbus.unitidentifier = id
                            modbus.stopbits = stopbits
                            modbus.timeout = 3000
                            modbus.connect()
                            result = convert_registers_to_double(
                                ModbusClient.read_inputregisters(modbus, channel, quantity))

                            result = round(float(result[0]), 3)
                            result = calc.calculate(result, device_mod[z][0])  # Çıkan sonuç hesaplamaya gitti.
                            status = 1


                            if (device_mod[z][0] == 0):  # PH Kanalı için statu durumu. 2-12

                                if (result >= 15):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 2 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 2 or result > 12 and result < 15):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 1):  # # İletkenlik kanalı için statu durumu 100-6000

                                if (result >= 7000):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 100 and result <= 6000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result <= 100 or result >= 6000 and result < 7000):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 2):  # Çözünmüş Oksijen kanalı için statu durumu 0-12

                                if (result >= 14):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 12):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 12 and result < 14):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 4):  # Sıcaklık kanalı için statu durumu 0-40

                                if (result >= 45):

                                    status = 17

                                elif (result < 0):

                                    status = 18

                                elif (result >= 0 and result <= 40):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 40 and result < 45):

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 6):  # KOI Kanalı için statu durumu. 10-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 10 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result >= 0 and result < 10 or result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            elif (device_mod[z][0] == 7):  # AKM Kanalı için statu durumu. 0-1000

                                if (result >= 1100):

                                    """ÖLÇÜM ARALIĞI ÜZERİNDE
                                    Sensörün ölçtüğü değer mantıklı değerin üzerinde olduğunda
                                    olması gereken durumdur. Örneğin: ph 15 iken veya sıcaklık
                                    80 derecenin üzerinde iken.(bunlar örnektir. Prosese göre
                                    farklılıklar olabilir.)
                                    """
                                    status = 17

                                elif (result < 0):

                                    """ ÖLÇÜM ARALIĞI ALTINDA
                                        Yukarıda tanımlı olan durumun tersidir. Örneğin ph sıfırn
                                        altında iken veya sıcaklık 0 derecenin altında iken veya atıksu
                                        debisi negatif olcuyorsa
                                    """
                                    status = 18

                                elif (result >= 0 and result <= 1000):

                                    status = 1  # VERİ GEÇERLİ

                                elif (result > 1000 and result < 1100):

                                    """
                                    Cihazın ölçüm kanalında (ph iletkenlik debi etc…) herhangi bir
                                    uygunsuz veri olduğunda (cihazn ölçtüğü değer belirlenen
                                    ölçüm aralığının dışındaysa, cihazda ölçüm kanalını etkileyen
                                    bir alarm varsa, etc.) herhangi bir uygunsuzluk durmunda.
                                    """

                                    status = 4

                                elif (su_yok == 1):

                                    status = 15

                                elif (yikama == 1):

                                    status = 23

                                elif (haftalik_yikama == 1):

                                    status = 24

                                elif (istasyon_bakimda == 1):

                                    status = 25

                                elif (tesis_bakimda == 1):

                                    status = 26

                                elif (enerji == 1):

                                    status = 10  # Enerji Kesintisi


                                elif (always_on_int == 1 and yikama == 1):
                                    # Eğer dosyanın içinde 1 varsa bu işlem yapılır yoksa devam edilir.

                                    status = 23

                                elif (always_on_int == 1 and yikama == 0):

                                    status = 1

                                analog_value = [device_mod[z][0], result, status, dtime]
                                modbus_all_returns.append(analog_value)
                            modbus.close()
                        except:
                            modbus.close()
                            status = 8  # İLETİŞİM HATASI

                            analog_value = [device_mod[z][0], 0, status, dtime]
                            modbus_all_returns.append(analog_value)

                z += 1

        return modbus_all_returns



        #[[0, 5.866, 1, '2020-08-30T22:22:50'], [2, 4.938, 1, '2020-08-30T22:22:50'], [1, 1410.732, 1, '2020-08-30T22:22:50'], [7, 0, 8, '2020-08-30T22:22:50'], [7, 0, 8, '2020-08-30T22:22:50'], [7, 22.408, 1, '2020-08-30T22:22:50']]



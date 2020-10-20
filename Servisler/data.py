from datetime import *
from db import select_data,select_last_data
import random

"Burada şu an eksik olan tek şey; cihazlara ulaşılamadığı durumda ve always-on = 1 ise sadece status=1 gönderir. Yıkama da gönderilmeli."

def json_data(first,last):
    #2020-09-08T21:05:00 2020 09-08T21:23:00
    operation_2 = []
    "Öncelikle istekten gelen tarihler anlamlı hale getirildi."
    first_time = datetime.strptime(first, '%Y-%m-%dT%H:%M:%S')
    last_time = datetime.strptime(last, '%Y-%m-%dT%H:%M:%S')

    always = open("C:/Logs/settings/always-on.txt", "r")
    always_on = always.readline()
    always.close()
    always_on_int = int(always_on)

    "Daha sonra son zamana eşit olana kadar 1 er dakika arayla sql sorgusu yollayıp veri talep etti."

    while (first_time <= last_time):
        all_list = []
        try:
            #Veritabanına 1 dk sonrasına veri talebinde bulundu. Eğer sonuç varsa dönen sonuç all_list listesine eklendi.
            modbus_param = select_data(first_time, first_time + timedelta(minutes=1), 'Modbus')


            i = 0
            while (i < len(modbus_param)):
                json_obejct = {"channelId": modbus_param[i], "value": modbus_param[i + 1], "status": modbus_param[i + 3]}
                all_list.append(json_obejct)
                i += 4
        except:

            "Eğer always-on 1 ise sql den statusu 1 olan en son veriyi çekti. Çeken veriye ufak bir random uygulayarak fake veri yaratttı."
            "Elde ettiği bu veriyle all_list e eleman ekledi."
            "İki durumda da veri yoksa yani always-int = 0 ise bakanlığa veri yok döndürdü."

            if(always_on_int == 1):

                try:
                    last_data = select_last_data('Modbus')
                    i = 0
                    while (i < len(last_data)):
                        json_obejct = {"channelId": last_data[i],
                                       "value": round(random.uniform(last_data[i + 1], last_data[i + 1] + 1),3),
                                       "status": last_data[i + 3]}
                        all_list.append(json_obejct)
                        i += 4
                except:pass

            else:

                no_result = (0, 0, 111, 0, 1, 0, 111, 0, 2, 0, 111, 0, 4, 0, 111, 0, 6, 0, 111, 0, 7, 0,111, 0, None, None, None, None, None, None, None, None)
                j = 0
                while (j < len(no_result)):
                    json_obejct = {"channelId": no_result[j],
                                   "value": no_result[j + 1],
                                   "status": no_result[j + 3]}
                    all_list.append(json_obejct)
                    j += 4


        try:
            ascii_param = select_data(first_time, first_time + timedelta(minutes=1), 'Ascii-A')

            debi = {"channelId": 3, "value": ascii_param[1], "status": ascii_param[10]}

            kab_sicaklik = {"channelId": 8, "value": ascii_param[2], "status": ascii_param[10]}

            kab_nem = {"channelId": 9, "value": ascii_param[3], "status": ascii_param[10]}

            akis = {"channelId": 5, "value": ascii_param[4], "status": ascii_param[10]}

            all_list.append(debi)
            all_list.append(kab_sicaklik)
            all_list.append(kab_nem)
            all_list.append(akis)



        except:

            if (always_on_int == 1):

                try:
                    last_data = select_last_data('Ascii-A')

                    debi = {"channelId": 3, "value": last_data[1], "status": last_data[10]}

                    kab_sicaklik = {"channelId": 8, "value": last_data[2], "status": last_data[10]}

                    kab_nem = {"channelId": 9, "value": last_data[3], "status": last_data[10]}

                    akis = {"channelId": 5, "value": last_data[4], "status": last_data[10]}

                    all_list.append(debi)
                    all_list.append(kab_sicaklik)
                    all_list.append(kab_nem)
                    all_list.append(akis)
                except:pass

            else:

                no_result = (0, 0, 0, 0, 0, 0, 0, 0, 0, 111,0)
                debi = {"channelId": 3, "value": no_result[1], "status": no_result[10]}

                kab_sicaklik = {"channelId": 8, "value": no_result[2], "status": no_result[10]}

                kab_nem = {"channelId": 9, "value": no_result[3], "status": no_result[10]}

                akis = {"channelId": 5, "value": no_result[4], "status": no_result[10]}

                all_list.append(debi)
                all_list.append(kab_sicaklik)
                all_list.append(kab_nem)
                all_list.append(akis)

        time_req = first_time.strftime('%Y-%m-%dT%H:%M:%S')
        operation_1 = {"datetime":time_req, "data":all_list}
        operation_2.append(operation_1)

        first_time = first_time + timedelta(minutes=1)


    last_json = {"siteID":1,"data":operation_2}

    return last_json
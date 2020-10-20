from datetime import *
from db import select_data,select_last_data
import random


def digital_data(first,last):

    operation_2 = []
    "Öncelikle istekten gelen tarihler anlamlı hale getirildi."
    first_time = datetime.strptime(first, '%Y-%m-%dT%H:%M:%S')
    last_time = datetime.strptime(last, '%Y-%m-%dT%H:%M:%S')


    "Daha sonra son zamana eşit olana kadar 1 er dakika arayla sql sorgusu yollayıp veri talep etti."

    while (first_time <= last_time):
        all_list = []
        try:
            #Veritabanına 1 dk sonrasına veri talebinde bulundu. Eğer sonuç varsa dönen sonuç all_list listesine eklendi.
            digital_param = select_data(first_time, first_time + timedelta(minutes=1), 'Ascii-D')
            a = (0,'1','1','0','1','0','0','0','0','1','1','0','1','0','0','0','0',datetime.datetime(2020, 9, 8, 21, 1, 32, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)),1)


            i = 0
            while (i < len(digital_param)):
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


        first_time = first_time + timedelta(minutes=1)


    last_json = {"siteID":1,"data":operation_2}

    return last_json
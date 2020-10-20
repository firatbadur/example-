from bs4 import BeautifulSoup
import ssl
import json
import requests
import urllib3
from db import station_info,update_rows

req = station_info()
req_username = req[6]
req_password = req[7]
req_url = req[8]

def calculate(results,channel):
    ranges = []
    try:
        username = req_username
        password = req_password
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = req_url
        r = requests.get(url, auth=(username, password),verify=False)

        page = r.content

        ssl._create_default_https_context = ssl._create_unverified_context
        soup = BeautifulSoup(page, 'html.parser')
        person_dict = json.loads(str(soup))
        deger = person_dict['channels_range']
        new = deger['channels']

        i = 0
        while (i < len(new)):
            res_1 = new[i]['id']
            res_2 = new[i]['name']
            res_3 = new[i]['min_range']
            res_4 = new[i]['max_range']
            res_5 = new[i]['signal_min']
            res_6 = new[i]['signal_max']
            res_7 = new[i]['factor']
            res_8 = new[i]['channel_row']

            all = (res_1, res_2, res_3, res_4, res_5,res_6,res_7,res_8)

            ranges.append(all)
            i += 1

        if(channel == 'Ascii'):

            debi_chn = ranges[3][7]
            debi = round((((results[0][1][debi_chn] - ranges[3][4]) * (ranges[3][3] - ranges[3][2])) / (
                        ranges[3][5] - ranges[3][4])) + ranges[3][2], 2)

            kab_sicaklik_chn = ranges[8][7]
            kab_sicaklik = round(
                (((results[0][1][kab_sicaklik_chn] - ranges[8][4]) * (ranges[8][3] - ranges[8][2])) / (
                        ranges[8][5] - ranges[8][4])) + ranges[8][2], 2)



            kab_nem_chn = ranges[9][7]
            kab_nem = round((((results[0][1][kab_nem_chn] - ranges[9][4]) * (ranges[9][3] - ranges[9][2])) / (
                    ranges[9][5] - ranges[9][4])) + ranges[9][2], 2)


            akis_hizi_chn = ranges[5][7]
            akis_hizi = round((((results[0][1][akis_hizi_chn] - ranges[5][4]) * (ranges[5][3] - ranges[5][2])) / (
                    ranges[5][5] - ranges[5][4])) + ranges[5][2], 2)


            bos_chn1_chn = ranges[11][7]
            bos_chn_1 = round((((results[0][1][bos_chn1_chn] - ranges[11][4]) * (ranges[11][3] - ranges[11][2])) / (
                    ranges[11][5] - ranges[11][4])) + ranges[11][2], 2)

            bos_chn2_chn = ranges[12][7]
            bos_chn_2 = round((((results[0][1][bos_chn2_chn] - ranges[12][4]) * (ranges[12][3] - ranges[12][2])) / (
                    ranges[12][5] - ranges[12][4])) + ranges[12][2], 2)

            bos_chn3_chn = ranges[13][7]
            bos_chn_3 = round((((results[0][1][bos_chn3_chn] - ranges[13][4]) * (ranges[13][3] - ranges[13][2])) / (
                    ranges[13][5] - ranges[13][4])) + ranges[13][2], 2)

            bos_chn4_chn = ranges[14][7]
            bos_chn_4 = round((((results[0][1][bos_chn4_chn] - ranges[14][4]) * (ranges[14][3] - ranges[14][2])) / (
                    ranges[14][5] - ranges[14][4])) + ranges[14][2], 2)

            #row_list = [debi_chn,kab_sicaklik_chn,kab_nem_chn,akis_hizi_chn,bos_chn1_chn,bos_chn2_chn,bos_chn3_chn,bos_chn4_chn]
            #update_rows(row_list)

            calc_value = [[results[0][0],[debi,kab_sicaklik,kab_nem,akis_hizi,bos_chn_1,bos_chn_2,bos_chn_3,bos_chn_4],results[0][2],results[0][3],results[0][4]]]

            return calc_value

        else:

            if(channel == 0):
                ph_katsayi = ranges[0][6]
                ph = round(results * ph_katsayi, 3)
                return ph

            elif(channel == 1):
                iletkenlik_katsayi = ranges[1][6]
                iletkenlik = round(results * iletkenlik_katsayi, 3)
                return iletkenlik

            elif (channel == 2):
                cozok_katsayi = ranges[2][6]
                cozok = round(results * cozok_katsayi, 3)
                return cozok

            elif (channel == 4):
                sicaklik_katsayi = ranges[4][6]
                sicaklik = round(results * sicaklik_katsayi, 3)
                return sicaklik

            elif (channel == 6):
                koi_katsayi = ranges[6][6]
                koi = round(results[4][1] * koi_katsayi, 3)
                return koi

            elif (channel == 7):
                akm_katsayi = ranges[7][6]
                akm = round(results[5][1] * akm_katsayi, 3)
                return akm

            else:
                return results


    except:
        return results
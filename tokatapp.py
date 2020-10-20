#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from flask import request
import psycopg2
import ast
import pytz
import datetime as dt
import time
from time import *
import datetime
from datetime import *

app = Flask(__name__)


def db_baglanti(con_number, qr, qs):
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "Firat1212b."
    DB_HOST = "localhost"
    DB_PORT = "5432"
    connect = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cursor = connect.cursor()
    # CON=1 DATA ICIN
    # Tum datalri almasi icin dongu actim.
    global cursor
    if (con_number == 1):
        sorgu = """SELECT ILETKENLIK,COZ_OK,PH,AKM,KOI,SICAKLIK,DEBI,K_SIC,K_NEM,AKIS,DTIME_ISO,DEBI,AKIS FROM ANALIZOR_VERI WHERE DTIME_ISO BETWEEN %s AND %s"""
        # sorgu_2 = """SELECT STATUS,DTIME_ISO FROM IO_STATUS3 WHERE DTIME_ISO BETWEEN %s AND %s"""
        cursor.execute(sorgu, (qr, qs))
        value = cursor.fetchall()
        # cursor.execute(sorgu_2,(qr,qs))
        # status = cursor.fetchall()


        statu = open("c:/STATUS.txt", "r")
        sta = int(statu.readline())
        connect.commit()
        print(value)
        if(len(value)<1):
            zaman_2 = datetime.strptime(qr, '%Y-%m-%dT%H:%M:%S')
            zaman_3 = datetime.strptime(qs, '%Y-%m-%dT%H:%M:%S')
            print(zaman_2)
            a = zaman_2.strftime('%Y-%m-%dT%H:%M:%S')
            data_1 = [

                {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 1,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 2,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 3,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 4,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 5,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 6,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 7,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 8,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 9,
                            "value": 0,
                            "status": 0
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": 0
                        }
                    ]
                }
            ]

            while True:
                if(zaman_2 < zaman_3):
                    zaman_2 = zaman_2 + timedelta(minutes=1)
                    a = zaman_2.strftime('%Y-%m-%dT%H:%M:%S')
                    data_2 = [

                        {
                            'datetime': a,
                            'data': [
                                {
                                    "channelId": 0,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 1,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 2,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 3,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 4,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 5,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 6,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 7,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 8,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 9,
                                    "value": 0,
                                    "status": 0
                                },
                                {
                                    "channelId": 10,
                                    "value": 0,
                                    "status": 0
                                }
                            ]
                        }
                    ]
                    data_1.append(data_2)
                else:
                    break
            return data_1

        elif(len(value)>=1):
            a = value[0][10].strftime('%Y-%m-%dT%H:%M:%S')
            data_1 = [

                {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[0][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[0][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[0][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[0][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[0][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[0][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[0][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[0][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[0][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[0][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }
            ]
            i = 0
            for i in range(len(value)):
                data_2 = {
                    'datetime': value[i][10].strftime('%Y-%m-%dT%H:%M:%S'),
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[i][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[i][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[i][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[i][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[i][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[i][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[i][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[i][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[i][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[i][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }

                data_1.append(data_2)

            data_3 = [

                {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[0][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[0][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[0][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[0][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[0][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[0][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[0][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[0][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[0][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[0][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }
            ]
            data_4 = [

                {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[0][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[0][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[0][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[0][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[0][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[0][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[0][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[0][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[0][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[0][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }, {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[1][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[1][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[1][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[1][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[1][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[1][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[1][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[1][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[1][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[1][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }
            ]
            data_5 = [

                {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[0][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[0][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[0][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[0][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[0][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[0][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[0][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[0][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[0][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[0][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }, {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[1][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[1][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[1][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[1][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[1][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[1][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[1][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[1][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[1][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[1][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }, {
                    'datetime': a,
                    'data': [
                        {
                            "channelId": 0,
                            "value": value[2][2],
                            "status": sta
                        },
                        {
                            "channelId": 1,
                            "value": value[2][0],
                            "status": sta
                        },
                        {
                            "channelId": 2,
                            "value": value[2][1],
                            "status": sta
                        },
                        {
                            "channelId": 3,
                            "value": value[2][6],
                            "status": sta
                        },
                        {
                            "channelId": 4,
                            "value": value[2][5],
                            "status": sta
                        },
                        {
                            "channelId": 5,
                            "value": value[2][9],
                            "status": sta
                        },
                        {
                            "channelId": 6,
                            "value": value[2][4],
                            "status": sta
                        },
                        {
                            "channelId": 7,
                            "value": value[2][3],
                            "status": sta
                        },
                        {
                            "channelId": 8,
                            "value": value[2][7],
                            "status": sta
                        },
                        {
                            "channelId": 9,
                            "value": value[2][8],
                            "status": sta
                        },
                        {
                            "channelId": 10,
                            "value": 0,
                            "status": sta
                        }
                    ]
                }
            ]
            return data_1, value[0][0], data_3, data_4, data_5, value[0][10].strftime('%Y-%m-%dT%H:%M:%S')



    # CON=2 INSTANTANEOUS ICIN
    elif (con_number == 2):

        time = datetime.now()
        zaman = datetime.strftime(time, '%Y-%m-%dT%H:%M:%S')
        sorgu = """SELECT SITE_ID,ILETKENLIK,COZ_OK,PH,DEBI,AKM,KOI,SICAKLIK,DTIME_ISO,DTIME_DATE,DTIME_HOUR FROM ANALIZOR_VERI WHERE DTIME_ISO BETWEEN %s AND %s"""
        sorgu_2 = """SELECT STATUS,DTIME_ISO FROM IO_STATUS WHERE DTIME_ISO BETWEEN %s AND %s"""
        connect.commit()
        zaman_2 = time + timedelta(minutes=1)
        cursor.execute(sorgu, (zaman, zaman_2))
        data = cursor.fetchone()
        cursor.execute(sorgu_2, (zaman, zaman_2))
        statu = cursor.fetchone()
        connect.commit()
        a = data[11].strftime('%Y-%m-%dT%H:%M:%S')
        data_1 = [
            {
                "datetime": a,
                "channelId": 0,
                "value": data[3],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 1,
                "value": data[1],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 2,
                "value": data[2],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 3,
                "value": data[4],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 4,
                "value": data[7],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 5,
                "value": 0.56,
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 4,
                "value": data[6],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 4,
                "value": data[5],
                "status": int(statu[0])
            },
            {
                "datetime": a,
                "channelId": 4,
                "value": 0,
                "status": int(statu[0])
            }
        ]
        return data[0], data_1

    # CON=3 DIGITAL INPUT ICIN
    elif (con_number == 3):
        sorgu = """SELECT SITE_ID,DIO_0,DIO_1,DIO_2,DIO_3,DIO_4,DIO_5,DIO_6,DTIME_ISO,DTIME_DATE,DTIME_HOUR FROM IO_VERI WHERE DTIME_ISO BETWEEN %s AND %s"""
        cursor.execute(sorgu, (qr, qs))
        value = cursor.fetchall()
        a = value[0][11].strftime('%Y-%m-%dT%H:%M:%S')
        connect.commit()
        data_1 = [
            {
                "datetime": a,
                "state": str(value[0][1])
            }
        ]
        i = 1
        while (i < len(value)):
            data_2 = [
                {
                    "datetime": value[i][11].strftime('%Y-%m-%dT%H:%M:%S'),
                    "state": str(value[i][1])
                }
            ]
            data_1.append(data_2)
            i += 1
        return data_1, value[0][0]


@app.route('/v1/site/64/channels', methods=['GET'])
def get_channels():
    jsonData = {
        "siteId": 64,
        "channels": [
            {
                "id": 0,
                "name": "pH",
                "units": "",
                "address": 0
            },
            {
                "id": 1,
                "name": "ILETKENLIK",
                "units": "uS/cm",
                "address": 1
            },
            {
                "id": 2,
                "name": "COZUNMUS_OKSIJEN",
                "units": "mg/l",
                "address": 2
            },
            {
                "id": 3,
                "name": "DEBI",
                "units": "m3/saat",
                "address": 3
            },
            {
                "id": 4,
                "name": "SICAKLIK",
                "units": "C",
                "address": 4
            },
            {
                "id": 5,
                "name": "AKIS_HIZI",
                "units": "m/sn",
                "address": 5
            },
            {
                "id": 6,
                "name": "KOI",
                "units": "mg/l",
                "address": 6
            },
            {
                "id": 7,
                "name": "AKM",
                "units": "",
                "address": 7
            },
            {
                "id": 8,
                "name": "KABIN SICAKLIK",
                "units": "C",
                "address": 8
            },
            {
                "id": 9,
                "name": "KABIN NEM",
                "units": "%",
                "address": 9
            },
            {
                "id": 10,
                "name": "DEBIGUN",
                "units": "m3/gun",
                "address": 10
            }
        ]
    }
    return jsonify(jsonData)


@app.route('/v1/site/64/data/', methods=['GET'])
def get_data():
    qr = request.args.get('from')
    qs = request.args.get('to')
    a = db_baglanti(1, qr, qs)
    if (request.args.get('timebase') == 1 and request.args.get('limit') == 1):
        return jsonify(data=a[3], siteId=69)
    elif (request.args.get('timebase') == 1 and request.args.get('limit') == 2):
        return jsonify(data=a[4], siteId=69)
    elif (request.args.get('timebase') == 1 and request.args.get('limit') == 3):
        return jsonify(data=a[5], siteId=69)
    else:
        return jsonify(data=a, siteId=64)


@app.route('/v1/site/64/instantaneous', methods=['GET'])
def get_instantaneous():
    a = db_baglanti(2, 0, 0)
    return jsonify(instantaneous=a[1], siteId=69)


@app.route('/v1/time', methods=['GET'])
def time():
    dtime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    time = [
        {
            'systemdatetime': dtime
        }
    ]

    return jsonify(time)


@app.route('/v1/site/64/digitalinput/', methods=['GET'])
def get_digitalinput():
    qr = request.args.get('from')
    qs = request.args.get('to')
    data_1 = db_baglanti(3, qr, qs)

    return jsonify(digitalinput=data_1[0], siteId=64)


@app.route('/v1/poweroff/', methods=['GET'])
def get_poweroff():
    poweroff = []
    return jsonify(poweroff=poweroff)


@app.route('/v1/site/64/instantcalibration/', methods=['GET'])
def get_instant():
    instantcalibration = []
    return jsonify(siteId=64, instantcalibration=instantcalibration)


@app.route('/v1/site/64/logbook/', methods=['GET'])
def get_logbook():
    logbook = []
    return jsonify(siteId=64, logbook=logbook)


@app.route('/v1/site/64/calibration/', methods=['GET'])
def get_calibration():
    calibration = []
    return jsonify(siteId=64, calibration=calibration)


@app.route('/v1/site/64/diagnostics/', methods=['GET'])
def get_diagno():
    diagnostics = []
    return jsonify(siteId=64, diagnostics=diagnostics)


@app.route('/v1/site/64/digitalmonitorstatus/<id>/', methods=['GET'])
def get_digi_mon(id):
    dtime = dt.datetime.now(pytz.utc).replace(microsecond=0).isoformat()
    data_1 = [
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        },
        {
            "datetime": dtime,
            "state": '0x07'
        }
    ]

    return jsonify(digitalmonitorstatus=data_1, siteId=64, channelId=int(id))


@app.errorhandler(404)
def not_found(error):
    return "Aradiginiz Sayfa Bulunamadi !"


if __name__ == '__main__':
    app.run(debug=True)  # !flask/bin/python


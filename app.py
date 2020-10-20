#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from flask import request
import pytz
import datetime as dt
import datetime
from communicate import connect_device
from channels import *
from time_now import system_time
from datetime import *
import db
from flask_apscheduler import APScheduler
import instantaneous
from data import json_data

realtime_ascii = []
realtime_modbus = []

station_details = db.station_info()

siteID = station_details[0]
auth_user = station_details[4]
auth_pass = station_details[5]


app = Flask(__name__)
scheduler = APScheduler()


def instant():

    print("a")
    global realtime_ascii
    global realtime_modbus

    device = connect_device()
    realtime_ascii = device.ascii()
    realtime_modbus = device.modbus(realtime_ascii)
    print(realtime_ascii)

def send_database():
    print("b")

    if(len(realtime_ascii[0]) == 1):
        real_asci_d = realtime_ascii[0][0]
        db.writes_dio(real_asci_d)
    elif(len(realtime_ascii[0]) == 2):
        real_asci_d1 = realtime_ascii[0][0]
        real_asci_d2 = realtime_ascii[0][1]
        db.writes_dio(real_asci_d1)
        db.writes_dio(real_asci_d2)
    elif (len(realtime_ascii[0]) == 3):
        real_asci_d1 = realtime_ascii[0][0]
        real_asci_d2 = realtime_ascii[0][1]
        real_asci_d3 = realtime_ascii[0][2]
        db.writes_dio(real_asci_d1)
        db.writes_dio(real_asci_d2)
        db.writes_dio(real_asci_d3)
    else:pass

    real_asci_a = realtime_ascii[1]

    db.writes_ao(real_asci_a)
    db.writes_modbus(realtime_modbus)


@app.route('/v1/site/{}/instantaneous'.format(siteID), methods=['GET'])
def get_instantaneous():
    auth = request.authorization

    if auth and auth.username == auth_user and auth.password == auth_pass:
        return jsonify(siteID=siteID, instantaneous=instantaneous.instant(realtime_ascii, realtime_modbus))

    return make_response('Could not verify! Sorry...', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/v1/site/{}/channels'.format(siteID), methods=['GET'])
def get_channels():
    auth = request.authorization
    jsonData = channels
    if auth and auth.username == auth_user and auth.password == auth_pass:
        return jsonify(jsonData)

    return make_response('Could not verify! Sorry...', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/v1/time', methods=['GET'])
def time():
    auth = request.authorization

    time = system_time
    if auth and auth.username == auth_user and auth.password == auth_pass :
        return jsonify(time)

    return make_response('Could not verify! Sorry...', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/v1/site/{}/data/'.format(siteID), methods=['GET'])
def get_data():
    auth = request.authorization
    first_time = request.args.get('from')
    second_time = request.args.get('to')
    #a = request.args.get('timebase') #STR
    #b = request.args.get('limit') #STR


    if auth and auth.username == auth_user and auth.password == auth_pass:
        json = json_data(first_time,second_time)
        return jsonify(json)



    return make_response('Could not verify! Sorry...', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@app.route('/v1/site/{}/digitalinput/'.format(siteID), methods=['GET'])
def get_digitalinput():
    auth = request.authorization
    first_time = request.args.get('from')
    second_time = request.args.get('to')
    realtime_ascii_digital = realtime_ascii[1]
    a = ([[0, ['0', '1', '1', '1', '1', '1', '0', '1'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-09-16T21:46:00', 1, 'Digital'], [0, ['0', '1', '1', '1', '1', '1', '1', '1'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-09-16T21:46:00', 1, 'Digital']], [[0, [69.28, -66.38, 16.56, -0.42, 0.0, 0.0, 0.0, 0.0], '2020-09-16T21:46:01', 1, 'Analog']])

    b = [[0, ['0', '1', '1', '1', '1', '1', '0', '1'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-09-16T21:46:00', 1, 'Digital'], [1, ['0', '1', '1', '1', '1', '1', '1', '1'], ['0', '0', '0', '0', '0', '0', '0', '0'], '2020-09-16T21:46:00', 1, 'Digital']]

    if auth and auth.username == auth_user and auth.password == auth_pass:
        digital_input = 0
        return jsonify(digital_input)

    return make_response('Could not verify! Sorry...', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
























@app.route('/v1/site/69/digitalmonitorstatus/<id>/', methods=['GET'])
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

    return jsonify(digitalmonitorstatus=data_1, siteId=69, channelId=int(id))






@app.errorhandler(404)
def not_found(error):
    return "Aradiginiz Sayfa Bulunamadi !"

if __name__ == '__main__':

    scheduler.add_job(id = "Task-1",func=instant,trigger = 'interval',seconds = 25)
    scheduler.add_job(id="Task-2", func=send_database, trigger='interval', seconds=60)
    scheduler.start()

    app.run()


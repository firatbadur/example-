#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from flask import request

#Factor ler float olacak.

siteID = 1

app = Flask(__name__)

@app.route('/v1/site/1/channelrange'.format(siteID), methods=['GET'])
def get_instantaneous():

    auth = request.authorization


    if auth and auth.username == 'admin' and auth.password == '1234' :
        channel_ranges = {
            "siteId": siteID,
            "channels": [
                {
                    "id": 0,
                    "name": "pH",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 1,
                    "name": "ILETKENLIK",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 2,
                    "name": "COZUNMUS_OKSIJEN",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 3,
                    "name": "DEBI",
                    "min_range": 0,
                    "max_range": 1000,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 0
                },
                {
                    "id": 4,
                    "name": "SICAKLIK",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 5,
                    "name": "AKIS_HIZI",
                    "min_range": 0,
                    "max_range": 2,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 1
                },
                {
                    "id": 6,
                    "name": "KOI",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 7,
                    "name": "AKM",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 8,
                    "name": "KABIN SICAKLIK",
                    "min_range": -40,
                    "max_range": 85,
                    "factor": 1.0,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 1
                },
                {
                    "id": 9,
                    "name": "KABIN NEM",
                    "min_range": 0,
                    "max_range": 100,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 3

                },
                {
                    "id": 10,
                    "name": "DEBIGUN",
                    "min_range": 0,
                    "max_range": 14,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 'None'
                },
                {
                    "id": 11,
                    "name": 'null',
                    "min_range": 0,
                    "max_range": 0,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 4
                },
                {
                    "id": 12,
                    "name": "null",
                    "min_range": 0,
                    "max_range": 0,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 5
                },
                {
                    "id": 13,
                    "name": "null",
                    "min_range": 0,
                    "max_range": 0,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 6
                },
                {
                    "id": 14,
                    "name": "null",
                    "min_range": 0,
                    "max_range": 0,
                    "factor": 1,
                    "signal_min": 4,
                    "signal_max": 20,
                    "channel_row": 7
                }
            ]
        }

        return jsonify(channels_range=channel_ranges)

    else:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


if __name__ == '__main__':
    app.run(debug=True)
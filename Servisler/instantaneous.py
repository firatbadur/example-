
def instant(realtime_ascii,realtime_modbus):
    realtime_ascii_analog = realtime_ascii[1]

    """
    a = [[2, [7.919, 5.756, 4.591, 11.293, 7.408, 3.702, 1.942, 0.984], '2020-09-01T17:18:01', 1, 'Analog']]
    b = [[0, 5.908, 1, '2020-09-01T17:18:01'], [1, 1625.593, 1, '2020-09-01T17:18:01'],
         [2, 4.678, 1, '2020-09-01T17:18:01'], [4, 24.1, 1, '2020-09-01T17:18:02'],
         [6, 51.648, 1, '2020-09-01T17:18:02'], [7, 21.31, 1, '2020-09-01T17:18:02']]
    """

    instantaneous = [
        {
            "datetime": realtime_modbus[0][3],
            "channelId": realtime_modbus[0][0],
            "value": realtime_modbus[0][1],
            "status": realtime_modbus[0][2]
        },
        {
            "datetime": realtime_modbus[1][3],
            "channelId": realtime_modbus[1][0],
            "value": realtime_modbus[1][1],
            "status": realtime_modbus[1][2]
        },
        {
            "datetime": realtime_modbus[2][3],
            "channelId": realtime_modbus[2][0],
            "value": realtime_modbus[2][1],
            "status": realtime_modbus[2][2]
        },
        {
            "datetime": realtime_ascii_analog[0][2],
            "channelId": 3,
            "value": realtime_ascii_analog[0][1][0],
            "status": realtime_ascii_analog[0][3]
        },
        {
            "datetime": realtime_modbus[3][3],
            "channelId": realtime_modbus[3][0],
            "value": realtime_modbus[3][1],
            "status": realtime_modbus[3][2]
        },
        {
            "datetime": realtime_ascii_analog[0][2],
            "channelId": 5,
            "value": realtime_ascii_analog[0][1][1],
            "status": realtime_ascii_analog[0][3]
        },
        {
            "datetime": realtime_modbus[4][3],
            "channelId": realtime_modbus[4][0],
            "value": realtime_modbus[4][1],
            "status": realtime_modbus[4][2]
        },
        {
            "datetime": realtime_modbus[5][3],
            "channelId": realtime_modbus[5][0],
            "value": realtime_modbus[5][1],
            "status": realtime_modbus[5][2]
        },
        {
            "datetime": realtime_ascii_analog[0][2],
            "channelId": 8,
            "value": realtime_ascii_analog[0][1][2],
            "status": realtime_ascii_analog[0][3]
        },
        {
            "datetime": realtime_ascii_analog[0][2],
            "channelId": 9,
            "value": realtime_ascii_analog[0][1][3],
            "status": realtime_ascii_analog[0][3]
        },
        {
            "datetime": realtime_ascii_analog[0][2],
            "channelId": 10,
            "value": realtime_ascii_analog[0][1][0] * 24,
            "status": realtime_ascii_analog[0][3]
        }
    ]

    return instantaneous


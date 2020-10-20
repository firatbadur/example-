from datetime import *

a= "2020-09-08T21:05:00"

first_time = datetime.strptime(a, '%Y-%m-%dT%H:%M:%S')

print(first_time)

a = {"data": [{"data": [{"channelId": 0, "status": 1, "value": 9.273}, {"channelId": 1, "status": 1, "value": 2270.06},
                        {"channelId": 2, "status": 1, "value": 0.443}, {"channelId": 4, "status": 1, "value": 26.4},
                        {"channelId": 6, "status": 4, "value": 1.8}, {"channelId": 7, "status": 1, "value": 8.603},
                        {"channelId": null, "status": null, "value": null},
                        {"channelId": null, "status": null, "value": null},
                        {"channelId": 3, "status": 1, "value": 71.78}, {"channelId": 8, "status": 1, "value": -64.75},
                        {"channelId": 9, "status": 1, "value": 15.92}, {"channelId": 5, "status": 1, "value": -0.4}],
               "datetime": "Tue, 08 Sep 2020 21:05:00 GMT"}, {"data": [{"channelId": 0, "status": 1, "value": 9.268},
                                                                       {"channelId": 1, "status": 1, "value": 2287.75},
                                                                       {"channelId": 2, "status": 1, "value": 0.62},
                                                                       {"channelId": 4, "status": 1, "value": 26.4},
                                                                       {"channelId": 6, "status": 4, "value": 1.8},
                                                                       {"channelId": 7, "status": 1, "value": 8.603},
                                                                       {"channelId": null, "status": null,
                                                                        "value": null},
                                                                       {"channelId": null, "status": null,
                                                                        "value": null},
                                                                       {"channelId": 3, "status": 1, "value": 71.19},
                                                                       {"channelId": 8, "status": 1, "value": -64.8},
                                                                       {"channelId": 9, "status": 1, "value": 12.47},
                                                                       {"channelId": 5, "status": 1, "value": -0.4}],
                                                              "datetime": "Tue, 08 Sep 2020 21:06:00 GMT"}],
     "siteID": 1}





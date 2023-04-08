from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
#import requests
from json import dumps
import json
import requests
import base.config as cfg
import math
# Create your views here.

async def restconf(api):
    url = "http://" + cfg.SFLOW_IP + ":" + cfg.SFLOW_PORT + api
    rest = requests.get(url)
    if(rest.status_code == 200):
        return rest
    else:
        print("Error Sflow API")
#[
# { 
#     ip: ,
#     of_dpid: ,
#     of_port: ,
#     ifinutilization: ,
#     ifoututilization: ,
#     ifinoctets: ,
#     ifoutoctets: ,
#     ifspeed: 
# }, ...
#]
metrics = []
def get_metrics():
    metric_keys ="of_dpid,of_port,ifinutilization,ifoututilization,ifinoctets,ifoutoctets,ifspeed"
    metricresponse = restconf("/table/ALL/" + metric_keys + "/json")
    for i in metricresponse.json():
        temp = {}
        temp['ip'] = metricresponse.json()[i][0].agent
        for j in metricresponse.json()[i]:
            if(math.isnan( metricresponse.json()[i][j].metricValue)):
                temp[metricresponse.json()[i][j].metricName] = metricresponse.json()[i][j].metricValue
            else:
                temp[metricresponse.json()[i][j].metricName] = int(metricresponse.json()[i][j].metricValue)
        if (temp.ifinoctets > 1000) or (temp.ifoutoctets > 1000):
            metrics.append(temp)
    return metrics
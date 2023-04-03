import json
import requests
from config import ONOS_Ip,ONOS_PORT, ONOS_USER, ONOS_Password

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# ------------------- Meter Structure -------------------
# {
#   "deviceId": "of:0000000000000001",
#   "unit": "KB_PER_SEC",
#   "burst": true,
#   "bands": [
#     {
#       "type": "REMARK",
#       "rate": "0",
#       "burstSize": "0",
#       "prec": "0"
#     }
#   ]
# }

# return a meter json
def make_meter(deviceID, burst, bands):
    meter = {}
    meter["deviceId"] = deviceID
    meter["unit"] = "KB_PER_SEC"
    meter["burst"] = burst
    meter["bands"] = bands
    return meter

# add meter to a device
def add_meter(deviceID, meter):
    # post meter to ONOS
    req = requests.post("http://"+ ONOS_Ip + ":"+ ONOS_PORT+"/onos/v1/meters/"+ deviceID, auth =(ONOS_USER, ONOS_Password), data=meter)
    if(req.status_code == 201):
        print(meter + " : Meter created in device " + deviceID)
    else:
        print(meter + " : Meter not created in device " + deviceID)

# delete meter from a device
def delete_meter(deviceID, meterID):
    # delete meter from ONOS
    req = requests.delete("http://"+ ONOS_Ip + ":"+ ONOS_PORT+"/onos/v1/meters/"+ deviceID + "/" + meterID, auth =(ONOS_USER, ONOS_Password))
    if(req.status_code == 204):
        print(meterID + " : Meter deleted from device " + deviceID)
    else:
        print(meterID + " : Meter not deleted from device " + deviceID)

# get all meters from a device
def get_meters(deviceID):
    req = requests.get("http://"+ ONOS_Ip + ":"+ ONOS_PORT+"/onos/v1/meters/"+ deviceID, auth =(ONOS_USER,ONOS_Password))
    if(req.status_code == 200):
        print("Meters found in device : " + deviceID)
        DataMeters = req.json()
        return DataMeters
    else:
        print("Meters not found in device : " + deviceID)

# get a meter from a device by meterID
def get_meter(deviceID, meterID):
    # meterID Must converted to number
    # --- TODO: check if meterID is number ---
    req = requests.get("http://"+ ONOS_Ip + ":"+ ONOS_PORT+"/onos/v1/meters/"+ deviceID + "/" + meterID, auth =(ONOS_USER,ONOS_Password))
    if(req.status_code == 200):
        print("Meter found in device : " + deviceID)
        DataMeter = req.json()
        return DataMeter
    else:
        print("Meter not found in device : " + deviceID)

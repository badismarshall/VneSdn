import json
from config import ONOS_USER, ONOS_Password, ONOS_PORT, ONOS_Ip
import requests
# ------------------- Flow Structure -------------------
# flow = 
        # {
        #   "priority": 40000,
        #   "timeout": 0,
        #   "isPermanent": true,
        #   "deviceId": "of:0000000000000001",
        #   "treatment": {
        #     "instructions": [
        #       {
        #         "type": "OUTPUT",
        #         "port": "CONTROLLER"
        #       }
        #     ]
        #   },
        #   "selector": {
        #     "criteria": [
        #       {
        #         "type": "ETH_TYPE",
        #         "ethType": "0x88cc"
        #       }
        #     ]
        #   }
        # }

# create flow structure (flow json)
def make_flow(id, deviceID, priority, timeout, isPermanent, treatment, selector):
    flow = {}
    flow["id"] = id
    flow["priority"] = priority
    flow["timeout"] = timeout
    flow["isPermanent"] = isPermanent
    flow["deviceId"] = deviceID
    flow["treatment"] = treatment # put {"instructions": [{"type": "OUTPUT", "port": "CONTROLLER"}]} in treatment
    flow["selector"] = selector
    return flow

# add flow to device
def create_flow(deviceID, flow, appID):
        flow = requests.post("http://"+ ONOS_Ip + ":"+ ONOS_PORT +"/onos/v1/flows/"+ deviceID + "?" + "appID=" + appID, auth =(ONOS_USER, ONOS_Password), data=flow)
        if(flow.status_code == 201):
            print("Flow created")
        else:
            print("Flow not created")

# delete flow from device
def delete_flow(deviceID, flowID):
        flow = requests.delete("http://"+ ONOS_Ip + ":"+ ONOS_PORT +"/onos/v1/flows/"+ deviceID + "/" + flowID, auth =(ONOS_USER, ONOS_Password))
        if(flow.status_code == 204):
            print("Flow deleted")
        else:
            print("Flow not deleted from device : " + deviceID + " with flowID : " + flowID)

# get all flows in device
def get_flows(deviceID):
        flows = requests.get("http://"+  + ":" + ONOS_PORT +"/onos/v1/flows/"+ deviceID, auth =('onos','rocks'))
        if(flows.status_code == 200):
            DataFlows = flows.json()
            return DataFlows
        else:
            print("Flows not found In Device : " + deviceID)

# get flow by flowID
def get_flow(deviceID, flowID):
     flow = requests.get("http://"+ ONOS_Ip + ":"+ ONOS_PORT +"/onos/v1/flows/"+ deviceID + "/" + flowID, auth =(ONOS_USER, ONOS_Password))
     if(flow.status_code == 200):
         DataFlow = flow.json()
         return DataFlow
     else:
        print("Flow not found In Device : " + deviceID + " with flowID : " + flowID)


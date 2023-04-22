import json
# from config import ONOS_USER, ONOS_Password, ONOS_PORT, ONOS_Ip
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

# # create flow structure (flow json)
# def make_flow(id, deviceID, priority, timeout, isPermanent, treatment, selector):
#     flow = {}
#     flow["id"] = id
#     flow["priority"] = priority
#     flow["timeout"] = timeout
#     flow["isPermanent"] = isPermanent
#     flow["deviceId"] = deviceID
#     flow["treatment"] = treatment # put {"instructions": [{"type": "OUTPUT", "port": "CONTROLLER"}]} in treatment
#     flow["selector"] = selector
#     return flow

# # add flow to device
# def create_flow(deviceID, flow, appID):
#         flow = requests.post("http://"+ ONOS_Ip + ":"+ ONOS_PORT +"/onos/v1/flows/"+ deviceID + "?" + "appID=" + appID, auth =(ONOS_USER, ONOS_Password), data=flow)
#         if(flow.status_code == 201):
#             print("Flow created")
#         else:
#             print("Flow not created")

# # delete flow from device
# def delete_flow(deviceID, flowID):
#         flow = requests.delete("http://"+ ONOS_Ip + ":"+ ONOS_PORT +"/onos/v1/flows/"+ deviceID + "/" + flowID, auth =(ONOS_USER, ONOS_Password))
#         if(flow.status_code == 204):
#             print("Flow deleted")
#         else:
#             print("Flow not deleted from device : " + deviceID + " with flowID : " + flowID)

# # get all flows in device
# def get_flows(deviceID):
#         flows = requests.get("http://"+  + ":" + ONOS_PORT +"/onos/v1/flows/"+ deviceID, auth =('onos','rocks'))
#         if(flows.status_code == 200):
#             DataFlows = flows.json()
#             return DataFlows
#         else:
#             print("Flows not found In Device : " + deviceID)

# # get flow by flowID
# def get_flow(deviceID, flowID):
#      flow = requests.get("http://"+ ONOS_Ip + ":"+ ONOS_PORT +"/onos/v1/flows/"+ deviceID + "/" + flowID, auth =(ONOS_USER, ONOS_Password))
#      if(flow.status_code == 200):
#          DataFlow = flow.json()
#          return DataFlow
#      else:
#         print("Flow not found In Device : " + deviceID + " with flowID : " + flowID)

def install_flow_rule(IpAddress,ip_network, device_id,VN_ID,meter_id):
    # Define the flow rule data
    flow = {
        "flowId" : "4",
        "priority": 455,
        "timeout": 100,
        "appId": VN_ID,
        "isPermanent": "true",
        "deviceId": f"{device_id}",
        "selector": {
            "criteria": [
               {
                  "type": "ETH_TYPE",
                   "ethType": "0x0800"
                  },
                {
                    "type": "IPV4_SRC",
                    "ip": f"{ip_network}"
 
                },
                {
                    "type": "IPV4_DST",
                    "ip": f"{ip_network}"
 
                }
                
            ]
        },
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": "FLOOD"
                },
               
                {
                    "type": "METER",
                    "meterId": meter_id
                }
            ]
        },
       
        
    }
    appID=1
    flow = requests.post("http://"+ IpAddress + ":8181/onos/v1/flows/"+ device_id + "?" + "appID=" + f"{VN_ID}", auth =('karaf','karaf'), data=json.dumps(flow))
    if(flow.status_code == 201):
        print(f"Flow of the device mapping created in {device_id}")
    else:
        print("Flow not created")
    
def install_flow_rule_forward(IpAddress,ip_network,device_id,portIn,portOut,VN_ID,meter_id) :

    flow = {
        "flowId" : "4",
        "priority": 455,
        "timeout": 100,
        "appId": VN_ID,
        "isPermanent": "true",
        "deviceId": f"{device_id}",
        "selector": {
            "criteria": [
               {
                  "type": "ETH_TYPE",
                   "ethType": "0x0800"
                  },
                {
                 "type":"IN_PORT",
                 "port":f"{portIn}"
                },
                {
                    "type": "IPV4_SRC",
                    "ip": f"{ip_network}"
 
                },
                {
                    "type": "IPV4_DST",
                    "ip": f"{ip_network}"
 
                }
            ]
        },
        "treatment": {
            "instructions": [
                
                
                {
                    "type": "OUTPUT",
                    "port": f"{portOut}"
                }, 
                {
                    "type": "METER",
                    "meterId": meter_id
                },
                

            ]
        },
       
        
    }

    flow = requests.post("http://"+ IpAddress + ":8181/onos/v1/flows/"+ device_id + "?" + "appID=" + f"{VN_ID}", auth =('karaf','karaf'), data=json.dumps(flow))
    if(flow.status_code == 201):
        print(f"Flow of the bridge created in {device_id}")
    else:
        print("Flow not created")






def flow_for_isolating (IpAddress,ip_network, device_id, VN_ID):
    # Define the flow rule data 
    flow ={
   
   "flowId" : "5",
   "tableId":"0",
   "groupId":0,
   "priority":450,
   "timeout":100,
   "appId": VN_ID,
   "isPermanent": "true",
   "deviceId": f"{device_id}",
   "state":"ADDED",
   "life":0,
   "packets":0,
   "bytes":0,
   "liveType":"UNKNOWN",
   "lastSeen":0,
   "selector":{
      "criteria":[
        {
        "type": "ETH_TYPE",
        "ethType": "0x0800"
       },
       {
                    "type": "IPV4_DST",
                    "ip": f"{ip_network}"
 
                },
                {
                    "type": "IPV4_SRC",
                    "ip": f"{ip_network}"
 
                }
      ]
   },
   "treatment":{
      "instructions":[
      ]
   }
}
    
    flow = requests.post("http://"+ IpAddress + ":8181/onos/v1/flows/"+ device_id + "?" + "appID=" + f"{VN_ID}", auth =('karaf','karaf'), data=json.dumps(flow))
    if(flow.status_code == 201):
        print(f"Flow of isolation created in {device_id}")
    else:
        print("Flow of isolation not created")       

def delete_VN(IpAddress, VN_ID):
    
              flow = requests.delete("http://"+ IpAddress + ":8181/onos/v1/flows/application/" + f"{VN_ID}", auth =('karaf','karaf'))
              if(flow.status_code == 204):
                 print("VN deleted")
              else:
                   print("VN not deleted")

def create_meter(IpAddress,device_id,rate):
    rate = rate * 1000
    meter={
      "deviceId": f"{device_id}",
      "unit": "KB_PER_SEC",
      "burst": "true",
      "bands":[
             {
              "type": "DROP",
              "rate": rate,
              "burstSize": "100",
              "prec": "0"
             },
        ]
} 
     
    response = requests.post("http://"+ IpAddress + ":8181/onos/v1/meters/"+ device_id , auth =('karaf','karaf'), data=json.dumps(meter))
    if(response.status_code == 201):
        #print(f"meter  created in {device_id}")
        print(rate)
        print(response.headers.get('Location'))
        meter_id = response.headers.get('Location').split('/')[-1] # Convertir la réponse en format JSON
        #print(meter_id)
        return meter_id
    else:
        print("meter not created") 
     
   
 
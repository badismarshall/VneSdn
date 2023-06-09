from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import requests
from json import dumps
import json
from base.models import *
# # Create your views here.
# Récuperer l'addres ip du controller
IpAddress = "localhost"


# get La topologie de réseau // pour le moment on a que un seul cluster
topologies = requests.get("http://"+ IpAddress + ":8181/onos/v1/topology/clusters/0/links", auth =('onos','rocks'))
if(topologies.status_code == 200):
    DataTopo = topologies.json() # met dans un fichier json
    links = []
    for link in DataTopo['links']:
        links.append({"source": link ["src"]["device"] , "target": link["dst"]["device"] })
else:
    print("Topologies not found")




# get Devices
devices = requests.get("http://"+ IpAddress + ":8181/onos/v1/devices", auth =('onos','rocks'))
if(devices.status_code == 200):
    DataDevices = devices.json()
    # Récuperer les id des devices (switch)
    DevicesIDs = {} # liste des DevicesID
    DevicesIDs['devices'] = []
    for device in DataDevices['devices']:
        # DevicesIDs['devices'].append(device['id'])
        DevicesIDs['devices'].append({"id":device['id'], "chid": device['chassisId']})
else:
    print("Devices not found")



# Récuperer les id des Hosts
hosts_get = requests.get("http://"+ IpAddress + ":8181/onos/v1/hosts", auth =('onos','rocks'))
if(hosts_get.status_code == 200):
    DataHosts = hosts_get.json()
    Hosts = []
    for host in DataHosts['hosts']:
        Hosts.append({"hostID": host['id'], "DeviceID" : host['locations'][0]["elementId"]})
else:
    print("Hosts not found")



# ------------------- Flows ------------------- #
# get flows by device
def get_flows(deviceID):
        flows = requests.get("http://"+ IpAddress + ":8181/onos/v1/flows/"+ deviceID, auth =('onos','rocks'))
        if(flows.status_code == 200):
            DataFlows = flows.json()
            return DataFlows
        else:
            print("Flows not found")


# appId = Bakend
# flow = json
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

# create flow by device
def create_flow(deviceID, flow, appID):
        flow = requests.post("http://"+ IpAddress + ":8181/onos/v1/flows/"+ deviceID + "?" + "appID=" + appID, auth =('onos','rocks'), data=flow)
        if(flow.status_code == 201):
            print("Flow created")
        else:
            print("Flow not created")


# delete flow by device
def delete_flow(deviceID, flowID):
        flow = requests.delete("http://"+ IpAddress + ":8181/onos/v1/flows/"+ deviceID + "/" + flowID, auth =('onos','rocks'))
        if(flow.status_code == 204):
            print("Flow deleted")
        else:
            print("Flow not deleted")
            
def addDeviceTODB(device):
    Device = {
        "id": int(device['chassisId']),
        "name": device['id'],
        "capacity": 7,
    }
    substrate_device = SubstrateNode.objects.create(**Device)
    substrate_device.save()

def addlinkTODB(link):
    sourceNode = SubstrateNode.objects.get(name=link['src']['device'])
    targetNode = SubstrateNode.objects.get(name=link['dst']['device'])
    link = {
        'name': f'{link["src"]["device"]}-{link["dst"]["device"]}',
        "source_substrate_node": sourceNode,
        "target_substrate_node": targetNode,
        "bandwidth": 100,
    }
    substrate_link = SubstrateLink.objects.create(**link)
    substrate_link.save()

# for device in DataDevices['devices']:
#     addDeviceTODB(device)

# for link in DataTopo['links']:
#     addlinkTODB(link)

print(DevicesIDs)
# virtual_networks = VirtualNetwork.objects.get(name="VN1")
# virtual_nodes = LogicalNode.objects.filter(virtual_network=virtual_networks)
# logical_links = LogicalLink.objects.get(name="LL1VN1")
# substrate_links = Mapping.objects.filter(logical_link=logical_links)
# for link in substrate_links:
#     print(link.substrate_link.name)
# print(substrate_links)

# print(virtual_nodes)

def home(request):
    return render(request, 'home.html')

# def room(request):
#     return render(request, 'room.html',{'DeviceID': DevicesIDs, 'links':links, 'hosts': Hosts})


def main(request):
    return render(request, 'main.html')
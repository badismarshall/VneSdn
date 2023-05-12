import requests
from django.http import JsonResponse
from base.models import SubstrateNode, SubstrateLink, VirtualNetwork, LogicalNode, LogicalLink, Mapping
from .serializers import SubstrateNodeSerializer, SubstrateLinkSerializer, VirtualNetworkSerializer, LogicalNodeSerializer, LogicalLinkSerializer, MappingSerializer
from base.mapper import *
from django.views.decorators.csrf import csrf_exempt
import json
from base.flow_manipulate import delete_VN
from base.views import DevicesIDs
from django.contrib.auth import authenticate, login, logout



# make login 
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({'status': 'success'}, safe=True)
    else:
        return JsonResponse({'status': 'failed'}, safe=True)
    print("login")


def getTopologie(request):
    # get La topologie de réseau // pour le moment on a que un seul cluster
    topologies = requests.get("http://"+ "localhost" + ":8181/onos/v1/topology/clusters/0/links", auth =('onos','rocks'))
    if(topologies.status_code == 200):
        DataTopo = topologies.json() # met dans un objet json
    else:
        print("Topologies not found")

    links = []
    for link in DataTopo['links']:
        links.append({"source": link ["src"]["device"] , "target": link["dst"]["device"], "port": link["src"]["port"] }) # on récupère les liens entre les devices et le port de source

    return JsonResponse({'links':links}, safe=True)

def getDevices(request):
    # get Devices
    devices = requests.get("http://"+ "localhost" + ":8181/onos/v1/devices", auth =('onos','rocks'))
    if(devices.status_code == 200):
        DataDevices = devices.json()
    else:
        print("Devices not found")

    # Récuperer les id des devices (switch)
    DevicesIDs = {} # liste des DevicesID
    DevicesIDs['devices'] = []
    for device in DataDevices['devices']:
        DevicesIDs['devices'].append({"id":device['id'], "chid": device['chassisId']})
    # 

    return JsonResponse(DevicesIDs, safe=True)

@csrf_exempt
def postVn(request):
    data = json.loads(request.body)
    print(data)
    devices = data['devices']
    links = data['links']
    name = data['name']

    # check if devices and links are not empty
    if(devices == None or links == None or name == None):
        print("devices or links are empty")
        return 
    else:
        print(type(devices))
        print(type(links))
        G1 = virtual_network(devices, links)
        G = createGraph()
        ph = getphysicalDevices()
        if(mapper(G, G1, ph, 'localhost','192.168.1.0/24', name, name)):
            print("mapping done")
            return JsonResponse({"Vn": "true"}, safe=False)
            # create a new virtual network
            # Vn ={
            #     "name": data['name'],
            # }
            # virtualNetwork = VirtualNetwork.objects.create()
            # create logical nodes

            # TODO: check if the virtual network can be mapped if it is so insert it in the database
            # TODO: if the virtual network can't be mapped return an Notification (requestNot added) to the user (FrontEnd)
        return JsonResponse({"Vn": "false"}, safe=False)

def deleteVn(request, id):
    print(id)
    # delete a virtual network from the database
    virtualNetwork = VirtualNetwork.objects.get(id=id)
    # get virtual network name
    name = virtualNetwork.name
    delete_VN("localhost",name)
    virtualNetwork.delete()
    return JsonResponse({"message": "Virtual Network deleted"}, safe=False)

def getVn(request, id):
    # get a virtual network from the database
    virtualNetwork = VirtualNetwork.objects.get(id=id)
    LogicalLinks = LogicalLink.objects.filter( virtual_network=virtualNetwork)
    LogicalNodes = LogicalNode.objects.filter( virtual_network=virtualNetwork)
    serializerLink = LogicalLinkSerializer(LogicalLinks, many=True)
    serializerNode = LogicalNodeSerializer(LogicalNodes, many=True)
    return JsonResponse({"logicalnodes":serializerNode.data, "logicallinks":serializerLink.data}, safe=False)

def getSubstrateLinksbyid(request, id):
    # get a substrate link from the database
    substrateLink = SubstrateLink.objects.get(id=id)
    serializer = SubstrateLinkSerializer(substrateLink, many=False)
    return JsonResponse({"substratelinks":serializer.data}, safe=False)
def getSubstrateLinksbyname(request, name):
    # get a substrate link from the database
    substrateLink = SubstrateLink.objects.get(name=name)
    serializer = SubstrateLinkSerializer(substrateLink, many=False)
    return JsonResponse({"substratelinks":serializer.data}, safe=False)
def getSubstrateNodesbyid(request, id):
    # get a substrate node from the database
    substrateNode = SubstrateNode.objects.get(id=id)
    serializer = SubstrateNodeSerializer(substrateNode, many=False)
    return JsonResponse({"substratenodes":serializer.data}, safe=False)
def getStatistics(request):
    # get Statistics
    statistics = requests.get("http://"+ "localhost" + ":8181/onos/v1/statistics/delta/ports", auth =('onos','rocks'))
    if(statistics.status_code == 200):
        DataStatistics = statistics.json()
    else:
        print("Statistics not found")
    return JsonResponse(DataStatistics, safe=True)

def getSubstrateNodes(request):
    SubstrateNodes = SubstrateNode.objects.all()
    serializer = SubstrateNodeSerializer(SubstrateNodes, many=True)
    return JsonResponse({"substratenodes":serializer.data}, safe=False)

def getSubstrateLinks(request):
    SubstrateLinks = SubstrateLink.objects.all()
    serializer = SubstrateLinkSerializer(SubstrateLinks, many=True)
    return JsonResponse({"substratelinks":serializer.data}, safe=False)

def getVirtualNetworks(request):
    VirtualNetworks = VirtualNetwork.objects.all()
    # get the number of nodes and links for each virtual network
    # vnnodes = {}
    # vnlinks = {}
    # for vn in VirtualNetworks:
    #     vn.numberofnodes = LogicalNode.objects.filter(virtual_network=vn).count()
    #     vn.numberoflinks = LogicalLink.objects.filter(virtual_network=vn).count()
    serializer = VirtualNetworkSerializer(VirtualNetworks, many=True)
    return JsonResponse({"virtualnetworks":serializer.data}, safe=False)

def getLogicalNodes(request):
    LogicalNodes = LogicalNode.objects.all()
    serializer = LogicalNodeSerializer(LogicalNodes, many=True)
    return JsonResponse({"logicalnodes":serializer.data}, safe=False)
def getLogicalLinks(request):
    LogicalLinks = LogicalLink.objects.all()
    serializer = LogicalLinkSerializer(LogicalLinks, many=True)
    return JsonResponse({"logicallinks":serializer.data}, safe=False)

def getMappings(request):
    Mappings = Mapping.objects.all()
    serializer = MappingSerializer(Mappings, many=True)
    return JsonResponse({"mappings":serializer.data}, safe=False)

def getFlowNumberofDevices(request):
    response = {}
    response['Nflow'] = []
    for device in DevicesIDs['devices']:   
        data = {"deviceID": device['chid'] , "flownumber": len(requests.get("http://"+ "localhost" + ":8181/onos/v1/flows/"+ device['id'], auth =('onos','rocks')).json()['flows'])}
        response['Nflow'].append(data)
    return JsonResponse(response, safe=False)

def getNumberoflogicalNodesMapped(request):
    response = {}
    response['NlogicalNodes'] = []
    substrate_nodes = SubstrateNode.objects.all()
    for node in substrate_nodes:
        logical_nodes = LogicalNode.objects.filter(substrate_node=node)
        data = {"deviceID": node.id, "logicalnodenumber": len(logical_nodes)}
        response['NlogicalNodes'].append(data)
    return JsonResponse(response, safe=False)
def getNumberoflogicalLinksMapped(request):
    logical_links = LogicalLink.objects.all()
    data = {"logicallinknumber": len(logical_links)}
    return JsonResponse(data, safe=False)

def getMeterNumberofDevices(request):
    response = {}
    response['Nmeters'] = []
    for device in DevicesIDs['devices']:
        data = {"deviceID":device['chid'], "meternumber": len(requests.get("http://"+ "localhost" + ":8181/onos/v1/meters/"+ device['id'], auth =('onos','rocks')).json()['meters'])}
        response['Nmeters'].append(data)
    print(response)
    return JsonResponse(response, safe=False)

def getNetworkInformation(request):
    # get the number of virtual networks in the database
    virtualNetworks = VirtualNetwork.objects.all()
    networkinfo = requests.get("http://localhost:8181/onos/v1/system", auth =('onos','rocks'))
    if(networkinfo.status_code == 200):
        DataNetworkInfo = networkinfo.json()
        DataUtil = {"devices": DataNetworkInfo['devices'], "links": DataNetworkInfo['links'], "hosts": DataNetworkInfo['hosts'],"flows": DataNetworkInfo['flows'], "Vns": len(virtualNetworks)}
        return JsonResponse(DataUtil, safe=True)
    else:
        print("Network information not found")
        return JsonResponse({"message": "Network information not found"}, safe=False)

def getflowsnumberforVn(request):
    virtualNetworks = VirtualNetwork.objects.all()
    response = {}
    response['flowsnumber'] = []
    for virtualNetwork in virtualNetworks:
        flowsvn = requests.get("http://"+ "localhost" + ":8181/onos/v1/flows/application/"+ virtualNetwork.name, auth =('onos','rocks'))
        if(flowsvn.status_code == 200):
            data = {"virtualnetwork": virtualNetwork.name, "flowsnumber": len(flowsvn.json()['flows'])}
            response['flowsnumber'].append(data)
    return JsonResponse(response, safe=False)
def getmetersnumberofvn(request):
    virtualNetworks = VirtualNetwork.objects.all()
    response = {}
    response['metersnumber'] = []
    for virtualNetwork in virtualNetworks:
        metersvn = requests.get("http://"+ "localhost" + ":8181/onos/v1/meters/application/"+ virtualNetwork.name, auth =('onos','rocks'))
        if(metersvn.status_code == 200):
            data = {"virtualnetwork": virtualNetwork.name, "metersnumber": len(metersvn.json()['meters'])}
            response['metersnumber'].append(data)
    return JsonResponse(response, safe=False)
# Path: base\models.py
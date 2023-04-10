import requests
from django.http import JsonResponse
from base.models import SubstrateNode, SubstrateLink, VirtualNetwork, LogicalNode, LogicalLink, Mapping
from .serializers import SubstrateNodeSerializer, SubstrateLinkSerializer, VirtualNetworkSerializer, LogicalNodeSerializer, LogicalLinkSerializer, MappingSerializer
from base.mapper import *
from django.views.decorators.csrf import csrf_exempt
import json

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
        DevicesIDs['devices'].append(device['id'])

    return JsonResponse(DevicesIDs, safe=True)

@csrf_exempt
def postVn(request):
    data = json.loads(request.body)
    print(data)
    devices = data['devices']
    links = data['links']

    # check if devices and links are not empty
    if(devices == None or links == None):
        print("devices or links are empty")
        return 
    else:
        print(type(devices))
        print(type(links))
        G1 = virtual_network(devices, links)
        G = createGraph()
        ph=getphysicalDevices()
        if(mapper(G, G1,ph,'localhost','192.168.1.0/24',1)):
            print("mapping done")

    # create a new virtual network
    # TODO: check if the virtual network can be mapped if it is so insert it in the database
    # TODO: if the virtual network can't be mapped return an Notification (requestNot added) to the user (FrontEnd)

def deleteVn(request, id):
    print(id)
    # delete a virtual network from the database
    virtualNetwork = VirtualNetwork.objects.get(id=id)
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

# Path: base\models.py
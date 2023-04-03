import requests
from django.http import JsonResponse
from base.models import SubstrateNode, SubstrateLink, VirtualNetwork, LogicalNode, LogicalLink, Mapping
from .serializers import SubstrateNodeSerializer, SubstrateLinkSerializer, VirtualNetworkSerializer, LogicalNodeSerializer, LogicalLinkSerializer, MappingSerializer

def getTopologie(request):
    # get La topologie de réseau // pour le moment on a que un seul cluster
    topologies = requests.get("http://"+ "localhost" + ":8181/onos/v1/topology/clusters/0/links", auth =('onos','rocks'))
    if(topologies.status_code == 200):
        DataTopo = topologies.json() # met dans un objet json
    else:
        print("Topologies not found")

    links = []
    for link in DataTopo['links']:
        links.append({"source": link ["src"]["device"] , "target": link["dst"]["device"] })

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
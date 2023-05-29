import networkx as nx
import heapq
import requests
from heapq import heappop, heappush
from itertools import count
from base.flow_manipulate import *
from base.models import *
from base.models import SubstrateLink
from api.serializers import SubstrateLinkSerializer


def virtual_network(devices, links):
    G = nx.Graph()
    for deviceId, deviceData in devices.items():    
        # print(deviceId, deviceData['NodeCapacity'])
        G.add_node(deviceId, name=deviceData['name'], weight=deviceData['NodeCapacity'],weight2=1)
    for linkId, linkdata in links.items():
        G.add_edge(linkdata['source'], linkdata['target'], weight=linkdata['LinkCapacity'])
        G.add_edge(linkdata['target'], linkdata['source'], weight=linkdata['LinkCapacity'])
    # print(G.nodes.data())
    # print(G.edges.data())
    return G

def k_shortest_paths(G, source, target, k):
    paths = []
    queue = []
    heapq.heappush(queue, (0, [source]))
    while len(paths) < k and queue:
        (cost, path) = heapq.heappop(queue)
        node = path[-1]
        if node == target:
            paths.append(path)
        else:
            for neighbor, weight in G[node].items():
                if neighbor not in path:
                    heapq.heappush(queue, (cost + weight['weight'], path + [neighbor]))
    return paths

def getphysicalDevices():
    devices = requests.get("http://"+ "localhost" + ":8181/onos/v1/devices", auth =('onos','rocks'))
    if(devices.status_code == 200):
        DataDevices = devices.json()
    return DataDevices

def getphysicallinks():
    topologies = requests.get("http://"+ "localhost" + ":8181/onos/v1/topology/clusters/0/links", auth =('onos','rocks'))
    if(topologies.status_code == 200):
        DataTopo = topologies.json()
    return DataTopo
# pysical graph
def createGraph():
    G = nx.Graph()
    physicalDevices = getphysicalDevices()
    physicallinks = getphysicallinks()
    for device in physicalDevices['devices']:
        G.add_node(device['id'], weight=7,weight2=1)
    
    for link in physicallinks['links']:
        # get the capacity of the link from the database (TODO)
        # get the link by name from the database
        linksub = SubstrateLink.objects.get(name=link['src']['device'] +'-'+ link['dst']['device'])
        serializer = SubstrateLinkSerializer(linksub)
        ###
        G.add_edge(link['src']['device'], link['dst']['device'], weight=serializer.data['bandwidth'], src_port=link['src']['port'], dst_port=link['dst']['port'])
        G.add_edge(link['dst']['device'], link['src']['device'], weight=serializer.data['bandwidth'], src_port=link['dst']['port'], dst_port=link['src']['port'])

    return G

def getpath(path_list, source, target, virtuel_nodes, physical_nodes):
    for node in virtuel_nodes:
        if node == source:
            source = physical_nodes[virtuel_nodes.index(node)]
            print(source)
        else :
            if node == target:
                target = physical_nodes[virtuel_nodes.index(node)]
                print(target)    
    print(type(path_list[0][1]))
    for i in range(len(path_list)):
        if path_list[i][0] == source and path_list[i][len(path_list[i])-1] == target:
            print("am here")
            return path_list[i]

def mapper(G,G1,DataDevices,IpAddress,ip_networkk,VN_ID, name):
    ip_network = '192.168.' + str(ip_networkk) + '.0/24'

    # calcule availabitily of node

    for node in G.nodes():
       edges = G.edges(node, data=True)
       weight = 0
       for u, v, data in edges:
         weight = weight + data.get('weight')
         
         
        
       G.nodes[node]['weight2'] = G.nodes[node]['weight'] * weight  


    
    # sort the nodes b the availabilty 
    weights=nx.get_node_attributes(G, 'weight2')
    sorted_nodes = sorted(weights, key=weights.get, reverse=True)    
    #for node in sorted_nodes:
      # print(f"Node {node} has weight {weights[node]}.")

    # calcule the need in the VN
    for node in G1.nodes():
        edges = G1.edges(node, data=True)
        weight=0
        for u, v, data in edges:
            weight = weight + data.get('weight')
            
        G1.nodes[node]['weight2'] = G1.nodes[node]['weight'] * weight   



    weights1=nx.get_node_attributes(G1, 'weight2')
    virtualNodes = sorted(weights1, key=weights1.get, reverse=True)    
    #for node in virtualNodes:
       #print(f"Node {node} has weight {weights1[node]}.")  

   
    #print(len(virtualNodes))
    #print(len(sorted_nodes))
    paths_list=[]
    weight_list=[]

    networkmapp=True
    for i in range (len(virtualNodes)-1):
       #print(f"the node {virtualNodes[i]}")
       for j in range (i,len(virtualNodes)):
            if(i != j):
           
                if G1.has_edge(virtualNodes[i],virtualNodes[j] ):
                      #print(f"there is an edges between {virtualNodes[i]}{virtualNodes[j]}")
                      n=False
                      h=1
                      while (not n  and h < 3 ):
                          #print(f"the path between {virtualNodes[i]}  {virtualNodes[j]} {k_shortest_paths(G,sorted_nodes[i], sorted_nodes[j], 1)}")
                          paths=k_shortest_paths(G,sorted_nodes[i], sorted_nodes[j], h) 
                          #verifier jusqu a arriver a un path qui peut mapper le virtuel path 
                          k=0
                          mapper =False
                          while(k<h and not mapper):
                      
                             path=paths[k]
                             #calcule de le lien min de path    
                             min_weight =G.get_edge_data(path[0], path[1])['weight']
                             for l in range(len(path)-1):
                                edge_data = G.get_edge_data(path[l], path[l+1])
                                weight = edge_data['weight']    
                                if weight < min_weight:
                                    min_weight = weight
                             # verifier si le path peut mapper le lien virtuel 
                             edge_data=G1.get_edge_data(virtualNodes[i] , virtualNodes[j])
                             if edge_data is not None:
                                link_weight = edge_data['weight']               
                                if min_weight < link_weight :
                                    k = k +1 

                                else: 
                                    mapper = True 
                      
                          if(mapper == False ):
                             
                                 h=h+1
                          else : 
                              n =True

                      if n :
                           
                           
                           print(f"the link between {virtualNodes[i]},{virtualNodes[j]} can be mapped")
                           print(path)
                           paths_list.append(path)
                           weight_list.append(link_weight)

                     
                      else:
                          print(f"can't map the link {virtualNodes[i]},{virtualNodes[j]} ")
                          networkmapp=False
                        # i think break is good

    if(networkmapp ==True):
        print(virtualNodes) # les noeuds virtuekl
        for node in virtualNodes :
             print(G1.nodes[node]['weight'])
        network_data = {
        "device_id": None,
         "weight": None,
         "port_src": None,
         "port_dest": None
        }   
        
        network_data_list = []
        #mise a jours des liens et installation de flux
        for device in DataDevices['devices']:
             flow_for_isolating (IpAddress,ip_network, device['id'],VN_ID)

        n=len(paths_list)
        for i in range (n):
            path=paths_list[i]  
            link_weight=weight_list[i]
            for s in range(len(path)-1):
                u = path[s]
                v = path[s+1]
               

                # revoir le cas au le switch fait juste le forward de paquet ne mappe pas un device
                if(u in sorted_nodes[0:len(virtualNodes)]):
                     
                     if len(network_data_list) == 0:
                         data = {
                                  "device_id": u,
                                  "weight": link_weight,
                                  "port_src": 0,
                                  "port_dest": 0,
                                 }
                         #data=network_data(u,link_weight,0,0)
                         network_data_list.append(data)
                     else :
                        
                         Trouver=False
                         for data in network_data_list:
                            if(data['device_id'] == u ):
                                Trouver=True
                                if(link_weight > data['weight']):
                                    data['weight']=link_weight
                                else : 
                                    link_weight=data['weight']
                                
                            
                         
                         if(Trouver==False) : 
                            data = {
                                  "device_id": u,
                                  "weight": link_weight,
                                  "port_src": 0,
                                  "port_dest": 0,
                                 }
                            #data=network_data(u,link_weight,port_source,port_destination)
                            network_data_list.append(data)
                     meter_id=create_meter(IpAddress,u,link_weight)
                     install_flow_rule(IpAddress,ip_network,u,VN_ID,meter_id)
                     


                else:
                     u = path[s]
                     v = path[s+1]
                     edge_data=G.get_edge_data(u , v)
                     port_source=edge_data['src_port']
                     edge_data2=G.get_edge_data(u ,path[s-1])
                     port_destination =edge_data2['src_port']
                     print(path[s-1])                       
                     print(u)
                     print(path[s+1])
                     
                     print(port_source)
                     print(port_destination)
                    #  print(edge_data2['src_port'])
                    #  print(edge_data2['dst_port'])
                     if len(network_data_list) == 0:
                         data = {
                                  "device_id": u,
                                  "weight": link_weight,
                                  "port_src": port_source,
                                  "port_dest": port_destination,
                                 }
                         #data=network_data(u,link_weight,port_source,port_destination)
                         network_data_list.append(data)
                     else :
                         for data in network_data_list:
                            Trouver=False
                            if(data['device_id'] == u and port_source==data['port_src']  and port_destination == data['port_dest'] ):
                                Trouver=True
                                if(link_weight>data['weight']):
                                    data['weight']=link_weight
                                else : 
                                    link_weight=data['weight']
                                
                         if(Trouver==False) : 
                            data = {
                                  "device_id": u,
                                  "weight": link_weight,
                                  "port_src": port_source,
                                  "port_dest": port_destination,
                                 }
                            #data=network_data(u,link_weight,port_source,port_destination)
                            network_data_list.append(data)

                     meter_id=create_meter(IpAddress,u,link_weight)
                     install_flow_rule_forward(IpAddress,ip_network,u,port_source,port_destination,VN_ID,meter_id)   
                     install_flow_rule_forward(IpAddress,ip_network,u,port_destination,port_source,VN_ID,meter_id)
                    # install_flow_rule(IpAddress,ip_network,u,VN_ID)
                     #install_flow_rule(IpAddress,ip_network,u,VN_ID,meter_id)
                
                G[u][v]['weight'] -=link_weight
                # get the link from database
                linksub = SubstrateLink.objects.get(name = u +'-'+ v)
                linksub.bandwidth -= link_weight
            meter_id=create_meter(IpAddress,v,link_weight)
            install_flow_rule(IpAddress,ip_network,v,VN_ID,meter_id)
        liste_devices=sorted_nodes[0:len(virtualNodes)]
        print("la liste des noeuds ")
        print(liste_devices)
        print(virtualNodes)
        
        Vn = {
            'name': name
        }
        virtual_network = VirtualNetwork.objects.create(**Vn)
        virtual_network.save()
        # get capacity the logical nodes
        for node in virtualNodes:        
             Logicalnode = {
                    'name': node + Vn['name'],
                    'virtual_network': virtual_network,
                    'substrate_node': SubstrateNode.objects.get(name=liste_devices[virtualNodes.index(node)]),
                    'capacity': G1.nodes[node]['weight']
             }
             logical_node = LogicalNode.objects.create(**Logicalnode)
             logical_node.save()
        
        # #  get the logical links
        # print(G1.edges.data())
        for data in G1.edges.data():
            print(data[0])
            print(data[1])
            print(data[2])
            Logicallink = {
                    'name': data[0] + Vn['name'] + "-" + data[1] + Vn['name'],
                    'virtual_network': virtual_network,
                    # 'substrate_link': SubstrateLink.objects.get(name=data[0] + data[1]),
                    'bandwidth': data[2]['weight'],
                    'source_logical_node': LogicalNode.objects.get(name=data[0] + Vn['name']),
                    'target_logical_node': LogicalNode.objects.get(name=data[1] + Vn['name']),
                }
            logical_link = LogicalLink.objects.create(**Logicallink)
            logical_link.save()
            print("path_list")
            print(paths_list)
            path_map = getpath(paths_list, data[0], data[1], virtualNodes, liste_devices) 
            if path_map == None:
                path_map = getpath(paths_list, data[1], data[0], virtualNodes, liste_devices)
            print(path_map)
            for i in range(0, len(path_map) - 1): 
                mapping = {
                    'logical_link': logical_link,
                    'substrate_link': SubstrateLink.objects.get(name=path_map[i] +"-"+ path_map[i + 1]),
                }
                mapping = Mapping.objects.create(**mapping)
                mapping.save()
        print (paths_list)
            
        #la liste des chemins 
        # paths_list[0]
        # return liste_devices,paths_list
       
        return True
    else:
        # print("can't map the network ")
        return False


def delete_VN(IpAddress, VN_ID):
    
              flow = requests.delete("http://"+ IpAddress + ":8181/onos/v1/flows/application/" + f"{VN_ID}", auth =('karaf','karaf'))
              if(flow.status_code == 204):
                 print("VN deleted")
              else:
                   print("VN not deleted")
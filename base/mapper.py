import networkx as nx
import heapq
import requests
from heapq import heappop, heappush
from itertools import count
from base.flow_manipulate import *

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

def createGraph():
    G = nx.Graph()
    physicalDevices = getphysicalDevices()
    physicallinks = getphysicallinks()
    for device in physicalDevices['devices']:
        G.add_node(device['id'], weight=7,weight2=1)
    for link in physicallinks['links']:
        G.add_edge(link['src']['device'], link['dst']['device'], weight=100, src_port=link['src']['port'], dst_port=link['dst']['port'])
    return G

def mapper(G,G1,DataDevices,IpAddress,ip_network,VN_ID ):
    
    # calcule availabitily  of node

    for node in G.nodes():
       edges = G.edges(node, data=True)
       weight=0
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
    sorted_nodes1 = sorted(weights1, key=weights1.get, reverse=True)    
    #for node in sorted_nodes1:
       #print(f"Node {node} has weight {weights1[node]}.")  

   
    #print(len(sorted_nodes1))
    #print(len(sorted_nodes))
    paths_list=[]
    weight_list=[]

    networkmapp=True
    for i in range (len(sorted_nodes1)-1):
       #print(f"the node {sorted_nodes1[i]}")
       for j in range (i,len(sorted_nodes1)):
            if(i != j):
           
                if G1.has_edge(sorted_nodes1[i],sorted_nodes1[j] ):
                      #print(f"there is an edges between {sorted_nodes1[i]}{sorted_nodes1[j]}")
                      n=False
                      h=1
                      while (not n  and h < 3 ):
                          #print(f"the path between {sorted_nodes1[i]}  {sorted_nodes1[j]} {k_shortest_paths(G,sorted_nodes[i], sorted_nodes[j], 1)}")
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
                             edge_data=G1.get_edge_data(sorted_nodes1[i] , sorted_nodes1[j])
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
                           
                           
                           print(f"the link between {sorted_nodes1[i]},{sorted_nodes1[j]} can be mapped")
                           print(path)
                           paths_list.append(path)
                           weight_list.append(link_weight)

                     
                      else:
                          print(f"can't map the link {sorted_nodes1[i]},{sorted_nodes1[j]} ")
                          networkmapp=False

    if(networkmapp ==True):
        #mise a jours des liens et installation de flux
        for device in DataDevices['devices']:
             flow_for_isolating (IpAddress,ip_network, device['id'],VN_ID)
       # for node in G.nodes():
         #    flow_for_isolating (IpAddress,ip_network,node,VN_ID)    
        

        n=len(paths_list)
        for i in range (n):
            path=paths_list[i]  
            link_weight=weight_list[i]
            for s in range(len(path)-1):
                u = path[s]
                v = path[s+1]
                # link["src"]["device"] = u
                # link["dst"]["device"] = v

                # revoir le cas au le switch fait juste le forward de paquet ne mappe pas un device
                if(u in sorted_nodes[0:len(sorted_nodes1)]):
                     install_flow_rule(IpAddress,ip_network,u,VN_ID)
                else:
                     u = path[s]
                     v = path[s+1]
                     edge_data=G.get_edge_data(u , v)
                     port_source=edge_data['src_port']
                     edge_data=G.get_edge_data(u,path[s-1] )
                     port_destination =edge_data['src_port']

                     print(port_destination)
                     print(port_source)
                     install_flow_rule_forward(IpAddress,ip_network,u,port_source,port_destination,VN_ID)   
                     install_flow_rule_forward(IpAddress,ip_network,u,port_destination,port_source,VN_ID)


                G[u][v]['weight'] -=link_weight
            install_flow_rule(IpAddress,ip_network,v,VN_ID)
        liste_devices=sorted_nodes[0:len(sorted_nodes1)]
        return True
        # return liste_devices,paths_list
            
    else:
        print("can't map the network ")
        return False



def delete_VN(IpAddress, VN_ID):
    
              flow = requests.delete("http://"+ IpAddress + ":8181/onos/v1/flows/application/" + f"{VN_ID}", auth =('karaf','karaf'))
              if(flow.status_code == 204):
                 print("VN deleted")
              else:
                   print("VN not deleted")
import networkx as nx
import heapq
from heapq import heappop, heappush
from itertools import count
from base.flow_manipulate import create_flow
from base.flow_manipulate import make_flow

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

def mapper(G,G1): #,IpAddress,ip_mask ):
    
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
    for node in sorted_nodes:
       print(f"Node {node} has weight {weights[node]}.")

    # calcule the need in the VN
    for node in G1.nodes():
        edges = G1.edges(node, data=True)
        weight=0
        for u, v, data in edges:
            weight = weight + data.get('weight')

       
        G1.nodes[node]['weight2'] = G1.nodes[node]['weight'] * weight   



    weights1=nx.get_node_attributes(G1, 'weight2')
    sorted_nodes1 = sorted(weights1, key=weights1.get, reverse=True)    
    for node in sorted_nodes1:
       print(f"Node {node} has weight {weights1[node]}.")  

   
    print(len(sorted_nodes1))
    print(len(sorted_nodes))
    paths_list=[]
    weight_list=[]

    networkmapp=True
    for i in range (len(sorted_nodes1)-1):
       print(f"the node {sorted_nodes1[i]}")
       for j in range (i,len(sorted_nodes1)):
            if(i != j):
           
                if G1.has_edge(sorted_nodes1[i],sorted_nodes1[j] ):
                      print(f"there is an edges between {sorted_nodes1[i]}{sorted_nodes1[j]}")
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
                           
                           
                           print(f"the link {sorted_nodes1[i]},{sorted_nodes1[j]} can be mapp")
                           print(path)
                           paths_list.append(path)
                           weight_list.append(link_weight)

                     
                      else:
                          print(f"can't mappe the link {sorted_nodes1[i]},{sorted_nodes1[j]} ")
                          networkmapp=False

    if(networkmapp ==True):
        #mise a jours des liens et installation de flux
        n=len(paths_list)
        for i in range (n):
            path=paths_list[i]
            link_weight=weight_list[i]
            for s in range(len(path)-1):

                u = path[s]
                v = path[s+1]
                link["src"]["device"] = u
                link["dst"]["device"] = v
                #creé le flux
                '''
                    cette étape que nous devons réfléchir a une méthdode consistante
                    pour l'installation des flux (elle est marqué dans TODOList)
                '''
                create_flow(u)
                # ajouter le flux au noeud src
                create_flow(u, flow, appId)
                # ajouter le flux au noeud dst
                create_flow(v, flow, appId)
                # install_flow_rule(IpAddress,link["dst"]["port"],ip_mask,u)
                # install_flow_rule(IpAddress,link["src"]["port"],ip_mask,v)
                G[u][v]['weight'] -=link_weight

    else:
        print("can't mapp the network ")

def create_flow(deviceID)

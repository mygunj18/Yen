import networkx as nx #for processing network/graph functionality
import pandas as pd #for processing csv

def k_shortest_paths(G, source, target, K, weight='weight', all_kshortest = False):   #function to find kth shortest path using dijkstra and exploring k-1 paths
      
    A = []           #list A to maintain optimum solutions
    total_len = []   #cost of solution paths
    
    if source == target:      
        return (0, [source])

    B_len, B = nx.single_source_dijkstra(G, source, target, weight=weight)
            

    if K ==1:            #if kth shortest path value is 1 
        return B_len, B  #return list B with cost
    A.append(B)
    total_len.append(B_len)
       
    for n in range(1, K):

        for i in range(len(A[-1]) - 1):    #explore from spur node 
            spur_node = A[-1][i]
            root_path = A[-1][:i + 1]
           
            if weight:
                root_path_length = get_path_length(G, root_path, weight)
           
            edges_discarded = []       #when link is removed and weight is infinity
            if  weight:
            
                edge_cost_add = []
            for path in A:
                if root_path == path[:i + 1]:
                    u = path[i]
                    v = path[i + 1]
                    if (u,v) not in edges_discarded:
                        if  weight:
                        
                            edge_cost_add.append(G[u][v][weight])
                            
                        G.remove_edge(u, v)
                        edges_discarded.append((u, v))
           
            for node in root_path[:-1]:
                for u, v, attr in list(G.edges(node, data=True)):
                    if  weight:
                        edge_cost_add.append(attr[weight])
                    G.remove_edge(u,v)
                    edges_discarded.append((u,v))
           
            try:
                spur_path_len, spur_path = nx.single_source_dijkstra(G, spur_node, target, weight=weight)  
            except:
                spur_path_len = 0
                spur_path = []
               
            total_path = root_path[:-1] + spur_path      #gives total path
            if weight:
                total_path_len = root_path_length + spur_path_len         #gives total path length
            else:
                total_path_len = i + spur_path_len
            if total_path_len > total_len[-1]:
                if B:
                    if total_path_len < B_len:
                        B = total_path
                        B_len = total_path_len
                    else:
                        B = total_path
                        B_len = total_path_len
                   
            for w in range(len(edges_discarded)):   #checking re-considering removed edges
                u = edges_discarded[w][0]
                v = edges_discarded[w][1]
                G.add_edge(u,v)
                if  weight:
                    G.edges[u,v][weight]=edge_cost_add[w]
       
        if B:
            A.append(B)   
            total_len.append(B_len)
        else:
            break
    if all_kshortest:                   #returns optimal solution as per value of k
        return (total_len, A)
   
    return (total_len[-1], A[-1])

def get_path_length(G, path, weight='weight'):   
    length = 0

    if len(path) > 1:
        for i in range(len(path)-1):
            u = path[i]
            v = path[i + 1]
           
            length += G.edges[u,v][weight]      #finding length if more then 1 edge in path
   
    return length    


              
G = nx.DiGraph()   #object for directed graph

file = pd.read_csv('input_edges.csv', header = None)   #taking input from user in form of csv file
file1 = file.values.tolist()                     

for row in file1:                                      #using graph object creating edges between nodes with specific weight 
    G.add_edge(row[0],row[1], length = row[2])
   
#user inputs
sour = input ("Enter starting point or source :")
print("The source you have entered is:",sour)
dest = input("Enter destination :")
print("The destination you have entered is:",dest)
kth = input("Enter the value of k i.e. what number of shortest path you want to find? For example: 2nd shortest path or 6th shortest path..")
print("The value of k is: ",kth)


print(k_shortest_paths(G, sour, dest, int(kth), "length", False))   #passing user values into function
import networkx as nx
import random


NUM_NODES = 10
nwrk = nx.full_rary_tree(3,NUM_NODES)
MSG_SIZE = 10
STARTING_NODE = 3
DROP_PROB = 0.1

###############
# LOAD DATA
###############
for i in range(MSG_SIZE):
    nwrk.nodes[STARTING_NODE][str(i)] = ''

start_node = nwrk

i = 0
done = False
while not done:
    i += 1
    if i % 10 == 0:
        print("Iteration:",i)
    for node_tuple in nwrk.nodes(data=True):
        node_dict = node_tuple[1]
        if len(node_dict) == 0:
            continue
        else:
            #if "curr" not in node_dict.keys():
            for dp in node_dict.keys():
                for neighbors in nwrk.adj[node_tuple[0]]:
                    if random.random() > DROP_PROB:
                        nwrk.nodes[neighbors][dp] = 'data'
    num_full = 0
    for node_tuple in nwrk.nodes(data=True):
        if len(node_tuple[1]) == MSG_SIZE:
            num_full += 1
    done = (num_full == NUM_NODES)
    print(nwrk.nodes(data=True))
        
print ("Finished in ", i, " iterations!")                


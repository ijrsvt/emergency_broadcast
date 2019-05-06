import matplotlib.pyplot as plt
import networkx as nx
import random
import time 
from plot_graph import *

NUM_NODES = 100
nwrk = nx.full_rary_tree(3,NUM_NODES)
MSG_SIZE = 15
STARTING_NODE = 3
DROP_PROB = 0.9
DEBUG_STOP_AND_PRINT = 100

for nt in nwrk.nodes(data=True):
    nt[1]['nxt'] = dict()
    for nbr in nwrk.adj[nt[0]]:
        nt[1]['nxt'][nbr] = 0
    nt[1]['msg']  = []
    nt[1]['msg_set'] = set()

###############
# LOAD DATA
###############
for i in range(MSG_SIZE):
    nwrk.nodes[STARTING_NODE]['msg'] += [i]
    nwrk.nodes[STARTING_NODE]['msg_set'].add(i)


spring_layout = nx.spring_layout(nwrk)
i = 0
done = False
while not done:
    i += 1
    if i % 10 == 0:
        print("Iteration:",i)
    if DEBUG_STOP_AND_PRINT != None and i % DEBUG_STOP_AND_PRINT == 0:
        generate_graph_msg_list(nwrk, spring_layout)
        #print(nwrk.nodes(data=True))
    for node_tuple in nwrk.nodes(data=True):
        node_dict = node_tuple[1]
        if len(node_dict['msg']) == 0:
            continue
        else:
            for neighbors in nwrk.adj[node_tuple[0]]:
                send_msg = node_dict['nxt'][neighbors]
                if random.random() > DROP_PROB:
                    if send_msg not in nwrk.nodes[neighbors]['msg_set']:
                        nwrk.nodes[neighbors]['msg_set'].add(send_msg)
                        nwrk.nodes[neighbors]['msg'] += [send_msg]
                node_dict['nxt'][neighbors] = (send_msg + 1) % len(node_dict['msg'])
    num_full = 0
    for node_tuple in nwrk.nodes(data=True):
        if len(node_tuple[1]['msg']) == MSG_SIZE:
            num_full += 1
    done = (num_full == NUM_NODES)
    #print(nwrk.nodes(data=True))
    #time.sleep(5)        
print ("Finished in ", i, " iterations!")                


nx.draw_networkx(nwrk, withlabels=True)
plt.show()

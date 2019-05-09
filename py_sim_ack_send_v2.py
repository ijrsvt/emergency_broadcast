import matplotlib.pyplot as plt
import networkx as nx
import random
import time 
from plot_graph import *



def ack_send_synch(drop_prob, msg_size=15, adj_file=None,no_display=True,debug_stop=None,show_iter=False):
    if adj_file != None:
        nwrk = nx.readwrite.adjlist.read_adjlist(adj_file)
        NUM_NODES = len(nwrk.nodes())
    else:
        NUM_NODES = 100
        nwrk = nx.connected_watts_strogatz_graph(NUM_NODES, 3, .5, 10)
    MSG_SIZE = msg_size
    STARTING_NODE = list(nwrk.nodes())[random.randint(0,NUM_NODES-1)]
    DROP_PROB = drop_prob
    DEBUG_STOP_AND_PRINT = debug_stop #100
    PRINT_ITER = show_iter

    ##################
    #  DATA STRUCTURES
    #  - 'nxt' : Mapping of
    #     - (neighbor : next packet to sned)
    #
    #  - 'snd_ack' : Mapping of 
    #     - (neighbor received from : packet number)
    #
    #  - 'msg' : Actual message received so far
    #  - 'msg_set' : Set of message received so far
    #################


    for nt in nwrk.nodes(data=True):
        nt[1]['nxt'] = dict()
        nt[1]['snd_ack'] = dict()
        for nbr in nwrk.adj[nt[0]]:
            nt[1]['nxt'][nbr] = 0
        nt[1]['msg']  = []
        nt[1]['msg_set'] = set()
        nt[1]['msg_add_on_iter0'] = []
        nt[1]['msg_add_on_iter1'] = []
        nt[1]['ack_add_on_iter0'] = []
        nt[1]['ack_add_on_iter1'] = []

    ###############
    # LOAD DATA
    ###############
    for i in range(MSG_SIZE):
        nwrk.nodes[STARTING_NODE]['msg'] += [i]
        nwrk.nodes[STARTING_NODE]['msg_set'].add(i)


    spring_layout = nx.spring_layout(nwrk)
    i = -1
    done = False

    #############
    # ACTUAL SIMULATION
    #############
    while not done:
        i += 1
        if PRINT_ITER and i % PRINT_ITER == 0:
            print("Iteration:",i)
        if DEBUG_STOP_AND_PRINT != None and i % DEBUG_STOP_AND_PRINT == 0:
            generate_graph_msg_list(nwrk, spring_layout)

        ####################
        # SEND TO NEIGHBORS
        ####################
        for node_tuple in nwrk.nodes(data=True):
            node_dict = node_tuple[1]
            this_node = node_tuple[0]

            if i % 2 == 0:
                for new_msg,sndr in node_dict['msg_add_on_iter0']:
                    if new_msg not in node_dict['msg_set']:
                        node_dict['msg_set'].add(new_msg)
                        node_dict['msg'] += [new_msg]
                        node_dict['snd_ack'][sndr] = new_msg # Set SND_ACK Dict to have (Sending_host, send_msg)
                node_dict['msg_add_on_iter0'] = []           

                for hst in node_dict['ack_add_on_iter0']:
                    node_dict['nxt'][hst] = (node_dict['nxt'][hst] + 1) % len(node_dict['msg'])
                node_dict['ack_add_on_iter0'] = []            
            else:
                for new_msg,sndr in node_dict['msg_add_on_iter1']:
                    if new_msg not in node_dict['msg_set']:
                        node_dict['msg_set'].add(new_msg)
                        node_dict['msg'] += [new_msg]
                        node_dict['snd_ack'][sndr] = new_msg # Set SND_ACK Dict to have (Sending_host, send_msg)
                node_dict['msg_add_on_iter1'] = []           

                for hst in node_dict['ack_add_on_iter1']:
                    node_dict['nxt'][hst] = (node_dict['nxt'][hst] + 1) % len(node_dict['msg'])
                node_dict['ack_add_on_iter1'] = []   


            ######
            # Don't send if no messages saved
            #####
            if len(node_dict['msg']) == 0:
                continue
            
            else:
                for neighbors in nwrk.adj[this_node]:
                    send_msg = node_dict['nxt'][neighbors]
                    ########
                    # SENDING MESSAGE
                    ########
                    if random.random() > DROP_PROB:
                        if send_msg not in nwrk.nodes[neighbors]['msg_set']:
                            nwrk.nodes[neighbors]['msg_add_on_iter' + str((i+1) %2)] += [(send_msg, this_node)]

                ###########
                # SEND ACKs
                ###########
                for hst, msg  in node_dict['snd_ack'].items():
                    if random.random() > DROP_PROB:
                        nwrk.nodes[hst]['ack_add_on_iter' + str((i+1)%2)] += [this_node]
                        ### Note that this goes into the neighbor's NEXT dictionary and increments the current nodes 'next message to sendd'

        #################
        # ARE WE DONE? 
        #################
        num_full = 0
        for node_tuple in nwrk.nodes(data=True):
            if len(node_tuple[1]['msg']) == MSG_SIZE:
                num_full += 1
        done = (num_full == NUM_NODES)
        #print(nwrk.nodes(data=True))
        #time.sleep(5)        

    if not no_display:
        print ("Finished in ", i, " iterations!")                
        nx.draw_networkx(nwrk, withlabels=True)
        plt.show()
    return i

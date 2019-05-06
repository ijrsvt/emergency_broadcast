import matplotlib.pyplot as plt
import networkx as nx



def generate_graph_msg_list(graph, layout=None):
    if layout == None:
        layout = nx.spring_layout(graph)
    color_map = [len(x['msg']) for _,x in graph.nodes(data=True)]
    
    h_map = nx.draw_networkx_nodes(graph, layout, node_color=color_map, cmap='Blues')
    nx.draw_networkx_labels(graph,layout)
    nx.draw_networkx_edges(graph,layout)
    plt.colorbar(h_map)
    plt.show()

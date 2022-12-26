import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as img

image = img.imread('./image.jpg')

def shortpath_print_dijkstra(G,start,end):
    tg = nx.dijkstra_path(G,start,end, weight='weight')
    min = nx.dijkstra_path_length(G,end,start)
    NG = nx.MultiDiGraph.copy(G)
    nx.MultiDiGraph.clear_edges(NG)   
    for i in range(len(tg)-1):
        NG.add_edge(tg[i],tg[i+1])
    return NG, min


def nxgraph_draw(Graph,pos):
    
    nx.draw_networkx_nodes(Graph, pos=pos,node_size=300,node_color='yellow')
    #nx.draw_networkx_edge_labels(Graph, pos=pos)
    nx.draw_networkx_edges(Graph, pos=pos)
    nx.draw_networkx_labels(Graph, pos=pos, font_size=10)
    plt.imshow(image)
    plt.show()
    
    
    

    nx.MultiDiGraph.clear_edges()

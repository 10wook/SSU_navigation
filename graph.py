import networkx as nx
import pandas as pd
import matplotlib.image as img
from dijkstra import *
# 이미지 불러오기
image = img.imread('./image.jpg')

# csv 데이터 불러오기
#df_p = pd.read_csv('./position_data.csv')
# 엑셀에서 불러 올 수 있게 수정했습니다.
# position data
df_p = pd.read_excel('./excel_data/position_data.xlsx')
# weight data
df_w = pd.read_excel('./excel_data/weight_data.xlsx')

# 그래프 객체 설정
G = nx.MultiDiGraph()

# 노드 설정
for i in range(len(df_p['point_name'])):
    G.add_node(str(df_p['point_name'][i]))


# 엣지 설정
for i in range(len(df_w.values)):
    for j in range(len(df_w.values)):
        if i == j:
            continue
        elif i >= 25:
            tmp_i = chr(i+40)
            idx_i = chr(i+40)
            if j >= 25:
                tmp_j = chr(j+40)
            else:
                tmp_j = str(j+1)
        elif j >= 25:
            tmp_j = chr(j+40)
        else:
            tmp_i = str(i+1)
            tmp_j = str(j+1)
            idx_i = i+1
        #print(tmp_i, "->", tmp_j)
        G.add_edge(tmp_j, tmp_i, weight=int(df_w[idx_i][j]))

# 좌표 설정
pos = {}
for i in range(len(df_p['point_name'])):
    node = df_p['point_name'][i]
    pos[str(node)] = (df_p['pos_x'][i], df_p['pos_y'][i])


NG ,min = shortpath_print_dijkstra(G,'1','18')
nxgraph_draw(NG,pos)

print(min)
nx.draw(NG, pos)
nx.draw_networkx_nodes(NG, pos=pos, node_size=300, node_color='yellow')
nx.draw_networkx_edges(NG, pos=pos)
nx.draw_networkx_labels(NG, pos=pos, font_size=10)
plt.imshow(image)
plt.savefig("path.png")

# 그리기
# nx.draw(G, pos, node_size=100, font_size=5,
#         font_color="white", with_labels=True)
# plt.imshow(image)
# plt.show()

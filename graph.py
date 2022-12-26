import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as img

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
for i in range(len(df_w.values)-5):
    for j in range(len(df_w.values)):
        if i+1 == j+1:
            continue
        # print(type(df_w[i+1][j]))
        k = (j, i, int(df_w[i+1][j]))
        G.add_weighted_edges_from(k)

for i in range(5):
    for j in range(len(df_w.values)):
        if i+26 == j+1:
            continue
        # print(df_w[str(chr(i+65))][j])
        k = (j, chr(i+65), int(df_w[str(chr(i+65))][j]))
        G.add_weighted_edges_from(k)

# 좌표 설정
pos = {}
for i in range(len(df_p['point_name'])):
    node = df_p['point_name'][i]
    pos[str(node)] = (df_p['pos_x'][i], df_p['pos_y'][i])

# 그리기
nx.draw(G, pos, node_size=100, font_size=5,
        font_color="white", with_labels=True)
plt.imshow(image)
plt.show()

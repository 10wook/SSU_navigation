import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as img

# 이미지 불러오기
image = img.imread('./image.jpg')

# csv 데이터 불러오기
df_p = pd.read_csv('./position_data.csv')

# 그래프 객체 설정
G = nx.MultiDiGraph()

# 노드 설정
for i in range(len(df_p['point_name'])):
    G.add_node(str(df_p['point_name'][i]))

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

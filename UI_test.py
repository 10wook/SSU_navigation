import networkx as nx
import pandas as pd
import matplotlib.image as img
import matplotlib as plt
from dijkstra import *
import pygame
from PIL import Image
import platform
#######################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()
# 화면 타이틀 설정
icon = pygame.image.load("./img/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("SSU_navigation")


# Define the colors we will use in RGB format
color_0 = (255, 255, 255)
color_a = (130, 170, 227)
color_b = (145, 216, 228)
color_c = (201, 244, 255)
color_d = (234, 253, 252)


# 화면 크기 설정
screen_width = 920  # 가로크기
screen_height = 640  # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 배경 이미지
background = pygame.image.load("./img/image_pygame.jpg")
# test
background_width = background.get_width()
background_height = background.get_height()

# 버튼 크기
button_size = 40

# 패드 위치
pad_width = background_width + button_size/2
pad_height = button_size/2 + background_height/4

title_font = pygame.font.SysFont('Arial', 40, True, True)
font = pygame.font.SysFont('Arial', 35, True)
small_font = pygame.font.SysFont('Arial', 20, True)

alpha = ['A', 'B', 'C', 'D', 'E']

# 텍스트
text_source = font.render('where to \"start\"', True, color_a)
text_destination = font.render('where to \"end\"', True, color_a)
text_select = font.render('Select', True, color_b)
text_choose = font.render('select', True, color_0)
text_retry = small_font.render('back', True, color_0)
text_output = font.render('output', True, color_b)
text_check = font.render('check', True, color_0)


# FPS
done = False
clock = pygame.time.Clock()

# 기능보조


def index_to_node(index):
    if index[1] == 5:
        return alpha[index[0]]
    return str((1*index[0])+(5*index[1])+1)


def check_in_pad(mouse):
    return pad_width <= mouse[0] <= pad_width + 240 and pad_height <= mouse[1] <= pad_height+300


def check_in_main(mouse):
    return pad_width + 60 <= mouse[0] <= pad_width + 180 and screen_height - 100 <= mouse[1] <= screen_height-50


def check_in_retry(mouse):
    return pad_width+180 <= mouse[0] <= pad_width+230 and 20 <= mouse[1] <= 50


def make_button_number(color, number, i, j):
    if len(str(number)) == 1:
        pygame.draw.rect(
            screen, color, [pad_width + (50*j), pad_height+(50*i), button_size, button_size])
        screen.blit(font.render(str((1*j)+(5*i)+1),
                    True, color_0), (pad_width + (50*j)+12, pad_height+(50*i)))
    else:
        pygame.draw.rect(
            screen, color, [pad_width + (50*j), pad_height+(50*i), button_size, button_size])
        screen.blit(font.render(str((1*j)+(5*i)+1),
                    True, color_0), (pad_width + (50*j)+3, pad_height+(50*i)))


def make_button_alpha(color, i):
    pygame.draw.rect(
        screen, color, [pad_width + (50*i), pad_height+260, 40, 40])
    screen.blit(font.render(
        alpha[i], True, color_0), (pad_width + (50*i)+10, pad_height+260))


def make_button_main(color, text):
    pygame.draw.rect(
        screen, color, [pad_width + 60, screen_height - 100, 120, 50])
    screen.blit(text, (pad_width + 80, screen_height - 95))


def make_graph(start, end):
    # image = img.imread('./img/image.jpg')
    image = Image.open('./img/image.jpg')
    df_p = pd.read_excel('./excel_data/position_data.xlsx')
    df_w = pd.read_excel('./excel_data/weight_data.xlsx')
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
            G.add_edge(tmp_j, tmp_i, weight=int(df_w[idx_i][j]))

    # 좌표 설정
    pos = {}
    label = {}
    for i in range(len(df_p['point_name'])):
        node = df_p['point_name'][i]
        pos[str(node)] = (df_p['pos_x'][i], df_p['pos_y'][i])
        label[str(node)] = node
    NG, time = shortpath_print_dijkstra(G, start, end)
    nx.draw(NG, pos, node_size=100, node_color='yellow',
            labels=label, font_size=8, font_color="black")
    plt.imshow(image)
    plt.savefig("./img/path.png")
    plt.cla()
    return time


def make_button_back(color, text):
    pygame.draw.rect(
        screen, color, [pad_width+180, 20, 50, 30])
    screen.blit(text, (pad_width+187, 20))


def make_title(text1, text2):
    screen.blit(text1, (pad_width + 20, 70))
    if text2 != None:
        screen.blit(text2, (pad_width, 20))


def pos_to_index(x, y):
    return ((x-660)//50, (y-180)//50)


# 메인 기능


def input_source():  # source를 입력받음
    done = False
    click = (-1, -1)
    while not done:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # 클릭 시,패드 안에 마우스가 있으면, 그때의 위치 값을 버튼의 인덱스로 변환하여 click 변수에 저장
                if check_in_pad(mouse):
                    click = pos_to_index(mouse[0], mouse[1])
                # 클릭 시, choice버튼 안에 마우스가 있으면, 다음으로 넘어감.
                elif check_in_main(mouse):
                    if not click == (-1, -1):
                        done = True

        # 배경 채우고, 이미지 넣기
        screen.fill(color_c)
        screen.blit(background, (0, 0))

        # 타이틀 그려주기
        make_title(text_source, text_select)

        # mouse[0] -> x 축 좌표, mouse[1] -> y 축 좌표
        mouse = pygame.mouse.get_pos()

        # 패드 그려주기
        for i in range(5):
            for j in range(5):
                if j == click[0] and i == click[1]:
                    make_button_number(color_a, (1*j)+(5*i)+1, i, j)
                else:
                    make_button_number(color_b, (1*j)+(5*i)+1, i, j)

        for i in range(5):
            if i == click[0] and click[1] == 5:
                make_button_alpha(color_a, i)
            else:
                make_button_alpha(color_b, i)

        # choice 버튼 그려주기
        if check_in_main(mouse):
            make_button_main(color_a, text_choose)
        else:
            make_button_main(color_b, text_choose)

        # updates the frames of the game
        pygame.display.update()
    return click


def input_destination(source):  # destination을 입력받음
    done = False
    click = (-1, -1)
    while not done:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # 클릭 시,패드 안에 마우스가 있으면, 그때의 위치 값을 버튼의 인덱스로 변환하여 click 변수에 저장
                if check_in_pad(mouse):
                    click = pos_to_index(mouse[0], mouse[1])
                # 클릭 시, choice버튼 안에 마우스가 있으면, 다음으로 넘어감.
                elif check_in_main(mouse):
                    if not click == (-1, -1):
                        done = True
                elif check_in_retry(mouse):
                    return (click, False)
        # 배경 채우고, 이미지 넣기
        screen.fill(color_c)
        screen.blit(background, (0, 0))

        # destination text 그려주기
        make_title(text_destination, text_select)

        # stores the (x,y) coordinates into
        # the variable as a tuple
        # mouse[0] -> x 축 좌표, mouse[1] -> y 축 좌표
        mouse = pygame.mouse.get_pos()

        # 마우스 포인터가 패드 안에 위치 시, 블록 색상 변경
        for i in range(5):
            for j in range(5):
                if j == click[0] and i == click[1]:
                    make_button_number(color_a, (1*j)+(5*i)+1, i, j)

                elif j == source[0] and i == source[1]:
                    make_button_number((255, 0, 0), (1*j)+(5*i)+1, i, j)

                else:
                    make_button_number(color_b, (1*j)+(5*i)+1, i, j)

        for i in range(5):
            if i == click[0] and click[1] == 5:
                make_button_alpha(color_a, i)
            elif i == source[0] and source[1] == 5:
                make_button_alpha((255, 0, 0), i)
            else:
                make_button_alpha(color_b, i)

        # choice 버튼 그려주기
        if check_in_main(mouse):
            make_button_main(color_a, text_choose)
        else:
            make_button_main(color_b, text_choose)

        # back 버튼 그려주기
        if check_in_retry(mouse):
            make_button_back(color_a, text_retry)
        else:
            make_button_back(color_b, text_retry)

        # updates the frames of the game
        pygame.display.update()
    return (click, True)


def output(time, start, end):
    done = False

    while not done:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # 클릭 시, choice버튼 안에 마우스가 있으면, 다음으로 넘어감.
                if check_in_main(mouse):
                    return 0

        # 배경 채우고, 이미지 넣기
        screen.fill(color_c)
        screen.blit(output_image, (0, 0))

        # source text 그려주기
        make_title(text_output, None)

        mouse = pygame.mouse.get_pos()

        # check 버튼 그려주기
        if check_in_main(mouse):
            make_button_main(color_a, text_check)
        else:
            make_button_main(color_b, text_check)

        # 선택 항목 출력
        screen.blit(font.render(start + " to " + end, True, color_a),
                    (pad_width, screen_height - 450))

        # 시간 출력
        screen.blit(font.render('time: ' + str(time)+' minutes', True, color_a),
                    (pad_width + 30, screen_height - 400))
        # updates the frames of the game
        pygame.display.update()


# 실행
while True:
    source = input_source()
    destination = input_destination(source)
    if destination[1]:
        pygame.quit()

        start = index_to_node(source)
        end = index_to_node(destination[0])

        time = make_graph(start, end)

        img = Image.open('./img/path.png')
        xy = (80, 0, 560, 480)
        cut_img = img.crop(xy)
        resize_img = cut_img.resize((640, 640))
        resize_img.save('./img/path.png')

        # 재설정
        pygame.init()

        # 화면 타이틀 설정
        icon = pygame.image.load("./img/icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("SSU_navigation")

        # 화면 크기 설정
        screen = pygame.display.set_mode((screen_width, screen_height))

        # 배경 이미지
        background = pygame.image.load("./img/image_pygame.jpg")
        # test
        background_width = background.get_width()
        background_height = background.get_height()

        # 버튼 크기
        button_size = 40

        # 패드 위치
        pad_width = background_width + button_size/2
        pad_height = button_size/2 + background_height/4

        title_font = pygame.font.SysFont('Arial', 40, True, True)
        font = pygame.font.SysFont('Arial', 35, True)
        small_font = pygame.font.SysFont('Arial', 20, True)

        alpha = ['A', 'B', 'C', 'D', 'E']

        # 텍스트
        text_source = font.render('where to start', True, color_a)
        text_destination = font.render('where to end', True, color_a)
        text_select = font.render('Select', True, color_b)
        text_choose = font.render('select', True, color_0)
        text_retry = small_font.render('back', True, color_0)
        text_output = font.render('output', True, color_b)
        text_check = font.render('check', True, color_0)

        # FPS
        done = False
        clock = pygame.time.Clock()

        output_image = pygame.image.load("./img/path.png")

        output(time, start, end)

import cv2
import numpy as np
import argparse
import sys

# 配置图片存放参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())


# 读取图片
img = cv2.imread(args['image'])

# 照片提亮
alpha = 2
beta = 20
new_img = np.zeros(img.shape, img.dtype)
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        for c in range(img.shape[2]):
            new_img[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)
img_copy = new_img.copy()
img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
_, img_thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)

# 配置HSV
target_color = ['blue', 'purple', 'yellow']

color_dist = {'blue': {'Lower': np.array([87, 28, 66]), 'Upper': np.array([122, 146, 134])},
              'purple': {'Lower': np.array([121, 26, 125]), 'Upper': np.array([178, 71, 210])},
              'yellow': {'Lower': np.array([18, 134, 183]), 'Upper': np.array([25, 222, 255])},
              }

# 高斯模糊
img_gaussian = cv2.GaussianBlur(new_img, (5, 5), 0)

# 转换为HSV图像
img_hsv = cv2.cvtColor(img_gaussian, cv2.COLOR_BGR2HSV)

# 腐蚀操作
img_hsv = cv2.erode(img_hsv, None, iterations=2)

# 找匹配
color_dict = {}
for i, color in enumerate(target_color):
    inRange_hsv = cv2.inRange(img_hsv, color_dist[color]['Lower'], color_dist[color]['Upper'])
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    color_dict[color] = (np.int0(box)[0][0]+np.int0(box)[3][0]) / 2

# 柱子对应的盘子
match = {}
for col, gX in color_dict.items():
    if gX < int(0.3 * img.shape[1]):
        match[col] = 'a'
    elif int(0.3 * img.shape[1]) < gX < int(0.7 * img.shape[1]):
        match[col] = 'b'
    else:
        match[col] = 'c'

# 每根柱子上盘子从上到下的顺序
pillar_a, pillar_b, pillar_c = {}, {}, {}
a, b, c = 1, 1, 1
for target in target_color:
    if match[target] == 'a':
        pillar_a[a] = target
        a = a + 1
    elif match[target] == 'b':
        pillar_b[b] = target
        b = b + 1
    else:
        pillar_c[c] = target
        c = c + 1

color_match = {'blue': 1, 'purple': 2, 'yellow': 3}
# 保存为txt文件
txt = open('pillar_match.txt', "w", encoding='utf-8')
txt.write(str(len(pillar_a))+' ')
for i in range(len(pillar_a), 0, -1):
    txt.write(str(color_match[pillar_a[i]])+' ')
txt.write('\n'+str(len(pillar_b))+' ')
for i in range(len(pillar_b), 0, -1):
    txt.write(str(color_match[pillar_b[i]])+' ')
txt.write('\n'+str(len(pillar_c))+' ')
for i in range(len(pillar_c), 0, -1):
    txt.write(str(color_match[pillar_c[i]])+' ')
txt.write('\n')
txt.close()

# Hanoi.py
b, e, sf, ef = {}, {}, {}, {}
Step = {'step': 0}
match_color = {1: 'blue', 2: 'purple', 3: 'yellow'}


# 移动信息
def move(plate, x, y):
    txt = open("step.txt", "a", encoding='utf-8')
    txt.write('move plate '+match_color[plate]+' from pillar '+chr(x+65)+' to pillar '+chr(y+65)+'\n')
    tmp = open("temp.txt", "a", encoding='utf-8')
    tmp.write(str(plate) + chr(x + 65) + chr(y + 65) + '\n')
    b[plate] = y
    Step['step'] = Step['step'] + 1
    txt.close()
    tmp.close()


# 搜索算法
def dfs(plate, x, y, z):
    if x == y:
        return
    for i in range(plate-1, 0, -1):
        dfs(i, b[i], z, 3-z-b[i])
    move(plate, x, y)


n = 3
# 读取各柱子上的盘子
i = 0
with open("pillar_match.txt", "r") as txt:
    for data in txt.readlines():
        data = data.strip('\n')
        list = data.split(' ')
        list.pop()
        sf[i] = int(list[0])
        for j in range(1, sf[i] + 1, 1):
            x = int(list[j])
            b[x] = i
        i = i + 1
i = 0
with open("input.txt", "r") as txt:
    for data in txt.readlines():
        data = data.strip('\n')
        list = data.split(' ')
        list.pop()
        ef[i] = int(list[0])
        for j in range(1, ef[i] + 1, 1):
            x = int(list[j])
            e[x] = i
        i = i + 1
for i in range(n, 0, -1):
    if b[i] != e[i]:
        dfs(i, b[i], e[i], 3-b[i]-e[i])
sys.exit(0)

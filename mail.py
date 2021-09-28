# coordinate.py
# 指定B柱底部的xyz坐标，两柱之间距离，盘子的厚度，柱子的高度，盘子的直径，丢下时下降的微小量
left_down = '$KMS:-65,288,150,1000'
left_up = '$KMS:-65,292,200,1000'
mid_up = '$KMS:0,290,200,1000'
mid_down = '$KMS:10,320,120,2000'
right_up = '$KMS:72,285,200,2000'
right_down = '$KMS:72,300,115,2000'
craw_open = '#005P1150T1000'
craw_close = '#005P1300T1000'


# 返回初始坐标
def origin():
    tmp = open("control.txt", "a", encoding='utf-8')
    tmp.write(mid_up + '\n')
    tmp.close()


# 生成移动坐标，输入值为盘子的编号，层数，在何杆，去向何杆
def move(where, to):
    tmp = open("control.txt", "a", encoding='utf-8')
    # 判断机械臂初始位置
    if where == 'A':
        tmp.write(left_up + '\n')
        tmp.write(left_down + '\n')
        tmp.write(craw_close + '\n')
        tmp.write(left_up + '\n')
    elif where == 'B':
        tmp.write(mid_up + '\n')
        tmp.write(mid_down + '\n')
        tmp.write(craw_close + '\n')
        tmp.write(left_up + '\n')
    elif where == 'C':
        tmp.write(right_up + '\n')
        tmp.write(right_down + '\n')
        tmp.write(craw_close + '\n')
        tmp.write(left_up + '\n')
    # 判断机械臂截止位置，松爪后需要返回up
    if to == 'A':
        tmp.write(left_up + '\n')
        tmp.write(left_down + '\n')
        tmp.write(craw_open + '\n')
        tmp.write(left_up + '\n')
    elif to == 'B':
        tmp.write(mid_up + '\n')
        tmp.write(mid_down + '\n')
        tmp.write(craw_open + '\n')
        tmp.write(mid_up + '\n')
    elif to == 'C':
        tmp.write(right_up + '\n')
        tmp.write(right_down + '\n')
        tmp.write(craw_open + '\n')
        tmp.write(right_up + '\n')
    tmp.close()


# 编写坐标
txt = open("temp.txt", "r", encoding='utf-8')
lines = txt.readlines()
# 初始化
origin()
# 生成坐标
for i in range(len(lines)):
    move(lines[i][1], lines[i][2])

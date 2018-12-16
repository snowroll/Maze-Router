# -*- coding:utf-8 -*-

import os, sys
import numpy as np
import datetime
import random
import time

source_point = []


class Point:  # 点类
    x = 0
    y = 0
    lx = 0
    ly = 0
    p_type = ""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.lx = 0
        self.ly = 0
        p_type = ""


source = []
grid = []
target = []
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


def init_map(block_mode):
    with open("input.txt", 'r') as fin:
        line = fin.readline()
        info = line.strip().split(' ')
        rows = int(info[0])
        cols = int(info[1])
        for i in range(0, rows):  # 初始化布图
            temp = []
            for j in range(0, cols):
                tmp_point = Point()
                tmp_point.x = i
                tmp_point.y = j
                tmp_point.p_type = "empty"
                temp.append(tmp_point)
            grid.append(temp)

        line = fin.readline()  # 读取源点
        point_cnt = int(line.strip())
        info = fin.readline().strip().split(' ')
        x, y = int(info[0]), int(info[1])
        grid[x][y].p_type = "target"
        target.append(grid[x][y])
        source_point.append([x, y])  # chaihj add source point
        for i in range(0, point_cnt - 1):
            line = fin.readline()
            info = line.strip().split(' ')
            x, y = int(info[0]), int(info[1])
            grid[x][y].p_type = "source"
            source.append(grid[x][y])
            source_point.append([x, y])  # chaihj add source point

        line = fin.readline()
        block_cnt = int(line.strip())
        if block_mode == 0:  # 手动添加障碍点
            for i in range(0, block_cnt):
                line = fin.readline()
                info = line.strip().split(' ')
                grid[int(info[0])][int(info[1])].p_type = "block"
        else:  # 自动生成障碍点
            random_block(block_cnt, rows, cols, source_point)

    return rows, cols


def random_block(num, rows, cols, source_point):
    block_point = []
    while num != 0:
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        if [x, y] not in source_point and [x, y] not in block_point:
            block_point.append([x, y])
            num -= 1
        else:
            pass
    with open("block-point.txt", 'w') as fin:
        for i in block_point:
            x, y = i[0], i[1]
            fin.write(str(x) + ' ' + str(y) + '\n')
            grid[x][y].p_type = 'block'


def update_map(rows, cols):
    for i in range(0, rows):
        for j in range(0, cols):
            grid[i][j].lx = 0
            grid[i][j].ly = 0
            if grid[i][j].p_type == "trace_s" or grid[i][j].p_type == "trace_t":
                grid[i][j].p_type = "empty"


def isOK(x, y, rows, cols):
    if rows > x >= 0 and cols > y >= 0 and grid[x][y].p_type != "block":
        return True
    else:
        return False


def search(rows, cols):
    trace_s = []
    trace_t = []
    head_s = 0
    tail_s = -1
    head_t = 0
    tail_t = -1
    for i in range(0, len(source)):
        trace_s.append(source[i])
        tail_s = tail_s + 1
    for i in range(0, len(target)):
        trace_t.append(target[i])
        tail_t = tail_t + 1
    tar_x = 0
    tar_y = 0
    sou_x = 0
    sou_y = 0
    while True:
        cur_tail_s = tail_s
        while head_s <= cur_tail_s:
            for k in range(0, 4):
                temp_x = trace_s[head_s].x + dx[k]
                temp_y = trace_s[head_s].y + dy[k]
                if isOK(temp_x, temp_y, rows, cols) and grid[temp_x][temp_y].p_type != "source" and grid[temp_x][temp_y].p_type != "trace_s":
                    if grid[temp_x][temp_y].p_type == "target" or grid[temp_x][temp_y].p_type == "trace_t":
                        tar_x = temp_x
                        tar_y = temp_y
                        sou_x = trace_s[head_s].x
                        sou_y = trace_s[head_s].y
                        # print("find it!")
                        return tar_x, tar_y, sou_x, sou_y
                    elif grid[temp_x][temp_y].p_type == "empty":
                        grid[temp_x][temp_y].p_type = "trace_s"
                        trace_s.append(grid[temp_x][temp_y])
                        tail_s = tail_s + 1
                        grid[temp_x][temp_y].lx = trace_s[head_s].x
                        grid[temp_x][temp_y].ly = trace_s[head_s].y
            head_s = head_s + 1

        cur_tail_t = tail_t
        while head_t <= cur_tail_t:
            for k in range(0, 4):
                temp_x = trace_t[head_t].x + dx[k]
                temp_y = trace_t[head_t].y + dy[k]
                if isOK(temp_x, temp_y, rows, cols) and grid[temp_x][temp_y].p_type != "target" and grid[temp_x][temp_y].p_type != "trace_t":
                    if grid[temp_x][temp_y].p_type == "source" or grid[temp_x][temp_y].p_type == "trace_s":
                        sou_x = temp_x
                        sou_y = temp_y
                        tar_x = trace_t[head_t].x
                        tar_y = trace_t[head_t].y
                        # print("find it!")
                        return tar_x, tar_y, sou_x, sou_y
                    elif grid[temp_x][temp_y].p_type == "empty":
                        grid[temp_x][temp_y].p_type = "trace_t"
                        trace_t.append(grid[temp_x][temp_y])
                        tail_t = tail_t + 1
                        grid[temp_x][temp_y].lx = trace_t[head_t].x
                        grid[temp_x][temp_y].ly = trace_t[head_t].y
            head_t = head_t + 1


def print_grid(row, col):
    str_int = {"empty": '0', "target": '1', "block": '2', "source": '3'}
    for i in source_point:
        x, y = i[0], i[1]
        grid[x][y].p_type = 'source'

    with open("answer.txt", 'w') as f:  # 输出结果
        for i in range(0, row):
            for j in range(0, col):
                f.write(str_int[grid[i][j].p_type] + ' ')
            f.write('\n')


def main(block_mode):
    rows, cols = init_map(block_mode)

    source_size = len(source)
    for i in range(0, source_size):
        try:
            tar_x, tar_y, sou_x, sou_y = search(rows, cols)
        except:
            print("Error! Can't find the trace......")

        tmp_x = grid[tar_x][tar_y].x
        tmp_y = grid[tar_x][tar_y].y
        while grid[tmp_x][tmp_y].p_type != "target":
            grid[tmp_x][tmp_y].p_type = "target"
            target.append(grid[tmp_x][tmp_y])
            tempx = tmp_x
            tempy = tmp_y
            tmp_x = grid[tempx][tempy].lx
            tmp_y = grid[tempx][tempy].ly
        tmp_x = grid[sou_x][sou_y].x
        tmp_y = grid[sou_x][sou_y].y
        while grid[tmp_x][tmp_y].p_type != "source":
            grid[tmp_x][tmp_y].p_type = "target"
            target.append(grid[tmp_x][tmp_y])
            tempx = tmp_x
            tempy = tmp_y
            tmp_x = grid[tempx][tempy].lx
            tmp_y = grid[tempx][tempy].ly
        grid[tmp_x][tmp_y].p_type = "target"
        target.append(grid[tmp_x][tmp_y])
        # remove this source point
        source.remove(grid[tmp_x][tmp_y])
        update_map(rows, cols)

    print_grid(rows, cols)


if __name__ == "__main__":
    block_mode = sys.argv[1]  # 生成障碍点的方式
    start = time.clock()
    main(block_mode)
    end = time.clock()
    print(end-start)

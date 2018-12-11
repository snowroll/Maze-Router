#-*- coding:utf-8 -*-
from PIL import Image
import numpy as np
import cv2
from optparse import OptionParser

def read_file(): 
    pixels = []
    with open("answer.txt", 'r') as f:  # 读取文件  source -- 3  block -- 2 back -- 0 path -- 1
        for i in f.readlines():
            pixels.append(i.strip().split())
    rows, cols = len(pixels), len(pixels[0])  # 绘制准备
    return rows, cols, pixels

def draw_result(size, rows, cols, pixels):
    background = Image.new('RGB', (size * rows, size * cols), (255, 255, 255))
    blue  =  Image.new('RGB', (size, size), (0, 0, 255))
    red   =  Image.new('RGB', (size, size), (255, 0, 0))
    black =  Image.new('RGB', (size, size), (0, 0, 0))

    ptype = {"empty": '0', "target": '1', "block": '2', "source" : "3"}
    r_index = -1
    for row in pixels:
        r_index += 1
        c_index = -1
        for pixel in row:
            c_index += 1
            if pixels[r_index][c_index] == ptype['source']:  # 源 蓝色
                background.paste(blue, (r_index*size, c_index*size))
            elif pixels[r_index][c_index] == ptype['target']:  # 路径 红色
                background.paste(red, (r_index*size, c_index*size))
            elif pixels[r_index][c_index] == ptype['block']:  # 障碍物 黑色
                background.paste(black, (r_index*size, c_index*size))
    background.show()
    background.save("result.jpg")

if __name__ == '__main__':
    usage = 'Usage: %prog[-s size]'
    parser = OptionParser(usage)
    parser.add_option('-s', dest='size', default=1, help='cube size')
    (options, args) = parser.parse_args()

    rows, cols, pixels = read_file()
    draw_result(int(options.size), rows, cols, pixels)
    

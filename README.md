# Maze-Router
用迷宫算法解决布线问题

input.txt  --  输入文件

answer.txt  --  输出文件

maze_v0.py -- 基于BFS的迷宫算法，从源扩展

​	运行命令： python maze_v0.py 0  0 - 使用输入文件中的障碍点坐标 1 - 程序自动生成障碍点坐标 

maze_v1.py  -- 基于BFS的迷宫算法程序，从目标节点扩展

maze_v2.py  -- 改进算法，从目标节点和源同时扩展

draw.py  --  绘图程序，命令： python draw.py -s [size]

result.jpg  --  结果图像
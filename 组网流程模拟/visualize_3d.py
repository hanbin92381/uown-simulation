import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

# 生成随机点
num_points = 50
points = {i: np.random.rand(3) * 10 for i in range(1, num_points + 1)}

# 生成所有可能的边
edges = []
for i in range(1, num_points + 1):
    for j in range(i + 1, num_points + 1):
        edges.append((i, j))

# 随机删除一些边
num_edges_to_keep = num_points * 2  # 假设保留的边数为节点数的两倍
edges = random.sample(edges, min(len(edges), num_edges_to_keep))

# 创建一个三维坐标系
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制点
for point, coordinates in points.items():
    ax.scatter(*coordinates, color='r', label=f'Point {point}')

# 绘制边
for edge in edges:
    start, end = edge
    start_coordinates = points[start]
    end_coordinates = points[end]
    ax.plot3D(*zip(start_coordinates, end_coordinates), color='b')

# 设置图例
ax.legend()

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 显示图形
plt.show()

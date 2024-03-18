import random
import time
import os

from node import *
from visualize import *

# 全局变量设置
range_x = 30
range_y = 30
range_z = 30
num_nodes = 20  # 5, 10, 15, 20
broadcast_range = 17
broadcast_interval = 0

coordinates_dir = './coordinates'

def write_coordinates(file_path, num, X, Y):
    """
    生成随机的二维坐标并写入文件
    """
    coordinates = []
    for _ in range(num):
        x = random.uniform(0, X)  # 在区间内生成随机的x坐标
        y = random.uniform(0, Y)  # 在区间内生成随机的y坐标
        # 引入随机扰动来分散节点的位置
        x += random.uniform(-0.2 * X, 0.2 * X)
        y += random.uniform(-0.2 * Y, 0.2 * Y)
        coordinates.append((x, y))

    # 将坐标写入文件
    with open(file_path, 'w') as file:
        for coordinate in coordinates:
            file.write(f"{coordinate[0]} {coordinate[1]}\n")


def write_coordinates_3d(file_path, num, X, Y, Z):
    """
    生成随机的三维坐标并写入文件
    """
    coordinates = []
    for _ in range(num):
        x = random.uniform(0, X)  # 在区间内生成随机的x坐标
        y = random.uniform(0, Y)  # 在区间内生成随机的y坐标
        z = random.uniform(0, Z)  # 在区间内生成随机的z坐标
        # 引入随机扰动来分散节点的位置
        x += random.uniform(-0.2 * X, 0.2 * X)
        y += random.uniform(-0.2 * Y, 0.2 * Y)
        z += random.uniform(-0.2 * Z, 0.2 * Z)
        coordinates.append((x, y, z))

    # 将坐标写入文件
    with open(file_path, 'w') as file:
        for coordinate in coordinates:
            file.write(f"{coordinate[0]} {coordinate[1]} {coordinate[2]}\n")

        
def read_coordinates(file_path, dimension=2):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            if dimension == 2:
                x, y = line.strip().split()
                coordinates.append((float(x), float(y)))
            else:
                x, y, z = line.strip().split()
                coordinates.append((float(x), float(y), float(z)))

    return coordinates


# 创建节点并添加到节点列表中
def create_nodes():
    for i in range(1, num_nodes + 1):
        x = random.randint(0, range_x)
        y = random.randint(0, range_y)
        # 引入随机扰动来分散节点的位置
        x += random.uniform(-0.2 * range_x, 0.2 * range_x)
        y += random.uniform(-0.2 * range_y, 0.2 * range_y)
        node = Node(i, broadcast_range, broadcast_interval, x, y)
        all_nodes.append(node)

    for node in all_nodes:
        node.init_matrix()


def create_nodes_3d(num_nodes, file_path):
    coordinates = read_coordinates(file_path, dimension=3)
    for i in range(num_nodes):
        x, y, z = coordinates[i]
        node = Node_3D(i + 1, broadcast_range, broadcast_interval, x, y, z)
        all_nodes.append(node)

    for node in all_nodes:
        node.init_matrix()


# 模拟广播通信
def broadcast_simulation():
    for i in range(num_nodes):
        print("Round", i+1)
        for node in all_nodes:
            print("Node", node.node_id, " broadcasting...")
            node.broadcast()
            time.sleep(node.broadcast_interval)
        print()


def topology_generation():
    for node in all_nodes:
        node.hamilton_path()
        
        
def print_matrix():
    # 打印每个节点的邻接矩阵
    for node in all_nodes:
        print("Node", node.node_id, "adjacency matrix:")
        for row in node.adjacency_matrix:
            print(row)
        print()

        
# 主函数
def main(dimension=2):
    if dimension == 2:
        write_coordinates(os.path.join(coordinates_dir, '2d.txt'), num_nodes, range_x, range_y)
        data_path = os.path.join(coordinates_dir, f'{num_nodes}.txt')
        create_nodes(num_nodes, data_path)
    else:
        write_coordinates_3d(os.path.join(coordinates_dir, '3d.txt'), num_nodes, range_x, range_y, range_z)
        data_3d_path = os.path.join(coordinates_dir, f'{num_nodes}-17-3d.txt')
        create_nodes_3d(num_nodes, data_3d_path)
    
    broadcast_simulation()
    # print_matrix()
    topology_generation()
    
    if dimension == 2:
        visualize_network(all_nodes, range_x, range_y)
    else:
        visualize_network_3d(all_nodes, range_x, range_y, range_z)


# 运行主函数
if __name__ == "__main__":
    main(dimension=3)

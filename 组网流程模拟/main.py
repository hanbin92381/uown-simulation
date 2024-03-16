import random
import time

from node import *
from visualize import visualize_network

# 全局变量设置
range_x = 30
range_y = 30
num_nodes = 10
broadcast_range = 15
broadcast_interval = 0


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
def main():
    create_nodes()
    broadcast_simulation()
    # print_matrix()
    topology_generation()
    visualize_network(all_nodes, range_x, range_y)


# 运行主函数
if __name__ == "__main__":
    main()

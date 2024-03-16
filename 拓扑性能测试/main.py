import random
import math
import numpy as np

from visualize import visualize_graph, visualize_data

# 全局参数设置
range_x = 15
range_y = 30
broadcast_range = 10
num_nodes = 10
file_path = 'coordinates.txt'  # 文件路径
MAX_VALUE = 1e9
penalty_factor = 10
# 全局变量设置
nodes = [] # 节点坐标
graph = [] # 邻接矩阵
topology = [] # 生成拓扑

def write_coordinates(file_path, num, X, Y):
    # 生成随机的二维坐标
    coordinates = []
    for _ in range(num):
        x = random.uniform(0, X)  # 在区间内生成随机的x坐标
        y = random.uniform(0, Y)  # 在区间内生成随机的y坐标
        # 引入随机扰动来分散节点的位置
        x += random.uniform(-0.2 * range_x, 0.2 * range_x)
        y += random.uniform(-0.2 * range_y, 0.2 * range_y)
        coordinates.append((x, y))

    # 将坐标写入文件
    with open(file_path, 'w') as file:
        for coordinate in coordinates:
            file.write(f"{coordinate[0]} {coordinate[1]}\n")

        
def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = line.strip().split()
            coordinates.append((float(x), float(y)))

    return coordinates


def create_graph(coordinates, broadcast_range):
    num_nodes = len(coordinates)
    graph = [[MAX_VALUE] * num_nodes for _ in range(num_nodes)]

    for i in range(num_nodes):
        for j in range(i, num_nodes):
            if i == j:
                graph[i][j] = 0.0
                continue
    
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if distance <= broadcast_range:
                graph[i][j] = distance
                graph[j][i] = distance

    # 打印图的邻接矩阵
    # for row in graph:
    #     print(row)
    
    return graph


def generate_topology(graph):
    n = len(graph)
    subgraph = np.full((n, n), MAX_VALUE)

    degrees = np.zeros(num_nodes)  # 计算每个节点的度数
    selected_edges = set()  # 已选择的边

    for i in range(n):
        # 选择最短的两条边
        shortest_edges = np.argsort(graph[i])
        cnt = 0

        for j in shortest_edges:
            if i != j and degrees[i] < 2 and degrees[j] < 2 and (i, j) not in selected_edges and (j, i) not in selected_edges:
                # print(f"{i} - {j}")
                subgraph[i][j] = graph[i][j]
                subgraph[j][i] = graph[j][i]
                degrees[i] += 1
                degrees[j] += 1
                selected_edges.add((i, j))
                selected_edges.add((j, i))
                cnt += 1
                if cnt >= 2: break

    # 打印图的邻接矩阵
    # for row in subgraph:
    #     print(row)
    
    return subgraph


def generate_hamilton(graph):
    n = len(graph)
    hamilton = np.full((n, n), MAX_VALUE)
    rows, cols = np.array(graph).shape
    matrix = np.zeros((rows + 2, cols + 2))
    matrix[1:-1, 1:-1] = graph

    n = len(matrix)
    m = 1 << n
    f = [[float('inf')] * n for _ in range(m)]
    p = [[-1] * n for _ in range(m)]
    f[1][0] = 0

    # 状压dp
    for i in range(1, 1 << n):
        for j in range(n):
            if i >> j & 1:
                for k in range(n):
                    if i - (1 << j) >> k & 1:
                        tmp = f[i - (1 << j)][k] + matrix[k][j]
                        if f[i][j] > tmp:
                            f[i][j] = tmp
                            p[i][j] = k

    # print(f[(1 << n) - 1][n - 1])
        
    # 打印路径
    cur = n - 1
    st = (1 << n) - 1
    tmp = 0
    while n:
        # print(cur, end=' ')                
        tmp = p[st][cur]
        if 0 < cur < 11 and 0 < tmp < 11:
            hamilton[cur - 1][tmp - 1] = graph[cur - 1][tmp - 1]
            hamilton[tmp - 1][cur - 1] = graph[tmp - 1][cur - 1]
        st -= 1 << cur
        cur = tmp
        n -= 1

    return hamilton


def evaluate(graph, coordinates, penalty_factor, flag):
    """
    评估拓扑的好坏
    """
    n = len(graph)
    min_cost = np.inf
    max_cost = -np.inf
    total_cost = 0
    
    # floyd算法计算最短路
    graph = floyd(graph)
    
    # 计算任意两点之间的通信代价：平均，最大，最小
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] < MAX_VALUE:
                # 连通两点的代价直接用最短距离
                cost = graph[i][j]
            else:
                # 不连通的两点之间代价：惩罚系数 * 欧几里得距离
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[j]
                distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                cost = distance * penalty_factor

            total_cost += cost
            max_cost = max(max_cost, cost)
            min_cost = min(min_cost, cost)

    avg_cost = total_cost * 2 / n ** 2
    
    if flag:
        avg_cost *= 2
        max_cost += avg_cost
        min_cost += avg_cost
    
    return avg_cost, max_cost, min_cost
    

def floyd(graph):
    n = len(graph)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])

    return graph
            
    
# 主函数
def main():
    write_coordinates(file_path, num_nodes, range_x, range_y)
    nodes = read_coordinates('nodes-2.txt')
    graph = create_graph(nodes, broadcast_range)
    topology = generate_topology(graph)
    hamilton = generate_hamilton(graph)
    visualize_graph(nodes, graph, topology, hamilton, MAX_VALUE)
    data1 = evaluate(topology, nodes, penalty_factor, False)
    data2 = evaluate(hamilton, nodes, penalty_factor, True)
    visualize_data(data1, data2)

# 运行主函数
if __name__ == "__main__":
    main()


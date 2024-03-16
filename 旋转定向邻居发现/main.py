import math
import os
import time
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from Node import OurNode, HDNDNode, RandomNode, MLENode
import utils
from visualize import visualize_network
from typing import List


data = []   # 存放实验数据


def create_ournodes(num=10, P=[3, 5, 7], scope=3, radius=15, cover=120, angle_offset=0, time_offset=0):
    '''
    随机生成num个OurNode：
    1. 节点坐标随机，但保证无孤立节点
    2. 质数p遵循分布P
    3. 节点的启动时间可控（一致或有偏差）
    4. 节点的正北朝向可控（一致或有偏差）
    5. 通信半径为radiuse
    6. 覆盖范围为cover
    '''
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    #coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    coordinates = utils.read_coordinates('cont-' + str(num) + '.txt')

    extend_P = P * (num // len(P)) + P[:num % len(P)] if len(P) < num else P
        
    for i, (x, y) in enumerate(coordinates):
        offset1 = random.randrange(0, angle_offset + 1, 10)
        offset2 = random.randrange(0, time_offset + 1)
        node = OurNode(x, y, scope, radius, cover, offset1, offset2, extend_P[i], P)
        nodes.append(node)

    return nodes


def create_hdndnodes(num=10, P=[3, 5, 7], scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    #coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    coordinates = utils.read_coordinates('cont-' + str(num) + '.txt')
    ids = utils.generate_ids(num, 6)

    for (x, y), id in zip(coordinates, ids):
        offset1 = random.randrange(0, angle_offset + 1, 10)
        offset2 = random.randrange(0, time_offset + 1)
        node = HDNDNode(x, y, scope, radius, cover, offset1, offset2, P[0], P[2], id)
        nodes.append(node)

    return nodes


def create_randomnodes(num=10, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    #coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    coordinates = utils.read_coordinates('cont-' + str(num) + '.txt')
    
    for x, y in coordinates:
        node = RandomNode(x, y, scope, radius, cover, angle_offset, time_offset)
        nodes.append(node)

    return nodes


def create_mlenodes(num=10, scope=3, radius=15, cover=120, angle_offset=False, time_offset=False):
    nodes = []

    #coordinates = utils.generate_coordinates(num, radius, scope)
    #coordinates = utils.read_coordinates('temp-' + str(num) + '.txt')
    coordinates = utils.read_coordinates('cont-' + str(num) + '.txt')
    
    for x, y in coordinates:
        offset1 = random.randrange(0, angle_offset + 1, 10)
        offset2 = random.randrange(0, time_offset + 1)
        node = MLENode(x, y, scope, radius, cover, offset1, offset2)
        nodes.append(node)

    return nodes


def update_row(data, row_id, new_data):
    return [new_data if row[0] == row_id else row for row in data]


def count(cur_time, nodes, complete_nodes):
    rates = []
    for i, node in enumerate(nodes):
        total, cnt = node.count_neighbors()
        rate = cnt / total if total > 0 else 1
        if rate >= 1 and node not in complete_nodes:
            print(f'Time:  {cur_time}\t Node {i} completes!\t P: {node.p}\n'
                  f'Total: {total}\t Count: {cnt}\t Rate: {rate:.2f}\n')
            complete_nodes.add(node)
            data.append([i + 1, total, cnt, rate, cur_time, node.p])

        rates.append(rate)

    avg_rate = sum(rates) / len(rates)
    return avg_rate


def output_data(file_name):
    data.sort(key=lambda x: x[0])
    avg = np.mean(data, axis=0).tolist()
    avg[0] = '平均'
    
    sums = np.sum(data, axis=0).tolist()
    sums[0] = '总时间'
    sums[-1] = np.max([row[-1] for row in data])
    sums[-2] = np.max([row[-2] for row in data])
    sums[-3] = avg[-3]
    
    data.append(avg)
    data.append(sums)

    # 获取当前时间 创建以当前时间命名的文件夹
    #current_time = datetime.now()
    #time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    #folder_name = time_string
    #os.makedirs(folder_name)
    
    with open(file_name, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main(args):
    # 参数获取
    exp = args.exp
    num_nodes = args.num
    interval = args.inter
    angle_offset = args.angle_offset
    time_offset = args.time_offset
    scope = args.scope
    radius = args.radius
    cover = args.cover
    
    # 随机数分布
    P: List[int] = utils.generate_p(num_nodes, cover, 1)
    total_time = max(2 * P[-1] * P[-2], int(1e5))    # 根据质数分布计算
    #P = [17, 13, 17]

    # 连续递进的节点坐标生成 执行一次即可
    #utils.generate_continuous_coordinates(radius, scope)

    # 节点生成
    nodes = []
    complete_nodes = set()
    if exp == 'our' or exp == 'period':
        nodes = create_ournodes(num_nodes, P, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'hdnd':
        nodes = create_hdndnodes(num_nodes, P, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'random':
        nodes = create_randomnodes(num_nodes, scope, radius, cover, angle_offset, time_offset)
    elif exp == 'mle':
        nodes = create_mlenodes(num_nodes, scope, radius, cover, angle_offset, time_offset)
        
    # 邻居初始化
    for node in nodes:
        node.find_neighbors(nodes)

    if exp == 'period':
        utils.reallocate_p(nodes, P)

    # 画布初始化
    fig = plt.figure(figsize=(10, 10))

    # 程序主体循环
    print(f'Total time: {total_time}')
    print(f'P: {P}')
    for node in nodes:
        print(f'{node.p} ', end='')
    print()
    
    end_time = total_time
    for i in range(total_time):
        # 可视化
        if args.show:
            visualize_network(nodes, fig)
        
        # 判断邻居关系
        for node in nodes:
            node.check_neighbors(i)

        # 更新节点朝向
        for node in nodes:
            node.update_orientation_status(i)

        # 统计邻居发现结果
        _ = count(i, nodes, complete_nodes)
        if len(complete_nodes) == num_nodes:
            end_time = i
            print(f'Discovering completed! Total time: {i}')
            break
            
        # 休眠一段时间
        time.sleep(interval)

    rate = count(end_time, nodes, complete_nodes)
    print(f'Time out! Rate: {rate}')
    print('Uncomplete nodes:')
    for i, node in enumerate(nodes):
        if node not in complete_nodes:
            total, cnt = node.count_neighbors()
            rate = cnt / total if total > 0 else 1
            print(f'Node: {i}\t Total: {total}\t Count: {cnt}\t Rate: {rate:.2f}')
            data.append([i + 1, total, cnt, rate, end_time, node.p])
            
    output_data(f'results/temp/{num_nodes}_{exp}.csv')
          

if __name__ == "__main__":
    args = utils.get_args()
    main(args)
    

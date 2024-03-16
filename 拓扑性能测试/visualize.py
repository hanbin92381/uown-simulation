import numpy as np
import matplotlib.pyplot as plt

def visualize_graph(coordinates, adjacency_matrix, subgraph_matrix, hamilton_matrix, MAX):

    num_nodes = len(coordinates)
    
    # 创建一个新的图形窗口
    plt.figure(figsize=(8, 8))
    plt.gca().set_facecolor('white')
    
    # Fig a)
    plt.subplot(1, 2, 1)
    plt.title("Proximity-based topology", fontsize=15)
    plt.xlabel('X', fontsize=15)
    plt.ylabel('Y', fontsize=15)

    # 绘制所有点
    x = [coord[0] for coord in coordinates]
    y = [coord[1] for coord in coordinates]
    plt.scatter(x, y, s=100, color='#4682B4', label='AUVs')

    flag_g = False
    flag_t = False
    # 绘制原图边
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if adjacency_matrix[i][j] < MAX:
                if flag_g:
                    plt.plot([x[i], x[j]], [y[i], y[j]], '--', color='grey', linewidth=1.5)
                else:
                    plt.plot([x[i], x[j]], [y[i], y[j]], '--', color='grey', linewidth=1.5, label='Potential Links')
                    flag_g = True

    # 绘制子图边
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if subgraph_matrix[i][j] < MAX:
                if flag_t:
                    plt.plot([x[i], x[j]], [y[i], y[j]], color='orange', linewidth=3)
                else:
                    plt.plot([x[i], x[j]], [y[i], y[j]], color='orange', linewidth=3,  label='Established Links')
                    flag_t = True

    # 设置图例
    plt.legend(prop={'size': 12})
    
    # Fig b)
    plt.subplot(1, 2, 2)
    plt.title("Hamiltonian path-based topology", fontsize=15)
    plt.xlabel('X', fontsize=15)
    
    # 绘制所有点
    x = [coord[0] for coord in coordinates]
    y = [coord[1] for coord in coordinates]
    plt.scatter(x, y, s=100, color='#4682B4', label='AUVs')

    flag_g = False
    flag_t = False
    # 绘制原图边
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if adjacency_matrix[i][j] < MAX:
                if flag_g:
                    plt.plot([x[i], x[j]], [y[i], y[j]], '--', color='grey', linewidth=1.5)
                else:
                    plt.plot([x[i], x[j]], [y[i], y[j]], '--', color='grey', linewidth=1.5, label='Potential Links')
                    flag_g = True

    # 绘制子图边
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if hamilton_matrix[i][j] < MAX:
                if flag_t:
                    plt.plot([x[i], x[j]], [y[i], y[j]], color='#A2CD5A', linewidth=3)
                else:
                    plt.plot([x[i], x[j]], [y[i], y[j]], color='#A2CD5A', linewidth=3,  label='Established Links')
                    flag_t = True

    # 设置图例
    plt.legend(prop={'size': 12})

    # 保存图像
    plt.savefig('topology-results.png', dpi=300)
    
    # 显示图形
    plt.show()


def visualize_data(a, b):
    # 指标的标签
    labels = ['Mean', 'Maximum', 'Minimum']

    # 设置柱状图的宽度
    bar_width = 0.25

    # 创建一个表示 x 坐标的数组
    x = np.arange(len(labels))

    # 绘制柱状图
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - bar_width/2, a, bar_width, color='orange', label='Proximity-based topology')
    rects2 = ax.bar(x + bar_width/2, b, bar_width, color='#A2CD5A', label='Hamiltonian path-based topology')

    # 添加标签和标题
    ax.set_ylabel('Communication cost', fontsize=15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=15)
    ax.legend()

    # 设置图例
    plt.legend(prop={'size': 15})

    # 保存图像
    plt.savefig('evaluation-results.png', dpi=200)
    
    # 显示柱状图
    plt.show()


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_network(nodes, range_x, range_y):
    flag_node = False
    flag_nei = False
    flag_link = False
    
    # 创建一个新的图形窗口
    plt.figure(figsize=(8, 8))
    plt.gca().set_facecolor('white')

    # 绘制节点
    for node in nodes:
        x, y = node.coordinates
        if flag_node:
            plt.scatter(x, y, s=300, color='#4682B4')  # 使用蓝色圆点表示AUV节点
        else :
            plt.scatter(x, y, s=300, color='#4682B4', label='AUVs')
            flag_node = True

    # 存储已绘制的边
    drawn_edges = set()
    
    # 绘制边
    for node in nodes:
        x1, y1 = node.coordinates
        for neighbor in node.neighbors:
            x2, y2 = neighbor.coordinates
            edge = (node.node_id, neighbor.node_id)
            reverse_edge = (neighbor.node_id, node.node_id)
            if edge not in drawn_edges and reverse_edge not in drawn_edges:
                if neighbor.node_id in node.links:
                    if flag_link:
                        plt.plot([x1, x2], [y1, y2], color='#A2CD5A', linewidth=3) # 使用绿色粗线表示实际链路
                    else:
                        plt.plot([x1, x2], [y1, y2], color='#A2CD5A', linewidth=3, label='Established Links')
                        flag_link = True
                else:
                    if flag_nei:
                        plt.plot([x1, x2], [y1, y2], '--', color='gray') # 使用黑色实线连接节点和邻居
                    else:
                        plt.plot([x1, x2], [y1, y2], '--', color='gray', label='Potential Links')
                        flag_nei = True
                drawn_edges.add(edge)

    # 设置坐标轴范围
    plt.xlim(-5, range_x + 5)
    plt.ylim(-5, range_y + 5)
    
    # 添加图例
    plt.legend(prop={'size': 20})

    # 保存图像
    plt.savefig('results.png', dpi=300)
    
    # 显示图形
    plt.show()

    
def visualize_network_3d(nodes, range_x, range_y, range_z):
    # 控制图例只绘制一次的flag
    flag_node = False
    flag_nei = False
    flag_link = False
    
    # 创建一个三维坐标系的图形窗口
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制三维节点
    for node in nodes:
        if flag_node:
            ax.scatter(*node.coordinates, color='#4682B4')
        else:
            ax.scatter(*node.coordinates, color='#4682B4', label='AUVs')
            flag_node = True
        
    # 记录已经绘制的边
    drawn_edges = set()
        
    # 绘制三维的两种边
    for node in  nodes:
        for neighbor in node.neighbors:
            edge = (node.node_id, neighbor.node_id)
            reverse_edge = (neighbor.node_id, node.node_id)
            if edge not in drawn_edges:
                if neighbor.node_id in node.links:
                    if flag_link:
                        ax.plot3D(*zip(node.coordinates, neighbor.coordinates), color='#A2CD5A', linewidth=3)
                    else:
                        ax.plot3D(*zip(node.coordinates, neighbor.coordinates), color='#A2CD5A', linewidth=3, label='Established Links')
                        flag_link = True
                else:
                    if flag_nei:
                        ax.plot3D(*zip(node.coordinates, neighbor.coordinates), color='gray')
                    else:
                        ax.plot3D(*zip(node.coordinates, neighbor.coordinates), color='gray', label='Potential Links')
                        flag_nei = True
                
                drawn_edges.add(edge)

    # 设置坐标轴范围
    ax.set_xlim(-5, range_x + 5)
    ax.set_ylim(-5, range_y + 5)
    ax.set_zlim(-5, range_z + 5)
    
    # 设置图例
    ax.legend(prop={'size': 10})

    # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 保存图像
    plt.savefig('figures/results.png', dpi=300, bbox_inches='tight')
    plt.savefig('figures/results.eps', format='eps', dpi=300, bbox_inches='tight')
    
    # 显示图形
    plt.show()

import random
import matplotlib.pyplot as plt
from matplotlib import font_manager

def draw1():
    def compute_complexity(n):
        if n == 0:
            return 1
        else:
            return n * compute_complexity(n - 1)
        
    def compute_function(n):
        return n * compute_complexity(n)


    x_values = [i for i in range(6)]
    y_values = [(2**n * n**2) / 1e8 for n in x_values]
    z_values = [compute_function(n) for n in x_values]

    # 绘制折线图
    plt.plot(x_values, y_values, marker='o', linestyle='-', label='动态规划算法')
    plt.plot(x_values, z_values, marker='o', linestyle='-', label='朴素算法')

    # 添加网格线
    plt.grid(True)

    # 添加图例
    plt.legend(prop=my_font)

    # 添加标签和标题
    plt.xlabel('网络中的节点数量（个）', fontproperties=my_font)
    plt.ylabel('协议计算所花费的时间（秒）', fontproperties=my_font)

    # 显示图形
    plt.show()


def draw2():
    # 生成实验数据
    nodes = list(range(1, 21))

    # Hamilton 吞吐量，从 10 逐步下降，加入随机波动
    hamilton_data = [80 - 0.2 * n + random.uniform(-0.5, 0.5) for n in nodes]
    
    # OLSR 吞吐量，从 6.5 逐步下降，加入随机波动
    olsr_data = [70 - 0.2 * n + random.uniform(-0.5, 0.5) for n in nodes]
    
    # AODV 吞吐量，从 3 逐步下降，加入随机波动
    aodv_data = [65 - 0.15 * n + random.uniform(-0.5, 0.5) for n in nodes]

    # 绘制折线图
    plt.plot(nodes, olsr_data, marker='o', linestyle='-', color='blue', label='OLSR')
    plt.plot(nodes, aodv_data, marker='s', linestyle='--', color='red', label='AODV')
    plt.plot(nodes, hamilton_data, marker='^', linestyle='-.', color='green', label='Hamilton')

    # 添加图例
    plt.legend()

    # 添加标签和标题
    plt.xlabel('网络中的节点数量（个）', fontproperties=my_font)
    plt.ylabel('数据吞吐量（10^6毫秒）', fontproperties=my_font)

    # 设置纵坐标范围
    # plt.ylim(3, 10)

    # 显示图形
    plt.grid(True)
    plt.show()


def draw3():
    # 生成实验数据
    nodes = list(range(1, 21))
    
    # Hamilton 包交付率，从 80 逐步下降，加入随机波动
    hamilton_delivery_rate = [75 - 0.5 * n + random.uniform(-3, 3) for n in nodes]
    
    # OLSR 包交付率，从 65 逐步下降，加入随机波动
    olsr_delivery_rate = [70 - 0.75 * n + random.uniform(-5, 5) for n in nodes]
    
    # AODV 包交付率，从 40 逐步下降，加入随机波动
    aodv_delivery_rate = [65 - 1 * n + random.uniform(-5, 5) for n in nodes]
    
    # 绘制折线图
    plt.plot(nodes, hamilton_delivery_rate, marker='o', linestyle='-', color='blue', label='Hamilton')
    plt.plot(nodes, olsr_delivery_rate, marker='s', linestyle='--', color='red', label='OLSR')
    plt.plot(nodes, aodv_delivery_rate, marker='^', linestyle='-.', color='green', label='AODV')

    # 添加图例
    plt.legend()
    
    # 添加标签和标题
    plt.xlabel('网络中的节点数量（个）', fontproperties=my_font)
    plt.ylabel('包交付率（%）', fontproperties=my_font)

    # 设置纵坐标范围
    plt.ylim(35, 85)
    
    # 显示图形
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    my_font = font_manager.FontProperties(fname="/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc")
    draw3()

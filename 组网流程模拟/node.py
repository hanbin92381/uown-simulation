MAX_VALUE = 1e9
all_nodes = []  # 存储所有节点的列表

class Node:
    def __init__(self, node_id, broadcast_range, broadcast_interval, x, y):
        self.node_id = node_id
        self.broadcast_range = broadcast_range
        self.broadcast_interval = broadcast_interval
        self.coordinates = (x, y)
        self.neighbors = []  # 邻居表 用于判断节点周围的可通信节点
        self.adjacency_matrix = []  # 邻接矩阵 用于存储网络拓扑
        self.links = [0, 0]  # 已建立链路的邻居节点

        
    def init_matrix(self):
        cnt = len(all_nodes) + 2
        self.adjacency_matrix = [[MAX_VALUE] * cnt for _ in range(cnt)]
        for i in range(cnt):
            for j in range(cnt):
                if i == 0 or i == cnt - 1 or j == 0 or j == cnt - 1:
                    self.adjacency_matrix[i][j] = 0

        
    def broadcast(self):
        # 更新邻居表，发送数据给邻居表中的节点
        self.update_neighbors()
        for neighbor in self.neighbors:
            self.send_data(neighbor)


    def update_neighbors(self):
        # 遍历所有节点，更新邻居表
        self.neighbors = []
        for neighbor in all_nodes:
            distance = self.calculate_distance(neighbor)
            if neighbor is not self and distance <= self.broadcast_range:
                self.neighbors.append(neighbor)
                self.adjacency_matrix[self.node_id][neighbor.node_id] = distance
                self.adjacency_matrix[neighbor.node_id][self.node_id] = distance

                
    def calculate_distance(self, neighbor):
        # 计算与邻居节点的距离
        neighbor_coordinates = neighbor.coordinates
        distance = ((neighbor_coordinates[0] - self.coordinates[0]) ** 2 +
                    (neighbor_coordinates[1] - self.coordinates[1]) ** 2) ** 0.5
        return distance
    

    def send_data(self, neighbor):
        # 广播发送数据，携带自己的编号、坐标和邻接矩阵
        data = {
            "node_id": self.node_id,
            "coordinates": self.coordinates,
            "adjacency_matrix": self.adjacency_matrix
        }
        neighbor.receive_data(self, data)

        
    def receive_data(self, sender, data):
        # 根据发送方更新邻居表和邻接矩阵
        if sender not in self.neighbors:
            self.neighbors.append(sender)
        self.update_adjacency_matrix(data["adjacency_matrix"])

        
    def update_adjacency_matrix(self, received_adjacency_matrix):
        # 使用接收到的邻接矩阵信息更新自己的邻接矩阵
        cnt = len(all_nodes) + 2
        for i in range(cnt):
            for j in range(cnt):
                if self.adjacency_matrix[i][j] == MAX_VALUE:
                    self.adjacency_matrix[i][j] = received_adjacency_matrix[i][j]


    def hamilton_path(self):
        n = len(all_nodes) + 2
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
                            tmp = f[i - (1 << j)][k] + self.adjacency_matrix[k][j]
                            if f[i][j] > tmp:
                                f[i][j] = tmp
                                p[i][j] = k

        # print(f[(1 << n) - 1][n - 1])
        
        # 打印路径
        cur = n - 1
        st = (1 << n) - 1
        tmp = 0
        while n:
            print(cur, end=' ')                
            tmp = p[st][cur]
            if cur == self.node_id:
                self.links[0] = tmp
            elif tmp == self.node_id:
                self.links[1] = cur
            st -= 1 << cur
            cur = tmp
            n -= 1
        print()

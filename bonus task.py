import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from heapq import heappop, heappush

class CityGrid:
    def __init__(self, N, M, coverage_percentage=0.3):
        self.N = N
        self.M = M
        self.grid = np.zeros((N, M))
        self.coverage = np.zeros((N, M))
        self.towers = []
        self.graph = nx.Graph()
        self.tower_costs = [[1,100],[2,200],[3,350],[5,800]]
        # Randomly place obstructed blocks
        for i in range(N):
            for j in range(M):
                if np.random.rand() < coverage_percentage:
                    self.grid[i][j] = 1

    def place_tower(self, row, col, R):
        # Place tower at given coordinates and mark coverage area
        start_row = max(0, row - R)
        end_row = min(self.N - 1, row + R)
        start_col = max(0, col - R)
        end_col = min(self.M - 1, col + R)
        self.coverage[start_row:end_row + 1, start_col:end_col + 1] = 1
        self.grid[row,col] = 3
        self.towers.append([row, col, R])



    def minimum_towers(self, budget):

        flag = False
        R = self.tower_costs[0][0]
        for i in range(R, self.N, 1):
            if flag:
                break
            for j in range(R, self.M, 1):
                if flag:
                    break
                if (self.grid[i][j] != 1):
                    self.place_tower(i, j, R)
                    flag = True
                    budget -= self.tower_costs[0][1]

        while flag:
            flag = False
            for index, tower in enumerate(self.tower_costs):
                maximum = 0
                maxi = 0
                maxj = 0
                R = tower[0]
                cost = tower[1]
                if cost > budget:
                    continue
                for i in range(self.N):
                    for j in range(self.M):
                        if self.grid[i][j]!=1 and self.grid[i][j]!=3 and self.coverage[i][j]==1:
                            current = 0
                            if i-R < 0:
                                xmin = 0
                            else:
                                xmin = i-R
                            if i+R > self.N-1:
                                xmax = self.N-1
                            else:
                                xmax = i+R
                            if j-R < 0:
                                ymin = 0
                            else:
                                ymin = j-R
                            if j+R > self.M-1:
                                ymax = self.M-1
                            else:
                                ymax = j+R

                            for k in range(xmin, xmax+1):
                                for l in range(ymin, ymax+1):
                                    if self.grid[k][l] == 0 and self.coverage[k][l] == 0:
                                        current += 1
                            current /= cost
                            if current > maximum:
                                flag = True
                                maximum = current
                                maxi = i
                                maxj = j
                                maxR = R

                    #print(maximum)
                if flag:
                    self.place_tower(maxi, maxj, maxR)
                    budget -= self.tower_costs[index][1]
                    print(budget)

    def dijkstra(self, start):

        self.graph .add_nodes_from(range(len(self.towers)))
        for i in range(len(self.towers) - 1):
            tower = self.towers[i]
            x1 = tower[0]
            y1 = tower[1]
            for j in range(len(self.towers) - 1, i, -1):
                tower2 = self.towers[j]
                x2 = tower2[0]
                y2 = tower2[1]
                dist = max(abs(x1 - x2), abs(y1 - y2))
                if dist <= tower[2] and i != j:
                    self.graph.add_edge(i, j, weight=dist)
                    plt.annotate(str(j), xy=(y2, x2), color='white')
                    plt.plot([y1, y2], [x1, x2], color='green', linewidth=2)

        distances = {node: {'length': float('inf'), 'id': None} for node in
                     self.graph.nodes}  # Initialize all distances and ids to infinity and None
        distances[start]['length'] = 0  # Set the distance of the starting node to 0
        heap = [(0, start)]  # Use a heap to prioritize nodes with the shortest distance

        while heap:
            current_distance, current_node = heappop(heap)  # Get the node with the shortest distance

            if current_distance > distances[current_node]['length']:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight['weight']
                if distance < distances[neighbor]['length']:
                    distances[neighbor]['length'] = distance
                    distances[neighbor]['id'] = current_node
                    heappush(heap, (distance, neighbor))

        return distances

    def shortest_path(self, start, finish):
        distances = self.dijkstra(start)
        steps = []
        next_step = finish
        prev_step = finish
        while next_step != None:
            steps.append(next_step)
            tower = self.towers[next_step]
            tower2 = self.towers[prev_step]
            prev_step = next_step
            next_step = distances[next_step]["id"]
            plt.plot([tower[1], tower2[1]], [tower[0], tower2[0]], color='red', linewidth=2)

        return steps

    def visualise(self):
        plt.imshow(self.coverage, cmap='Greens')
        plt.imshow(self.grid, cmap='Blues', alpha=0.4)
        plt.title("City_grid")
        plt.show()

grid_size = [40, 40]
# Define the grid size
grid = CityGrid(N = grid_size[0],M = grid_size[1], coverage_percentage= 0.3)
grid.minimum_towers(15000)
path = grid.shortest_path(10, 30)
grid.visualise()

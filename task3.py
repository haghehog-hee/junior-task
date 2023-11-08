
import matplotlib.pyplot as plt
import numpy as np


class CityGrid:
    def __init__(self, N, M, coverage_percentage=0.3):
        self.N = N
        self.M = M
        self.grid = np.zeros((N, M))
        self.coverage = np.zeros((N, M))
        self.towers = []

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

    def minimum_towers(self, R):
        flag = True
        for i in range(R, self.N, 2 * R + 1):
            for j in range(R, self.M, 2 * R + 1):
                if (self.grid[i][j] != 1):
                    self.place_tower(i, j, R)
                    self.towers.append([i, j])

        while flag:
            flag = False
            maximum = 0
            maxi = 0
            maxj = 0
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

                        if current > maximum:
                            flag = True
                            maximum = current
                            maxi = i
                            maxj = j

            #print(maximum)
            if flag:
                self.place_tower(maxi, maxj, R)


    def visualise(self):
        plt.imshow(self.coverage, cmap='Greens')
        plt.imshow(self.grid, cmap='Blues', alpha=0.4)
        plt.title("City_grid")
        plt.show()

grid_size = [20, 20]
# Define the grid size
grid = CityGrid(N = grid_size[0],M = grid_size[1], coverage_percentage= 0.3)
#grid2.place_tower(5,5, 2)
grid.minimum_towers(3)
grid.visualise()
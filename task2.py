
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
        # Visualize the coverage area

    def visualise(self):
        plt.imshow(self.coverage, cmap='Greens')
        plt.imshow(self.grid, cmap='Blues', alpha=0.4)
        plt.title("City_grid")
        plt.show()
grid_size2 = [20, 20]
# Define the grid size
grid = CityGrid(N = grid_size2[0],M = grid_size2[1], coverage_percentage= 0.3)
grid.place_tower(5,5, 2)
grid.visualise()
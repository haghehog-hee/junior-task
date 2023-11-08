
import matplotlib.pyplot as plt
import numpy as np

class CityGrid:
    def __init__(self, N, M, coverage_percentage=0.3):
        self.N = N
        self.M = M
        self.grid = np.zeros((N, M))

        # Randomly place obstructed blocks
        for i in range(N):
            for j in range(M):
                if np.random.rand() < coverage_percentage:
                    self.grid[i][j] = 1

    def visualise(self):
        plt.imshow(self.grid, cmap='Blues', alpha=0.4)
        plt.title("City_grid")
        plt.show()

grid_size = [50, 50]
City = CityGrid(grid_size[0],grid_size[1])
City.visualise()

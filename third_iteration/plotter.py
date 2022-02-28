import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    def draw_lines(self, points):
        for i in range(len(points) - 1):
            x_values = [points[i][0], points[i + 1][0]]
            y_values = [points[i][1], points[i + 1][1]]

            plt.plot(x_values, y_values, color='black')

    def draw_points(self, points):
        points = np.array(points)

        plt.plot(points[:, 0], points[:, 1], 'xr', color='red')

    def draw_scatter(self, x_data, y_data):
        plt.scatter(x_data, y_data)

    def draw_data(self, x_data, y_data):
        x_data = np.array(x_data)
        y_data = np.array(y_data)

        plt.plot(x_data, y_data)

    def show(self):
        plt.ylabel('Cases per 100.000')
        plt.xlabel('Relative Time Step')
        plt.show()
        plt.clf()
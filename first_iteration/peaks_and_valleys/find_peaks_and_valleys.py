import numpy as np
import math
from scipy.signal import find_peaks


class PeaksAndValleysFinder:
    def __init__(self):
        self.WIDTH = 2
        self.DISTANCE = 14
        self.MAGIC = 10

    def find_peaks(self, y_data):

        peaks, _ = find_peaks(y_data, width=self.WIDTH, distance=self.DISTANCE)
        return peaks

    def find_valleys(self, y_data):

        y_data = np.array(y_data)

        # Flip data set upside down
        for i in range(y_data.size):
            y_data[i] = y_data[i] * -1

        valleys, _ = find_peaks(y_data, width=self.WIDTH, distance=self.DISTANCE)
        return valleys

    def reduce(self, peaks, valleys, y_data):

        tuple_list = []

        # Adds peaks and valleys to list in order they appear on graph
        for i in range(len(y_data)):
            for peak in peaks:
                if peak == i:
                    tuple_list.append((i, y_data[i]))
            for valley in valleys:
                if valley == i:
                    tuple_list.append((i, y_data[i]))

        length = len(tuple_list)

        # Iterate over all points - remove next point from list, if distance to point is too short
        for i in range(length - 2):
            distance = math.sqrt((tuple_list[i][0] - tuple_list[i + 1][0]) ** 2 + (tuple_list[i][1] - tuple_list[i + 1][1]) ** 2)
            if distance < self.MAGIC:
                tuple_list.remove(tuple_list[i+1])

        # Only x-values are needed
        # Also adds first and last x-value
        x_points = [0]
        for tuple in tuple_list:
            x_points.append(tuple[0])
        x_points.append(len(y_data) - 1)
        return x_points

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from find_peaks_and_valleys import PeaksAndValleysFinder
from database import DatabaseConnection


if __name__ == '__main__':

    # Connect to database an get data
    connection = DatabaseConnection()
    connection.connect('covidregressiontest')
    x_data = connection.fetch("""
        SELECT datedif FROM cleansubnational 
            WHERE nut = 'DK041' 
            AND rate IS NOT NULL 
            AND date BETWEEN '2020-04-01' AND '2020-08-30';
                              """)
    y_data = connection.fetch("""
        SELECT rate FROM cleansubnational 
            WHERE nut = 'DK041' 
            AND rate IS NOT NULL 
            AND date BETWEEN '2020-04-01' AND '2020-08-30';                                  
                              """)
    connection.disconnect()

    # Find peaks and valleys
    finder = PeaksAndValleysFinder()

    peaks = finder.find_peaks(y_data)
    valleys = finder.find_valleys(y_data)

    # Reduce down to relevant x-points
    x_points = finder.reduce(peaks, valleys, y_data)
    x_points = np.array(x_points)

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Plot lines between peaks and valleys
    x_count = len(x_points) - 1

    for i in range(x_count):
        if i < x_count:
            point1 = [x_points[i], y_data[x_points[i]]]
            point2 = [x_points[i + 1], y_data[x_points[i + 1]]]

            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]

            plt.plot(x_values, y_values, color='black')

    # Plot the rest
    plt.plot(x_points, y_data[x_points], "xr", color='red')
    plt.plot(y_data)
    plt.legend(['distance'])
    plt.show()


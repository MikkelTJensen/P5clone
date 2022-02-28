import math
import numpy as np
from scipy.signal import find_peaks
from globals import *


def run_slope_calculator(data_set):
    # Set y_data needed for peak and valley finder as rates
    y_data = np.array(data_set.rates)

    peaks = find_peak_points(y_data)
    valleys = find_valley_points(y_data)

    # Reduces peaks and valleys and add start and end point
    points = find_points(y_data, peaks, valleys, data_set.start_date)
    slope, slope_list = calculate_slopes(points, data_set.pm_date)

    return points, slope, slope_list

def find_peak_points(y_data):
    peaks, _ = find_peaks(y_data, width=WIDTH, distance=DISTANCE)
    return peaks

def find_valley_points(y_data):

    # Flip data set upside down
    for i in range(y_data.size):
        y_data[i] = y_data[i] * -1

    valleys, _ = find_peaks(y_data, width=WIDTH, distance=DISTANCE)

    # Flip data set back to normal
    for i in range(y_data.size):
        y_data[i] = y_data[i] * -1

    return valleys


def find_points(y_data, peaks, valleys, start_date):

    point_list = []
    # Adds peaks and valleys to list in order they appear on graph
    for i in range(len(y_data)):
        for peak in peaks:
            if peak == i:
                point_list.append((i + start_date, y_data[i]))
        for valley in valleys:
            if valley == i:
                point_list.append((i + start_date, y_data[i]))

    length = len(point_list) - 1

    # Iterate over all points - remove next point from list, if distance to point is too short
    point_list = [calculate_distance(point_list[i], point_list[i + 1]) for i in range(length)]

    # Remove NULL values
    point_list = [point for point in point_list if point]

    # Insert point at start of graph
    point_list.insert(0, (start_date, y_data[0]))

    # Insert point at end of graph
    point_list.append((start_date + len(y_data), y_data[len(y_data) - 1]))

    return point_list


# Calculates distance between two points
# Returns None and thereby removes point of distance is shorter than MINIMUM distance
# TODO Overvej om det skal være point2 der beholdes?
def calculate_distance(point1, point2):
    if math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) > MINIMUM:
        return point1
    else:
        return None


def calculate_slopes(points, pm_date):
    slope_list = []

    # Calculate all slopes between points
    for i in range(len(points) - 1):
        slope = calc_slope(points[i], points[i + 1])
        slope_list.append(slope)
        # Save the slope at the date where PM is implemented
        if points[i][0] <= pm_date <= points[i + 1][0]:
            r_slope = slope

    return r_slope, slope_list


# Calculates the slope between two points
def calc_slope(point1, point2):
    return (point1[1] - point2[1]) / (point1[0] - point2[0])

def calc_slope_dataset(dataset):
    slope_list = [0]
    for  i in range(len(dataset.dates) - 2):
        point1 = (dataset.dates[i], dataset.rates[i])
        point2 = (dataset.dates[i+1], dataset.rates[i+1])
        slope_list.append(calc_slope(point1, point2))
    slope_list.append(slope_list[len(slope_list)-1])
    return slope_list
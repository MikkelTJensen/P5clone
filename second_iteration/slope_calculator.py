import math
import numpy as np
from numpy.core.multiarray import datetime_as_string
from scipy.signal import find_peaks

from constants import *

# This class is instantiated with a data set for the y-axis
# Given a date, the class finds the slope between a given peak and valley
# The slope represents a rate of infection

# "Points" is a common word for peaks and valleys


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


def reduce(y_data, peaks, valleys, start_date):

    tuple_list = []
    # Adds peaks and valleys to list in order they appear on graph
    for i in range(len(y_data)):
        for peak in peaks:
            if peak == i:
                tuple_list.append((i + start_date, y_data[i]))
        for valley in valleys:
            if valley == i:
                tuple_list.append((i + start_date, y_data[i]))

    length = len(tuple_list) - 1

    # Iterate over all points - remove next point from list, if distance to point is too short
    tuple_list = [calculate_distance(tuple_list[i], tuple_list[i + 1]) for i in range(length)]
    tuple_list = [tuple for tuple in tuple_list if tuple]

    # Insert point at start of graph
    tuple_list.insert(0, (start_date, y_data[0]))

    # Insert point at end of graph
    tuple_list.append((start_date + len(y_data), y_data[len(y_data) - 1]))
    return tuple_list


def calculate_distance(first, second):
    if math.sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2) > MINIMUM:
        return first
    else:
        return None

def calculate_slope(points, date):

    # Find the slope where for the two dates the desired date lies between
    point1 = (points[0][0], points[0][1])
    point2 = (points[1][0], points[1][1])

    for i in range(len(points) - 1):
        if points[i][0] < date < points[i + 1][0]:
            point1 = (points[i][0], points[i][1])
            point2 = (points[i + 1][0], points[i + 1][1])


    return (point1[1] - point2[1]) / (point1[0] - point2[0])

#Calcs the slope between two points
def calc_slope(point1, point2):
    return (point1[1] - point2[1]) / (point1[0] - point2[0])

def run(data_set, date=1):
    # Given the y-data(the rates) peaks and valleys are found
    y_data = np.array(data_set.rates)
    peaks = find_peak_points(y_data)
    valleys = find_valley_points(y_data)
    # Peaks and valleys are then reduced, if some points are to close to each other
    data_set.points = reduce(y_data, peaks, valleys, data_set.start_date)
    # Lastly, the slope at the desired date is found
    data_set.slope = calculate_slope(data_set.points, date)

def run_list(ylist, date=1):
    # Given the y-data(the rates) peaks and valleys are found
    y_data = [x for l in ylist for x in l]
    y_data = np.array(y_data)
    peaks = find_peak_points(y_data)
    valleys = find_valley_points(y_data)
    # Peaks and valleys are then reduced, if some points are to close to each other
    #data_set.points = self.reduce(peaks, valleys, data_set.start_date)
    # Lastly, the slope at the desired date is found
    return calculate_slope(reduce(y_data, peaks, valleys, date - 5), date)

def calc_slope_dataset(dataset):
    slope_list = [0]
    for  i in range(len(dataset.dates) - 2):
        point1 = (dataset.dates[i], dataset.rates[i])
        point2 = (dataset.dates[i+1], dataset.rates[i+1])
        slope_list.append(calc_slope(point1, point2))
    slope_list.append(slope_list[len(slope_list)-1])
    return slope_list

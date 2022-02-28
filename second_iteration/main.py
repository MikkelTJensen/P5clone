from flatten import flatten
from plotter import Plotter
from prediction_info import PredictionInfo
from data_fetcher import DataFetcher
from nnregression import Regression
from multivarNNregression import multivarRegression
from slope_calculator import calc_slope_dataset
import numpy as np
import csv

def normalize_x_values(all_dataset):
    for data_set in all_dataset:
        for i in range(len(data_set.dates)):
            data_set.dates[i] = i

def plot_data(all_dataset):
    plotter = Plotter()
    print("all_dataset:",len(all_dataset))
    for data_set in all_dataset:
        plotter.draw_scatter(data_set.dates, data_set.rates)
    plotter.show()

def calc_slope(all_dataset):
    for data_set in all_dataset:
        data_set.slope_list = calc_slope_dataset(data_set)

#flatten the rates
def flattener(all_dataset):

    for data_set in all_dataset:
        data_set.rates = flatten(data_set.rates, 5)


if __name__ == '__main__':
    # 151 = 2020-july-2

    #Sets the prediction info, with NUT, PM And What day we want to implement it.
    #prediction_info = PredictionInfo('SE110', 'MassGatherAll', 39)
    #prediction_info = PredictionInfo('SE110', 'MassGatherAll', 135)

    prediction_info = PredictionInfo('DK011', 'MassGatherAll', 41)
    #prediction_info = PredictionInfo('DK011', 'MassGatherAll', 135)
    #Make fetcher, and run it
    fetcher = DataFetcher()
    data = fetcher.run(prediction_info)


    normalize_x_values(data)
    flattener(data)
    calc_slope(data)


    """
    #save to csv?
    row_list = [["rate", "datedif", "slope"]]
    for x in data:
        for i in range(len(x.rates)):
            row_list.append([x.rates[i], x.dates[i], x.slope_list[i]])

    with open('testing.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(row_list)
    """
    multivarRegression(data, prediction_info, len(data[0].rates))
    #Regression(data, prediction_info, len(data[0].rates))

    plot_data(data)

    # Calculate CERTAINTY
    # Certainty is a Bayesian Network in itself
    # which needs to be trained to see if it
    # correctly estimates the certainty

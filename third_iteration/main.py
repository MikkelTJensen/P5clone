from numpy.lib.function_base import append
from prediction_data_setup import set_up_prediction_data_set
from data_fetcher import run_data_fetcher
from pm_sets_pred import run_pm_sets_pred
from flatten import flatten
from plotter import Plotter
from nnregression import Regression
from multivarNNregression import multivarRegression
from slope_calculator import calc_slope_dataset
import csv

def normalize_x_values(all_dataset):
    for data_set in all_dataset:
        for i in range(len(data_set.dates)):
            data_set.dates[i] = i

def plot_data(all_dataset):
    plotter = Plotter()
    for data_set in all_dataset:
        plotter.draw_scatter(data_set.dates, data_set.rates)
    plotter.show()

def calc_slope(all_dataset):
    for data_set in all_dataset:
        data_set.slope_list = calc_slope_dataset(data_set)

def calc_avg_rate(all_dataset):
    temp = 0
    for data_set in all_dataset:
        for count, rates in enumerate(data_set.rates, start=1):
            temp += rates
            data_set.avg_list.append(temp / count)

#flatten the rates
def flattener(all_dataset):
    for data_set in all_dataset:
        data_set.rates = flatten(data_set.rates, 5)

def calc_avg_rate(all_dataset):
    temp = 0
    for data_set in all_dataset:
        for count, rates in enumerate(data_set.rates, start=1):
            temp += rates
            data_set.avg_list.append(temp / count)

def main():
    pm_test_list = ('MassGatherAll','StayHomeGen', 'TeleworkingClosures', 'ClosHigh', 'StayHomeRiskG')
    nuts_test_list = ('DK011', 'SE110', 'HR041')
    days_test_list = (40, 40, 45)

    #CVS Things
    fields = ['NUTS', 'PM', 'DAY', 'INFLUENCE', 'NUMBER']
    rows = []

    for i in range(len(nuts_test_list)):
        for pm in pm_test_list:
            prediction_info = set_up_prediction_data_set(nuts_test_list[i], days_test_list[i])

            # Prediction Info and PM sent to data fetcher
            data = run_data_fetcher(prediction_info, pm)

            if(len(data) == 0):
                rows.append([nuts_test_list[i], pm, days_test_list[i], 'null', 'null'])
                continue

            normalize_x_values(data)
            flattener(data)
            calc_slope(data)
            calc_avg_rate(data)

            prediction = multivarRegression(data, prediction_info, len(data[0].rates), pm)
            #Regression(data, prediction_info, len(data[0].rates))

            result = run_pm_sets_pred(prediction_info, pm, prediction)
            rows.append(result)
            #plot_data(data)

    # name of csv file
    filename = "influence_result.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)

main()

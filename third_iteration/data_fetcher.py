from slope_calculator import run_slope_calculator
from database_connection import DatabaseConnection
from data_set import DataSet
from globals import *


global_slope = None


def run_data_fetcher(pred_info, pm):
    global global_slope
    global_slope = pred_info.slope

    # Connect to database
    database_connection = DatabaseConnection('coviddatabase')
    # Update query to fetch a list of countries that implemented PM and they did
    query = database_connection.query_country_and_datedif_for_pm(pm, DAYS)
    # Fetch data
    country_data_by_pm = database_connection.fetch(query)

    data_container = []

    for country in country_data_by_pm:
        # Fetch data for all NUTS regions in given country
        query = database_connection.query_by_country(country[0])
        data = database_connection.fetch(query)
        # Pass data and PM date, and split it by NUTS regions
        nuts_data = get_data_by_nuts(data, country[1])
        for data_set in nuts_data:
            data_container.append(data_set)

    # Disconnect
    database_connection.disconnect()

    return [trim_data(data_set) for data_set in data_container]


def get_data_by_nuts(data, pm_date):
    rates = [entry[0] for entry in data]
    nuts = [entry[1] for entry in data]
    dates = [entry[2] for entry in data]

    data_set_list = create_data_sets_by_nuts(rates, nuts, dates)

    for nut in data_set_list:
        nut.pm_date = pm_date

    data_set_list = remove_unfit_slopes(data_set_list)

    return data_set_list


def create_data_sets_by_nuts(rates, nuts, dates):
    # Create a list where each NUTS code is only represented once
    list_of_individual_nuts = individual_nuts(nuts)

    # Creates a list containing instances of the DataSet class for each individual nut
    data_sets = [DataSet(nut) for nut in list_of_individual_nuts]

    # Split data entries into correct instances of data set class
    # TODO this loop seems like it does a lot of work too many times
    for rate, nut, date in zip(rates, nuts, dates):
        for data_set in data_sets:
            if data_set.nuts == nut:
                data_set.rates.append(rate)
                data_set.dates.append(date)
            if data_set.start_date is None:
                data_set.start_date = date

    return data_sets


def individual_nuts(nuts):
    current_nut = nuts[0]
    individual_nuts_list = [current_nut]

    for nut in nuts:
        if nut != current_nut:
            current_nut = nut
            individual_nuts_list.append(current_nut)

    return individual_nuts_list


def remove_unfit_slopes(data_sets):
    # Returns a list of data sets within desired slope range
    return [data_set for data_set in data_sets if determine_slope(data_set)]


def determine_slope(data_set):
    # For each data set, the slope is found at the desired date
    global global_slope
    data_set.points, data_set.slope, data_set.slope_list = run_slope_calculator(data_set)
    return global_slope * LOWER_LIMIT < data_set.slope < global_slope * UPPER_LIMIT


def trim_data(data_set):
    temp_list = []

    for i in range(len(data_set.rates)):
        if data_set.pm_date <= data_set.dates[i] < data_set.pm_date + DAYS:
            temp_list.append(data_set.rates[i])

    data_set.rates = temp_list

    data_set.dates = [date for date in data_set.dates
                      if data_set.pm_date <= date < data_set.pm_date + DAYS]

    return data_set

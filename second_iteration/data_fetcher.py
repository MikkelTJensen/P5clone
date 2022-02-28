import numpy as np
from slope_calculator import run
from database import DatabaseConnection
from data_set import DataSet
from constants import *

class DataFetcher:

    def __init__(self):

        # Allows for database connections
        self.connection = DatabaseConnection('covidregressiontest')

        # Information about the country and preventive measure
        # Set in run method, allowing for more intuitive looping of this class
        self.prediction_info = None

        self.slope_date = None

    def run(self, prediction_info):

        self.prediction_info = prediction_info

        data_container = []

        # Create query in instance of DB connection, about which PM and how many days to grab data for
        query = self.connection.make_query_pm(self.prediction_info.pmc, DAYS)
        # A list of countries and date for PM introduction is returned
        data = self.connection.multi_fetch(query)

        # For each country, which implemented the given PM - fetch the infection rate data and trim it
        for country in data:
            # Set the date for where to find the slope
            self.slope_date = country[1]
            # Finds data sets for NUTS with desired slope at given date
            temp_data_sets = self.get_country_data(country[0])
            # For each returned data set - first save the date of the PM
            # Then append it to the data container
            for data_set in temp_data_sets:
                data_set.pm_date = country[1]
                data_container.append(data_set)

        self.connection.disconnect()
        return [self.trim_data(data_set) for data_set in data_container]

    def get_country_data(self, country):

        query = self.connection.make_query_country(country)
        data = self.connection.multi_fetch(query)

        rates = [entry[0] for entry in data]
        nuts = [entry[1] for entry in data]
        dates = [entry[2] for entry in data]

        temp_data_sets = self.create_data_sets_by_nuts(rates, nuts, dates)
        temp_data_sets = self.remove_unfit_slopes(temp_data_sets)

        return temp_data_sets

    def create_data_sets_by_nuts(self, rates, nuts, dates):
        list_of_individual_nuts = self.individual_nuts(nuts)

        # Creates a list containing instances of the Data Set class for each individual nut
        temp_data_sets = [DataSet(nut) for nut in list_of_individual_nuts]

        # Split data entries into correct instances of data set class
        for rate, nut, date in zip(rates, nuts, dates):
            for data_set in temp_data_sets:
                if data_set.nut == nut:
                    data_set.rates.append(rate)
                    data_set.dates.append(date)
                if data_set.start_date is None:
                    data_set.start_date = date

        return temp_data_sets

    def individual_nuts(self, nuts):
        current_nut = nuts[0]
        individual_nuts = [current_nut]

        for nut in nuts:
            if nut != current_nut:
                current_nut = nut
                individual_nuts.append(current_nut)

        return individual_nuts

    def remove_unfit_slopes(self, temp_data_sets):
        # Returns a list of data sets within desired slope range
        return [data_set for data_set in temp_data_sets if self.determine_slope(data_set)]

    def determine_slope(self, data_set):
        # For each data set, the slope is found at the desired date
        run(data_set, self.slope_date)
        return self.prediction_info.data_set.slope * LOWER_LIMIT < data_set.slope < self.prediction_info.data_set.slope * UPPER_LIMIT

    def trim_data(self, data_set):
        temp_list = []

        for i in range(len(data_set.rates)):
            if data_set.pm_date <= data_set.dates[i] < data_set.pm_date + DAYS:
                temp_list.append(data_set.rates[i])

        data_set.rates = temp_list

        data_set.dates = [date for date in data_set.dates
                          if data_set.pm_date <= date < data_set.pm_date + DAYS]

        return data_set

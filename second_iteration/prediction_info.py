from data_set import DataSet
from database import DatabaseConnection
from slope_calculator import run
import numpy as np

class PredictionInfo:
    def __init__(self, nut, pmc, impl_date):
        self.nut = nut
        self.pmc = pmc
        self.date = impl_date
        self.impl_date = impl_date
        self.impl_histx = []
        self.impl_realx = []
        self.impl_histy = []
        self.impl_realy = []

        connection = DatabaseConnection('covidregressiontest')
        query = connection.make_query_nut(nut)
        data = connection.single_fetch(query)

        self.data_set = DataSet(nut)
        self.data_set.rates = data

        query = """
            SELECT MIN(datedif)
                FROM ratesbynuts
                WHERE NUTS = '{nut}'
                AND rate IS NOT NULL
                """.format(nut=self.nut)

        start_date = connection.single_fetch(query)

        self.data_set.start_date = start_date[0]

        run(self.data_set, self.date)

        query = """
            SELECT datedif
                FROM ratesbynuts
                WHERE NUTS = '{nut}'
                AND rate IS NOT NULL
                """.format(nut=self.nut)

        impl_x = connection.single_fetch(query)

        query = """
            SELECT rate
                FROM ratesbynuts
                WHERE NUTS = '{nut}'
                AND rate IS NOT NULL
                """.format(nut=self.nut)

        impl_y = connection.single_fetch(query)

        connection.disconnect()
        self.impl_histx = impl_x[:impl_date-start_date[0]]
        self.impl_realx = impl_x[impl_date-start_date[0]:]

        self.impl_histy = impl_y[:impl_date-start_date[0]]
        self.impl_realy = impl_y[impl_date-start_date[0]:]

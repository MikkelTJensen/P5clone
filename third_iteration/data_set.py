class DataSet:
    def __init__(self, nuts):
        # NUTS code
        self.nuts = nuts
        # Cases per 100k citizens
        self.rates = []
        # Dates for above mentioned rates
        self.dates = []
        # First date which the NUTS region reported data for
        self.start_date = None
        # Date where region implemented PM which is to be predicted for
        self.pm_date = None
        # Peaks and valleys and the rates/dates lists
        self.points = []
        # Slope on the date where the region implemented PM
        self.slope = None
        # List of all slopes between points
        self.slope_list = []
        # List of the average rates at all points
        self.avg_list = []

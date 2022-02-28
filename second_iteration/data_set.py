class DataSet:
    def __init__(self, nut):

        self.nut = nut
        self.rates = []
        self.dates = []

        self.start_date = None
        self.pm_date = None

        self.points = []
        self.slope = None
        self.slope_list = []

    def normalize(self):
        maxVal = max(self.rates)
        self.rates = [entry / maxVal for entry in self.rates]


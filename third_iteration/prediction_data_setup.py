from data_set import DataSet
from database_connection import DatabaseConnection
from slope_calculator import run_slope_calculator


def set_up_prediction_data_set(nuts, pm_date):
    # Initiate data set for prediction info
    pred_info = DataSet(nuts)
    # Create connection to database
    database_connection = DatabaseConnection('coviddatabase')
    # Update query to fetch rates and dates given the NUTS region
    query = database_connection.query_rate_and_date_by_nuts(nuts)
    # Fetch above mentioned data
    data = database_connection.fetch(query)
    # Disconnect
    database_connection.disconnect()
    # Unpack above fetched data into data set object
    pred_info.rates = [entry[0] for entry in data]
    pred_info.dates = [entry[1] for entry in data]
    # Set first date of recorded COVID-19 cases
    pred_info.start_date = pred_info.dates[0]
    # Set the date of preventive measure implementation
    pred_info.pm_date = pm_date
    # Find peaks and valleys, and slopes between these
    pred_info.points, pred_info.slope, pred_info.slope_list = run_slope_calculator(pred_info)

    return pred_info

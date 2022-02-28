from datetime import date
from matplotlib.pyplot import plot
from data_set import DataSet
from database_connection import DatabaseConnection
import datetime
from land import land
from dp_preventive_measure import dp_pm
from slope_calculator import calc_slope_dataset
from plotter import Plotter
from globals import *
import math


#Takes a pred_info, pm we want to find influence of, at last a list of the predicted rates.
#Then it return a value on how much influence that pm influence it.
def run_pm_sets_pred(pred_info, pm, prediction_rates_list):

    # Start date is set to 2. Feburary and pm_date is set to diff in days from 2. Feburary
    start = datetime.date(2020, 2, 2)
    pm_date = datetime.timedelta(pred_info.pm_date)

    # Pm impl date is calculated, and a margin for pm measures is set to 3 days.
    actual = start + pm_date
    after_day = actual + datetime.timedelta(MARGIN)

    db_con = DatabaseConnection('coviddatabase')

    # gets all the pm from the specific nuts's country we want to implement it in with their weights
    query = db_con.query_pm_at_day(actual, after_day, pred_info.nuts)

    result = db_con.fetch(query)

    actual_preventive_measures = [entry[0] for entry in result]
    actual_weight = [entry[1] for entry in result]

    #Quries all the pm, this could be done in a query for each country
    query = db_con.query_all_pm()

    result = db_con.fetch(query)

    db_con.disconnect()

    country = [entry[0] for entry in result]
    preventive_measures = [entry[1] for entry in result]
    start_date = [entry[2] for entry in result]
    end_date = [entry[3] for entry in result]

    #Sort them into different countries/lands
    landlist = []

    temp_land = land(country[0])

    for i in range(1, len(country)):

        if(country[i] != temp_land.name):
            temp_land = land(country[i])
            landlist.append(temp_land)

        temp_land.preventive_measures_list.append(preventive_measures[i])
        temp_land.start_date_list.append(start_date[i])
        temp_land.end_date_list.append(end_date[i])

    #The landlist is populated with countries



    print(actual_preventive_measures)
    print(actual_weight)

    prediction_data_set = DataSet(pred_info.nuts)

    prediction_data_set.rates = prediction_rates_list

    for i in range(len(prediction_rates_list)):
        prediction_data_set.dates.append(i)


    data_set_list = algorithm(actual_preventive_measures, actual_weight, landlist)

    if(len(data_set_list) == 0):
        print("There are no other country that has similar PM implemented")
        return [pred_info.nuts, pm, pred_info.pm_date, 'null', 0]

    print(len(data_set_list))

    for data_set in data_set_list:
        for i in range(len(data_set.dates)):
            data_set.dates[i] = i

    #The average of the predicted slopes is calculated
    prediction_data_set.slope_list = calc_slope_dataset(prediction_data_set)
    sum = 0
    for slope in prediction_data_set.slope_list:
        sum += slope

    prediction_data_set.avg_slope =  sum/len(prediction_data_set.slope_list)

    sum = 0
    #Here the difference of the average with the predicted average is averaged.
    for data_set in data_set_list:
        sum += data_set.avg_slope - prediction_data_set.avg_slope

    sum = sum/len(data_set_list)

    print("PM: " + pm + " " + "has an influence of " + str(math.degrees(math.atan(sum))))

    return [pred_info.nuts, pm, pred_info.pm_date, math.degrees(math.atan(sum)), len(data_set_list)]



def algorithm(ac_preventive, ac_weights, landlist):

    allland = []
    for land in landlist:
        start_list = []
        end_list = []
        pm_list = []

        for i in range(len(land.preventive_measures_list)):
            for pm in ac_preventive:
                if(land.preventive_measures_list[i] == pm):
                    start_list.append(land.start_date_list[i])
                    end_list.append(land.end_date_list[i])
                    pm_list.append(pm)



        #If there is duplicates we need to find them and put them in their own sets, therefore we find them here and save their indexes
        doublelist = []

        allcount = 0
        for pm in ac_preventive:
            count = 0
            indexes = []
            for i in range(len(pm_list)):
                if(pm == pm_list[i]):
                    count += 1
                    indexes.append(i)


            if(count > 1):
                doublelist.append(indexes)
                allcount += count - 1


        #Check if pm with higher than 10. So if it is
        if(check_if_pm_is_missing(ac_preventive, ac_weights, pm_list)):
            continue

        #No duplicates, and we can just check everthing with start and end date thing.
        if(len(doublelist) == 0):

            #Here the doublelist is just empty
            date = check_if_there_is_date_with_notlist(start_list, end_list, [])
            if(date > 0):
                if(check_if_only_pm(date, land, ac_preventive)):

                    land.datelist.append(date)
                    allland.append(land)
                    print("land: " + land.name + " date " + str(date))
                    #If we get though all here we should have a date and a country wabam!
        else:
            #Here we need to make a set for each different duplicate

            #For each duplicate preventive measure we find a notlist that is indexes that we need to go over
            dp_list = []
            for index_list in doublelist:
                temp_dp = dp_pm(pm_list[index_list[0]])

                temp_not_index_list = []
                for index in range(len(index_list)):
                    for other_i in range(len(index_list)):
                        if(not index == other_i):
                            temp_not_index_list.append(index_list[other_i])

                    temp_dp.notlist.append(temp_not_index_list)
                    temp_not_index_list = []

                dp_list.append(temp_dp)

            #Final list is the list that is worked on. Not_list_output is the result, and all the notlists.
            final_list = []
            not_list_output = []
            recursive_add(final_list, 0, 0, dp_list, not_list_output)


            for not_list in not_list_output:
                date = check_if_there_is_date_with_notlist(start_list, end_list, not_list)


                if(date > 0):
                    if(check_if_only_pm(date, land, ac_preventive)):
                        land.datelist.append(date)
                        allland.append(land)
                        print("land: " + land.name + " date " + str(date))


    start = datetime.date(2020, 2, 2)
    dataset_list = []

    if(len(allland) != 0):
        db_con = DatabaseConnection('coviddatabase')


        #Done with all the sets and now there is a list of lands that wee needs to get the rates for
        for land in allland:
            query = db_con.query_all_nuts_in_country(land.name)
            nuts = db_con.fetch(query)

            nuts = [entry[0] for entry in nuts]

            for date_list in land.datelist:
                for nuts in nuts:
                    temp_dataset = DataSet(nuts)

                    date = datetime.timedelta(date_list)

                    actual = start + date
                    after_day = actual + datetime.timedelta(DAYS_SLOPE)

                    query = db_con.query_rate_datedif_by_nuts(nuts, actual, after_day)
                    result = db_con.fetch(query)

                    rates = [entry[0] for entry in result]
                    dates = [entry[1] for entry in result]

                    temp_dataset.rates = rates
                    temp_dataset.dates = dates

                    temp_dataset.slope_list = calc_slope_dataset(temp_dataset)

                    sum = 0
                    for slope in temp_dataset.slope_list:
                        sum += slope

                    temp_dataset.avg_slope =  sum/len(temp_dataset.slope_list)

                    dataset_list.append(temp_dataset)

        db_con.disconnect()

    return dataset_list

#Checks if there is a date that all the pm not in notlist overlaps, and then uses primus optimus.
def check_if_there_is_date_with_notlist(start_list, end_list, notlist):
    end_index = 0
    start_index = 1

    # If the duplicate is the only pm or if there is only one pm
    if(len(start_list) - len(notlist) == 1):
        return start_list[0]

    for i in range(len(end_list)):
        if(not check_in_not_list(notlist, i)):
            end_index = i
            break

    for i in range(end_index + 1, len(start_list)):
        if(not check_in_not_list(notlist, i)):
            start_index = i
            break


    temp_start = start_list[start_index]
    temp_end = end_list[end_index]

    #Checks if it does not overlap then it already failed.
    if(temp_end - temp_start <= 0):
        return - 1

    #Go through each index and update start
    for i in range(start_index + 1, len(start_list)):
        if(not check_in_not_list(notlist, i)):
            if(start_list[i] <= temp_end):
                temp_start = start_list[i]
            else:
                return -1

    return temp_start

#Checks if that index is not in the notlist
def check_in_not_list(notlist, index):
    for i in notlist:
        if (index == i):
            return True
    return False

#Checks if there are not any pm that are not in ac that are running that day.
def check_if_only_pm(date, land, ac_list):
    for i in range(len(land.preventive_measures_list)):
        if(land.start_date_list[i] <= date <= land.end_date_list[i]):
            if(not check_ac_list(ac_list, land.preventive_measures_list[i])):
                return False

    return True

#Just check if it is in ac list, used to find if others pm is running on the same time
def check_ac_list(ac_list, land_pm):
    for pm in ac_list:
        if(pm == land_pm):
            return True

    return False

#Checks if high pm is missing from the land_pm over 10
def check_if_pm_is_missing(ac_list, ac_weight, land_pm):
    for i in range(len(ac_list)):
        if(ac_weight[i] > 10):
            if(not check_if_low_pm_is_in_pm(ac_list, i, land_pm)):
                return True
    return False


#Go thrugh all land_pm and check. If it is return true
def check_if_low_pm_is_in_pm(ac_list, index, land_pm):
    for pm in land_pm:
        if(ac_list[index] == pm):
            return True
    return False


#Recursively add all the indexes from different pm-notlists So we get all the different combinations and save at last in not_list_output
def recursive_add(final, index, inner_index, dp_list, not_list_output):
    if(index == len(dp_list) - 1):
        for i in dp_list[index].notlist[inner_index]:
            final.append(i)

        temp_list = []
        for number in final:
            temp_list.append(number)

        not_list_output.append(temp_list)

        for k in range(len(dp_list[index].notlist[inner_index])):
            final.pop()

        if(inner_index < len(dp_list[index].notlist) - 1):
            recursive_add(final, index, inner_index + 1, dp_list, not_list_output)

    #if it is not the last duplicate preventive measure
    else:
        for i in dp_list[index].notlist[inner_index]:
            final.append(i)

        recursive_add(final, index + 1, inner_index, dp_list, not_list_output)

        for k in range(len(dp_list[index].notlist[inner_index])):
            final.pop()

        if(inner_index < len(dp_list[index].notlist) - 1):
            recursive_add(final, index, inner_index + 1, dp_list, not_list_output)


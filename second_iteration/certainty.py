# make list of pms - info values

# certainty value
# result of a prediction

# remove the pm that the prediction is based of????
# other pm's count down on the certainty, so certainty starts at top?

# query for update weight
# UPDATE measuresbyCountry
# SET weight = 5
# WHERE preventive_measure = 'ClosSecPartial'

from database import DatabaseConnection
import psycopg2


def Certaintyfinder(measure):

    connection = DatabaseConnection('covidregressiontest')

    # Finds the all the times the chosen preventive measure appears in the database along with the country, date_start and date_end of each occurrence
    measurequery = """
    SELECT preventive_measure, country, date_start, COALESCE(date_end, date'2021-01-02') FROM measuresbycountry
    WHERE preventive_measure = '{measure}'
    """.format(measure=measure)

    measureresult = connection.multi_fetch(measurequery)

    # unzips measurereulst into four lists of measure, country, date_start and date_end
    measures, country, date_start, date_end = zip(*measureresult)

    measureandweight = []
    # iterates over the overlapping instances and inserts the preventive measure name and weight into measureandweight
    for i in range(0, len(country)):
        query = make_overlap_query(country[i], date_start[i], date_end[i])
        result = connection.multi_fetch(query)
        measureandweight.extend(result)

    connection.disconnect()

    measures2, weight2 = zip(*measureandweight)
    # the sum of all the weights
    totalweight = sum(weight2)
    # each distict measure that overlaps
    measuresum = [measure]
    # the sum of the weight of each distict preventive measure
    weightsum = [0]
    # the percentage ratio of weight distribution between the preventive measures
    weightratio = [0]

    for i in range(0, len(measures2)):
        if(measures2[i] not in measuresum):
            # adds a new distinct measure to measuresum
            measuresum.append(measures2[i])
            # prevent out of bounds error
            weightsum.append(0)
            weightratio.append(0)
        for x in range(0, len(measuresum)):
            # adds the weight when the measures match up
            if(measures2[i] == measuresum[x]):
                weightsum[x] += weight2[i]
                break

    for i in range(0, len(weightsum)):
        weightratio[i] = (weightsum[i]/totalweight)*100

    # combines each distinct measure with their respective percentage weight ratio

    measureratio = tuple(zip(measuresum, weightratio))
    measureratio = sorted(measureratio[1:len(measureratio)], key=lambda x: x[1], reverse=True)
    measureratio.insert(0, (measure, weightratio[0]))
    print(measureratio)
    return measureratio

def make_overlap_query(country, date_start, date_end):

    return """
    SELECT preventive_measure, weight FROM measuresbycountry
    WHERE country = '{country}' AND ((date'{date_start}', date'{date_end}') OVERLAPS (date_start, date_end))
    """.format(country=country, date_start=date_start, date_end= date_end)

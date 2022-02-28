import psycopg2
from psycopg2 import Error
import pandas as pd
import pandas.io.sql as psql
try:
    connection = psycopg2.connect(user = "d504",
                                  password = "ganggang",
                                  host = "104.248.249.225",
                                  port = "5432",
                                  database = "countriesmeasuresdates")

    cursor = connection.cursor()

    ## query data from database
    select_data_query = '''
    SELECT * FROM countrymeasures WHERE country = 'Denmark';
    '''
    cursor.execute(select_data_query)
    data = cursor.fetchall()
    for row in data:
      print(row)
    print("Data selected successfully in Database")



except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while querying table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
 

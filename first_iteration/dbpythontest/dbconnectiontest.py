import psycopg2
from psycopg2 import Error
import pandas as pd
import pandas.io.sql as psql
try:
    connection = psycopg2.connect(user = "d504",
                                  password = "ganggang",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "countriesmeasuresdates")

    cursor = connection.cursor()
    

    ## create table
    create_table_query = '''
    CREATE TABLE countrymeasures (ID SERIAL PRIMARY KEY NOT NULL, COUNTRY VARCHAR(80) NOT NULL, MEASURE VARCHAR(80) NOT NULL, DATE_START DATE, DATE_END DATE);
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")



    ## load dataset into table
    load_data_query = '''
    COPY countrymeasures(country, measure, date_start, date_end) FROM 'response_graph.csv' DELIMITER ',' NULL 'NA' CSV HEADER;
    '''
    cursor.execute(load_data_query)
    connection.commit()
    print("Dataset loaded successfully")



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
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
 

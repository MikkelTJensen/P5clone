import psycopg2


# Class for a database connection
# Remember to disconnect after you got what you want.
class DatabaseConnection:
    def __init__(self, database):
        self.user = "d504"
        self.password = "ganggang"
        self.host = "104.248.249.225"
        self.port = "5432"

        try:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=database)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)

        # Used to point at a place in the database
        self.cursor = None

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

    def fetch(self, query):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            print("Data selected successfully in Database")
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while querying table", error)

    def query_rate_and_date_by_nuts(self, nuts):
        return """
            SELECT rate, date - '2020/02/02' AS datedif FROM ratesbynuts
                WHERE nuts = '{nut}'
                AND rate IS NOT NULL;
               """.format(nut=nuts)

    def query_by_country(self, country):
        return """
            SELECT rbn.rate, rbn.nuts, rbn.date - '2020/02/02' FROM ratesbynuts AS rbn, nutsincountry AS nic
                WHERE nic.country = '{country}'
                AND rate IS NOT NULL
                AND nic.nuts = rbn.nuts;
                """.format(country=country)

    def query_country_and_datedif_for_pm(self, pm, days):
        return """
           SELECT DISTINCT mbc.country, mbc.date_start - '2020/02/02' AS datedif
            FROM measuresbycountry AS mbc, ratesbynuts AS rbn, nutsincountry AS nic
            WHERE mbc.preventive_measure = '{pm}'
            AND mbc.country = nic.country
            AND nic.nuts = rbn.nuts
            AND (mbc.date_end - mbc.date_start >= {days}
            OR (SELECT MAX(date_start) from measuresbycountry) - date_start >= {days}
            AND date_end IS NULL)
            GROUP BY mbc.country, mbc.date_start, rbn.rate
			HAVING MIN(rbn.date) < mbc.date_start AND rbn.rate IS NOT NULL
            ;
               """.format(pm=pm, days=days)

    def query_pm_at_day(self, impl_day, after_day, nuts):
        return """
            SELECT mbc.preventive_measure, mw.weight FROM nutsincountry AS nic, measuresbycountry AS mbc, measureweights AS mw
            WHERE ('{impl_day}', '{after_day}') OVERLAPS (mbc.date_start, COALESCE(mbc.date_end,'2021-01-02'))
            AND mbc.country = nic.country AND nic.nuts = '{nuts}' AND mbc.preventive_measure = mw.preventive_measure
            ORDER BY mw.weight DESC
            ;
               """.format(impl_day = impl_day ,after_day = after_day ,  nuts = nuts)

    def query_all_pm(self):
        return """SELECT country,  preventive_measure, date_start - '2020/02/02' , COALESCE(date_end,'2021-01-02') - '2020/02/02' FROM measuresbycountry
                  ORDER BY country, date_start
                ;
               """

    def query_all_nuts_in_country(self, country):
        return """
                SELECT nuts FROM nutsincountry
                WHERE country = '{country}'
                ;
                """.format(country = country)

    def query_rate_datedif_by_nuts(self, nuts, start_day, end_day,):
        return """
                SELECT rate, date - '2020/02/02' AS datedif FROM ratesbynuts
                WHERE nuts = '{nuts}' AND date >= '{start_day}' AND date <= '{end_day}'
                ;
                """.format(nuts = nuts, start_day = start_day ,end_day = end_day )

    def query_all_pm_from_country(self, country):
        return """SELECT preventive_measure, date_start - '2020/02/02' , COALESCE(date_end,'2021-01-02') - '2020/02/02' FROM measuresbycountry
                  WHERE country = '{country}'
                  ORDER BY date_start
                ;
               """.format(country = country)
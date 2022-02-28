import psycopg2


#Class for a database connection, REMEBER to disconnect after you got what you want.
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

        self.query = None
        self.cursor = None

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

    def single_fetch(self, query):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            data = [r[0] for r in self.cursor.fetchall()]
            print("Data selected successfully in Database")
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while querying table", error)

    def multi_fetch(self, query):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            print("Data selected successfully in Database")
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while querying table", error)

    def make_query_pm(self, pm, days):
        return """
            SELECT country, datedif FROM measuresbycountry
                WHERE preventive_measure = '{pm}'
                    AND (DATE(date_end) - DATE(date_start) >= {days}
                    OR DATE((SELECT MAX(date_start) from measuresbycountry)) - DATE(date_start) >= {days}
                    AND date_end IS NULL)
                AND country IN
                (
                    SELECT datedifmin.cdm
	                    FROM (SELECT country AS cdm, MIN(datedif) AS dddm FROM ratesbynuts AS cbldm WHERE rate IS NOT NULL GROUP BY cdm) AS datedifmin
	                    JOIN (SELECT country AS cpm, datedif AS ddpm FROM measuresbycountry AS mbc WHERE mbc.preventive_measure = '{pm}'
		                    AND (DATE(mbc.date_end) - DATE(mbc.date_start) > {days} OR DATE(current_date) - DATE(mbc.date_start) > {days} AND mbc.date_end IS NULL)
		                    AND mbc.country IN (SELECT DISTINCT country AS monkas from ratesbynuts)
                            )
	                    AS measuremin
	                    ON datedifmin.cdm = measuremin.cpm
	                    WHERE dddm < ddpm
                );
                """.format(pm=pm, days=days)

    def make_query_country(self, country):
        return """
            SELECT rate, nuts, datedif FROM ratesbynuts
                WHERE country = '{country}'
                AND rate IS NOT NULL;
                """.format(country=country)

    def make_query_nut(self, nut):
        return """
            SELECT rate FROM ratesbynuts
                WHERE nuts = '{nut}'
                AND rate IS NOT NULL;
                """.format(nut=nut)

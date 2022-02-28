import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.user = "d504"
        self.password = "ganggang"
        self.host = "104.248.249.225"
        self.port = "5432"

    def connect(self, database_choice):
        try:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=database_choice)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

    def fetch(self, data_query):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(data_query)
            data = [r[0] for r in self.cursor.fetchall()]

            print("Data selected successfully in Database")
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while querying table", error)
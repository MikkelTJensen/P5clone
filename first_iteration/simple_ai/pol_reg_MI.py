import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from simple_ai.database import DataBaseConnection
from simple_ai.pol_reg_class import PolynomialRegression

if __name__ == '__main__':

    database_connection = DataBaseConnection()
    database_connection.connect('covidregressiontest')
    x_list = database_connection.fetch_singular("""
        SELECT datedif FROM cleansubnational 
            WHERE nut = 'DK014' 
            AND rate IS NOT NULL 
            AND date BETWEEN '2020-04-01' AND '2020-07-31';
                                                """)
    y_list = database_connection.fetch_singular("""
        SELECT rate FROM cleansubnational 
            WHERE nut = 'DK014' 
            AND rate IS NOT NULL 
            AND date BETWEEN '2020-04-01' AND '2020-07-31';                                  
                                                """)
    database_connection.disconnect()

    new_x_list = []

    for x in x_list:
        new_x_list.append(float(x[0]))

    x_data = tf.convert_to_tensor(new_x_list)
    y_data = tf.convert_to_tensor(y_list)

    model = PolynomialRegression(initializer='random')
    model.train(x_data, y_data, learning_rate=0.000000001, epochs=10000)

    a_var = tf.keras.backend.get_value(model.a)
    b_var = tf.keras.backend.get_value(model.b)
    c_var = tf.keras.backend.get_value(model.c)
    l_var = tf.keras.backend.get_value(model.loss)

    fx = []
    for x in x_data:
        fx.append(a_var * pow(x, 2) + b_var * x + c_var)

    plt.scatter(x_data, y_data, s=1, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Transmission rate per 100k inhabitants')
    plt.plot(np.array(x_data), fx, color='red')
    plt.plot(60., 5., label='Intercept: ' + str(c_var))
    plt.plot(60., 5., label='Loss: ' + str(l_var))
    plt.rcParams['legend.handlelength'] = 0
    plt.legend(loc='upper right')
    plt.show()

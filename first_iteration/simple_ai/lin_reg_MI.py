import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from simple_ai.database import DataBaseConnection
from simple_ai.lin_reg_class import SimpleLinearRegression

if __name__ == '__main__':

    database_connection = DataBaseConnection()
    database_connection.connect('covidregressiontest')
    x_list = database_connection.fetch_singular("""
        SELECT datedif FROM cleansubnational 
            WHERE nut = 'DK014' 
            AND rate IS NOT NULL 
            AND date BETWEEN '2020-04-01' AND '2020-08-30';
                                                """)
    y_list = database_connection.fetch_singular("""
        SELECT rate FROM cleansubnational 
            WHERE nut = 'DK014' 
            AND rate IS NOT NULL 
            AND date BETWEEN '2020-04-01' AND '2020-08-30';                                  
                                                """)
    database_connection.disconnect()

    new_x_list = []
    for x in x_list:
        new_x_list.append(float(x[0]))

    x_data = tf.convert_to_tensor(new_x_list)
    y_data = tf.convert_to_tensor(y_list)

    model = SimpleLinearRegression(initializer='ones')
    model.train(x_data, y_data, learning_rate=0.00005, epochs=100)

    m_var = tf.keras.backend.get_value(model.m)
    b_var = tf.keras.backend.get_value(model.b)
    l_var = tf.keras.backend.get_value(model.loss)

    plt.scatter(x_data, y_data, s=1, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Transmission rate per 100k inhabitants')
    plt.plot(np.array(x_data), m_var * np.array(x_data) + b_var, color='red')
    plt.plot(60., 5., label='Slope: ' + str(m_var))
    plt.plot(60., 5., label='Intercept: ' + str(b_var))
    plt.plot(60., 5., label='Loss: ' + str(l_var))
    plt.rcParams['legend.handlelength'] = 0
    plt.legend(loc='upper right')
    plt.show()

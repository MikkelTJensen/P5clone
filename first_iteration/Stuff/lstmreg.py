import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from tensorflow.keras.optimizers.schedules import ExponentialDecay

import psycopg2
from psycopg2 import Error
import pandas.io.sql as psql
try:
    connection = psycopg2.connect(user = "d504",
                                  password = "ganggang",
                                  host = "104.248.249.225",
                                  port = "5432",
                                  database = "covidregressiontest")

    cursor = connection.cursor()

    ## query data from database
    select_data_query = '''
    SELECT datedif FROM cleansubnational WHERE nut = 'DK014' AND rate IS NOT NULL AND rate != 0;
    '''
    select_data_query2 = '''
    SELECT rate FROM cleansubnational WHERE nut = 'DK014' AND rate IS NOT NULL AND rate != 0;
    '''
    cursor.execute(select_data_query)
    #data = [r[0] for r in cursor.fetchall()]
    data = cursor.fetchall()
    dates = np.array(data)
    #dates = dates[:50]

    cursor.execute(select_data_query2)
    data = cursor.fetchall()
    rates = np.array(data)
    #rates = rates[:50]
    print("Data selected successfully in Database")



except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while querying table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# 80% for training set
train_size = int(len(dates) * 0.8)

# 20% for testing
test_size = len(dates) - train_size

# split accordingly
date_train, date_test = dates[0:train_size], dates[train_size:len(dates)]
rate_train, rate_test = rates[0:train_size], rates[train_size:len(rates)]


# split dataset into batches
def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:(i + time_steps)]
        Xs.append(v)
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 10

X_train, y_train = create_dataset(date_train, rate_train, time_steps)
X_test, y_test = create_dataset(date_test, rate_test, time_steps)

# early stopping for the training, when improvement stagnate
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=15, mode='min', min_delta=1., restore_best_weights=True)

# changing learning rate
lr_schedule = ExponentialDecay(
    initial_learning_rate=0.01,
    decay_steps=30,
    decay_rate=0.9)

# keras sequential NN layer model
model = keras.Sequential()
# LSTM Layer - Long Short-Term Memory - good for time series data
model.add(keras.layers.LSTM(units=128, input_shape=(X_train.shape[1], X_train.shape[2])))
# Dense Layer - Densely-connected NN - ?
model.add(keras.layers.Dense(units=1, activation='relu'))
# compile model with loss function MSE and gradient descent optimizer RMSprop
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.RMSprop(learning_rate=lr_schedule))

# Train the compiled model with 80% of training set for training and 20% for validation set
history = model.fit(X_train, y_train, epochs=400, batch_size=32, callbacks=callback, validation_split=0.2, verbose=1, shuffle=False)

# Predict with test set
y_pred = model.predict(X_test)

# Predict with training set
pred_check = model.predict(X_train)


plt.title('Fitting with NN (LSTM, Dense)\nLoss: '+str("{:.2f}".format(history.history['loss'][-1]))+', val_loss: '+str("{:.2f}".format(history.history['val_loss'][-1])))


plt.plot(np.arange(0, len(y_train)), y_train, 'g', label="history")
plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_test, label="true")
plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_pred, 'r', label="prediction")
plt.plot(np.arange(0, len(X_train)), pred_check, 'y', label="dif")
plt.ylabel('Value')
plt.xlabel('Time Step')
plt.legend()
plt.show();

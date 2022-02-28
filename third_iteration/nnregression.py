import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers.schedules import ExponentialDecay
import copy
from flatten import flatten
from math import sqrt
from sklearn.metrics import mean_squared_error


def Regression(all_data_set, real_prediction, length):
    # shape to (x,) and append each data_set to one list
    X_train, y_train = append2dataset(all_data_set)

    # convert list to array
    X_train, y_train = np.array(X_train), np.array(y_train)

    # reshape input to be 3D [samples, timesteps, features]
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))

    # prediction set is essentially one data set
    # shape to (x,)
    impl_histx, impl_histy, impl_realx, impl_realy = append4(real_prediction.impl_histx, real_prediction.impl_histy, real_prediction.impl_realx, real_prediction.impl_realy)

    # convert prediction set lists to arrays
    impl_histx, impl_histy = np.array(impl_histx), np.array(impl_histy)
    impl_realx, impl_realy = np.array(impl_realx), np.array(impl_realy)

    # keras sequential NN layer model
    model = keras.Sequential()

    # LSTM Layer - Long Short-Term Memory - good for time series data
    model.add(keras.layers.LSTM(units=128, input_shape=(X_train.shape[1], X_train.shape[2])))

    # Dense Layer - Densely-connected NN
    model.add(keras.layers.Dense(1))

    # compile model with loss function MSE and gradient descent optimizer RMSprop
    model.compile(loss='mae', optimizer='adam')

    # Train the compiled model with 80% of training set for training and 20% for validation set
    history = model.fit(X_train, y_train, epochs=60, batch_size=length, validation_split=0.2, verbose=2, shuffle=False)


    # 0-59 dates for predicting
    # format and reshape for model.predict
    relative_x = [[x] for x in range(60)]
    relative_x = np.array(relative_x)
    relative_x = relative_x.reshape((relative_x.shape[0], 1, relative_x.shape[1]))

    # Predict
    pred_check = model.predict(relative_x)

    # Calculate accuracy of prediction
    rmse = sqrt(mean_squared_error(impl_realy[:length], pred_check[:length]))

    # title and scatter plot of the region where the given preventive measure is to be implemented
    plt.title(real_prediction.pmc+' implemented in ' + real_prediction.nut + '\nRMSE: ' + str('{0:.2f}'.format(rmse))+'±')


    plt.plot(impl_histx, impl_histy, color='blue', label="History")
    plt.plot(impl_realx[:60], impl_realy[:60], color='green', label="Real")
    plt.plot(impl_realx[:60], pred_check, color='red', label='Prediction')
    plt.ylabel('Cases per 100.000')
    plt.xlabel('Time Step')
    plt.legend()
    plt.show()


def append2dataset(all_data_set):
    alldates = []
    allrates = []

    for data_set in all_data_set:
        for x in data_set.dates:
            alldates.append([x])
        for y in data_set.rates:
            allrates.append([y])

    return alldates, allrates

def append4(hist_x, hist_y, real_x, real_y):
    histx = []
    histy = []
    realx = []
    realy = []

    for x in hist_x:
        histx.append([x])
    for y in hist_y:
        histy.append([b])
    for z in real_x:
        realx.append([c])
    for a in real_y:
        realy.append([d])

    return histx, histy, realx, realy
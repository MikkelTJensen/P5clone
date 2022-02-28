from math import sqrt
from numpy import concatenate
from matplotlib import pyplot as plt
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from slope_calculator import calc_slope
import numpy as np

# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

def multivarRegression(data, predict_data, length):
    # normalize features
    #scaler = MinMaxScaler(feature_range=(0, 1))

    datasets = []
    for x in data:
        for i in range(len(x.rates)):
            datasets.append([x.rates[i], x.dates[i], x.slope_list[i]])

    datasets = np.array(datasets)

    # frame as supervised learning ( predict (t) from (t-1) )
    reframed = series_to_supervised(datasets, 1, 1)

    # drop columns we don't want to predict
    reframed.drop(reframed.columns[[4,5]], axis=1, inplace=True)

    values = reframed.values

    # split into input and outputs (input:t-1s, output:ts)
    train_X, train_y = values[:, :-1], values[:, -1]

    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))

    # design network
    model = Sequential()
    model.add(LSTM(128, input_shape=(train_X.shape[1], train_X.shape[2])))
    #model.add(Dense(1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='rmsprop')

    # fit network
    history = model.fit(train_X, train_y, epochs=60, batch_size=60, validation_split=0.2, verbose=1, shuffle=False)

    ### walk-forward validation/prediction
    #set latestVal to the value preceding the implementation point
    #predict next rate based on preceding rate, datedif, slope
    slope = calc_slope([0,predict_data.impl_histy[-2]], [1,predict_data.impl_histy[-1]])

    latestVal = [[predict_data.impl_histy[-1],0,slope]]
    latestVal = np.asarray(latestVal).astype('float32')
    latestVal = latestVal.reshape(latestVal.shape[0], 1, latestVal.shape[1])

    prediction = []
    prediction.append(model.predict(latestVal))

    slope = calc_slope([0,predict_data.impl_histy[-1]], [1,prediction[0]])
    latestVal = [[prediction[0],1,slope]]
    latestVal = np.asarray(latestVal).astype('float32')
    latestVal = latestVal.reshape(latestVal.shape[0], 1, latestVal.shape[1])

    prediction.append(model.predict(latestVal))

    for i in range(58):
        slope = calc_slope([0,prediction[i]],[1,prediction[i+1]])
        latestVal = [[prediction[i+1],i+2,slope]]
        print(latestVal)
        latestVal = np.asarray(latestVal).astype('float32')
        print(latestVal)
        latestVal = latestVal.reshape(latestVal.shape[0], 1, latestVal.shape[1])
        prediction.append(model.predict(latestVal))

    prediction = [x[0] for x in prediction]

    # calculate RMSE (deviation in original units (rate +-))
    rmse = sqrt(mean_squared_error(predict_data.impl_realy[:60], prediction))

    plt.title(predict_data.pmc+' implemented in ' + predict_data.nut + '\nRMSE: ' + str('{0:.2f}'.format(rmse))+'±')
    plt.ylabel('Cases per 100.000')
    plt.xlabel('Time Step')

    #plot prediction
    plt.plot(predict_data.impl_histx, predict_data.impl_histy, color='blue', label='History')
    plt.plot(predict_data.impl_realx[:60], predict_data.impl_realy[:60], color='green', label='Real')
    plt.plot(predict_data.impl_realx[:60], prediction, color='red', label='Prediction')


    plt.legend()
    plt.show()
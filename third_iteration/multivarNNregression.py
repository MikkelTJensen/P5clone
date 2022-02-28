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

def multivarRegression(data, predict_data, length, pm):

    datasets = []
    for x in data:
        for i in range(len(x.rates)):
            datasets.append([x.rates[i], x.dates[i], x.slope_list[i]])

    datasets = np.array(datasets)

    # frame as supervised learning ( predict (t) from (t-1) )
    reframed = series_to_supervised(datasets, 1, 1)

    # drop columns we don't want to predict - only use for single step
    reframed.drop(reframed.columns[[4,5]], axis=1, inplace=True)

    values = reframed.values

    # split into input and outputs (input:t-1s, output:ts) - only use for single step
    train_X, train_y = values[:, :-1], values[:, -1]

    #train_X, train_y = values[:,:3*5], values[:, -3]

    # reshape input to be 3D [samples, timesteps, features] - only use for single step
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    #train_X = train_X.reshape((train_X.shape[0], 5, 3))

    # design network
    model = Sequential()
    model.add(LSTM(128, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')

    # fit network
    history = model.fit(train_X, train_y, epochs=60, batch_size=60, validation_split=0.2, verbose=1, shuffle=False)
    #[print (i.shape,i.dtype) for i in model.inputs]
    #[print (i.shape,i.dtype) for i in model.outputs]

    ### walk-forward validation/prediction
    # split predict dataset into historic and real, dates and rates.
    impl_histx = predict_data.dates[:predict_data.pm_date-predict_data.start_date]
    impl_realx = predict_data.dates[predict_data.pm_date-predict_data.start_date:]

    impl_histy = predict_data.rates[:predict_data.pm_date-predict_data.start_date]
    impl_realy = predict_data.rates[predict_data.pm_date-predict_data.start_date:]
    """
    # multi step predictor
    # the first point is made of t-5 - t-1 steps from the historic data
    # the resulting prediction is the first t step of the prediction.
    # first 5 tuples have to be made manually, before the rest can be made with a loop
    prediction = impl_histy[-5:]
    latestVal = []

    # first point has to be made by appending the 5 tuples as t-5 to t-1 steps
    # when a preventive measure has been implemented with less than 5 days of historic data (most preventive measures were implemented in the beginning)
    # add 0,0,0 tuples to fill in the start
    for i in range(5-len(prediction)):
        latestVal.append(0.)
        latestVal.append(i)
        latestVal.append(0.)

    # add the first non-zero tuple, made up of the first entry in prediction corresponding to impl_histy
    # and the slope between 0 and the first rate
    latestVal.append(prediction[0])
    latestVal.append(5-len(prediction))
    latestVal.append(calc_slope([0,0.],[1,prediction[0]]))
    #latestVal.append(prediction[0])

    # rest of slopes can be looped as they are based on values in prediction
    for i in range(len(prediction)-1):
        latestVal.append(prediction[i+1])
        latestVal.append(i+(5-len(prediction)+1))
        latestVal.append(calc_slope([0,prediction[i]],[1,prediction[i+1]]))
        #latestVal.append(sum(prediction[:i + 2]) / len(prediction[:i + 2]))

    latestVal = [latestVal]
    latestVal = np.array(latestVal)
    latestVal = latestVal.reshape((latestVal.shape[0], 5, 3))

    prediction.append(model.predict(latestVal)[0][0])

    # prepare days 5-10
    for i in range(3,(3+10-len(impl_histy[-5:]))-1):
        latestVal = [columns for steps in latestVal[0][-4:] for columns in steps]
        latestVal.append(prediction[i+1])
        latestVal.append(i+2)
        latestVal.append(calc_slope([0,prediction[i]],[1,prediction[i+1]]))
        #latestVal.append(sum(prediction[:i + 2]) / len(prediction[:i + 2]))

        # format and shape
        latestVal = [latestVal]
        latestVal = np.array(latestVal)
        latestVal = latestVal.reshape((latestVal.shape[0], 5, 3))

        prediction.append(model.predict(latestVal)[0][0])

    # reframe 5-10 as 0-5
    prediction = prediction[5:]
    for i in range(0,len(latestVal[0])):
        latestVal[0][i][1] = i

    # the rest of the predictions can be made in a loop
    for i in range(3,58):
        latestVal = [columns for steps in latestVal[0][-4:] for columns in steps]
        latestVal.append(prediction[i])
        latestVal.append(i+2)
        latestVal.append(calc_slope([0,prediction[i]],[1,prediction[i+1]]))
        #latestVal.append(sum(prediction[:i + 2]) / len(prediction[:i + 2]))

        # format and shape
        latestVal = [latestVal]
        latestVal = np.array(latestVal)
        latestVal = latestVal.reshape((latestVal.shape[0], 5, 3))

        prediction.append(model.predict(latestVal)[0][0])
    """
    #"""
    ## single step predictor
    # predict next rate based on preceding rate, datedif, slope
    slope = calc_slope([0,impl_histy[-2]], [1,impl_histy[-1]])
    #avg = sum(impl_histy[-2:]) / len(impl_histy[-2:])

    #set latestVal to the value preceding the implementation point
    latestVal = [[impl_histy[-1],0,slope]]
    #latestVal = [[impl_histy[-1],0,avg]]
    latestVal = np.asarray(latestVal).astype('float32')
    latestVal = latestVal.reshape(latestVal.shape[0], 1, latestVal.shape[1])

    prediction = []
    prediction.append(model.predict(latestVal))

    slope = calc_slope([0,impl_histy[-1]], [1,prediction[0]])
    #avg = impl_histy[-1] + prediction[0] / 2

    latestVal = [[prediction[0],1,slope]]
    #latestVal = [[prediction[0],1,avg]]

    latestVal = np.asarray(latestVal).astype('float32')
    latestVal = latestVal.reshape(latestVal.shape[0], 1, latestVal.shape[1])

    prediction.append(model.predict(latestVal))

    for i in range(58):
        slope = calc_slope([0,prediction[i]],[1,prediction[i+1]])
        #avg = sum(prediction) / len(prediction)

        latestVal = [[prediction[i+1],i+2,slope]]
        #latestVal = [[prediction[i+1],i+2,avg]]

        latestVal = np.asarray(latestVal).astype('float32')
        latestVal = latestVal.reshape(latestVal.shape[0], 1, latestVal.shape[1])
        prediction.append(model.predict(latestVal))

    prediction = [x[0] for x in prediction]
    #"""

    # calculate RMSE (deviation in original units (rate +-))
    rmse = sqrt(mean_squared_error(impl_realy[:60], prediction))

    plt.title(pm +' implemented in ' + predict_data.nuts + '\nRMSE: ' + str('{0:.2f}'.format(rmse))+'±')
    plt.ylabel('Cases per 100.000')
    plt.xlabel('Time Step')

    #plot prediction
    plt.plot(impl_histx, impl_histy, color='blue', label='History')
    plt.plot(impl_realx[:60], impl_realy[:60], color='green', label='Real')
    plt.plot(impl_realx[:60], prediction, color='red', label='Prediction')


    plt.legend()

    name_str =  'pics/' + predict_data.nuts + '_' + pm + '_' + str(predict_data.pm_date)
    plt.savefig(name_str)
    plt.clf()
    return prediction
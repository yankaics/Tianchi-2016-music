import numpy as np
import sklearn
from sklearn.cluster import KMeans
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot,savefig
import matplotlib
#from __future__ import print_function
import statsmodels.api as sm
import pandas as pd
from pandas import Series
import config as cfg
from statsmodels.tsa.arima_process import arma_generate_sample

#
# The series are not stationary ... Auto-regression is not a good idea
# Need more features
#


# Calculate ADF to test stationarity
from statsmodels.tsa.stattools import adfuller
def test_stat(timeseries):
    
    #Determing rolling statistics
    rolmean = timeseries.rolling(window=12,center=False).mean()
    rolstd = timeseries.rolling(window=12,center=False).std()

    #Plot rolling statistics:
    #orig = plt.plot(timeseries, color='blue',label='Original')
    #mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    #std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    #plt.legend(loc='best')
    #plt.title('Rolling Mean & Standard Deviation')
    #plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput

matplotlib.use('Agg') 
# 20150304
datestr = open(cfg.ROOT + '/data/derived/days_list.txt','r').readlines()
datestr = [x.split(',')[0] for x in datestr]

daily_play_f = open(cfg.ROOT + '/data/derived/singers/daily_play.txt','r')
artists = []
daily_play = {}

for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    l[1] = l[1].replace('-','')

    # 0:id  1:date: 2012-09-08  2:play
    # given data of first 6 months (183 days), predict the data of next 2 months (60 days)
    if l[0] not in artists:
        daily_play[l[0]] = [-1] * len(datestr)
        daily_play[l[0]][datestr.index(l[1])] = int(l[2])
        artists.append(l[0])
    else:
        daily_play[l[0]][datestr.index(l[1])] = (int(l[2]))
daily_play_f.close()
# Missing value = value of the day before
for artist in artists:
    for i in range(len(datestr)):
        if daily_play[artist][i] == -1:
            daily_play[artist][i] = daily_play[artist][i-1]
dates = []
for i in range(60):
    dates.append((datetime.datetime(2015,9,1) + datetime.timedelta(days = i)).strftime("%Y%m%d"))


from statsmodels.tsa.arima_model import ARIMA
  
from statsmodels.tsa.seasonal import seasonal_decompose

output = open('AIRMA_mars_tianchi_artist_plays_predict.csv','w')

for artist in artists:
    print artist, len(daily_play[artist])
    y_data =  daily_play[artist][-30:]
    l = len(y_data)
    dates_str = sm.tsa.datetools.date_range_str('2005m1',length=l)
    dates_all = sm.tsa.datetools.dates_from_range('2005m1', length=l)
    y = pd.Series(y_data, index=dates_all)
    plt.plot(y)

    
    decomposition = seasonal_decompose(y)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    y_decompose = residual
    y_decompose.dropna(inplace=True)

    test_stat(y_decompose)


    # remove moving avg
    moving_avg = y.rolling(window=12,center=False).mean()
    y_moving_avg_diff = y - moving_avg
    y_moving_avg_diff.dropna(inplace=True)
    print "Stationarity for TS - moving avg:"
    test_stat(y_moving_avg_diff)

    # remove exp weighted moving avg
    expwighted_avg = pd.ewma(y, halflife=12)
    y_ewma_diff = y - expwighted_avg
    y_ewma_diff.dropna(inplace=True)
    print "Stationarity for TS - exp weighted moving avg"
    test_stat(y_ewma_diff)
    


    # AR
    y_diff = y_moving_avg_diff
    diff = expwighted_avg
    model = ARIMA(y, order=(1, 1, 2))  
    results_ARIMA = model.fit(trend='nc',disp=-1)  
    forecast, fcerr, conf_int = results_ARIMA.forecast(steps =  60)

    #plt.plot(results_ARIMA.fittedvalues, color='red')
    #plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-y_diff)**2))
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    print predictions_ARIMA_diff.head()
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    print predictions_ARIMA_diff_cumsum.head()

    predictions_ARIMA_log = pd.Series(y_diff.ix[0] , index=y_diff.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    print predictions_ARIMA_log.head()
    plt.plot(dates_all, daily_play[artist][-l:])
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    dates_fc =  sm.tsa.datetools.dates_from_range(dates_str[-1], length=60)

    plt.plot(dates_fc,forecast, color='red')
    plt.show()
    break
    #arma_res = arma_mod.fit(trend='nc', disp=-1)
    #plt.figure(1)
    #forecast, fcerr, conf_int = arma_res.forecast(steps =  60)
    #dates_fc =  sm.tsa.datetools.dates_from_range(dates_str[-1], length=60)
    #plt.clf()
    #plt.plot(dates_all, daily_play[artist])
    #plt.plot(dates_fc, forecast)
    #plt.savefig('ARMA/' + '12_0_'+artist + '.jpg')
    #for i in range(60):
    #    count = forecast[i]
    #    date = dates[i]
    #    output.write(artist + ',' + str(int(count)) + ',' + date + '\n' )

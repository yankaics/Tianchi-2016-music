import numpy as np
import sklearn
from sklearn.cluster import KMeans
import keras
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot,savefig
import matplotlib
#from __future__ import print_function
import statsmodels.api as sm
import pandas as pd
import config as cfg
from statsmodels.tsa.arima_process import arma_generate_sample

#
# The series are not stationary ... Auto-regression is not a good idea
# Need more features
#

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


output = open('linreg_mars_tianchi_artist_plays_predict.csv','w')

for artist in artists:
    print artist, len(daily_play[artist])
    l = 183
    dates_str = sm.tsa.datetools.date_range_str('2005m1',length=l)
    dates_all = sm.tsa.datetools.dates_from_range('2005m1', length=len(daily_play[artist]))
    y = pd.Series(daily_play[artist], index=dates_all)
    arma_mod = sm.tsa.ARMA(y, order=(12,0))
    arma_res = arma_mod.fit(trend='nc', disp=-1)
    plt.figure(1)
    forecast, fcerr, conf_int = arma_res.forecast(steps =  60)
    dates_fc =  sm.tsa.datetools.dates_from_range(dates_str[-1], length=60)
    plt.clf()
    plt.plot(dates_all, daily_play[artist])
    plt.plot(dates_fc, forecast)
    plt.savefig('ARMA/' + '12_0_'+artist + '.jpg')
    for i in range(60):
        count = forecast[i]
        date = dates[i]
        output.write(artist + ',' + str(int(count)) + ',' + date + '\n' )

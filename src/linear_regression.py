#code=utf-8
import pandas as pd
from pandas import DataFrame as df
import config as cfg
import datetime
import sklearn
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
import copy

#artist_list_f = open(cfg.ROOT + '/data/derived/artist_list.txt','r')
#artist_list = [ x.strip() for x in artist_list_f.readlines()]
#artist_list_f.close()

daily_play_f = open(cfg.ROOT + '/data/derived/singers/daily_play.txt','r')
artists = []
daily_play = {}
for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    # 0:id  1:date  2:play
    # given data of first 6 months, predict the data of next 2 months
    if l[0] not in artists:
        daily_play[l[0]] = [int(l[2])]
        artists.append(l[0])
    else:
        daily_play[l[0]].append(int(l[2]))

daily_play_f.close()

# future dates list
dates = []
for i in range(60):
    dates.append((datetime.datetime(2015,9,1) + datetime.timedelta(days = i)).strftime("%Y%m%d"))
print dates


output = open('p2_linreg_result_2.csv','w')
# predict
for artist in artists:
    tmp = copy.deepcopy(daily_play[artist])
    tmp.sort()
    X = df(range(60))  # 0 to 29
    All = df(tmp) # 183 days, 0 to 182
    Y = df(daily_play[artist][-60:]) # last 30 days' play counts
    linreg = LinearRegression()
    linreg.fit(X,Y)
    X2 = df(range(60,120))
    Y2 = df(linreg.predict(X2),range(60,120))
    for y in Y2.values:
        if y[0] < min(tmp):
            y[0] = tmp[0]
            tmp.remove(tmp[0])
    #final = Y.append(Y2)
    #final.plot.line()
    #plt.show()
    for i in range(60):
        count = Y2.values[i][0]
        date = dates[i]
        output.write(artist + ',' + str(int(count)) + ',' + date + '\n' )


     














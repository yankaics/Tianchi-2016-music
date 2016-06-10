import cPickle as cp
import matplotlib.pyplot as plt
# use cPickle.load(<file>) to load object from a file
artists = cp.load(open('cp_artists.txt','r'))
daily_play = cp.load(open('cp_daily_play.txt'))
daily_down = cp.load(open('cp_daily_down.txt'))
daily_col = cp.load(open('cp_daily_col.txt'))
# 20150212
datestr = cp.load(open('cp_datestr.txt'))
future_dates = cp.load(open('cp_future_dates.txt'))
prediction_1 = {}
prediction_2 = {}
prediction_3 = {}

prediction_l_1 = open('p2_arima_result_2.csv', 'r').readlines()
prediction_l_2 = open('p2_stlf_result_2.csv', 'r').readlines()
prediction_l_3 = open('p2_linreg_result_2.csv', 'r').readlines()
for artist in artists:
    prediction_1[artist] = []
    prediction_2[artist] = []
    prediction_3[artist] = []
for line in prediction_l_1:
    prediction_1[line.split(',')[0]].append(float(line.split(',')[1]))
for line in prediction_l_2:
    prediction_2[line.split(',')[0]].append(float(line.split(',')[1]))
for line in prediction_l_3:
    prediction_3[line.split(',')[0]].append(float(line.split(',')[1]))
print "Enter :q to quit, enter a number from 1 - 100 to view the prediction of the artist."
f = open('p2_after_tuning.csv','w')
for artist in artists:
    print "1. blue:ARIMA \n2. red:STLF  \n3. green:LINREG"

    plt.cla()
    plt.plot(range(len(daily_play[artist])),daily_play[artist])
    plt.plot(range(len(daily_play[artist]),len(daily_play[artist]) + 60),prediction_1[artist], color='blue')
    plt.plot(range(len(daily_play[artist]),len(daily_play[artist]) + 60),prediction_2[artist], color='red')
    plt.plot(range(len(daily_play[artist]),len(daily_play[artist]) + 60),prediction_3[artist], color='green')
    plt.show()

    action = int(raw_input())
    while action not in [1,2,3]:
        action = int(raw_input('again:'))
    if action == 1:
        i = 0
        for line in prediction_1[artist]:
            f.write(artist+','+str(prediction_1[artist][i])+','+future_dates[i]+'\n')
            i += 1
    if action == 2:
        i = 0
        for line in prediction_2[artist]:
            f.write(artist+','+str(prediction_2[artist][i])+','+future_dates[i]+'\n')
            i += 1

    if action == 3:
        i = 0
        for line in prediction_3[artist]:
            f.write(artist+','+str(prediction_3[artist][i])+','+future_dates[i]+'\n')
            i += 1

    





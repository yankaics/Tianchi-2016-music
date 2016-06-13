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

predictions = {}
prediction_ensembled_l = open('p2_arima_ensembled.csv','r').readlines()
prediction_ensembled = {}
for artist in artists:
    prediction_ensembled[artist] = []

for line in prediction_ensembled_l :
    prediction_ensembled[line.split(',')[0]].append(float(line.split(',')[1]))
    
for i in range(10,100,10):
    lines = open('p2_arima_ensemble_' + str(i)+'_2.csv','r').readlines()
    prediction = {}
    for artist in artists:
        prediction[artist] = []
    for line in lines:
        prediction[line.split(',')[0]].append(float(line.split(',')[1]))
    predictions[i] = prediction

for artist in artists:
    plt.cla()
    plt.plot(range(len(daily_play[artist])),daily_play[artist], color='blue')  
    legends = {}
    for i in range(10,100,10):  
        plt.plot(range(len(daily_play[artist]),len(daily_play[artist]) + 60),predictions[i][artist], label=str(i))
    plt.plot(range(len(daily_play[artist]),len(daily_play[artist]) + 60),prediction_ensembled[artist], label=str(i))
   
    plt.legend(loc = 'upper left')
    plt.savefig('arima_ensembled/'+artist + '.jpg')
       



    




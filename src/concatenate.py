import cPickle as cp
import matplotlib.pyplot as plt
prediction_l = open('p2_ets_result_2.csv', 'r').readlines()
# use cPickle.load(<file>) to load object from a file
artists = cp.load(open('cp_artists.txt','r'))
daily_play = cp.load(open('cp_daily_play.txt'))
daily_down = cp.load(open('cp_daily_down.txt'))
daily_col = cp.load(open('cp_daily_col.txt'))
# 20150212
datestr = cp.load(open('cp_datestr.txt'))
future_dates = cp.load(open('cp_future_dates.txt'))
prediction = {}
for artist in artists:
    prediction[artist] = []
for line in prediction_l:
    prediction[line.split(',')[0]].append(float(line.split(',')[1]))
print "Enter :q to quit, enter a number from 1 - 100 to view the prediction of the artist."
while True:
    q = raw_input()
    if q == ":q":
        print "bye"
        break
    else:
        plt.cla()
        artist = artists[int(q)-1]
        plt.plot(range(len(daily_play[artist])),daily_play[artist])
        i = 0
        for date in datestr:
            print date,daily_play[artist][i]
            i += 1
        plt.plot(range(len(daily_play[artist]),len(daily_play[artist]) + 60),prediction[artist], color='red')
        plt.show()
    





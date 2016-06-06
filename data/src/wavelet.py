import config.config as cfg
import datetime
import numpy  
import pywt  
import matplotlib.pyplot as plt
daily_play_f = open(cfg.ROOT+'/data/derived/singers/daily_play.txt','r')
artists = []
daily_play = {}
for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    # 0:id  1:date  2:play
    # given data of first 6 months, predict the data of nepxt 2 months
    if l[0] not in artists:
	daily_play[l[0]] = [l[2]]
	artists.append(l[0])
    else:
	daily_play[l[0]].append(l[2])
    
#print daily_play
daily_play_f.close()

# future dates list
dates = []
for i in range(60):
    dates.append((datetime.datetime(2015,9,1) + datetime.timedelta(days = i)).strftime("%Y%m%d"))
#print dates

#output = open('ar_mars_tianchi_artist_plays_predict.csv','w')
#predict 
spl = []
for e in daily_play[artists[6]]:
    spl.append(int(e))

(cA, cD) = pywt.dwt(spl, 'coif5')  
  
plt.subplot(311)  
plt.plot(spl)  
  
plt.subplot(312)  
plt.plot(cA)  
  
plt.subplot(313)  
plt.plot(cD)  
  
plt.show()  

import numpy as np
import sklearn
from sklearn.cluster import KMeans
import keras
import matplotlib.pyplot as plt
# Settings 

dim_input = 60
dim_hidden = 10
dim_output = 60
lam = 0.001
restart = True
daily_play_f = open(cfg.ROOT + '/data/derived/singers/daily_play.txt','r')
artists = []
daily_play = {}
train_input= []
train_output= []
test_input = []

print "Read data"
for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    # 0:id  1:date  2:play
    # given data of first 6 months (183 days), predict the data of next 2 months (60 days)
    if l[0] not in artists:
        daily_play[l[0]] = [int(l[2])]
        artists.append(l[0])
    else:
        daily_play[l[0]].append(int(l[2]))
daily_play_f.close()


# build input & output set
print "Build input & output set"
for artist in artists:
   # print "Artist id: ",artist
    l = len(daily_play[artist])
    begin = 0
    while begin + 120 <= l:
        # l == 183
        min_log = np.log(min(daily_play[artist][begin:begin+dim_input]))
        max_log = np.log(max(daily_play[artist][begin:begin+dim_input]))
        diff = max_log - min_log
        input_all.append([(np.log(x)-min_log)/diff for x in daily_play[artist][begin:begin+60]])
        output_all.append([(np.log(x)-min_log)/diff for x in daily_play[artist][begin+60:begin+120]])
        begin += 1

size_input = len(input_all) # should be 64 * 50
size_output = len(output_all) # should also be 64 * 50

size_test = 500
size_train = size_input - size_test 

X = np.array(input_all[0:size_train]).T
Y = np.array(output_all[0:size_train]).T

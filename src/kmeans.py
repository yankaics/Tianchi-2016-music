from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans, SpectralClustering, AffinityPropagation,MeanShift,DBSCAN
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
import cPickle as cp
from sklearn.decomposition import PCA 

# 1. raw_data_singer_matrix_train: {singer_id: matrix} matrix if of 183 days 
#    data_singer_matrix_train: list of tuples(input,output)
#    input_singer_matrix_train 
#    => output_singer_matrix_train
#   Each singer has a feature matrix, each column is the feature of one single day
#   .shape = (dim_feature_1,input_days_1)
#   [0,day]: daily play
#   [1,day]: daily download
#   [2,day]: daily collect
#   [3,day]: the number of users who play songs of the singer
#   [4,day]: the number of users who download songs of the singer
#   [5,day]: the number of users who collect songs of the singer
#   [6,day]: the avg of songs play !!! doesn't contain those count = 0
#   [7,day]: the avg of songs down
#   [8,day]: the avg of songs col
#   [9,day]: the stddev of songs play
#   [10,day]: the stddev of songs download 
#   [11,day]: the stddev of songs collect !!! doesn't contain those count = 0
#   #[12,day]: highest played song's play 
#   #[13,day]: highest played song's download 
#   #[14,day]: highest played song's collect
#   #[15,day]: singer gender 1 if 1 # M
#   #[16,day]: singer gender 1 if 2 # F
#   #[17,day]: singer gender 1 if 3 # Band
#   #[18,day]: singer's total song number
#
#========================================================
# prepare data

raw_data_matrix = cp.load(open('cp_raw_data_matrix.txt','r'))
artists = cp.load(open('cp_artists.txt', 'r'))
datestr = cp.load(open('cp_datestr.txt', 'r')) # 20150607
future_dates = cp.load(open('cp_future_dates.txt', 'r'))
all_days = 183
input_daily_play = {}
for artist in artists:
    input_daily_play[artist] = np.zeros([183,1])
    for day in range(all_days):
        input_daily_play[artist][day] = raw_data_matrix[artist][0,day]
input_daily_col = {}
for artist in artists:
    input_daily_col[artist] = np.zeros([183,1])
    for day in range(all_days):
        input_daily_col[artist][day] = raw_data_matrix[artist][2,day]

input_stddev_play = {}
for artist in artists:
    input_stddev_play[artist] = np.zeros([183,1])
    for day in range(all_days):
        input_stddev_play[artist][day] = raw_data_matrix[artist][9,day]


# Settings
batch_size = 800
data_dim = 1
output_size = 60
skip = 13 # diff of start indexs of 2 time series, skip=2 => 0,2,4,6...
timesteps = 15
input_length = timesteps * 1      # if we have 3 daily features, then it's timesteps * 3
all_size = (183 -(timesteps + output_size-1) - 1 )/skip + 1
print "Num of samples: ",all_size * 100
train_size = min(2000,all_size) # 94
print "training data extracted from one artist:",train_size
train_size_all = train_size * 100 # num of training instances, train a model with all artists' data
test_size = all_size - train_size
test_size_all = test_size * 100  # 1

def smooth(x,window_len=11,window='hanning'):
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."
    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."
    if window_len<3:
        return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    s=np.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:  
        w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='same')
    return y[window_len:-window_len+1]


x_train = np.zeros([train_size_all, input_length, data_dim])
x_cls = np.zeros([train_size_all, input_length]) # n_sample, n_feature
x_cls_origin = np.zeros([train_size_all, input_length]) # n_sample, n_feature
y_train = np.zeros([train_size_all, output_size])
x_test = np.zeros([test_size_all, input_length, data_dim])
y_test = np.zeros([test_size_all, output_size])
for k in range(100):
    test_artist = artists[k]
    for i in range(train_size):
        col = input_daily_play[test_artist][i*skip:i*skip+timesteps,0]
        col_s = col
        x_cls[k*train_size+i,:] = ((col_s)/np.sqrt((col_s.T.dot(col_s))))**1.5#/np.log(max(col)+2)
        x_cls_origin[k*train_size+i,:] = col#/np.log(max(col)+2)
#        y_train[k*train_size+i,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]
 #       x_train[k*train_size+i,:] = np.vstack((input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1]),input_stddev_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])) )
#        y_train[k*train_size+i,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]





#for j in range(test_size):
#    i = j+train_size
#    x_test[k*test_size+j,:,:] = input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])
#    y_test[k*test_size+j,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]

#for k in range(100):
#    test_artist = artists[k]
#    plt.cla()
#    X = np.zeros([batch_size, input_length, data_dim])
#    X[0,:,:] = np.vstack((input_daily_play[test_artist][-timesteps:,0].reshape([timesteps,1]),input_daily_col[test_artist][-timesteps:,0].reshape([timesteps,1]),input_stddev_play[test_artist][-timesteps:,0].reshape([timesteps,1])))
#    for kk in range(batch_size):
#        X[kk,:,:] = np.vstack((input_daily_play[test_artist][-timesteps:,0].reshape([timesteps,1]),input_stddev_play[test_artist][-timesteps:,0].reshape([timesteps,1])))


# PCA 

pca=PCA(n_components=2)
newData=pca.fit_transform(x_cls)
#import pylab as pl
#pl.scatter(newData[:,0],newData[:,1])



random_state = 170
print "Start clustering"
n_clusters = 20
y_pred = KMeans(n_clusters=n_clusters ).fit_predict(x_cls)
print y_pred
fig = plt.figure(1)
for cluster in range(n_clusters):
    count = 0
    plt.cla()
    for i in range(len(y_pred)):
        if y_pred[i] == cluster:
            count += 1
            l1 = plt.plot(x_cls_origin[i], label="data"+str(i))

    print "cluster %d: " % cluster, count
    plt.show()


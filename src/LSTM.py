import numpy as np
import sklearn
from sklearn.cluster import KMeans
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, Dropout, Merge, GRU, Reshape, AveragePooling1D
import cPickle as cp


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

print raw_data_matrix[artists[1]][9,:]
# Settings
batch_size = 800
data_dim = 1
output_size = 60
timesteps = 100
input_length = timesteps * 2      # if we have 3 daily features, then it's timesteps * 3
all_size = 183 -(timesteps + output_size-1)
train_size = min(95,all_size) # 94
print "training data extracted from one artist:",train_size
train_size_all = train_size * 100 # num of training instances, train a model with all artists' data
test_size = all_size - train_size
test_size_all = test_size * 100  # 1


# Model Settings 
model = Sequential()
# output_dim = 5; input_length/time_step = 10; data_dim = 11
model.add(LSTM(240, batch_input_shape=(batch_size, input_length , data_dim),init='glorot_normal', return_sequences=False,stateful=True))
#model.add((AveragePooling1D(batch_input_shape=(batch_size, input_length , data_dim))))
#model.add(Dense(640, init='glorot_normal'))
#model.add(Activation('softplus'))
model.add(Dense(60, init='glorot_normal'))
model.add(Activation('softplus'))
model.compile(loss="mape", optimizer=keras.optimizers.RMSprop(lr=0.00001, rho=0.9, epsilon=1e-06),metrics=["accuracy"])


result = open('p2_LSTM_result.csv','w')
# data should be like size = ( num of instances, timestpes=30, data_dim=1)
x_train = np.zeros([train_size_all, input_length, data_dim])
y_train = np.zeros([train_size_all, output_size])
x_test = np.zeros([test_size_all, input_length, data_dim])
y_test = np.zeros([test_size_all, output_size])
for k in range(100):
    test_artist = artists[k]
    print k,test_artist
    for i in range(train_size):
#        x_train[k*train_size+i,:,:] = np.vstack((input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1]) , input_daily_col[test_artist][i:i+timesteps,0].reshape([timesteps,1]), input_stddev_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])) )
#        y_train[k*train_size+i,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]
        x_train[k*train_size+i,:,:] = np.vstack((input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1]),input_stddev_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])) )
        y_train[k*train_size+i,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]




    for j in range(test_size):
        i = j+train_size
        x_test[k*test_size+j,:,:] = input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])
        y_test[k*test_size+j,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]
print "Training & testing data built"
model.fit(x_train,y_train,batch_size = batch_size, nb_epoch=50)

for k in range(100):
    test_artist = artists[k]
    print k,"predict for :",test_artist
    plt.cla()
    X = np.zeros([batch_size, input_length, data_dim])
#    X[0,:,:] = np.vstack((input_daily_play[test_artist][-timesteps:,0].reshape([timesteps,1]),input_daily_col[test_artist][-timesteps:,0].reshape([timesteps,1]),input_stddev_play[test_artist][-timesteps:,0].reshape([timesteps,1])))
    for kk in range(batch_size):
        X[kk,:,:] = np.vstack((input_daily_play[test_artist][-timesteps:,0].reshape([timesteps,1]),input_stddev_play[test_artist][-timesteps:,0].reshape([timesteps,1])))
    print "input",X[0,:,:]

    prediction = model.predict(X, batch_size = batch_size)
    print prediction.shape
    print prediction[0]
    for kk in range(60):
        result.write(test_artist+','+str(prediction[0][kk]) + ','+future_dates[kk]+'\n')
    plt.plot(range(len(input_daily_play[test_artist])),input_daily_play[test_artist], color='blue')
    plt.plot(range(len(input_daily_play[test_artist]),len(input_daily_play[test_artist])+len(prediction[0])),prediction[0], color='red')
    plt.savefig('lstm2/'+test_artist+'.jpg')


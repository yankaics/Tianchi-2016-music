import numpy as np
import sklearn
from sklearn.cluster import KMeans
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, Dropout
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
#   [7,day]: the avg of songs download
#   [8,day]: the avg of songs collect
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
batch_size = 1
data_dim = 1
output_size = 60
timesteps = 60
input_length = 60 * 3
all_size = 183 -(timesteps + output_size-1)
train_size = min(95,all_size) # num of training instances
test_size = all_size - train_size # 1


# Model Settings 
model = Sequential()
# output_dim = 5; input_length/time_step = 10; data_dim = 11
model.add(LSTM(60, batch_input_shape=(batch_size, input_length , data_dim), return_sequences=False,stateful=True))
model.add(Dense(120))
model.add(Activation('softplus'))
model.add(Dense(60))
model.add(Activation('softplus'))
model.compile(loss="mape", optimizer=keras.optimizers.RMSprop(lr=0.0005, rho=0.9, epsilon=1e-06))


result = open('p2_Simple_LSTM_result.csv','w')
for k in range(100):
    test_artist = artists[k]
    print test_artist

    # data should be like size = ( num of instances, timestpes=30, data_dim=1)
    x_train = np.zeros([train_size, input_length, data_dim])
    y_train = np.zeros([train_size, output_size])
    for i in range(train_size):
        x_train[i,:,:] = np.vstack((input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1]) , input_daily_col[test_artist][i:i+timesteps,0].reshape([timesteps,1]), input_stddev_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])) )
        y_train[i,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]
    x_test = np.zeros([train_size, timesteps, data_dim])
    y_test = np.zeros([train_size, output_size])

    #for j in range(test_size):
    #    i = j+train_size
    #    x_test[j,:,:] = input_daily_play[test_artist][i:i+timesteps,0].reshape([timesteps,1])
    #    y_test[j,:] = input_daily_play[test_artist][i+timesteps:i+timesteps+output_size,0]

    X = np.zeros([1, input_length, data_dim])
    X[0,:,:] = np.vstack((input_daily_play[test_artist][-timesteps:,0].reshape([timesteps,1]),input_daily_col[test_artist][-timesteps:,0].reshape([timesteps,1]),input_stddev_play[test_artist][-timesteps:,0].reshape([timesteps,1])))

    plt.cla()

    model.fit(x_train,y_train,batch_size = batch_size, nb_epoch=20)
    prediction = model.predict(X,batch_size=batch_size)
    for kk in range(60):
        result.write(test_artist+','+str(prediction[0][kk]) + ','+future_dates[kk]+'\n')
    plt.plot(range(len(input_daily_play[test_artist])),input_daily_play[test_artist], color='blue')
    plt.plot(range(len(input_daily_play[test_artist]),len(input_daily_play[test_artist])+len(prediction[0])),prediction[0], color='red')
    plt.savefig('lstm/'+test_artist+'.jpg')


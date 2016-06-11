import numpy as np
import sklearn
from sklearn.cluster import KMeans
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
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

# Settings
input_


# prepare data

raw_data_matrix = cp.load(open('cp_raw_data_matrix.txt','r'))`:w



# Model Settings 
model = Sequential()
# output_dim = 5; input_length/time_step = 10; input_dim = 11
model.add(LSTM(30, batch_input_shape=(None, 10, 11), dropout_W = .2, return_sequences=False)
model.add(Dense(
model.add(Activation('relu'))







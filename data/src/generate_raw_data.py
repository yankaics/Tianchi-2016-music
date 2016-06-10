import numpy as np
import sklearn
import datetime
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm
import pandas as pd
import config.config as cfg
import cPickle as cp

cp_path = cfg.ROOT + '/src/'
output_days = 60
all_days = 183
# date strig: 20150304
datestr_l = open(cfg.ROOT + '/data/derived/days_list.txt','r').readlines()
datestr = [x.strip().split(',')[0] for x in datestr_l]
cp.dump(datestr,open(cp_path+'cp_datestr.txt','w'))
artists_l = open(cfg.ROOT + '/data/derived/artist_list.txt','r').readlines()
artists = [x.strip() for x in artists_l]
cp.dump(artists,open(cp_path+'cp_artists.txt','w'))
#============================ build daily play data =======================
#
daily_play_f = open(cfg.ROOT + '/data/derived/singers/daily_play.txt','r')
daily_play = {}

for artist in artists:
    daily_play[artist] = [0] * len(datestr)
for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    l[1] = l[1].replace('-','')
    # 0:id  1:date: 2012-09-08  2:play
    # given data of first 6 months (183 days), predict the data of next 2 months (60 days)
    daily_play[l[0]][datestr.index(l[1])] = (int(l[2]))
daily_play_f.close()
cp.dump(daily_play,open(cp_path + 'cp_daily_play.txt','w'))

# Missing value = 0
#for artist in artists:
#    for i in range(len(datestr)):
#        if daily_play[artist][i] == -1:
#            print "play missing",artist,i
#            daily_play[artist][i] = daily_play[artist][i-1] # is missing
#            # Now the length is 183 for each singer
#
#============================ build daily play data =======================


#============================ build daily download data =======================
#
daily_down_f = open(cfg.ROOT + '/data/derived/singers/daily_download.txt','r')
daily_down = {}

for artist in artists:
    daily_down[artist] = [0] * len(datestr)
for line in daily_down_f.readlines():
    l = line.strip().split('\t')
    l[1] = l[1].replace('-','')
    # 0:id  1:date: 2012-09-08  2:download
    # given data of first 6 months (183 days), predict the data of next 2 months (60 days)
    daily_down[l[0]][datestr.index(l[1])] = (int(l[2]))
daily_down_f.close()
cp.dump(daily_down,open(cp_path+'cp_daily_down.txt','w'))

# Missing value = 0
#for artist in artists:
#    for i in range(len(datestr)):
#        if daily_play[artist][i] == -1:
#            print "download missing",artist,i
#            daily_play[artist][i] = 0 # is missing
# Now the length is 183 for each singer
#
#============================ build daily download data =======================


#============================ build daily collect data =======================
#
daily_col_f = open(cfg.ROOT + '/data/derived/singers/daily_collect.txt','r')
daily_col = {}

for artist in artists:
    daily_col[artist] = [0] * len(datestr)
for line in daily_col_f.readlines():
    l = line.strip().split('\t')
    l[1] = l[1].replace('-','')
    # 0:id  1:date: 2012-09-08  2:play
    # given data of first 6 months (183 days), predict the data of next 2 months (60 days)
    daily_col[l[0]][datestr.index(l[1])] = (int(l[2]))
daily_col_f.close()
cp.dump(daily_col,open(cp_path+'cp_daily_col.txt','w'))

# Missing value = value of the day before
#for artist in artists:
#    for i in range(len(datestr)):
#        if daily_play[artist][i] == -1:
#            print "play missing",artist,i
#            daily_play[artist][i] = daily_play[artist][i-1] # is missing, use previous value
# Now the length is 183 for each singer
#
#============================ build daily play data =======================


# Used for output
# list of str of dates for next 60 days
future_dates = []
for i in range(60):
    future_dates.append((datetime.datetime(2015,9,1) + datetime.timedelta(days = i)).strftime("%Y%m%d"))

cp.dump(future_dates,open(cp_path+'cp_future_dates.txt','w'))
# use the previous input_days days to predict the next 60 days


# num of users play ...
num_user_play_f = open(cfg.ROOT + '/data/derived/singers/daily_number_user_play.txt','r')
num_user_play = {}
for artist in artists:
    num_user_play[artist] = [0] * len(datestr)
for line in num_user_play_f.readlines():
    l = line.strip().split('\t')
    num_user_play[l[0]][datestr.index(l[1].replace('-',''))] = int(l[2])


# num of users download ...
num_user_down_f = open(cfg.ROOT + '/data/derived/singers/daily_number_user_download.txt','r')
num_user_down = {}
for artist in artists:
    num_user_down[artist] = [0] * len(datestr)
for line in num_user_down_f.readlines():
    l = line.strip().split('\t')
    num_user_down[l[0]][datestr.index(l[1].replace('-',''))] = int(l[2])



# num of users collect ...
num_user_col_f = open(cfg.ROOT + '/data/derived/singers/daily_number_user_collect.txt','r')
num_user_col = {}
for artist in artists:
    num_user_col[artist] = [0] * len(datestr)
for line in num_user_col_f.readlines():
    l = line.strip().split('\t')
    num_user_col[l[0]][datestr.index(l[1].replace('-',''))] = int(l[2])
print num_user_col




input_days_1 = 60
dim_feature_1 = 19
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
#   [6,day]: the avg of songs play
#   [7,day]: the avg of songs download
#   [8,day]: the avg of songs collect
#   [9,day]: the stddev of songs play
#   [10,day]: the stddev of songs download
#   [11,day]: the stddev of songs collect
#   [12,day]: highest played song's play 
#   [13,day]: highest played song's download 
#   [14,day]: highest played song's collect
#   [15,day]: singer gender 1 if 1 # M
#   [16,day]: singer gender 1 if 2 # F
#   [17,day]: singer gender 1 if 3 # Band
#   #[18,day]: singer's total song number
#
#========================================================

#raw_output_singer_matrix_train = np.zeros([1,output_days])

#   [dim_feature_1,all_days] to [60,1]
# all_days = 183
#for day in input_days_1:
#    raw_input_singer_matrix_train
raw_data_singer_matrix_train = {}
for artist in artists:
    raw_data_singer_matrix_train[artist] = np.zeros([dim_feature_1,all_days])
    # 0. daily_play
    for day in range(all_days):
        raw_data_singer_matrix_train[artist][0,day] = daily_play[artist][day]

    # 0. daily_download
    for day in range(all_days):
        raw_data_singer_matrix_train[artist][1,day] = daily_play[artist][day]

    # 0. daily_collect
    for day in range(all_days):
        raw_data_singer_matrix_train[artist][2,day] = daily_play[artist][day]








# 2. raw_data
#
#











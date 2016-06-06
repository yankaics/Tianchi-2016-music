#code=utf-8
import pandas as pd
from pandas import DataFrame as df
import config as cfg
import datetime
import sklearn
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
import copy
import numpy as np
import math
import time
#artist_list_f = open(cfg.ROOT + '/data/derived/artist_list.txt','r')
#artist_list = [ x.strip() for x in artist_list_f.readlines()]
#artist_list_f.close()

dim_input = 60
dim_hidden = 10
dim_output = 60
lam = 0.001
restart = True
daily_play_f = open(cfg.ROOT + '/data/derived/singers/daily_play.txt','r')
artists = []
daily_play = {}
input_all = []
output_all = []
dates = open(cfg.ROOT + '/data/derived/days_list.txt','r').readlines()
dates = [x.split(',')[0] for x in dates]
print "Read data"
for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    # 0:id  1:date  2:play
    # given data of first 6 months, predict the data of next 2 months
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
        # l == 183 ?
        min_log = np.log(min(daily_play[artist][begin:begin+60]))
        max_log = np.log(max(daily_play[artist][begin:begin+60]))
        diff = max_log - min_log
        input_all.append([(np.log(x)-min_log)/diff for x in daily_play[artist][begin:begin+60]])
        output_all.append([(np.log(x)-min_log)/diff for x in daily_play[artist][begin+60:begin+120]])
        begin += 2

size_input = len(input_all) # should be 64 * 50
size_output = len(output_all) # should also be 64 * 50

size_test = 500
size_train = size_input - size_test 

X = np.array(input_all[0:size_train]).T
Y = np.array(output_all[0:size_train]).T
X_test = np.array(input_all[size_train:]).T
Y_test = np.array(output_all[size_train:]).T


# future dates list
dates = []
for i in range(60):
    dates.append((datetime.datetime(2015,9,1) + datetime.timedelta(days = i)).strftime("%Y%m%d"))
#print dates



def loss(X,Y,W1,W2,b1,b2):
    #a2 = 1/(1+np.exp(-(np.dot(W1,X)))) + np.tile(b1,[1,X.shape[1]])  # a1 == X
    # The last layer uses softmax unit
    #a3_temp = np.exp(-(np.dot(W2,a2)))
    #a3 = 1/(1+np.exp(-(np.dot(W2,a2)))) + np.tile(b2,[1,X.shape[1]]) 
    a2 = 1/(1+np.exp(-(np.dot(W1,X)+np.tile(b1,[1,X.shape[1]]))))   # a1 == X
    # The last layer uses softmax unit
    #a3_temp = np.exp(-(np.dot(W2,a2)))
    a3 = 1/(1+np.exp(-(np.dot(W2,a2) + np.tile(b2,[1,X.shape[1]]))))


    print "output: ", a3
    print "target: ", Y

    diff = a3 - Y
    n = diff.shape[1]
    loss = 0
    #cosine = 0
    for i in range(n):
        loss += diff[:,i].T.dot(diff[:,i])/2
        #cosine += a3[:,i].T.dot(Y[:,i])/math.sqrt(a3[:,i].T.dot(a3[:,i])*Y[:,i].T.dot(Y[:,i]))
        #print "one case: ", loss_1
    print "Loss: ", loss/n  +lam*(np.sum(W1*W1)/2 + np.sum(W2*W2)/2)  #, "Cosine: ",cosine/n

print "begin"

if restart == True:
    W1 = 2*np.random.random((dim_hidden,dim_input)) - 1 # wights of 1st layer
    W2 = 2*np.random.random((dim_output,dim_hidden)) - 1 # weight of 2nd layer
    b1 = 2*np.random.random((dim_hidden,1)) - 1 # wights of 1st layer
    b2 = 2*np.random.random((dim_output,1)) - 1 # weight of 2nd layer
else:
    W1 = np.loadtxt('W1.txt')
    W2 = np.loadtxt('W2.txt')
    b1 = np.loadtxt('b1.txt').reshape([dim_hidden,1])
    b2 = np.loadtxt('b2.txt').reshape([dim_output,1])
print b1.shape
#print "dim: W
for j in xrange(100000): # no penalty term
    alpha = 1/np.log(j+10)
    
    #print -(np.dot(W1,X))
    #print b1.shape
    a2 = 1/(1+np.exp(-(np.dot(W1,X)+np.tile(b1,[1,size_train]))))   # a1 == X
    # The last layer uses softmax unit
    #a3_temp = np.exp(-(np.dot(W2,a2)))
    a3 = 1/(1+np.exp(-(np.dot(W2,a2) + np.tile(b2,[1,size_train]))))

    #a3 = a3_temp/a3_temp.sum(0)
    #sigma3_soft = (Y - a3)
   
    sigma3 = - (Y - a3) * (a3 * (1 - a3))
    sigma2 = W2.T.dot(sigma3) * (a2 * (1 - a2))
    
    #l2_delta = (y - l2)*(l2*(1-l2))
    #l1_delta = l2_delta.dot(syn1.T) * (l1 * (1-l1))
    W2 -= alpha * (sigma3.dot(a2.T)/size_train + lam * W2)
    W1 -= alpha * (sigma2.dot(X.T)/size_train + lam * W1)
    
    #print sigma3.reshape((60,1))
    
    b2 -= alpha * np.sum(sigma3,1).reshape(dim_output,1)/size_train
    b1 -= alpha * np.sum(sigma2,1).reshape(dim_hidden,1)/size_train
    #print "Training: ",
    #loss(X,Y,W1,W2)
    #print "Test: ",
    #loss(X_test,Y_test,W1,W2)
    if j % 100 ==1:
        print j
        #print "Training: "
        loss(X,Y,W1,W2,b1,b2)
        print "Test: "
        loss(X_test,Y_test,W1,W2,b1,b2)
        np.savetxt("W1.txt",W1)
        np.savetxt("W2.txt",W2)
        np.savetxt("b1.txt",b1)
        np.savetxt("b2.txt",b2)
        print "write finish"
    
#eW2 = 2*np.random.random((dim_output,dim_hidden)) - 1 # weight of 2nd layer
nd = time.clock()
#print "take %fs" %(end - start)
#np.savetxt("w0.txt",syn0)
#np.savetxt("w1.txt",syn1)




# Show test results
i = 1
X_show = X_test[:,i]
Y_show = Y_test[:,i]


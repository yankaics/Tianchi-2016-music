import config.config as cfg
import datetime
import numpy
import math
daily_play_f = open(cfg.ROOT+'/data/derived/singers/daily_play.txt','r')
artists = [[],[],[],[],[],[]]
months = ['03','04','05','06','07','08']
daily_play = [{},{},{},{},{},{}]
for line in daily_play_f.readlines():
    l = line.strip().split('\t')
    # 0:id  1:date  2:play
    # given data of first 6 months, predict the data of next 2 months
    m = l[1].split('-')[1]
    for i in range(0,6):
	if m == months[i]:
	    if l[0] not in artists[i]:
		daily_play[i][l[0]] = [l[2]]
		artists[i].append(l[0])
	    else:
		daily_play[i][l[0]].append(l[2])
    
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
for e in daily_play[1][artists[1][4]]:
    spl.append(int(e))

def auto_relate_coef(data,avg,s2,k):  
    ef=0.;  
    for i in range(0,len(data)-k):  
    	ef=ef+(data[i]-avg)*(data[i+k]-avg);  
    	ef=ef/len(data)/s2;  
    return ef;
 
def ar_coefs(sample):  
    efs=[];  
    data=[];  
    avg=numpy.mean(sample);  
    s2=numpy.var(sample);  
    array=sample 
    for x in array:  
    	data.append(x);  
    for k in range(0,len(data)):  
    	ef=auto_relate_coef(data,avg,s2,k);  
    	efs.append(ef);  
    return efs;  

def ar_least_square(sample,p):  
    matrix_x = numpy.zeros((len(sample)-p,p))
    matrix_x = numpy.matrix(matrix_x)
    array = sample
    j = 0 
    for i in range(0,len(sample)-p):  
    	matrix_x[i,0:p] = array[j:j+p]
    	j = j+1
    matrix_y = numpy.zeros((len(sample)-p,1))
    for i in range(0,len(sample)-p):
        matrix_y[i] = array[p+i]
    matrix_y=numpy.matrix(matrix_y)
    #fi
    fi=numpy.dot(numpy.dot((numpy.dot(matrix_x.T,matrix_x)).I,matrix_x.T),matrix_y);  
    matrix_y=numpy.dot(matrix_x,fi);  
    #matrix_y=numpy.row_stack((array[0:p].reshape(p,1),matrix_y));  
    return fi,matrix_y; 

def ar_aic(rss,p):  
    n=len(rss);  
    s2=numpy.var(rss);  
    return 2*p+n*math.log(s2);  
      
def ar_sc(rss,p):  
    n=len(rss);  
    s2=numpy.var(rss);  
    return p*math.log(n)+n*math.log(s2);  

Y = []

for p in range(1,2):
    #print ar_least_square(spl,p)[1]
    for i in range(0,27):
	Y.append(float(ar_least_square(spl,p)[1][i]) - float(daily_play[2][artists[2][4]][i]))
    print ar_aic(Y,p)
    print ar_sc(Y,p)
    print ' '

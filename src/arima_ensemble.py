import numpy as np
files = []
n = 5
out = open('p2_arima_ensembled.csv','w')
for i in range(10,100,10):
    files.append(open('p2_arima_ensemble_'+str(i)+'_2.csv','r').readlines())
print files[0][1]
for j in range(6000):
    print j
    scores = []
    distances = []
    score = 0
    artist = files[0][j].split(',')[0]
    date = files[0][j].split(',')[2]
    for flines in files:
        scores.append(int(flines[j].split(',')[1]))
    for i in range(len(files)):
        distances.append(sum(np.abs([int(x) - int(scores[i]) for x in scores])))
    for k in range(n):
        min_index = distances.index(np.min(distances))
        score = score + scores[min_index]
        print scores[min_index]
        distances[min_index] = 9999999
    
    score = score/n
    out.write(artist + ',' + str(score) + ',' + date)







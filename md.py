f = open('p2_ARIMA.csv','r')
f2 = open('p2-R-ARIMA-result-2.csv','w')

for line in f.readlines():
    l = line.split(',')
    print l
    if "2015-09-31" in l[3]:
        print "skip"
        continue
    else:
        f2.write(l[1][1:-1]+','+l[2]+','+l[3].replace('"','').replace('-',''))


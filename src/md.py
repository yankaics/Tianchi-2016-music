filename = 'p2_stlf_result'
print "File: ",filename
f = open(filename + '.csv','r')
f2 = open(filename + '_2.csv','w')
lines = f.readlines()[1:]
for i in range(len(lines)):
    l = lines[i].split(',')
    #print l
    if "2015-09-31" in l[3]:
        print "skip"
        continue
    else:
        if 'NA' in l[2]:
            print l,count
        else:
            count = l[2]
        f2.write(l[1][1:-1]+','+count+','+l[3].replace('"','').replace('-',''))



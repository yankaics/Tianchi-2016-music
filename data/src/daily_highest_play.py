#
#   Extract daily information for every artist.
#   
#   Structure:
#   
#   date,song_id,play/download/collect
#   Order by ds, count(desc)
#

import MySQLdb, config.config as cfg

sql_highest_play = "select User_actions.ds as date,User_actions.song_id as song_id,count(*) as play from User_actions where User_actions.action_type=1 group by User_actions.ds,User_actions.song_id order by User_actions.ds,count(*) desc;"
sql_highest_download = "select User_actions.ds as date,User_actions.song_id as song_id,count(*) as play from User_actions where User_actions.action_type=2 group by User_actions.ds,User_actions.song_id order by User_actions.ds,count(*) desc;"
sql_highest_collect = "select User_actions.ds as date,User_actions.song_id as song_id,count(*) as play from User_actions where User_actions.action_type=3 group by User_actions.ds,User_actions.song_id order by User_actions.ds,count(*) desc;"


print "Connecting to the database..."
conn = MySQLdb.connect ( host = cfg.HOST, user = cfg.USER,\
                        passwd = cfg.PASSWORD,\
                         charset='utf8')
print "Connected."
# Get cursor
cur = conn.cursor(MySQLdb.cursors.DictCursor)
conn.select_db('tianchi_music')

print "Start executing sql_highest_play"
cur.execute(sql_highest_play)
play = open(cfg.ROOT + '/data/derived/singers/daily_highest_play.txt', 'w') 
dates = []
for row in cur.fetchall():
    if row['date'] not in dates:
    	play.write(str(row['date'])+'\t'+row['song_id']+'\t'+str(row['play'])+'\n')
        dates.append(row['date'])

print "Start executing sql_highest_download"
cur.execute(sql_highest_download)
play = open(cfg.ROOT + '/data/derived/singers/daily_highest_download.txt', 'w') 
dates = []
for row in cur.fetchall():
    if row['date'] not in dates:
    	play.write(str(row['date'])+'\t'+row['song_id']+'\t'+str(row['play'])+'\n')
        dates.append(row['date'])

print "Start executing sql_highest_collect"
cur.execute(sql_highest_collect)
play = open(cfg.ROOT + '/data/derived/singers/daily_highest_collect.txt', 'w') 
dates = []
for row in cur.fetchall():
    if row['date'] not in dates:
    	play.write(str(row['date'])+'\t'+row['song_id']+'\t'+str(row['play'])+'\n')
        dates.append(row['date'])

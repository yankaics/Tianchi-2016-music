#
#   Extract daily information for every artist.
#   
#   Structure:
#
#   artist_id,play,download,collect,play_user,download_user,collect_user,ds,gmt_create
#   play_user: the number of users that play the music of the artist
#   Order by artist_id, ds, gmt_create
#

import MySQLdb, config.config as cfg

sql_play = "select Songs.artist_id, User_actions.ds as date, count(*) as play from User_actions left join Songs on Songs.song_id = User_actions.song_id  where User_actions.action_type = 1 group by Songs.artist_id, User_actions.ds order by Songs.artist_id, User_actions.ds;"
sql_download = "select Songs.artist_id, User_actions.ds as date, count(*) as download from User_actions left join Songs on Songs.song_id = User_actions.song_id  where User_actions.action_type = 2 group by Songs.artist_id, User_actions.ds order by Songs.artist_id, User_actions.ds;"
sql_collect = "select Songs.artist_id, User_actions.ds as date, count(*) as collect from User_actions left join Songs on Songs.song_id = User_actions.song_id  where User_actions.action_type = 3 group by Songs.artist_id, User_actions.ds order by Songs.artist_id, User_actions.ds;"

print "Connecting to the database..."
conn = MySQLdb.connect ( host = cfg.HOST, user = cfg.USER,\
                        passwd = cfg.PASSWORD,\
                         charset='utf8')
print "Connected."
# Get cursor
cur = conn.cursor(MySQLdb.cursors.DictCursor)
conn.select_db('tianchi_music')

print "Start executing sql_play"
cur.execute(sql_play)
play = open(cfg.ROOT + '/data/derived/singers/daily_play.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['play'])+'\n')

print "Start executing sql_download"
cur.execute(sql_download)
play = open(cfg.ROOT + '/data/derived/singers/daily_download.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['download'])+'\n')

print "Start executing sql_collect"
cur.execute(sql_collect)
play = open(cfg.ROOT + '/data/derived/singers/daily_collect.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['collect'])+'\n')







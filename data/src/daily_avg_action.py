#
#   Extract daily average play/download/collect of songs of every artist.
#   
#   Structure:
#   
#   play_user: the number of users that play the music of the artist
#   Order by artist_id, ds
#

import MySQLdb, config.config as cfg

sql_play = 'select A.artist_id, A.ds as date, AVG(A.song_play) as play from (select Songs.artist_id , User_actions.ds, Songs.song_id, count(*) as song_play from User_actions left join Songs on Songs.song_id = User_actions.song_id where User_actions.action_type = 1 group by Songs.artist_id, User_actions.ds, Songs.song_id order by Songs.artist_id, Songs.song_id, User_actions.ds) as A group by A.artist_id, A.ds order by A.artist_id, A.ds;'
sql_download = 'select A.artist_id, A.ds as date, AVG(A.song_download) as download from (select Songs.artist_id , User_actions.ds, Songs.song_id, count(*) as song_download from User_actions left join Songs on Songs.song_id = User_actions.song_id where User_actions.action_type = 1 group by Songs.artist_id, User_actions.ds, Songs.song_id order by Songs.artist_id, Songs.song_id, User_actions.ds) as A group by A.artist_id, A.ds order by A.artist_id, A.ds;'

sql_collect = 'select A.artist_id, A.ds as date, AVG(A.song_collect) as collect from (select Songs.artist_id , User_actions.ds, Songs.song_id, count(*) as song_collect from User_actions left join Songs on Songs.song_id = User_actions.song_id where User_actions.action_type = 1 group by Songs.artist_id, User_actions.ds, Songs.song_id order by Songs.artist_id, Songs.song_id, User_actions.ds) as A group by A.artist_id, A.ds order by A.artist_id, A.ds;'

print "Connecting to the database..."
conn = MySQLdb.connect ( host = cfg.HOST, user = cfg.USER,\
                        passwd = cfg.PASSWORD,\
                         charset='utf8')
print "Connected."
# Get cursor
cur = conn.cursor(MySQLdb.cursors.DictCursor)
conn.select_db('tianchi_music')

print "Start executing sql_user_play"
cur.execute(sql_play)
play = open(cfg.ROOT + '/data/derived/singers/daily_avg_song_play.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['play'])+'\n')

print "Start executing sql_user_download"
cur.execute(sql_download)
play = open(cfg.ROOT + '/data/derived/singers/daily_avg_song_download.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['download'])+'\n')

print "Start executing sql_user_collect"
cur.execute(sql_collect)
play = open(cfg.ROOT + '/data/derived/singers/daily_avg_song_collect.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['collect'])+'\n')












#
#   Extract daily user number for every artist.
#   
#   e.g. the number of users who play songs of a certain artist in one day
#   Structure:
#   
#   
#   play_user: the number of users that play the music of the artist
#   Order by artist_id, ds
#

import MySQLdb, config.config as cfg

sql_play = 'select Songs.artist_id, User_actions.ds as date, count(distinct User_actions.user_id) as play from User_actions left join Songs on Songs.song_id = User_actions.song_id where User_actions.action_type = 1 group by Songs.artist_id, User_actions.ds order by Songs.artist_id, User_actions.ds;'
sql_download = 'select Songs.artist_id, User_actions.ds as date, count(distinct User_actions.user_id) as download from User_actions left join Songs on Songs.song_id = User_actions.song_id where User_actions.action_type = 2 group by Songs.artist_id, User_actions.ds order by Songs.artist_id, User_actions.ds;'
sql_collect = 'select Songs.artist_id, User_actions.ds as date, count(distinct User_actions.user_id) as collect from User_actions left join Songs on Songs.song_id = User_actions.song_id where User_actions.action_type = 3 group by Songs.artist_id, User_actions.ds order by Songs.artist_id, User_actions.ds;'


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
play = open(cfg.ROOT + '/data/derived/singers/daily_number_user_play.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['play'])+'\n')

print "Start executing sql_user_download"
cur.execute(sql_download)
play = open(cfg.ROOT + '/data/derived/singers/daily_number_user_download.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['download'])+'\n')

print "Start executing sql_user_collect"
cur.execute(sql_collect)
play = open(cfg.ROOT + '/data/derived/singers/daily_number_user_collect.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['date'])+'\t'+str(row['collect'])+'\n')












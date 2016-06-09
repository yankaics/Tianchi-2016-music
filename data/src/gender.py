#
#   Extract daily information for every artist.
#   
#   Structure:
#
#   artist_id,Gender
#   Order by Gender
#

import MySQLdb, config.config as cfg

sql_gender = "select artist_id, Gender as gender from Songs group by Songs.artist_id order by Gender;"

print "Connecting to the database..."
conn = MySQLdb.connect ( host = cfg.HOST, user = cfg.USER,\
                        passwd = cfg.PASSWORD,\
                         charset='utf8')
print "Connected."
# Get cursor
cur = conn.cursor(MySQLdb.cursors.DictCursor)
conn.select_db(cfg.DBNAME)

print "Start executing sql_gender"
cur.execute(sql_gender)
play = open(cfg.ROOT + '/data/derived/singers/gender.txt', 'w') 
for row in cur.fetchall():
    play.write(row['artist_id']+'\t'+str(row['gender'])+'\n')







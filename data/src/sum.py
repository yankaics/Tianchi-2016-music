#
#   Extract daily information for every artist.
#   
#   Structure:
#   
#   artist_id,song_id,play/download/collect
#   Order by ds, count(desc)                    
#

import MySQLdb, config.config as cfg

sql_sum = "select Songs.artist_id as id,count(*) as sum from Songs group by Songs.artist_id;"

print "Connecting to the database..."
conn = MySQLdb.connect ( host = cfg.HOST, user = cfg.USER,\
                        passwd = cfg.PASSWORD,\
                         charset='utf8')
print "Connected."
# Get cursor
cur = conn.cursor(MySQLdb.cursors.DictCursor)
conn.select_db(cfg.DBNAME)

print "Start executing sql_sum"
cur.execute(sql_sum)
play = open(cfg.ROOT + '/data/derived/singers/artist_sum.txt', 'w') 
dates = []
for row in cur.fetchall():
    play.write(row['id']+'\t'+str(row['sum'])+'\n')



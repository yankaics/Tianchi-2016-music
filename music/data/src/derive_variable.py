#coding=utf-8

# 歌曲艺人
# 列名  类型  说明  示例
# song_id  String  歌曲唯一标识  c81f89cf7edd24930641afa2e411b09c
# artist_id  String  歌曲所属的艺人Id  03c6699ea836decbc5c8fc2dbae7bd3b
# publish_time  String  歌曲发行时间，精确到天  20150325
# song_init_plays  String  歌曲的初始播放数，表明该歌曲的初始热度  0
# Language  String  数字表示1,2,3…  100
# Gender  String  1,2,3  1

tc_songs_file = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/original/mars_tianchi_songs.csv', 'r')
tc_songs_lines = tc_songs_file.readlines()
tc_songs = [x.strip('\n').split(',') for x in tc_songs_lines]

songs_info = {}
for tc_song in tc_songs:
    songs_info[tc_song[0]] = tc_song

# 用户行为表
# 列名  类型  说明  示例
# 0. user_id  String  用户唯一标识  7063b3d0c075a4d276c5f06f4327cf4a
# 1. song_id  String  歌曲唯一标识  effb071415be51f11e845884e67c0f8c
# 2. gmt_create  String  用户播放时间（unix时间戳表示）精确到小时  1426406400
# 3. action_type  String  行为类型：1，播放；2，下载，3，收藏  1
# 4. Ds  String  记录收集日（分区）  20150315
tc_users_file = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/original/mars_tianchi_user_actions.csv', 'r')
tc_users_lines = tc_users_file.readlines()
tc_users = [x.strip('\n').split(',') for x in tc_users_lines]

# users_info[user_id] = [[user_id, song_id,...], ...]
#users_info = {}

#for tc_user in tc_users:
#    user_info = tc_user.split(',')
#    users_info[user_info[0]] = user_info


#
def generate_artist_list():
    artist_list = []
    print "Generating singer list"
    artist_list_file = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/derived/artist_list.txt', 'w')
    for line in tc_songs:
        artist = line.split(',')[1]
        if artist not in artist_list:
            artist_list.append(artist)
            artist_list_file.write(artist + '\n')
    print "Total " + str(len(artist_list)) + " artists"

# Singer information
# s

def generate_days():
    days = []
    print "Generating days"
    for tc_user in tc_users:
        Ds = tc_user[4]
        if Ds not in days:
            days.append(Ds)
    days.sort()
    days_file = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/derived/days_list.txt','w')
    i = 0
    for day in days:
        i += 1
        days_file.write(day+","+str(i) + "\n")
    print "finish"


def generate_artists_info():
    print "Start generating artists information"
    artists = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/derived/artist_list.txt', 'r').readlines()
    days = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/derived/days_list.txt', 'r').readlines()
    artists_infos = {}
    artists_appear = []
    for tc_user in tc_users:
        song_id = tc_user[1]
        artist_id = songs_info[song_id][1]
        if artist_id not in artists_appear:
            artists_appear.append(artist_id)
            artists_infos[artist_id] = {'1':{}, '2':{}, '3':{}}
            if artists_infos[artist_id][tc_user[3]].has_key(tc_user[4]):
                artists_infos[artist_id][tc_user[3]][tc_user[4]] += 1
            else:
                artists_infos[artist_id][tc_user[3]][tc_user[4]] = 1
        else:
            if artists_infos[artist_id][tc_user[3]].has_key(tc_user[4]):
                artists_infos[artist_id][tc_user[3]][tc_user[4]] += 1
            else:
                artists_infos[artist_id][tc_user[3]][tc_user[4]] = 1
    for artist in artists:
        artist = artist.strip('\n')
        artists_infos_file = open('/Users/wangyifan/workspace/python_workspace/tianchi/music/data/derived/singers/' + artist + ".txt",'w')
        line = artist + "\t"
        play = ""
        for day in days:
            day = day.strip('\n').split(',')[0]
            if artists_infos.has_key(artist):
                if artists_infos[artist].has_key('1'):
                    if artists_infos[artist]['1'].has_key(day):
                        play += str(artists_infos[artist]['1'][day]) + ","
                    else:
                        play += "0,"
                else:
                    play += "-1"
        artists_infos_file.write(line + play)
        print "finish artist: " + artist
    print "finish all"







# 1.
# generate_song_list()

# 2.
generate_days()

generate_artists_info()


# Tianchi-2016-music

Popular Music Prediction - Tianchi Big Data Challenge 2016


### Structure

    ___ROOT/
     |___README.md
     |___data/   Here store the original data and derived data (not features) as well as the code to generate them
       |___derived/
       | |___singers/    Here stores the derived data for singers
       | |___songs/  Here stores the derived data for songs
       |___original/
       |___src/ Here stores the code to generate derived data
         |___config/    Here stores the configuration files
         |___db/    Here stores the scripts to initialize the database

### How to use:

1. Add `__init__.py` and `config.py` to `config` directory, set the following variables:
 * `HOST` your database host
 * `USER` your database username ( use `mysql -u USER -p` to log in )
 * `PASSWORD` password
 * `DBNAME` the name of database ( use `use DBNAME` to select the database )
 * `ROOT` root path of git repository
 * `USER_ACTIONS` the path of `mars_tianchi_user_actions.csv` 
 * `SONGS` the path of `mars_tianchi_songs.csv` 

2. run `init.py` to add original data to database






echo "[data/derived/] generate artist list & day list"
python derive_variable.py

echo "[data/derived/singers/] daily play & download & collection" 
python artist_daily.py

echo "[data/derived/singers/] daily avg action"
pythob daily_avg_action.py

echo "[data/derived/singers/] daily highest play & download & collection"
python daily_highest_play.py

echo "[data/derived/singers/] daily etddev"
python daily_stddev_action.py

echo "[data/derived/singers/] gender"
python gender.py

echo "[data/derived/singers/] number of user for artist"
python number_of_user_for_artist.py

echo "[data/derived/singers/] number of artist's songs"
python sum.py

echo "[src/] Dumping data into txt files"
python generate_raw_data.py

echo "All done, bye"



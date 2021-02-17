#!/bin/bash
rm -rf game_raterapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations game_raterapi
python3 manage.py migrate game_raterapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata raters
python3 manage.py loaddata games
python3 manage.py loaddata pictures
python3 manage.py loaddata categories
python3 manage.py loaddata game_categories
python3 manage.py loaddata ratings
python3 manage.py loaddata reviews
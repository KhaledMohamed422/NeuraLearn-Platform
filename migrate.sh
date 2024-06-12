#!bin/bash
cd /code/

python manage.py migrate users
python manage.py migrate courses
python manage.py migrate
python manage.py loaddata auth.json users.json courses.json || true
# User End-Points Authentication:

## Features
- Register
- Email active
- Login
- Send reset password
- Reset password
- Logout
- Get user info
- Change user info
- Change user password
- Get users info

## Installation steps

1. Ensure you have python3 installed
2. Clone the repository
3. create a virtual environment using `virtualenv venv`
4. Activate the virtual environment by running `source venv/bin/activate`
- On Windows use `.\venv\Scripts\activate`
5. Install the dependencies using `pip install -r requirements.txt`
6. Make migration existing db tables by running `python manage.py makemigrations users --settings=NeuraLearn.settings.local`
7. Migrate existing db tables by running `python manage.py migrate --settings=NeuraLearn.settings.local`
8. Run the django development server using `python manage.py runserver --settings=NeuraLearn.settings.local`

## Installation With Docker
1. Clone the repository
2. Run the following command to start the Docker containers `docker-compose up`
3. Apply the migrations to users `docker compose exec web python /code/manage.py migrate users`
4. Apply the migrations to users `docker compose exec web python /code/manage.py migrate courses`
5. Apply the migrations to users `docker compose exec web python /code/manage.py migrate`
6. Create superuser (optional) `docker compose exec web python /code/manage.py createsuperuser`
7. Load some initial data courses `docker compose exec web python /code/manage.py loaddata courses.json`
8. Load some initial data users `docker compose exec web python /code/manage.py loaddata users.json`
9. Load some initial data auth `docker compose exec web python /code/manage.py loaddata auth.json`
10. Run celery worker`docker compose exec web celery -A NeuraLearn worker -l info`
11. Run flower to monitor celery tasks`docker compose exec web celery -A NeuraLearn flower`
12. Access the app at [http://localhost:8000](http://localhost:8000)

## Project Setup Backend (Using terminal)

1. Install **Python3** and **pip** for backend and **Node** and **NPM** for frontend
2. Create a virutal environment using command `python3 -m venv env` (here env is the name of environment that gets created)
3. Activate environment using commad `source env/bin/activate`
4. Clone the project or go into project directory
5. Run `pip install -r requirements.txt` This will install all the required libraries for python and Backend
6. Migrating Data
   - Run `python manage.py migrate` to migrate Django's built in model
   - Run `python manage.py makemigrations account` to make migrations for our models under account/models
   - Run `python manage.py migrate` to migrate account models
7. To load data from given **CSVs**
   - Run `python manage.py extract_faculty` for populating professor data
   - Run `python manage.py extract_student` for populating student datt
   - Run `python manage.py extract_posts` for populatuing forum and post data

## Project Setup Frontend

1. Then run go to **frontend** folder by running `cd frontend`
2. Run command `npm i`. This will install all required libraries needed for frontend
3. Go to root directory of project and run `python manage.py runserver` This will start backend server.
4. To run frontend, open a different terminal and go to frontend directory and run `npm run dev`
5. Now enter `http://localhost:8000` in browser url to see the project running

## Admin Page

Admin page can be accessed by going to address `http://localhost:8000/admin` . To login into admin create a superuser first by running `python manage.py createsuperuser` in project root directory. Enter **username**, **email** and **password** and use these username and password to login into admin.

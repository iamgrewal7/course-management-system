## Project Setup (Using terminal)

1. Install **Python3** and **pip** for backend and **Node** and **NPM** for frontend
2. Create a virutal environment using command `python3 -m venv env` (here env is the name of environment that gets created)
3. Activate environment using commad `source env/bin/activate`
4. Clone the project or go into project directory
5. Run `pip install -r requirements.txt` This will install all the required libraries for python and Backend
6. Then run go to **frontend** folder by running `cd frontend`
7. Run command `npm i`. This will install all required libraries needed for frontend
8. Go to root directory of project and run `python manage.py runserver` This will start backend server.
9. To run frontend, open a different terminal and go to frontend directory and run `npm run dev`
10. Now enter `http://localhost:8000` in browser url to see the project running

## Admin Page

Admin page can be accessed by going to address `http://localhost:8000/admin` . To login into admin create a superuser first by running `python manage.py createsuperuser` in project root directory. Enter **username**, **email** and **password** and use these username and password to login into admin.

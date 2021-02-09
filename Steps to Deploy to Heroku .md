# How to Deploy Django web app on Heroku direcly from git (automatic deployment from git) with postgresql as a database?

- Steps to follow:-

1. Goto your project directory, and create a virtual environment using either `python3 -m venv venv` or `virtualenv venv`.
2. Now install the necessary packages, modules in the newly created env. To activate the environment either use `source venv/bin/activate` on linux, and if on windows `venv\Scripts\activate` on windows.
3. To install the packages and modules, use pip `pip install gunicorn whitenoise dj-database-url`. These are the additional packages that we need to install. Make sure to make the requirements.txt file and add these packages in that.
4. Setting up whitenoise,
   Add this to your seetings.py in the middleware at the second position from the top. `"whitenoise.middleware.WhiteNoiseMiddleware",`
   Now add, `STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"` at the end in the Static files section in settings.py file.
5. Setting up STATIC ROOT AND MEDIA ROOT, paste the following at the end in the static files section,

   STATIC_URL = "/static/"

   STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

   STATICFILES_DIRS = [os.path.join(BASE_DIR, "web_main/staticfiles")]

   MEDIA_URL = "/media/"

   MEDIA_ROOT = os.path.join(BASE_DIR, "media")

6. Setting up gunicorn, we have set STATIC ROOT and MEDIA ROOT. So what we need to do now is to create `Procfile` ( with no extension). Head over to the directory where manage.py is present and create Procfile using `touch Procfile` or `cd . > Procfile`.
   In that, paste this
   web: gunicorn <`name of directory where wsgi is present`>.wsgi:application --log-file - --log-level debug
   ( Note: The above line is very important )
   python manage.py collectstatic --noinput  
    For eg,
   web: gunicorn web_main.wsgi:application --log-file - --log-level debug
   python manage.py collectstatic --noinput

As you can here on the second line we can input the command the we want like if we want the script to run, we can do this by `python3 manage.py runscript <name of script file(without extension)>` Note that script folder must be set before doing this if you are doing so.

7.  Setting up runtime.txt, create a file runtime.txt ( in the directory where manage.py file is present). And check your python version installed in your virtualenv using `python3 --version` and set the version same as the eg. given below.
    For eg.
    `python-3.8.5` this is the python version you want Heroku to use while building.

8.  Setting up settings.py for Database and credentials.
    You can setup you .env file for local postgres while development use `python-decouple` for that. (Just a suggestion) and then you can use try and except when setting up for production.

    while in development:-
    DATABASES = {
    "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "USER": os.environ.get("DB_USER"),
    "NAME": os.environ.get("DB_NAME"),
    "HOST": os.environ.get("DB_HOST"),
    "PASSWORD": os.environ.get("DB_PASSWORD"),
    "PORT": os.environ.get("DB_PORT"),
    },
    }

    when deploying:
    try:
    DB_HEROKU_URL = os.environ.get("DB_HEROKU_URL")
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DATABASES["default"] = dj_database_url.config(default=DB_HEROKU_URL)
    DATABASES["default"] = dj_database_url.parse(DB_HEROKU_URL, conn_max_age=600,)

    except:
    DB_HEROKU_URL = os.environ.get("DATABASE_URL")
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DATABASES["default"] = dj_database_url.config(default=DB_HEROKU_URL)
    DATABASES["default"] = dj_database_url.parse(DB_HEROKU_URL, conn_max_age=600,)

    Now after doing all this we need to set up our local postgresql database on heroku.
    So let's go to your heroku cli.

9.  Install heroku cli, `sudo snap install --classic heroku`. After this, login by `heroku login` ( follow the process on browser, it will automatically login).

10. Now create your app on heroku by `heroku create <name of app>`. And then, you will get a url of your app. Set this up in your settings.py file in ALLOWED_HOSTS. You can set your herokuapp url and localhost url there.
    `ALLOWED_HOSTS =['127.0.0.1','<name of app>.herokuapp.com']`

11. Setting up `Django_Secret_key`, so for setting up secret_key on heroku, use `heroku config:set SECRET_KEY="<your secret key>`. Similarly add your other important credentials if any. Like, Set `DEBUG=False`

- In case you want to unset use ` heroku config:unset <Name of that variable>`
- If you want to see all your env variables of that app. Go into your local project directory and then, `heroku config -j`
- For help on heroku, `heroku help` and `heroku config --help`

12. Setting up postgresql database on heroku. For setting up heroku datbase in your project, Folow Step 8.
    Now on `heroku cli`, first check if any addon is added or not.
    `psql` is used as an addon in heroku. If not register for the free version of psql by `heroku addons:create heroku-postgresql:hobby-dev`

- `hobby-dev` is the free version of psql. To know more type, `heroku pg`

13. You can see on your `heroku dashboard`, postgres database in the resources.
    Now we need to push our local database on heroku postgres. By default, in free version we are given 10,000 rows limit on DB.

- Note:- For that, grab the url `heroku config -s | grep DATABASE_URL`. Note this command is for info. We have already setup `DATABASE_URL` variable in step 8 in our settings.py. So when deploying heroku will get the `DATABASE_URL` variable if present and will be able to detect the database.

14. PUSHING LOCAL DATABASE TO HEROKU POSTGRES DB. To know the DB name, `heroku pg`.
    On heroku cli using this `PGUSER=postgres PGPASSWORD=password heroku pg:push postgres://<name_of_host>/<name_of_your_local_database> name_of_Heroku_DATABASE`

For eg. `PGUSER=postgres PGPASSWORD=password heroku pg:push postgres://localhost/DB_NAME name_of_Heroku_DATABASE`

15. Disable collectstatic by `heroku config:set DISABLE_COLLECTSTATIC=1`

16. Note that you must create a .gitignore file if you want some files not want to be tracked by git. Also before commiting all your changes make sure to remove all the non-used imports.

17. After all these steps, make sure your `requirements.txt` is updated. To update `pip3 freeze > requirements.txt`. Now commit all the changes and push to your github repo and then go to your heroku dashboard. You will see an app created click on that, and under `deploy` Enable Github Coneection and set the repo and project directory.

Now finally, click on `Deploy changes`. And in the end, enable `Github automatic deployment`. It should work hopefully.

- Note:- If not, you can see the error it shows while deploying using `heroku logs --tail`. I fanything comesup try to fix it or google it.
  Mostly the error is due to the misconfigured Procfile. Try to set the right path of the wsgi file. It will then work flawlessly.

# Where did I got stuck for the first time?

First of all when we setup the project we keep the project inside the folder, and outside that folder we keep our `requirements.txt` file and other contributing.md, Readme file etc. But I have noticed that heroku is not able to find the Procfile when kept in this way.

Solution to that I came out with was to initialize the git repo in the directory where manage.py was present.

I mean i tries that way but was not able to successfully dedployed, everytime I tried that Heroku was not able to find the Procfile. I will try to fix that issue, as i think I'm missing something.

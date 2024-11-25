# Hotel Manager Assignment
This small project was made as an assignment for Maykin Media. It contains a small Django project that fetches CSV data over HTTP, transforms it into database data, and then uses it to provide a front-end for hotel managers. This README briefly describes some details of this project and how to get it up and running.

## Design Choices
### Database
As database, SQLite was used. This is because for a small assignment like this, it is a quicker/easier setup than a 'dedicated' RDBMS such as MySQL. In a real project, I would use MySQL or a similar database system since it would likely have performance benefits.

### Front-end technology
I chose to implement the front-end using native Javascript alongside Django's built-in templating engine. Since this was a small project, this was little hassle and I felt like using a big framework might have made the project feel a bit bloated. In a 'real'/bigger project, I would most likely have chosen a 'reactive' framework such as React, Svelte or something similar.

### Markup
On the front-end, I chose to use the CDN of TailwindCSS for the CSS styling. While I could have used native CSS too, it's very little hassle to setup Tailwind using the CDN script-url, and it made styling the front-end feel much more comfortable for me since I'm used to working with it.

## Setting up the project

### With Docker
To easily set up the project locally, the project has a Dockerfile that handles nearly everything automatically. To use it, perform the following steps:

After cloning the project, navigate into the root folder. Since the project relies on some environment variables, first create a `.env` file and place it in the root folder. Then paste the following into it:
```
SECRET_KEY=
CITY_CSV_URL=
HOTEL_CSV_URL=
AUTH_USERNAME=
AUTH_PASSWORD=
```
And then fill in the environment variables.
((note: I've sent the values for these environment variables in my Email to you. You already have most of them yourselves, except the secret key))

Then build the Dockerfile with:
```
docker build -t hotel-app .
```

Then run it with:
```
docker run --name hotel-app -p 8000:8000 hotel-app
```

The server then runs on:
```
http://localhost:8000
```

The project also has functionality set up to use the Django admin dashboard to view the database tables. The admin user still needs to be created in your local database however. To do this, first enter the containers TTY with:
```
docker exec -it hotel-app /bin/sh
```

and then run the following command:
```
python manage.py createsuperuser
```

and then follow the steps. The admin dashboard will then be available on:
```
http://localhost:8000/admin
```

### Manually

After cloning the project and navigating to the folder, create an isolated environment for the projects' dependencies using Venv:
```
python -m venv venv
```

Then activate it (note that the command might be different on Windows):
```
source venv/bin/activate
```

Then when you're inside the Venv environment, install the dependencies using pip:
```
pip install -r requirements.txt
```

Then, add a `.env` file to the root directory and paste in the following contents:
```
SECRET_KEY=
CITY_CSV_URL=
HOTEL_CSV_URL=
AUTH_USERNAME=
AUTH_PASSWORD=
```
And then fill in the environment variables.

((note: I've sent the values for these environment variables in my Email to you))

Before the project can be started, run the following commands to properly set up the database and cronjob:
```
python manage.py makemigrations
python manage.py migrate
python manage.py crontab add
```

Note that at this point the database is still empty. Even though there is a cronjob set up that populates the database, it is only triggered at 2:00 AM every day. To fill the database right now with the CSV data, run the following command:
```
python manage.py import_csv_data
```

Lastly, since the project is setup to work with an admin interface, you can generate an admin account in the database with:
```
python manage.py createsuperuser
```
and then follow the steps in the terminal.

At this point the application is ready to start. Run it with:
```
python manage.py runserver
```

The server then runs on:
```
http://localhost:8000
```
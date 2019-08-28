# Shop Score Page

[This site](https://dvmn-shop-score2.herokuapp.com/)  is a simple service to control order processing. Index page displays total score as pie chart shows how many orders waiting confirmation and how long. Based on Flask with PostgreSQL and Matplotlib for drawing the pie chart.


# How to Install

Python 3.6 and libraries from **requirements.txt** should be installed. Use virtual environment tool, for example **virtualenv**.

```bash

virtualenv virtualenv_folder_name
source virtualenv_folder_name/bin/activate
python3.6 -m pip install -r requirements.txt
```

Put all necessary parameters to .env file.

```bash
HOST=127.0.0.1
PORT=5000
PG_HOST=postgresql_host
PG_PORT=postgresql_port
PG_DB=postgresql_db
PG_TABLE=postgresql_table
PG_USER=postgresql_user
PG_PWD=postgresql_password
TIME_UNIT=hour
TIME_MULT=3600
TIME_LIMITS=[[0, 80], [80, 160], [160, 240]]
```

FLASK_DEBUG environment variable Flask loads by itself, but for PORT loading we should use python-dotenv package.


# Quickstart

1. Run **server.py**.

```bash

$ python server.py

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with inotify reloader
 * Debugger is active!

```

2. Goto [http://127.0.0.1:5000/ ](http://127.0.0.1:5000/ )


# How to Deploy

For example, you can deploy the site on [Heroku](https://heroku.com), with
GitHub integration.

1. Create a new app on Heroku with GitHub deployment method.

2. Do not forget about **Procfile**:

```bash

web: python3 server.py

```

3. Add your environment variables to Settings > Config Vars section. Use PORT=80 and HOST=0.0.0.0

4. Open https://[your-app-name].herokuapp.com/ in your browser

5. For reading logs install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install), log in and use:

```bash
$ heroku logs -t --app app-name
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

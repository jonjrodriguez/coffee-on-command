# Coffee on Command

## Setup App

Requirements:

- python 3.7
- pyenv
- postgres
- redis
- ngrok

Create and enter a virtualenv

```bash
pyenv install 3.7.4
$(pyenv root)/versions/3.7.4/bin/python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Setup Local DB

```bash
createdb <db_name>
createuser --superuser --createdb --createrole --login --encrypted <username>
./manage.py migrate
./manage.py loaddata recommendations
```

Setup Local Settings

1. `cp config/local_settings.py app/local_settings.py`
2. Update relevant values (ie. `db_name` and `username` from above)

## Run App

```bash
./manage.py runserver
ngrok http 8000
celery worker --loglevel=info -A app
```

Save your `ngrok` address from above. You'll need it when configuring a Slackbot.
You can also view and replay your incoming requests at http://127.0.0.1:4040.

## Setup Slack

1. Go to https://api.slack.com/apps -> Create App
   - Enter App Name
   - Choose development workspace
2. Enable Interactive Components
   - Request URL: `ngrok_url/response`
3. Enable slash commands
   - Request URL: `ngrok_url/command`
   - Command: something unique
4. Create a bot user
5. Enable events
   - Request URL: `ngrok_url/event`
   - Add Bot events: `member_joined_channel`, `member_left_channel`
6. Finally go to `Install App` -> `Reinstall App`

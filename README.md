# Coffee on Command

## Setup App

(Assumes pyenv and postgres are already setup)

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
createdb coffee_on_command
createuser --superuser --createdb --createrole --login --encrypted coffee_on_command
./manage.py migrate
./manage.py createsuperuser
```

Setup Local Settings

1. Copy `local_settings.copy` -> `local_settings.py` and update the values

## Run App

```bash
brew cask install ngrok
./manage.py runserver
ngrok http 8000
```

Save your `ngrok` address from above. You'll need it when configuring a Slackbot.
You can also view and replay your incoming requests at http://127.0.0.1:4040.

## Setup Slack

1. Go to https://api.slack.com/apps -> Create App
   - Enter App Name
   - Choose development workspace
2. Enable Interactive Components using your `ngrok` address + `/response`
3. Enable slash commands using your `ngrok` address and a unique command
4. Create a bot user
5. Enable incoming webhooks
   - Add new webhook to a development channel for your slack app
6. Finally go to `Install App` -> `Reinstall App`


## Celery Setup
If you want to run it async, you should install redis and start redis
```
redis-server
```
Start celery worker
```
celery worker --loglevel=info -A app
```
If you want to run it synchronously, you can set `CELERY_TASK_ALWAYS_EAGER=True` in `settings.py`
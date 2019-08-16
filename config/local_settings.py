# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Celery

CELERY_BROKER_URL = "redis://localhost"

# Integrations

SLACK = {"BOT_TOKEN": "", "CHANNEL": "", "SIGNING_SECRET": ""}

# Demo
LANDING_PAGE_REDIRECT = ""

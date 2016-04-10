import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = ''

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


GA_CODE = ""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""


EMAIL_HOST = ""
EMAIL_PORT = 0


EMAIL_USE_TLS = True
SERVER_EMAIL = ""

ADMINS = (.)

"""
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if socket.gethostname().upper() == "FEYNMAN":
    DEBUG = True
    IS_LIVE = False
    SITE_ROOT = "http://127.0.0.1:8000"
else:
    SITE_ROOT= "http://postalvote.inkleby.com"
    DEBUG = False
    IS_LIVE = True

USE_L10N  = False
DATE_FORMAT = 'j N, Y'


from .config import * #stores database and key outside repo


ALLOWED_HOSTS = ["127.0.0.1","testserver","postalvote.inkleby.com"]

PROJECT_PATH = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        'DIRS': [
                 PROJECT_PATH + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'proj.universal.universal_context',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


STATICFILES_DIRS = (
    PROJECT_PATH + '/static/',
    #"E:\\display_maps",
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'postalvote',
    'useful_inkleby.useful_django',
    'django.contrib.humanize',
    'bootstrapform',
    #'jsignature'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
)

ROOT_URLCONF = 'proj.urls'

WSGI_APPLICATION = 'proj.wsgi.application'

HTML_MINIFY = not DEBUG

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_NAME = "Postal Vote Helper"

SITE_DESC = "A site to help you apply for a Postal Vote"

SITE_TWITTER = "inkleby"

MAIN_MENU = []

SHARE_IMAGE = "http://postalvote.inkleby.com/static/images/postalvote.png"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
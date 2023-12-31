"""
Django settings for fuzolo_pickup project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
config_path = os.path.join(BASE_DIR, 'fuzolo_pickup/variables_config.json')

with open(config_path) as config_file:
    config = json.load(config_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['172.105.58.248', 'www.fuzolo.in', 'fuzolo.in']
ALLOWED_HOSTS = [config['IP_ADDRESS'], 'fuzolo.in', 'www.fuzolo.in', 'localhost']

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic', #for hosting static files on live server
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #myapps
    'users',
    'fuzolo_pickup',

    #3rd party
    'crispy_forms', # for the forms 
    'crispy_bootstrap4',
    'django_celery_results',
    'django_celery_beat'
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware', # for serving the static files 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#custom authenticate using phone number
AUTHENTICATION_BACKENDS = [
    'users.custom_authenticate.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',  # Include the default ModelBackend as a fallback
]


SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'fuzolo_pickup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['users/templates/users/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fuzolo_pickup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.FuzoloUser'

#login url if the user wants to book a slot but is not logged in 
LOGIN_URL = 'mobile-login'


#CELERY SETTING
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'


#To get info of task(pending/completed) by celery
CELERY_RESULT_BACKEND = 'django-db'

#CELERY BEAT SETTING
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


#Environment Variables
TWILIO_ACCOUNT_SID = config["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
TWILIO_COUNTRY_CODE = config["TWILIO_COUNTRY_CODE"]
TWILIO_WHATSAPP_NUMBER = config["TWILIO_WHATSAPP_NUMBER"]
TWILIO_PHONE_NUMBER = config["TWILIO_PHONE_NUMBER"]
RZP_ACCOUNT_ID = config["RZP_ACCOUNT_ID"]
RZP_KEY = config["RZP_KEY"]
WHASTSAPP_KEY = config["WHASTSAPP_KEY"]
RZP_REDIRECT = config['RZP_REDIRECT']

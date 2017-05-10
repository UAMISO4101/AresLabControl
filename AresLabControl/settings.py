from __future__ import print_function

import os
import sys
import urlparse

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=c2c#@97z8t(8q_=ahcxqydkj(6%ckc6jzmuq87pha5bd@cnh%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party Apps
    'crispy_forms',
    'django_extensions',
    'registration',
    'storages',
    'widget_tweaks',
    # Our Apps
    'LabModule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'AresLabControl.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AresLabControl.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SOUTH_TESTS_MIGRATE = False

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : 'test_dblpbhpi2otb4q'
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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

# Globalization (i18n/l10n)
# https://docs.djangoproject.com/en/1.10/ref/settings/#globalization-i18n-l10n
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# Default formatting for date objects. See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
DATE_FORMAT = 'D, j F Y'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGE_CODE = 'es-co'

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('es-co', _('Colombian Spanish')),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'conf/', 'locale/')]

TIME_ZONE = 'America/Bogota'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_in_env', 'static_root')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static", "lab_static"),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

AUTH_PROFILE_MODULE = 'LabModule.Usuario'

# Crispy Forms Tag Settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django Registration Redux Settings
REGISTRATION_OPEN = False
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email Configuration Settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cuentatestares@gmail.com'
EMAIL_HOST_PASSWORD = '123456789E'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

GRAPH_MODELS = {
    'all_applications': True,
    'group_models'    : True,
}

# Atributos por defecto para creacion de superusuario
SUPERUSUARIO = 'admin'
CONTRASENA = '1a2d3m4i5n6'

# Atributos para conectarse al S3 de amazon
AWS_STORAGE_BUCKET_NAME = 'maquinasymuestras'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

AWS_ACCESS_KEY_ID = 'AKIAJWOKWCK44OHCI6XA'
AWS_SECRET_ACCESS_KEY = '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'

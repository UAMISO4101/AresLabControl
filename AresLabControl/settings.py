from __future__ import print_function

import os
import urlparse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ["SECRET_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party Apps
    'crispy_forms',
    'django_extensions',
    'registration',
    #Our Apps
    'LabModule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AresLabControl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'AresLabControl.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

DATABASES = {
       # 'default': {
       #  'ENGINE': 'django.db.backends.postgresql',
       #  'NAME': url.path[1:],
       #  'USER': url.username,
       #  'PASSWORD': url.password,
       #  'HOST': url.hostname,
       #  'PORT': url.port,
       #  }
    'default': {
          'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'areslab',
        'HOST':'127.0.0.1',
       'PORT':'5432',
      'USER':'postgres',
     'PASSWORD':'admin'
    }
    # 'default': {
    #       'ENGINE': 'django.db.backends.postgresql',
    #       'NAME': 'lab',
    #       'HOST':'127.0.0.1',
    #       'PORT':'5432',
    #       'USER':'postgres',
    #       'PASSWORD':''
    #   }
    #
    # 'default': {
    #       'ENGINE': 'django.db.backends.postgresql',
    #       'NAME': 'areslab',
    #       'HOST':'localhost',
    #       'PORT':'5432',
    #       'USER':'postgres',
    #       'PASSWORD':'admin'
    #   }
    #    'default': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #    }
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

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_in_env', 'static_root')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static", "lab_static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('media')
#MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_in_env', 'media_root')

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

# Email Configuration Settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cuentatestares@gmail.com'
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = 587
EMAIL_USE_TLS = True


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# Atributos por defecto para creacion de superusuario (pasar a variables de entorno)
SUPERUSUARIO = os.environ["SUPERUSUARIO"]
CONTRASENA = os.environ["CONTRASENA"]


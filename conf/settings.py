"""
Django settings for gigsblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uasrguvmrz@-^kcm@c0u3ucu+am9$e70yf%fhkg+@6&1u3a2mw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'mongoengine.django.mongo_auth',
    'apps.blog',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PASSWORD_HASHERS = (
 'django.contrib.auth.hashers.BCryptPasswordHasher',
)

# ROOT_URLCONF = 'conf.urls'
ROOT_URLCONF = 'urls.main'

WSGI_APPLICATION = 'conf.wsgi.application'

# **************** AUTHENTICATION ***************
LOGIN_URL = 'login'

# LOGIN_REDIRECT_URL = '/accounts/profile/'

# LOGOUT_URL = '/accounts/logout/'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)


# MONGOENGINE_USER_DOCUMENT = 'apps.blog.models.User'

AUTH_USER_MODEL = 'mongo_auth.MongoUser'

MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'

SESSION_ENGINE = 'mongoengine.django.sessions'

TEST_RUNNER = 'config.tests.MongoTestSuiteRunner'

from mongoengine import *
connect('gigsblog')

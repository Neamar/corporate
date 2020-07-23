"""
Django settings for corporate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else "test_key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "DEBUG" in os.environ and bool(os.environ["DEBUG"])

TEMPLATE_DEBUG = True


def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    # ...
    'SHOW_TOOLBAR_CALLBACK': 'corporate.settings.show_toolbar',
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    #'compressor',
    'website',
    'docs',
    'engine',
    'logs',
    'engine_modules.influence',
    'engine_modules.corporation',
    'engine_modules.invisible_hand',
    'engine_modules.vote',
    'engine_modules.citizenship',
    'engine_modules.share',
    'engine_modules.run',
    'engine_modules.corporation_run',
    'engine_modules.corporation_asset_history',
    'engine_modules.player_run',
    'engine_modules.speculation',
    'engine_modules.effects',
    'engine_modules.detroit_inc',
    'engine_modules.wiretransfer',
    'engine_modules.market',
    'engine_modules.end_turn',
    'engine_modules.player_points',
    'engine_modules.player_messages',
    # 'storages',  # to store avatar on AWS
    'stdimage',  # standard image field to resize avatars and use bd id for names
    # 'debug_toolbar',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'corporate.urls'

WSGI_APPLICATION = 'corporate.wsgi.application'


# settings.py
AUTH_USER_MODEL = 'website.User'
LOGIN_REDIRECT_URL = 'website.views.index.index'
LOGIN_URL = 'django.contrib.auth.views.login'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#For Azure SQL server database
#DATABASES = {
#    'default': {
#        'ENGINE': 'sql_server.pyodbc',
#        'NAME': os.environ.get('DATABASENAME'),
#        'USER': os.environ.get('DATABASEUSER'),
#        'PASSWORD': os.environ.get('DATABASEPASSWORD'),
#        'HOST': os.environ.get('DATABASEHOST'),
#    },
#}

# for sqlLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Security
ALLOWED_HOSTS = ["localhost", "corporategame.me", "corporate-game-pr-131.herokuapp.com"]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/opt/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static"),)
for staticfile_dir in STATICFILES_DIRS:
    if not os.path.exists(staticfile_dir):
        os.mkdir(staticfile_dir)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)
MEDIA_URL = "/media/"

#COMPRESS_PRECOMPILERS = (
#    ('text/less', 'scss {infile} {outfile}'),
#)
#COMPRESS_OUTPUT_DIR = "cache"
#COMPRESS_ENABLED = True


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)


# Settings for the game
if "test" in " ".join(sys.argv):
    CITY = "Test"
else:
    CITY = "Detroit"

CITY_BASE_DIR = "%s/data/cities/%s" % (BASE_DIR, CITY.lower())


# Environment overrides
if "PYTHON_ENV" in os.environ and os.environ["PYTHON_ENV"] == "production":
    DEBUG = os.environ['DEBUG'] if 'DEBUG' in os.environ else False

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Compress less file on deployment
    # COMPRESS_OFFLINE = True


if "OPBEAT_ORGANIZATION_ID" in os.environ:
    INSTALLED_APPS += (
        "opbeat.contrib.django",
    )
    OPBEAT = {
        "ORGANIZATION_ID": os.environ['OPBEAT_ORGANIZATION_ID'],
        "APP_ID": os.environ['OPBEAT_APP_ID'],
        "SECRET_TOKEN": os.environ['OPBEAT_SECRET_TOKEN'],
    }
    MIDDLEWARE_CLASSES += (
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    )

if "CIRCLECI" in os.environ:
    # We're running on circleci.com, toggle XML test output
    TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
    TEST_OUTPUT_DIR = os.environ['CIRCLE_TEST_REPORTS']

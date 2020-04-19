#Django social auth settings

# Django settings for LinkedIN project.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Haseeb Ahmad', 'haseebahmad109@gmail.com'),
)


MANAGERS = ADMINS
# rempte db provided by heroku postgresql
#"""
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'damtmnm46gfj1d',
    'HOST': 'ec2-174-129-33-159.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'lntgcwevjvicxn',
    'PASSWORD': 'b384c0ace52228671714cb2a26ea69b81183f0b6e6e1e686643a7a9ab5da7bca'
  }
}
#"""

#for localhost
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'LinkedinDB_Test',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
"""


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

from os.path import abspath, dirname, join, normpath
DJANGO_ROOT = dirname(abspath(__file__))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = normpath(join(SITE_ROOT, 'LinkedApp/media/'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'



# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"


STATIC_ROOT = normpath(join(SITE_ROOT, 'LinkedApp/static/'))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    #"LinkedApp/static/",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'co($*99^hpgg=b#zgpb&9x(!@6u5l5^oh9d9nbz%t+b=-1*yl6'

# List of callables that know how to import templates from various sources.




TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader',
    (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    ),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    #'social_auth.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'LinkedIN.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'LinkedIN.wsgi.application'

import os
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),
    #'/home/haseeb/Documents/UniWork/django/Projects/Sprint2 Repo/LinkedIN/templates',
    #'/home/haseeb/Documents/UniWork/django/Projects/Sprint2 Repo/LinkedIN/LinkedApp/templates'
    #'/abdul/Documents/Projects/LinkedIN/templates',
    #'/abdul/Documents/Projects/LinkedIN/LinkedApp/templates',

)

""" localhost ids
GOOGLE_OAUTH2_CLIENT_ID = '410674073935.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'mYY3S41fndp-ddY8S-Sly-XP'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.google.com/m8/feeds']

LIVE_CLIENT_ID = '000000004C10094A'
LIVE_CLIENT_SECRET = 'ZrmLXf1h2lj9Yb-dWGP1oZi4lJFg8PzP'

YAHOO_CONSUMER_KEY = 'dj0yJmk9TVMyeWhHNk5YNUJhJmQ9WVdrOVZWVnVSR1V5TldjbWNHbzlNakExTURBMk1ESTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1jMw--'
YAHOO_CONSUMER_SECRET = '51b4310a0f938c2412c72b095c464fbe460ccda1'
"""

#localhost
#BASE_URL = "http://mylinkedin.com:8000"

#Heroku
BASE_URL = "http://mylinkedin.herokuapp.com"



#""" heroku ids

GOOGLE_OAUTH2_CLIENT_ID = '801022486996.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '7fygcfhMe-00VK90UQoRDz7o'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.google.com/m8/feeds']

LIVE_CLIENT_ID = '0000000048105F4F'
LIVE_CLIENT_SECRET = 'dNs1YXdFJZ6D5qQf45DfeqI5lAM9Vozm'

YAHOO_CONSUMER_KEY = 'dj0yJmk9TVMyeWhHNk5YNUJhJmQ9WVdrOVZWVnVSR1V5TldjbWNHbzlNakExTURBMk1ESTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1jMw--'
YAHOO_CONSUMER_SECRET = '51b4310a0f938c2412c72b095c464fbe460ccda1'

#"""""""""""""""


AUTHENTICATION_BACKENDS = (
  'social_auth.backends.google.GoogleOAuth2Backend',
  'django.contrib.auth.backends.ModelBackend',
  'social_auth.backends.facebook.FacebookBackend',
  'social_auth.backends.contrib.live.LiveBackend',
  'social_auth.backends.yahoo.YahooBackend',
)

SOCIAL_AUTH_CREATE_USERS = False

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.load_extra_data',
    'LinkedApp.backends.api_contacts',
)

#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
    'LinkedApp.contextProcessors.notifications',
    'django.core.context_processors.request',
)

LOGIN_URL = '/sign-in/'

CONTACTS = {}

MESSAGE = ""

AUTH_USER_MODEL = 'LinkedApp.User'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'LinkedApp',
    'social_auth',
    'endless_pagination',
)


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'infoomylinkedin@gmail.com'
EMAIL_HOST_PASSWORD = 'capricorn1993'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'infoomylinkedin@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



# Parse database configuration from $DATABASE_URL
#import dj_database_url
#DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


SOCKJS_PORT = 9999
SOCKJS_CHANNEL = 'echo'
SOCKJS_CLASSES = (
    'LinkedApp.sockserver.ChatConnection',
)


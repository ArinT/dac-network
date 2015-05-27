"""
Django settings for DAC_network_analysis project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qenk02i3^te@g6u)195$hj_nq+x+p#5=9tl+7(gx^qav7__vce'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

#TEST EMAIL STUFF
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dacnetworkanalysis@gmail.com' #Used to the Feedback tab and sending feedback
EMAIL_HOST_PASSWORD = 'uiucsummer'
EMAIL_PORT = 587

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'network_visualizer',
    'south',
    'djangular' # Interface between Angular.js and Django
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DAC_network_analysis.urls'

WSGI_APPLICATION = 'DAC_network_analysis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default':
        { #The MySQL database info
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'DACNetworkAnalysis',
            'USER': 'ebroot',
            'PASSWORD': 'citations1',
            'HOST': 'dac-network.c8kxvfryaahi.us-west-2.rds.amazonaws.com',
            'PORT':'3306'
        },
        'debug':
         {
             'ENGINE':'django.db.backends.sqlite3',
             'NAME': 'debug',
         }
}


# DATABASES = {
#     'default':
#         { #The MySQL database info
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'DACNetworkAnalysis',
#             'USER': 'ebroot',
#             'PASSWORD': 'citations1',
#             'HOST': 'dacnetworkanalysis.c8kxvfryaahi.us-west-2.rds.amazonaws.com',
#             'PORT':'3306'
#         },
#         'debug':
#          {
#              'ENGINE':'django.db.backends.sqlite3',
#              'NAME': 'debug',
#          }
# }

#dac-network.c8kxvfryaahi.us-west-2.rds.amazonaws.com:3306 new host name

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

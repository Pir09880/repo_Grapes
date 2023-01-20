"""
Django settings for SampleDjangoWebApp02 project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a7c86ed6-fa4b-4543-bfb1-441158c96be0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SampleDjangoWebApp02.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'SampleDjangoWebApp02.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

# Media Files (jpg,jpeg,png)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_local')
MEDIA_URL = '/media/'

#InstagramAPIアカウント情報
IS_ACCESS_TOKEN         = 'EAAwdPYqXkMIBAHo5JRZCGTRzbDCQ0qEc0CAJZBrXKPtaHOpLzZAE88dn2dyRO6mcjdEZC234G5WMdYi3DRKZCfcinWTLDP3X3VGxUPGt7bN8ZCeUvXxtLK57hcwDcggrIx6ZBmQyyD0vIrZCATnQslSfrWsBAlSLfZCx8HHfI3EkwowAKSJcE7Ifh'
IS_APP_ID               = '3409849875927234'
IS_APP_SECRET           = 'c4a17f95489d797366dd0da404f9d0f2'
IS_INSTAGRAM_ACCOUNT_ID = "17841456624391358"
IS_VERSION              = 'v15.0'
IS_GRAPH_DOMAIN        = 'https://graph.facebook.com/'

#TwitterAPIアカウント情報
TW_BEARER_TOKEN        = "AAAAAAAAAAAAAAAAAAAAAETpkQEAAAAAW1PfA0QNSH%2BMrRUSPIdq1PnGxfs%3DbRoGBVoIukkcWRrB9hL9DrdncVJPgda0l1xaJIDxBigBEnl1Fl"
TW_API_KEY             = "NvEJeoArC4QX6Rdpz33hxKaxI"
TW_API_SECRET          = "uti6LPMNA5ajH3GOd8iTydRs2CaltcFK5eu84EV1bO1rKy5U3W"
TW_ACCESS_TOKEN        = "1603553576587911169-GMMsPWgC0dob7mFlYIzSqLLbWudauH"
TW_ACCESS_TOKEN_SECRET = "yEtVMBUHGmMw1lafHBE8lCpxDbgM4yqAWDnQe9zuG5bS1"
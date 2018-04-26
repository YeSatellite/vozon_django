# coding=utf-8
# ====================BASE==================== #

import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'config.urls'
AUTH_USER_MODEL = 'user.User'

# ====================APPS==================== #

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
]

LOCAL_APPS = [
    'apps.core.apps.CoreConfig',
    'apps.info.apps.InfoConfig',
    'apps.user.apps.UserConfig',
    'apps.client.apps.ClientConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ====================TEMPLATES & DATABASES==================== #
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')],
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
# ====================???==================== #
# Password validation
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
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ====================Internationalization==================== #
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ====================PATH & URL==================== #
# Static
STATIC_ROOT = str(BASE_DIR / 'static')
STATIC_URL = '/static/'
# Media
MEDIA_ROOT = str(BASE_DIR / 'media')
MEDIA_URL = '/media/'

# ====================REST_FRAMEWORK==================== #
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    'EXCEPTION_HANDLER': 'apps.core.utils.custom_exception_handler',

}
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1000),
}

"""
101 : nomer uzhe bar
102 : nomer tirkelmegen
103 : sms kate
"""

ERROR_CODE = {
    ('phone', 'user with this phone already exists.'): 101,
    ('phone', "phone doesn't exist"): 102,
    ('sms', 'sms not correct'): 103,
}

PUSH_NOTIFICATIONS_SETTINGS = {
        "APNS_CERTIFICATE": str(BASE_DIR / 'config/certificate.pem'),
        "APNS_TOPIC": "kz.testPush",
}
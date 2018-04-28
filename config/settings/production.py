# coding=utf-8
# noinspection PyUnresolvedReferences
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p_gnmp4v*+qks+bj)1d=(7v9-exb_e5vz41#l@-*etw4rtbzf('

ALLOWED_HOSTS += ['yesatellite.pythonanywhere.com', '188.166.50.157']

DEBUG = True  # WARNING

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
        },
        'server_logger': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(BASE_DIR / 'logs/log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'server_logger'],
            'level': 'ERROR',
            'propagate': True,
        },
        'registration': {
            'handlers': ['server_logger', ],
            'level': 'DEBUG',
        }
    }
}

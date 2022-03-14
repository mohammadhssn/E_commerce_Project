from config.envs.base import *
import os
import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv

load_dotenv()

# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = str(os.getenv('SECRET_KEY'))

INSTALLED_APPS += [
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # third-party apps
    'robots',
]
SITE_ID = 1

# Arvan Cloud Storage
DEFAULT_FILE_STORAGE = str(os.getenv('DEFAULT_FILE_STORAGE'))
AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))
AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))
AWS_STORAGE_BUCKET_NAME = str(os.getenv('AWS_STORAGE_BUCKET_NAME'))
AWS_SERVICE_NAME = str(os.getenv('AWS_SERVICE_NAME'))
AWS_S3_ENDPOINT_URL = str(os.getenv('AWS_S3_ENDPOINT_URL'))
AWS_S3_FILE_OVERWRITE = False
# AWS_LOCAL_STORAGE = f'{BASE_DIR}/aws/'

# Email backend confirm
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'mohammadhssn Website'

# debug_toolbar settings
if DEBUG:
    def custom_show_toolbar(request):
        return True  # Always show toolbar, for example purposes only.


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    }
    INTERNAL_IPS = ("0.0.0.0",)
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INSTALLED_APPS += ("debug_toolbar",)

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

    # DEBUG_TOOLBAR_CONFIG = {
    #     "INTERCEPT_REDIRECTS": False,
    # }

# Config redis cache
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:6379',
    }
}

# Config Log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

# Config Sentry
sentry_sdk.init(
    dsn="https://fa805be7a1eb43e082be46764c45e7e3@o1133698.ingest.sentry.io/6256089",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# DataBase Config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv('NAME')),
        'USER': str(os.getenv('USER')),
        'PASSWORD': str(os.getenv('PASSWORD')),
        'HOST': 'pgdb',
        'PORT': str(os.getenv('PORT')),
    }
}

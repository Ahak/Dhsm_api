import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

# Update the database configuration with the environment variable

ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')]

DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# CORS_ALLOWED_ORIGINS = [
#     'https://' + os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost'),   
# ]


STORAGE = {
    'default': {

    "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
     'staticfiles': {
         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
     },
}

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
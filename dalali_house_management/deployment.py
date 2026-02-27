import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR
from urllib.parse import urlparse

# Update the database configuration with the environment variable

def _to_origin(value, default="http://localhost"):
    """Return a clean origin (scheme + host[:port]) without path."""
    raw = (value or default).strip()
    if not raw:
        raw = default
    if "://" not in raw:
        raw = f"https://{raw}"

    parsed = urlparse(raw)
    if not parsed.netloc:
        return default
    return f"{parsed.scheme}://{parsed.netloc}"


def _to_host(value, default="localhost"):
    """Return only host[:port] for ALLOWED_HOSTS."""
    origin = _to_origin(value, default=f"https://{default}")
    return urlparse(origin).netloc


RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
FRONTEND_ORIGIN = _to_origin(os.environ.get("FRONTEND_URL"), default=FRONTEND_URL)

ALLOWED_HOSTS = [_to_host(RENDER_EXTERNAL_HOSTNAME)]

CSRF_TRUSTED_ORIGINS = [_to_origin(RENDER_EXTERNAL_HOSTNAME, default="http://localhost")]

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

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]


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

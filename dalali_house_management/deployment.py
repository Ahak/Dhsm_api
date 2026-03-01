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
    FRONTEND_ORIGIN,
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


# Configuration       
cloudinary.config( 
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'), 
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure= os.environ.get('CLOUDINARY_SECURE', False)
)

# Upload an image
upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
                                           public_id="shoes")
print(upload_result["secure_url"])

# Optimize delivery by resizing and applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
print(optimize_url)

# Transform the image: auto-crop to square aspect_ratio
auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
print(auto_crop_url)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
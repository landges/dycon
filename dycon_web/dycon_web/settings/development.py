from pathlib import Path
import os
from .base import *


SECRET_KEY = os.environ.get("SECRET_KEY", "my-secret-key")

DEBUG = bool(int(os.environ.get("DEBUG", "1")))
INSTALLED_APPS+=['debug_toolbar']

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME','postgres'),
        'USER': os.environ.get('POSTGRES_USER','postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD','postgres'),
        'HOST': os.environ.get('POSTGRES_SERVICE_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_SERVICE_PORT', 5432),
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]

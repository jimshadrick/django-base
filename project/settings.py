from pathlib import Path

from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # Helper app keeps Django from serving static files
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Set Django's default user model
AUTH_USER_MODEL = 'account.CustomUser'

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Postgres settings (connection, data integrity & connection handling)p
if not env.str('DATABASE_URL', default=None):
    raise ValueError("DATABASE_URL environment variable is required")
DATABASES = {
    'default': {
        **env.dj_db_url('DATABASE_URL'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': env.int('CONN_MAX_AGE', default=60),
    }
}

# Enable Django to detect secure requests coming from behind a proxy.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Define a list of trusted origins for CSRF protection. 
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS",
                                default=["http://localhost:8000"])

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

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static', ]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Whitenoise settings
WHITENOISE_USE_FINDERS = DEBUG  # Leverages Django’s static file finders in dev
WHITENOISE_AUTOREFRESH = DEBUG  # Whitenoise will watch for file changes in dev

# Media settings for storing uploaded data
MEDIA_ROOT = env('MEDIA_ROOT', default=BASE_DIR / 'media')
MEDIA_URL = env('MEDIA_URL', default='/media/')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

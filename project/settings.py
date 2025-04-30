from pathlib import Path

from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# Development and production flag 
DEBUG = env.bool('DJANGO_DEBUG', default=True)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'debug_toolbar',
    # allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # anymail
    'anymail',
    # local apps
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # for django-debug-toolbar
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Django and allauth authentication configurations
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_DOMAIN = env.str('SITE_DOMAIN', "localhost:8000")
SITE_NAME = env.str('SITE_NAME', "Local Dev")
SITE_ID = 1  # required by django.contrib.sites

ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', "password2*"]
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'  # Required by django-allauth
ACCOUNT_EMAIL_SUBJECT_PREFIX = '%s: ' % SITE_NAME
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False  # Send email for password reset attempts by unknown users
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'none'  # 'none' defaults to LOGIN_REDIRECT_URL
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

PASSWORD_RESET_TIMEOUT = 86400  # 24 hours in seconds

# Set Django's default user model
AUTH_USER_MODEL = 'users.CustomUser'

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

# Security and Hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://localhost:8000'])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if not DEBUG else None  # detect SSL behind proxy

# SSL Settings
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', default=False)
CSRF_COOKIE_SECURE = env.bool('DJANGO_CSRF_COOKIE_SECURE', default=False)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        },
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

# Debug toolbar settings
INTERNAL_IPS = [
    "127.0.0.1",
]
SHOW_TOOLBAR_CALLBACK = lambda request: DEBUG

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # for development

# Email settings (Mailgun)
ANYMAIL = {
    'MAILGUN_API_KEY': env.str('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env.str('MAILGUN_DOMAIN'),  # e.g., sandbox123456.mailgun.org or yourdomain.com
}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')
# DEFAULT_FROM_EMAIL = f"admin@{env.str('MAILGUN_DOMAIN')}"  # For user-facing emails
# SERVER_EMAIL = f"errors@{env.str('MAILGUN_DOMAIN')}"  # For system emails (e.g., error reports)

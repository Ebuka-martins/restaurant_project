import os
from pathlib import Path
import dj_database_url

# Load environment variables from env.py if it exists
if os.path.isfile("env.py"):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Default to False

# Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS for Heroku
ALLOWED_HOSTS = [
    'restaurant-project-524b51fc1cda.herokuapp.com',
    'localhost',
    '127.0.0.1',
    '*.codeinstitute-ide.net', 
    '8000-ebukamartin-restaurantp-r18xpwuiruo.ws.codeinstitute-ide.net'
]

CSRF_TRUSTED_ORIGINS = [
    'https://restaurant-project-524b51fc1cda.herokuapp.com',
    'http://restaurant-project-524b51fc1cda.herokuapp.com',
    'https://*.gitpod.io',
    'https://*.codeinstitute-ide.net',
    'https://8000-ebukamartin-restaurantp-r18xpwuiruo.ws.codeinstitute-ide.net'
    'https://ui.dev/amiresponsive'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'restaurant_project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurant_project.wsgi.application'

# Database configuration
db_url = os.environ.get('DATABASE_URL', '')

# Try to use DATABASE_URL if available, otherwise fall back to SQLite
if db_url:
    DATABASES = {
        'default': dj_database_url.parse(
            db_url,
            conn_max_age=600,
            ssl_require=True  # Enforce SSL for secure database connections
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login and logout redirects
LOGIN_REDIRECT_URL = 'booking_list'
LOGOUT_REDIRECT_URL = 'login'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Uncomment the following for production email settings
# EMAIL_HOST = 'smtp.your-email-provider.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your@email.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
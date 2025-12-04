import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# OpenAI mode: 'mock' (default) or 'real'. Use 'mock' to conserve credits during demos.
OPENAI_MODE = os.getenv('OPENAI_MODE', 'mock')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'exercises',
    'ai_tutor',
    'frontend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatsql.urls'

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

WSGI_APPLICATION = 'chatsql.wsgi.application'

# Databases
DB_NAME = os.getenv('DB_NAME')

# Optional shared credentials for workshop databases (WS1–WS11) hosted on GCP
WS_DB_USER = os.getenv('WS_DB_USER')
WS_DB_PASSWORD = os.getenv('WS_DB_PASSWORD')
WS_DB_HOST = os.getenv('WS_DB_HOST')
WS_DB_PORT = os.getenv('WS_DB_PORT', '3306')

# If DB_NAME is provided via env, configure MySQL databases as in the docs.
# Otherwise, fall back to a local SQLite DB for quick local development.
if DB_NAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        },
        # Existing practice databases (using WS_DB_* configuration)
        'practice_hr': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'practice_hr',
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'practice_ecommerce': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'practice_ecommerce',
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'practice_school': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'practice_school',
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        # Workshop databases on GCP (WS1–WS11).
        # Each entry assumes:
        #   - same host / user / password
        #   - different database name (schema) per workshop
        # You can override NAME via env if needed, e.g. WS1_DB_NAME.
        'WS1': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS1_DB_NAME', 'WS1'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS2': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS2_DB_NAME', 'WS2'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS3': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS3_DB_NAME', 'WS3'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS4': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS4_DB_NAME', 'WS4'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS5': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS5_DB_NAME', 'WS5'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS6': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS6_DB_NAME', 'WS6'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS7': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS7_DB_NAME', 'WS7'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS8': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS8_DB_NAME', 'WS8'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS9': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS9_DB_NAME', 'WS9'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS10': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS10_DB_NAME', 'WS10'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        },
        'WS11': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('WS11_DB_NAME', 'WS11'),
            'USER': WS_DB_USER,
            'PASSWORD': WS_DB_PASSWORD,
            'HOST': WS_DB_HOST,
            'PORT': WS_DB_PORT,
        }
    }
else:
    # Local development fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

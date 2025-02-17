"""
Django settings for registar project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == 'True'

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'groups.apps.GroupsConfig',
    'rest_framework',
    'api.apps.ApiConfig',
    'marketplace.apps.MarketplaceConfig',
    'django.contrib.admin',
    'django.contrib.auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'registar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "core" / "templates" / "core" / "base",
            BASE_DIR / "core" / "templates" / "core" / "modules",
        ],
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

WSGI_APPLICATION = 'registar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'), 
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"


STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_COOKIE_NAME = "lang"

LANGUAGES = [
    ("en", _("English")),
    ("lv", _("Latvian")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Groups and permissions

REGULAR_USER_ROLE = "Registered user"
ADMIN_ROLE = "Admin"

ROLES_PERMISSIONS = {
    REGULAR_USER_ROLE: {
        'core.Shop': ['add', 'change', 'delete', 'view', 'upload_to_marketplace', 'remove_from_marketplace'],
        'core.Coupon': ['add', 'change', 'delete', 'view', 'share', 'unshare'],
        'groups.Group': ['add', 'change', 'delete', 'view', 'leave', 'invite_user', 'remove_user', 'add_shop', 'remove_shop'],
        'groups.Invitation': ['add', 'change', 'view', 'accept', 'reject'],
        'accounts.User': ['change', 'delete', 'view'],
        'marketplace.Marketplace': ['view_shop', 'use_shop_from'],
    },
}


# REST framework

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Logging
import logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "only_info": {
            "()": "registar.filters.ExactLevelFilter",
            "levelno": logging.INFO,
        },
        "only_warning": {
            "()": "registar.filters.ExactLevelFilter",
            "levelno": logging.WARNING,
        },
        "disable_autoreload": {
            "()": "registar.filters.DisableAutoreload",
        },
    },

    "formatters": {
        "audit": {
            "format": "[{levelname} {asctime}] {message}",
            "style": "{",
        },
        "error": {
            "format": "[{levelname} {asctime} {name}] {filename} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "error",
        },
        "error_log": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "error.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "error",
        },
        "warning_log": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "warning.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "encoding": "utf-8",
            "filters": ["only_warning"],
            "formatter": "error",
        },
        "audit_log": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "audit.log",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
            "encoding": "utf-8",
            "filters": ["only_info", "disable_autoreload"],
            "formatter": "audit",
        },
    },

    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["audit_log", "error_log", "console", "warning_log"],
            "propagate": True,
        },
    },
}

# Pagination

PAGINATE_BY = 6
MAX_SHOPS_IN_INDEX = 6
MAX_COUPONS_IN_INDEX = 6

    
from .local import *

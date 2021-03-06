"""
Django settings for enough_recipes project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(qf#fl!3p!b39d1+p93z$^*(uo)0ome*s2zrifj5*=3@nw++!8"

ENV = os.environ.get("ENV", "dev")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "") == 1 or ENV == "dev"

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tailwind",
    "enough_recipes_theme",
    "django_browser_reload",
    "storages",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "enough_recipes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "enough_recipes.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="mysql://root:root@localhost:3306/enoughrecipes?charset=utf8mb4",
        conn_max_age=500,
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = str(BASE_DIR) + "/enough-recipes-static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if ENV == "prod":
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
    AWS_STORAGE_BUCKET_NAME = "enough-recipes-assets"
    AWS_S3_ENDPOINT_URL = "https://ewr1.vultrobjects.com/"
    AWS_S3_REGION_NAME = "ewr1"
    AWS_DEFAULT_ACL = "public-read"


def get_es_hosts() -> str:
    """Retrieve es hosts, depending on K8s settings."""
    if "ES_ELASTICSEARCH_SERVICE_HOST" in os.environ:
        return (
            "http://"
            + os.environ["ES_ELASTICSEARCH_SERVICE_HOST"]
            + ":"
            + os.environ["ES_ELASTICSEARCH_PORT_9200_TCP_PORT"]
        )
    return os.environ.get("ES_HOSTS", "http://localhost:9200")


def get_kafka_brokers() -> str:
    """Retrieve Kafka brokers, depending on K8s ssettings."""
    if "BROKER_KAFKA_SERVICE_HOST" in os.environ:
        return f"{os.environ['BROKER_KAFKA_SERVICE_HOST']}:9092"
    return os.environ.get("KAFKA_BROKERS", "localhost:9092")


ES_HOSTS = get_es_hosts()

KAFKA_BROKERS = get_kafka_brokers()

TAILWIND_APP_NAME = "enough_recipes_theme"

INTERNAL_IPS = [
    "127.0.0.1",
]

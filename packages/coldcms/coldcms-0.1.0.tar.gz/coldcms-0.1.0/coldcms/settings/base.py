# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import abspath, dirname, join
from secrets import token_hex

import dj_database_url

PROJECT_DIR = dirname(dirname(abspath(__file__)))
BASE_DIR = dirname(PROJECT_DIR)

SECRET_KEY = os.getenv("SECRET_KEY", token_hex(64))
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if os.getenv("ALLOWED_HOSTS"):
    ALLOWED_HOSTS += os.getenv("ALLOWED_HOSTS").split(",")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "coldcms.blocks",
    "coldcms.home",
    "coldcms.legal_notice",
    "coldcms.simple_page",
    "coldcms.contact",
    "coldcms.generic_page",
    "coldcms.faq",
    "coldcms.partners",
    "coldcms.site_settings",
    "coldcms.blog",
    "coldcms.wagtail_customization",
    "svg",
    "django_assets",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bakery",
    "wagtailbakery",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "coldcms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ]
        },
    }
]

WSGI_APPLICATION = "coldcms.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

db_name = os.getenv("DB_NAME", "coldcms")

db_url = os.getenv("DB_URL", "sqlite:///" + join(BASE_DIR, db_name) + ".db")

DATABASES = {"default": dj_database_url.parse(db_url, conn_max_age=600)}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
DCAPV = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": DCAPV + ".UserAttributeSimilarityValidator"},
    {"NAME": DCAPV + ".MinimumLengthValidator"},
    {"NAME": DCAPV + ".CommonPasswordValidator"},
    {"NAME": DCAPV + ".NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-en"
LANGUAGES = [("fr", "Français"), ("en", "English")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [join(PROJECT_DIR, "locale")]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [join(PROJECT_DIR, "static")]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail
# upgrade).
# See https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/
# #manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

default_static_root = join(os.path.dirname(BASE_DIR), "static")
STATIC_ROOT = os.getenv("STATIC_ROOT", default_static_root)
STATIC_URL = "/static/"

# Config django-assets
ASSETS_MODULES = ["coldcms.assets"]
ASSETS_URL_EXPIRE = True
ASSETS_VERSIONS = "timestamp"

# Wagtail settings
WAGTAIL_SITE_NAME = "coldcms"
WAGTAILIMAGES_JPEG_QUALITY = 80
WAGTAIL_ALLOW_UNICODE_SLUGS = False
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILDOCS_SERVE_METHOD = "direct"

# Base URL to use when referring to full URLs within the Wagtail admin backend
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "http://example.com"

# Wagtail-bakery config
BUILD_DIR = os.getenv("BUILD_DIR", "/srv/app/coldcms/build/")
BAKERY_VIEWS = ("wagtailbakery.views.AllPublishedPagesView",)

MEDIA_ROOT = join(BUILD_DIR, "media")
MEDIA_URL = "/media/"

# SVG settings
SVG_DIRS = [
    join(STATICFILES_DIRS[0], "svg", path)
    for path in [
        "",
        "fontawesome/solid/",
        "fontawesome/regular/",
        "fontawesome/brands/",
    ]
]

# Email settings
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "465"))
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")
DEFAULT_FROM_EMAIL_NAME = os.getenv("DJANGO_DEFAULT_FROM_EMAIL_NAME")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"

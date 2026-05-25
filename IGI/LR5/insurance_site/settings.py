"""
Django settings for insurance_site (lab: insurance company).
SQLite for local dev; PostgreSQL when POSTGRES_HOST or DATABASE_URL is set (Docker / prod).
"""
import importlib.util
import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-change-in-production-not-for-real-use",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "insurance",
]

_WHITENOISE_AVAILABLE = importlib.util.find_spec("whitenoise") is not None

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]
if _WHITENOISE_AVAILABLE:
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "insurance_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "insurance.context_processors.access_flags",
            ],
        },
    },
]

WSGI_APPLICATION = "insurance_site.wsgi.application"


def _database_config():
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        u = urlparse(url)
        if u.scheme not in ("postgres", "postgresql"):
            raise ValueError("DATABASE_URL must use postgres:// or postgresql://")
        path = (u.path or "").lstrip("/")
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": path or "insurance",
                "USER": u.username or "insurance",
                "PASSWORD": u.password or "",
                "HOST": u.hostname or "localhost",
                "PORT": str(u.port or 5432),
                "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            }
        }
    host = os.environ.get("POSTGRES_HOST", "").strip()
    if host:
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("POSTGRES_DB", "insurance"),
                "USER": os.environ.get("POSTGRES_USER", "insurance"),
                "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "insurance"),
                "HOST": host,
                "PORT": os.environ.get("POSTGRES_PORT", "5432"),
                "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            }
        }
    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


DATABASES = _database_config()

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Europe/Minsk")
USE_I18N = True
USE_TZ = True

# Leading slash required: otherwise /news/ resolves img src to /news/static/... (404).
STATIC_URL = "/static/"
_STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [_STATIC_DIR] if _STATIC_DIR.is_dir() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

_static_backend = (
    "whitenoise.storage.CompressedStaticFilesStorage"
    if _WHITENOISE_AVAILABLE
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": _static_backend,
    },
}

# WhiteNoise serves /static/ in runserver, Docker, and hosting (DEBUG true or false).
if _WHITENOISE_AVAILABLE:
    WHITENOISE_USE_FINDERS = True
    if os.environ.get("DJANGO_BEHIND_PROXY", "").lower() in ("1", "true", "yes"):
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    if os.environ.get("DJANGO_SECURE_COOKIES", "").lower() in ("1", "true", "yes"):
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
    _csrf = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "")
    if _csrf.strip():
        CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf.split(",") if x.strip()]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"

# Log level from config (stage 8 will expand handlers)
LOG_LEVEL = os.environ.get("DJANGO_LOG_LEVEL", "INFO")
LOG_TO_FILE = os.environ.get("DJANGO_LOG_TO_FILE", "false").lower() in ("1", "true", "yes")

LOG_DIR = BASE_DIR / "logs"
_handlers = {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "verbose",
    },
}
if LOG_TO_FILE:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    _handlers["file"] = {
        "class": "logging.FileHandler",
        "filename": str(LOG_DIR / "insurance.log"),
        "formatter": "verbose",
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": _handlers,
    "root": {
        "handlers": list(_handlers.keys()),
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": list(_handlers.keys()),
            "level": "WARNING",
            "propagate": False,
        },
        "insurance": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "insurance.external": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "insurance.api": {
            "handlers": list(_handlers.keys()),
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

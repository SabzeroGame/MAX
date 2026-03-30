"""Главный файл настроек Django-проекта MAX Portfolio.

Этот файл управляет:
- подключением приложений;
- middleware-цепочкой;
- базой данных (SQLite);
- локализацией (RU/EN);
- статикой, медиа, кэшем и логированием.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Корневая папка проекта (max_portfolio/).
BASE_DIR = Path(__file__).resolve().parent.parent

# Подгружаем переменные окружения из .env для безопасной и гибкой конфигурации.
load_dotenv(BASE_DIR / ".env")

# Переключатель окружения: dev/prod (влияет на DEBUG и доп. инструменты).
DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")
DEBUG = DJANGO_ENV == "dev"

# Базовые параметры безопасности/доступа.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-key-change-me")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Список приложений, из которых состоит проект.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.portfolio.apps.PortfolioConfig",
    "apps.api",
]

# DEV-инструмент: debug-toolbar подключается только локально по флагу.
if DEBUG and os.getenv("ENABLE_DEBUG_TOOLBAR", "0") == "1":
    INSTALLED_APPS.append("debug_toolbar")

# Middleware-цепочка: порядок важен, т.к. каждый слой обрабатывает request/response.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.portfolio.middleware.RequestTimingMiddleware",
]

if DEBUG and os.getenv("ENABLE_DEBUG_TOOLBAR", "0") == "1":
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Точка входа для URL-маршрутизации.
ROOT_URLCONF = "config.urls"

# Конфигурация шаблонов (где искать, какие процессоры подключать).
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
                "apps.portfolio.context_processors.site_identity",
            ],
        },
    },
]

# WSGI/ASGI конфигурации для синхронного/асинхронного запуска.
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Главная и единственная БД проекта — SQLite.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Валидаторы паролей для стандартной auth-системы Django.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Языки интерфейса и папка словарей переводов.
LANGUAGE_CODE = "ru"
LANGUAGES = [("ru", "Русский"), ("en", "English")]
LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Настройки статики и медиа-файлов.
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Редиректы после входа/выхода пользователя.
LOGIN_REDIRECT_URL = "portfolio:home"
LOGOUT_REDIRECT_URL = "portfolio:home"

# Базовые настройки DRF API (аутентификация и доступ).
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
}

# Локальный кэш (пока без внешнего Redis).
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "max-portfolio-cache",
    }
}

# Простое консольное логирование для мониторинга поведения приложения.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"apps.portfolio": {"handlers": ["console"], "level": "INFO"}},
}

# Тип авто-id для новых моделей.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = ["127.0.0.1"]
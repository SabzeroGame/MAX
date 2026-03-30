"""Центральная маршрутизация проекта.

Здесь подключаются:
- системные маршруты i18n;
- API-маршруты;
- auth-маршруты;
- маршруты веб-приложения portfolio.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Нелокализованные маршруты (общие для всех языков).
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/", include("apps.api.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

# Локализованные маршруты (веб-страницы и админка).
localized_patterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.portfolio.urls")),
]

urlpatterns += i18n_patterns(*localized_patterns, prefix_default_language=False)

# Подключение debug-toolbar только в DEV.
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Раздача media-файлов в режиме DEBUG.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
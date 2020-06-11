from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

urlpatterns = [
    path(
        "experiments/",
        include(("djinar.experiments.urls", "experiments"), namespace="experiments"),
    ),
    path(
        "",
        include(("djinar.home.urls", "home"), namespace="home"),
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("djinar.users.urls", namespace="users"),
    ),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
    ImportError at /experiments/webcam
    cannot import name 'ORDER_PATTERN' from 'django.db.models.sql.constants'
    (/Users/brunux/opt/miniconda3/envs/djinar/lib/python3.8/site-packages/django/db/models/sql/constants.py)
    /Users/brunux/opt/miniconda3/envs/djinar/lib/python3.8/site-packages/rest_framework/filters.py, line 11, in <module>

    Looks like the DRF is not compatible with Django 3.1
    path(
        "c/",
        include(("djinar.contacts.urls", "contacts"), namespace="contacts"),
    ),
    path(
        "e/",
        include(("djinar.events.urls", "events"), namespace="events")
    ),
"""

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns

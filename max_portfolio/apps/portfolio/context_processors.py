from django.utils.translation import gettext_lazy as _


def site_identity(request):
    return {
        "site_name": "MAX Portfolio",
        "site_subtitle": _("Portfolio of student club / sports section"),
    }
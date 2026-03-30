from django.urls import path

from .views import AboutView, ContactView, HomeView, ProjectCreateView, ProjectDetailView

app_name = "portfolio"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
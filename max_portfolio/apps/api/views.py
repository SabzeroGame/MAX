"""DRF views для API-части проекта.

Файл публикует read-only endpoint проектов.
"""

from rest_framework import permissions, viewsets

from apps.portfolio.models import Project

from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint для просмотра опубликованных проектов."""

    queryset = Project.objects.published().select_related("category", "created_by")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
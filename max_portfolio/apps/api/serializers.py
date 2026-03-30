"""Сериализаторы DRF.

Файл отвечает за преобразование модели Project в JSON для API.
"""

from rest_framework import serializers

from apps.portfolio.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор проекта для публичного read-only API."""

    category = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "description",
            "tech_stack",
            "category",
            "created_by",
            "is_published",
            "created_at",
        ]
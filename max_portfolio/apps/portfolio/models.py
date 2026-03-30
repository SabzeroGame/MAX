"""Модели предметной области портфолио.

Файл содержит структуру данных, которая хранится в SQLite:
- категории проектов;
- сами проекты;
- участники команды;
- входящие сообщения из контактной формы.
"""

from django.conf import settings
from django.db import models
from django.urls import reverse

from .managers import PublishedProjectManager


class Category(models.Model):
    """Категория, к которой относится проект (например: Web, Sport, Robotics)."""

    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Project(models.Model):
    """Карточка проекта для публичного портфолио."""

    # Базовые текстовые поля проекта.
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    summary = models.TextField(max_length=800)
    description = models.TextField()

    # Связи и медиа.
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="projects")
    image = models.FileField(upload_to="projects/", blank=True)

    # Технологический стек проекта.
    tech_stack = models.CharField(max_length=255, blank=True, help_text="Например: Django, SQLite, Bootstrap")

    # Кто добавил проект в систему.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")

    # Публикация и временные метки.
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Кастомный менеджер для фильтрации опубликованных проектов.
    objects = PublishedProjectManager()
    # Стандартный менеджер для доступа ко всем записям.
    all_objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        """Возвращает URL страницы деталей проекта."""
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})


class TeamMember(models.Model):
    """Участник кружка/секции для отображения на странице команды."""

    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=120)
    bio = models.TextField(max_length=600, blank=True)
    photo = models.FileField(upload_to="team/", blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.role})"


class ContactMessage(models.Model):
    """Сообщение, отправленное через контактную форму сайта."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name}: {self.email}"
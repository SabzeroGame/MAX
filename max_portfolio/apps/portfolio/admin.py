"""Админ-конфигурация моделей портфолио.

Файл делает управление контентом удобным для администраторов проекта.
"""

from django.contrib import admin

from .models import Category, ContactMessage, Project, TeamMember


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки списка и формы категории в Django Admin."""

    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Управление проектами: фильтрация, поиск, быстрый обзор."""

    list_display = ("title", "category", "created_by", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "summary", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Управление составом команды."""

    list_display = ("full_name", "role", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("full_name", "role")
    list_editable = ("order", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Просмотр входящих сообщений с контактной формы."""

    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
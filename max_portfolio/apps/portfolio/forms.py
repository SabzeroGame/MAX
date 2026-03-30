"""Формы Django для ввода данных пользователем.

Файл отделяет HTML-ввод от бизнес-логики и моделей.
"""

from django import forms

from .models import ContactMessage, Project


class ProjectCreateForm(forms.ModelForm):
    """Форма создания/редактирования проекта в интерфейсе."""

    class Meta:
        model = Project
        fields = ["title", "slug", "summary", "description", "category", "image", "tech_stack", "is_published"]
        # Визуальная настройка виджетов для аккуратного Bootstrap-отображения.
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 6, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tech_stack": forms.TextInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ContactMessageForm(forms.ModelForm):
    """Форма обратной связи для страницы контактов."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Ваш вопрос или предложение"}),
        }